#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import argparse
from collections import deque

import cv2

from cv_overlay_inset_image import cv_overlay_inset_image


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--bg_device", type=int, default=None)
    parser.add_argument("--bg_movie", type=str, default=None)
    parser.add_argument("--bg_image", type=str, default=None)

    parser.add_argument("--fg_device", type=int, default=None)
    parser.add_argument("--fg_movie", type=str, default=None)
    parser.add_argument("--fg_image", type=str, default=None)

    args = parser.parse_args()

    return args


class ImageCapture(object):
    _type = None
    TYPE_WEBCAM = 0
    TYPE_MOVIE = 1
    TYPE_IMAGE = 2

    _video_capture = None
    _image = None

    def __init__(self, device_no, movie_path, image_path):
        if movie_path is not None:
            self._type = self.TYPE_MOVIE
            self._video_capture = cv2.VideoCapture(movie_path)
        elif image_path is not None:
            self._type = self.TYPE_IMAGE
            self._video_capture = None
            self._image = cv2.imread(image_path)
        elif device_no is not None:
            self._type = self.TYPE_WEBCAM
            self._video_capture = cv2.VideoCapture(device_no)
        else:
            assert False, 'Be sure to specify device_no or movie_path or image_path.'

    def read(self):
        ret = False
        image = None
        if self._type == self.TYPE_WEBCAM:
            ret, self._image = self._video_capture.read()
            image = copy.deepcopy(self._image)
        elif self._type == self.TYPE_MOVIE:
            ret, self._image = self._video_capture.read()
            image = copy.deepcopy(self._image)
        elif self._type == self.TYPE_IMAGE:
            ret = True
            image = copy.deepcopy(self._image)

        return ret, image

    def release(self):
        if self._type == self.TYPE_WEBCAM:
            self._video_capture.release()
        elif self._type == self.TYPE_MOVIE:
            self._video_capture.release()
        elif self._type == self.TYPE_IMAGE:
            pass

    def get_video_capture_instance(self):
        return self._video_capture


class CvWindow(object):
    _window_name = ''
    _frame = None

    _click_point = None
    _click_point_queue = None

    def __init__(self, window_name='DEBUG', point_history_maxlen=4):
        self._window_name = window_name

        cv2.namedWindow(self._window_name)
        cv2.setMouseCallback(self._window_name, self._mouse_callback)

        self._click_point_queue = deque(maxlen=point_history_maxlen)

    def imshow(self, image):
        cv2.imshow(self._window_name, image)

    def get_click_point_history(self):
        return self._click_point_queue

    def _mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self._click_point = [x, y]
            self._click_point_queue.append(self._click_point)
        elif event == cv2.EVENT_RBUTTONDOWN:
            self._click_point = None
            self._click_point_queue.clear()


def main():
    # コマンドライン引数
    args = get_args()

    bg_device = args.bg_device
    bg_movie = args.bg_movie
    bg_image = args.bg_image

    fg_device = args.fg_device
    fg_movie = args.fg_movie
    fg_image = args.fg_image

    # 画像準備
    bg_image_capture = ImageCapture(bg_device, bg_movie, bg_image)
    fg_image_capture = ImageCapture(fg_device, fg_movie, fg_image)

    #
    cv_window = CvWindow(window_name='Sample', point_history_maxlen=4)

    while True:
        ret, bg_image = bg_image_capture.read()
        if not ret:
            break
        ret, fg_image = fg_image_capture.read()
        if not ret:
            break

        debug_image = copy.deepcopy(bg_image)

        # クリック位置取得
        click_point_history = cv_window.get_click_point_history()

        # デバッグ描画
        if len(click_point_history) < 4:
            for click_point in click_point_history:
                cv2.circle(
                    debug_image,
                    (click_point[0], click_point[1]),
                    4,
                    (255, 255, 255),
                    -1,
                )
                cv2.circle(
                    debug_image,
                    (click_point[0], click_point[1]),
                    2,
                    (0, 0, 0),
                    -1,
                )
        # はめ込み画像生成
        elif len(click_point_history) == 4:
            debug_image = cv_overlay_inset_image(
                bg_image,
                fg_image,
                click_point_history,
            )

        # 画面反映
        cv_window.imshow(debug_image)

        # キー処理(ESC：終了)
        key = cv2.waitKey(1)
        if key == 27:  # ESC
            break

    bg_image_capture.release()
    fg_image_capture.release()
    cv2.destroyAllWindows()


# --------------------------------------------------------------------
if __name__ == "__main__":
    main()
