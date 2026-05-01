from tkinter import *
from tkinter import ttk
from PIL import Image

def split_image_into_channels(img, img_name):
    cyan, magenta, yellow, key = img.split()
    


def convert_RGB_to_CMYK(img):
    img_CMYK = img.convert("CMYK")
    return img_CMYK

def main():
    window = Tk() # i made a window
    window.geometry("800x500")
    window.title("CMYK Helper :D")
    window.mainloop() # i can open it now. im scared.
