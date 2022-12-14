# cv_overlay_inset_image
OpenCVを用いてはめ込み画像を作るサンプルです。

![e8rwh-w8jfv](https://user-images.githubusercontent.com/37477845/184624532-375eff2b-ae19-48c6-907e-8be41b69f62d.gif)

# Requirement
```
opencv-python 4.5.5.62 or later
```

# Script example
```python
from cv_overlay_inset_image import cv_overlay_inset_image

image = cv_overlay_inset_image(
    bg_image,
    fg_image,
    points,  # coordinates of 4 points
)
```

# Demo
デモの実行方法は以下です。<br>
マウス左クリックではめ込み画像の座標を指定します。<br>
マウス右クリックで選択した座標をクリアします。
```bash
python sample.py --bg_image=sample.jpg --fg_device=0
```
* --bg_movie<br>
背景動画のパス指定<br>
デフォルト：指定なし
* --bg_image<br>
背景画像のパス指定<br>
デフォルト：指定なし
* --bg_device<br>
背景用Webカメラ画像のデバイス指定<br>
デフォルト：指定なし
* --fg_movie<br>
はめ込み用の動画のパス指定 <br>
デフォルト：指定なし
* --fg_image<br>
はめ込み用の画像のパス指定<br>
デフォルト：指定なし
* --fg_device<br>
はめ込み用のWebカメラ画像のデバイス指定<br>
デフォルト：指定なし

※bg_movie、bg_image、bg_deviceは何れか一つを指定してください<br>
※fg_movie、fg_image、fg_deviceは何れか一つを指定してください

# Author
高橋かずひと(https://twitter.com/KzhtTkhs)
 
# License 
cv_overlay_inset_image is under [Apache-2.0 license](LICENSE).<br><br>

また、サンプル画像は[フリー素材ぱくたそ](https://www.pakutaso.com)様の<br>
「[ずっと使われていない天井吊りのテレビの写真素材](https://www.pakutaso.com/20180344079post-15604.html)」を利用しています。
