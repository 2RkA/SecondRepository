import os
import traceback
import subprocess
from PIL import Image

# 13.4/4

class watermarker:
    def __init__(self, original_path: str, new_path: str, logo_path: str, width_scale: int):
        """
        - `original_path`: path of the video/image to watermark

        - `new_path`: new path of the video/image that gets watermarked
        - will create a new file if `original_path` and `new_path` are the same -> path will look like "NEW_FILENAME.xyz"

        - `logo_path`: path of the watermark to use, should be a image

        - `width_scale`: watermark to video/image ratio - not accurate at all
        """
        self.original_path: str = original_path
        self.new_path: str = new_path
        self.logo_path: str = logo_path
        self.width_scale: str = width_scale

        self.video_exts = ['webm', 'mkv', 'flv', 'vob', 'ogv', 'ogg', 'rrc', 'gifv', 'mng', 'mov', 'avi', 'qt', 'wmv', 'yuv', 'rm', 'asf', 'amv', 'mp4',
                           'm4p', 'm4v', 'mpg', 'mp2', 'mpeg', 'mpe', 'mpv', 'm4v', 'svi', '3gp', '3g2', 'mxf', 'roq', 'nsv', 'flv', 'f4v', 'f4p', 'f4a', 'f4b', 'mod']

    def start(self) -> bool:
        try:
            if os.path.exists(self.original_path):
                if os.path.exists(self.logo_path):

                    ext = self.original_path.lower().split(".")[-1]

                    if ext in self.video_exts:
                        return self.video()

                    else:
                        return self.image()

                else:
                    print(f"Following path was not found: {self.logo_path}")
                    raise SystemExit
            else:
                print(f"Following path was not found: {self.original_path}")
                raise SystemExit

        except Exception as e:
            print(traceback.format_exc())

            return False

    def video(self) -> bool:
        try:
            cmd = r"ffprobe -v error -select_streams v -show_entries stream=width,height -of csv=p=0:s=x {0}".format(
                self.original_path)
            dimensions = str(subprocess.check_output(cmd.split(" ")))

            width = dimensions.split("x")[0].split("'")[1]
            height = dimensions.split("x")[1].split("\\")[0]

            if int(height) <= int(width):
                scale = 2

            else:
                scale = 3

            if self.original_path.lower() == self.new_path.lower():
                if "/" in self.original_path:
                    name = self.original_path.split("/")[-1]
                    file = self.original_path.replace(name, "NEW_" + name)

                elif "\\" in self.original_path:
                    name = self.original_path.split("\\")[-1]
                    file = self.original_path.replace(name, "NEW_" + name)
                else:
                    file = "NEW_" + self.original_path

            cmd = r"""ffmpeg -i {0} -i {1} -filter_complex "[1][0]scale2ref=w=oh*mdar:h=ih*0.{2}[logo][video];[video][logo]overlay=5:H-h-5" -c:a copy {3} -y -loglevel quiet""".format(
                self.original_path, self.logo_path, int(str(self.width_scale / scale).replace(".", "")), file)

            output = os.system(cmd)

            if 1 == output:

                return False

            return True

        except Exception as e:
            print(traceback.format_exc())

            return False

    def image(self) -> bool:
        try:
            photo = Image.open(self.original_path)
            watermark = Image.open(self.logo_path)

            photo.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

            logo_width, logo_height = watermark.size
            photo_width, photo_height = photo.size

            new_width, new_height = int(
                photo_width/self.width_scale), int(logo_height*(photo_width/self.width_scale)/logo_width)

            watermark = watermark.resize((new_width, new_height))

            if photo_height <= photo_width:
                photo.paste(watermark, (int(photo_width/16),
                            int(photo_height - new_height)), watermark)  # int(photo_height - photo_height/4)), watermark)
            else:
                photo.paste(watermark, (int(photo_width/13),
                            int(photo_height - new_height)), watermark)  # int(photo_height - photo_height/8)), watermark)

            photo.save(self.new_path)

            return True

        except Exception as e:
            print(traceback.format_exc())

            return False
