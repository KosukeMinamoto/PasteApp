# README (JP ver.)

---

## About "PasteApp"

地震波形のペーストアップを作成するためのpythonベースのGUIです. 

![pasteapp](/pasteapp.png "[2022 Fukushima earthquake](https://en.wikipedia.org/wiki/2022_Fukushima_earthquake))")



## Download

```
git clone https://github.com/KosukeMinamoto/PasteApp
```


## Environment

python >= 3.10

(python =< 3.9.6 では`tkinter`のバグがあります)

```
conda env create -f env.yml
```

```
python3 -m pip3 install -r requirements.txt
```

## Required files

### Station list
	```txt
	station_code lat lon height
	station_code lat lon height
	... 
	```
	* station_code:  
		観測点名

	* lat & lon:  
		Station latitude / longitude in **degree**

	* height:  
		The station height in **km** direction of which is defined as a Z-axis (positive in the upper direction) here.

### Configure file (.json)
  * directory:  
    ObsPyで読める波形データのあるディレクトリ名

  * channel_tbl:  
    観測点リスト名

  * components:  
    波形データの「obspy.trace.stats.channel」と一致する成分名のリスト

  * line_colors:  
    "components" と同じサイズのリストで, 対応した色で描画される

  * normalize_type:  
    * "global_max": 読み込んだ全波形の最大値で規格化する
    * "None": 規格化されない
    * 上記以外: 各波形ごとに規格化される
  
  * mpl_rcparam:  
    See [`matplotlib.rcParams`](https://matplotlib.org/stable/users/explain/customizing.html)

## Usage

`c`オプションで設定ファイルのパスを指定できます (Default:'config.json').

```
python3 pasteup.py -c config.json
```

## Acknowledgment

サンプル画像`pasteapp.png`の作成にあたっては, [S-net](https://www.seafloor.bosai.go.jp/S-net/)の波形, 観測点情報を使用いたしました. 

> National Research Institute for Earth Science and Disaster Resilience (2019), NIED S-net, National Research Institute for Earth Science and Disaster Resilience, https://doi.org/10.17598/nied.0007.

## Report bugs

If you find any bugs or things to be updated, please contact [me](kosuke.minamoto.s8@gmail.com).
