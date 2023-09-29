# PasteApp
---

## About this app.

地震波形のペーストアップを作成するためのpythonベースのGUIです. 

![pasteapp](/PasteApp.png)

## Installation


## Required

* 観測点リスト

以下の形式のリスト
```txt
観測点名 緯度 経度 高度
観測点名 緯度 経度 高度
... 
```

* configure ファイル (json形式)

  * directory: str
    ObsPyで読める波形データのあるディレクトリ名
  * channel_tbl: str
    観測点リスト名
  * components: list
    波形データの「obspy.trace.stats.channel」と一致する成分名のリスト
  * line_colors: list
    "components" と同じサイズのリストで, 対応した色で描画される
  * normalize_type: str
    "global_max": 読み込んだ全波形の最大値で規格化する
    "None": 規格化されない
    上記以外: 各波形ごとに規格化される
  
  * mpl_rcparam: 
    Matplotlib の rcParam を参照
    
Example:
```txt
  "directory": "./sac-data",
  "channel_tbl": "station.list",
  "components": ["VZ"],
  "line_colors": ["gray"],
  "normalize_type": "global_max",
  "distance_ratio": 0.05,
  "mpl_rcparam": {}
```

## Report bugs

If you find any bugs or things to be updated, please contact [us](kosuke.minamoto.s8@gmail.com).
