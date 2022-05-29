# watermarker
Module to put a watermark in the bottom right corner of a video/image uwu

## Example of use
```py
from watermarker import watermarker

file_path = "D:/video.mp4" # can also be a image
new_path = "D:/watermarked_video.mp4" # it will create a new file if the file and new path are the same
logo_path = "D:/watermark.png" # path of the watermark to use
width_scale = 3 # image to video/image ratio - not accurate btw

watermarker(file_path, new_path, logo_path, width_scale).start() # will return True if success and False if it failed
```
