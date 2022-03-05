import glob
from PIL import Image
import cv2
import argparse
import os
import time
import shutil

EXTENSION_GIF = ".gif"
TEMP_FOLDER = "output"

def convert_mp4_to_jpgs(filename):
    if os.path.exists(TEMP_FOLDER):
        shutil.rmtree(TEMP_FOLDER)
    os.mkdir(TEMP_FOLDER)
    video_capture = cv2.VideoCapture(filename)
    still_reading, image = video_capture.read()
    frame_count = 0
    while still_reading:
        filename_jpg = f"{TEMP_FOLDER}/frame_{frame_count:03d}.jpg"
        cv2.imwrite(filename_jpg, image)
        print("Writing: {}".format(filename_jpg))
        # read next image
        still_reading, image = video_capture.read()
        frame_count += 1

def make_gif(filename):
    images = glob.glob(f"{TEMP_FOLDER}/*.jpg")
    images.sort()
    frames = [Image.open(image) for image in images]
    frame_one = frames[0]
    frame_one.save(filename, format="GIF", append_images=frames,
                   save_all=True, duration=50, loop=0)

def is_valid_path(parser, arg):
    """
    Check if user input path exists
    """
    path = os.path.realpath(arg)
    if not os.path.exists(path):
        parser.error("The path {} does not exist!".format(path))
    else:
        return path

def find_all_files(path, extension):
    """
    Returns list of all files in folder including its subfolders
    Example of extension is .xls, .txt, .csv
    """
    list_filepath = []
    for root, __, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                list_filepath.append(os.path.join(root, file))
    return list_filepath

def generate_output_filename(extension):
    """
    Generates the default output filename
    """
    timestr = time.strftime("%Y%m%d_%H%M%S")
    return timestr + extension

def main():
    parser = argparse.ArgumentParser(description='Convert .mp4 into .gif')
    parser.add_argument(dest="input_file", help="input filename should be .mp4", metavar="INPUT_FILENAME", type=lambda x: is_valid_path(parser, x))
    parser.add_argument("-o", "--output", dest="output_filename", help="output filename", default=generate_output_filename(EXTENSION_GIF))
    args = parser.parse_args()
    INPUT_FILENAME = args.input_file
    OUTPUT_FILENAME = args.output_filename
    convert_mp4_to_jpgs(INPUT_FILENAME)
    make_gif(OUTPUT_FILENAME)
    print("Created: {}".format(OUTPUT_FILENAME))
    

if __name__ == "__main__":
    main()