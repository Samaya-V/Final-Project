from tkinter import *
from tkinter import ttk
from PIL import Image

def get_split_image_into_channels(img, img_name):
    img_CMYK = img.convert("CMYK")
    cyan, magenta, yellow, key = img_CMYK.split()
    cyan.save(f"{img_name}_cyan.pdf", resolution=300.0)
    magenta.save(f"{img_name}_magenta.pdf)", resolution=300.0)
    yellow.save(f"{img_name}_yellow.pdf)", resolution=300.0)
    key.save(f"{img_name}_key.pdf)", resolution=300.0)

def convert_RGB_to_CMYK(img, img_name):
    img_CMYK = img.convert("CMYK")
    img_CMYK.save(f"{img_name}_CMYK.pdf", resolution=300.0)
    return img_CMYK

def give_cropped_images(img, padding=150):
    w, h = img.size
    new_size = (w + {padding}*2, h + {padding}*2)
    new_img = Image.new("CMYK", new_size, (0, 0, 0, 0))
    new_img.paste(img.convert("CMYK"), (padding, padding))

def apply_halftone(img, dot_size, angle):
    img_CMYK = img.convert("CMYK")
    cyan, magenta, yellow, key = img_CMYK.split()
    cyan_halftone.save("cyan_halftone.pdf", resolution=300.0)
    magenta_halftone.save("magenta_halftone.pdf", resolution=300.0)
    yellow_halftone.save("yellow_halftone.pdf", resolution=300.0)
    key_halftone.save("key_halftone.pdf", resolution=300.0)

def main():
    window = Tk() # i made a window
    window.geometry("800x500")
    window.title("CMYK Helper :D")
    window.mainloop() # i can open it now. im scared.

if __name__ == "__main__":
    main()
