#!usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Last update: @23/09/29 by K.M.
'''

import argparse
import os
import json
# from glob import glob
import numpy as np
import pandas as pd
from geopy.distance import Point,distance #,geodesic
from obspy import read

import tkinter as tk
# from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk

def read_json(json_path:str)->dict:
	with open(json_path) as js:
		param = json.load(js)
	return param

def read_chtbl(chtbl_path:str)->pd.DataFrame:
	chtbl =  pd.read_csv(chtbl_path,
					  delim_whitespace=True,
					  index_col=0,
					  names=['code','lat','lon','dep'])
	return chtbl

def getarg():
	parser = argparse.ArgumentParser(description='Paste-Up tool for seismograms')
	parser.add_argument('--configure_file','-c',
					 required=True,
					 help='path to the configure file in "json"')
	args = parser.parse_args()
	return args

def read_all_stream(input_dir,normalize_type):
	stream = read(os.path.join(input_dir,'*'))
	if not normalize_type:
		pass
	elif normalize_type == 'global_max':
		stream.normalize(global_max=True)
	else:
		stream.normalize()
	return stream

class PasteApp(tk.Frame):
	def __init__(self,json_path,master=None):
		super().__init__(master)
		self.param = read_json(json_path)
		plt.rcParams.update(self.param['mpl_rcparam'])

		# Channels & Waveform
		self.chtbl = read_chtbl(self.param['channel_tbl'])
		self.codes = self.chtbl.index.tolist()
		self.stream = read_all_stream(self.param['directory'],
								normalize_type=self.param['normalize_type'])

		# GUI master
		self.master = master
		self.master.geometry("1000x750")
		self.master.title('PasteApp')
		# self.master.resizable(False, False)

		self._create_side_panel()
		self._create_main_panel()
		self.master.protocol("WM_DELETE_WINDOW", self.click_close)

		# Plot initial paste-up
		self.plot_pasteup()

	def _create_main_panel(self):
		self.main_frame = tk.Frame(self.master)
		self.fig, self.ax = plt.subplots()
		self.ax.yaxis.tick_right()
		self.fig_canvas = FigureCanvasTkAgg(self.fig, self.main_frame)
		self.toolbar = NavigationToolbar2Tk(self.fig_canvas, self.main_frame)
		self.fig_canvas.get_tk_widget().pack()
		self.main_frame.pack(side=tk.LEFT)

	def _create_side_panel(self):
		ilat, ilon, idep = self.chtbl.mean(axis=0).tolist()
		self.side_frame = tk.Frame(self.master,borderwidth=2,relief=tk.GROOVE)

		# Latitude
		lab_lat = tk.Label(text='Latitude')
		lab_lat.place(relx=0.8,rely=0.02)
		self.ent_lat = tk.Entry(self.side_frame,fg='red',bg='white')
		self.ent_lat.insert(tk.END,str(ilat))
		self.ent_lat.pack(padx=10,pady=10,expand=True)
		
		# Longitude
		lab_lon = tk.Label(text='Longitude')
		lab_lon.place(relx=0.8,rely=0.16)
		self.ent_lon = tk.Entry(self.side_frame,fg='blue',bg='white')
		self.ent_lon.insert(tk.END,str(ilon))
		self.ent_lon.pack(padx=10,pady=10,expand=True)

		# Depth
		lab_dep = tk.Label(text='Depth')
		lab_dep.place(relx=0.8,rely=0.3)
		self.ent_dep = tk.Entry(self.side_frame,fg='green',bg='white')
		self.ent_dep.insert(tk.END,str(idep))
		self.ent_dep.pack(padx=10,pady=10,expand=True)

		# Bandpass Filter
		lab_fmin = tk.Label(text='Freq. min')
		lab_fmin.place(relx=0.8,rely=0.45)
		self.fmin = tk.Entry(self.side_frame,fg='black',bg='white')
		self.fmin.insert(tk.END,str(2))
		self.fmin.pack(padx=10,pady=10,expand=True)

		lab_fmax = tk.Label(text='Freq. max')
		lab_fmax.place(relx=0.8,rely=0.59)
		self.fmax = tk.Entry(self.side_frame,fg='black',bg='white')
		self.fmax.insert(tk.END,str(16))
		self.fmax.pack(padx=10,pady=10,expand=True)

		lab_fnum = tk.Label(text='Num. of filters')
		lab_fnum.place(relx=0.8,rely=0.73)
		self.fnum = tk.Entry(self.side_frame,fg='black',bg='white')
		self.fnum.insert(tk.END,str(1))
		self.fnum.pack(padx=10,pady=10,expand=True)

		btn = tk.Button(self.side_frame, 
						text='PasteUp!!',
						command=self.plot_pasteup,
						width=15)
		btn.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
		self.side_frame.pack(side=tk.RIGHT, fill=tk.Y)

	def _calc_distance_km(self,slat,slon,sdep,hlat,hlon,hdep):
		station_point = Point(slat,slon,sdep)
		hypocenter = Point(hlat,hlon,sdep)
		dist_hori = distance(hypocenter,station_point).km
		# dist = np.sqrt(dist_hori**2+(sdep-hdep)**2)
		return dist_hori


	def plot_pasteup(self):
		self.ax.clear()
		hlat = self.ent_lat.get()
		hlon = self.ent_lon.get()
		hdep = self.ent_dep.get()
		fmin = float(self.fmin.get())
		fmax = float(self.fmax.get())
		fnum = int(self.fnum.get())

		stream = self.stream.copy()
		for _ in range(fnum):
			stream.filter('bandpass',freqmin=fmin,freqmax=fmax,zerophase=True)

		for tr in stream:
			if not tr.stats.channel in self.param['components']\
			or not tr.stats.station in self.codes:
				continue
			else:
				station = self.chtbl.loc[tr.stats.station]
				y_posi = self._calc_distance_km(
					station['lat'],station['lon'],station['dep'],
					hlat,hlon,hdep
					)*self.param["distance_ratio"]
				idx = self.param['components'].index(tr.stats.channel)
				colo = self.param['line_colors'][idx]
				self.ax.plot(tr.data+y_posi,c=colo)
				self.ax.text(10, y_posi,tr.stats.station,weight='bold')
		self.ax.yaxis.set_major_formatter(self._label_formatter)
		self.ax.set_xlabel('Samples',weight='bold')
		self.ax.set_ylabel('Distance [km]',weight='bold')
		self.fig_canvas.draw()

	def _label_formatter(self,val,_):
		return f'{val / self.param["distance_ratio"]:.0f}'

	def click_close(self):
		if tk.messagebox.askokcancel("Alert", "Would you like to quit?"):
			self.master.destroy()
			quit()

if __name__=='__main__':
	json_path = 'config.json'
	root = tk.Tk()
	app = PasteApp(json_path,master=root)
	app.mainloop()

