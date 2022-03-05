import glob
from PIL import Image
import cv2
import argparse
import os
import time
import shutil

EXTENSION_GIF = ".gif"


def make_gif(filename, input_path):
    images = glob.glob(f"{input_path}/*.jpg")
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
    make_gif(OUTPUT_FILENAME, INPUT_FILENAME)
    print("Created: {}".format(OUTPUT_FILENAME))
    

if __name__ == "__main__":
    main()