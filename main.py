import os
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
import time
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, vfx
from moviepy.video.fx.all import crop
from moviepy.editor import *
from scipy.ndimage import gaussian_filter
from skimage.filters import gaussian
import cv2
import numpy as np
from PIL import Image, ImageFilter
import matplotlib.font_manager as font_manager
import json




current_directory = os.getcwd()

directory_path = f'{current_directory}/videos'

channelname = "t.me/premiumpyt"

def set_currently_busy(status):
    with open("fileexchangeconfig.json", 'r') as f:
        data = json.load(f)

    data['currently_busy'] = status

    with open("fileexchangeconfig.json", 'w') as f:
        json.dump(data, f, indent=4) 

def list_system_fonts():
    font_paths = font_manager.findSystemFonts()
    font_names = [font_manager.FontProperties(fname=font_path).get_name() for font_path in font_paths]
    return sorted(set(font_names))

totalfonts = 0

for font in TextClip.list("font"):
    print(font)
    totalfonts+=1
print(totalfonts)

#640 = 75

def lilpytvideo():
    # Loop through each file in the directory
    set_currently_busy(True)
    for filename in os.listdir(f'{current_directory}/lilvideos'):
        blurred_frames = []
        file_path = os.path.join(f'{current_directory}/lilvideos', filename)
        if os.path.isfile(file_path):
            try:
                video = VideoFileClip(file_path)
                if video.duration > 15:
                    video = video.subclip(0, 15)

                    
                f_size = int((video.w / 640) * 50)
                stroke_size = int((video.w / 640) * 50)

                blurx1 = int((video.w/453)*120)
                blurx2 = video.w - blurx1
                bluryoffset = int((video.h/852)*14)
                blury1 = int((video.h/2)+bluryoffset)
                blury2 = int((video.h/2)-bluryoffset)

                frames = video.iter_frames()
                for frame in frames:
                    image = Image.fromarray(frame)
                    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=13))  # Adjust radius as needed
                    blurred_image = blurred_image.crop((blurx1, blury2, blurx2, blury1))
                    blurred_frame = np.array(blurred_image)
                    blurred_frames.append(blurred_frame)
                print("done")
                blurred_clip = ImageSequenceClip(blurred_frames, fps=video.fps)

                image = ImageClip("logo.png")
                image = image.set_duration(video.duration)
                ogimgx = image.w
                ogimgy = image.h
                newimgy = int(blurred_clip.h*(31/13))
                newimgx = int((newimgy/ogimgy)*ogimgx)
                image = image.resize(newsize=(newimgx, newimgy)) 

                position = (blurx1, blury2-5) 

                logo_position_offset = int((video.w/640)*8)

                logo_position = (int(video.w/2)-int(image.w/2), int(video.h/2)-int(image.h/2)-logo_position_offset)

                video = CompositeVideoClip([video, blurred_clip.set_position(position), image.set_position(logo_position)])

                video.write_videofile(f'liloutput/{filename.split(".")[0]}.mp4')

                time.sleep(3)
                os.remove(file_path)

            except Exception as e:
                print(f"Error processing {filename}: {e}")

    set_currently_busy(False)


def normalvideo():
    for filename in os.listdir(directory_path):
        blurred_frames = []
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            try:
                video = VideoFileClip(file_path)

                f_size = int((video.w / 640) * 75)

                blurx1 = int((video.w/453)*120)
                blurx2 = video.w - blurx1
                bluryoffset = int((video.h/852)*18)
                blury1 = int((video.h/2)+bluryoffset)
                blury2 = int((video.h/2)-bluryoffset)

                frames = video.iter_frames()
                for frame in frames:
                    image = Image.fromarray(frame)
                    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=13))  # Adjust radius as needed
                    blurred_image = blurred_image.crop((blurx1, blury2, blurx2, blury1))
                    blurred_frame = np.array(blurred_image)
                    blurred_frames.append(blurred_frame)
                print("done")
                blurred_clip = ImageSequenceClip(blurred_frames, fps=video.fps)


                '''
                first_frame = video.get_frame(0)
                video.save_frame("temp.jpg", t=0)
                input()
                image = Image.open("temp.jpg")
                blurred_image = image.filter(ImageFilter.GaussianBlur(radius=5))  # Adjust radius as needed
                cropped_image = blurred_image.crop((blurx1, blury2, blurx2, blury1))
                cropped_image.save("temp.jpg")

                blurred_video = video.fl_image( blur )
                cropped_blurred = blurred_video.crop(x1=blurx1, y1=blury2, x2=blurx2, y2=blury1)

                '''

                txt_clip = TextClip(channelname, fontsize=f_size, color='white', font="Burbank Big Condensed")

                start_time = int(video.duration / 5)

                txt_clip = txt_clip.set_pos('center').set_duration(video.duration - start_time).set_start(start_time)

                position = (blurx1, blury2-5) 

                video = CompositeVideoClip([video, blurred_clip.set_position(position), txt_clip])

                video.write_videofile(f'output/{filename.split(".")[0]}.mp4')

                
                input()

                #os.remove(file_path)
                
            except Exception as e:
                print(f"Error processing {filename}: {e}")


def delete_all_videos():
    try:
        current_directory = os.getcwd()
        lildirectory_path = f'{current_directory}/lilvideos'
        for filename in os.listdir(lildirectory_path):
            file_path = os.path.join(lildirectory_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
    except:
        pass


last_video_amount = len(os.listdir('lilvideos'))
while True:
    if last_video_amount != len(os.listdir('lilvideos')):
        print("found new videos")
        last_video_amount = len(os.listdir('lilvideos'))
        time.sleep(10)
        if last_video_amount == len(os.listdir('lilvideos')):
            lilpytvideo()
            delete_all_videos()
    time.sleep(2)
    print("checking..")

