from tkinter import *
from tkinter import filedialog
from PIL import Image
import math

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

def halftone_one_channel(channel_img, cell_size, grid_angle_degrees):
    image_width, image_height = channel_img.size
    output_image = Image.new("L", (image_width, image_height), 255)
    
    angle_rad = math.radians(grid_angle_degrees)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)

    pixels = channel_img.load()
    output_pixels = output_image.load()

    for y in range(0, image_height, cell_size):
        for x in range(0, image_width, cell_size):
            cell_sum = 0
            cell_count = 0
            for dy in range(cell_size):
                for dx in range(cell_size):
                    px = min(x + dx, image_width - 1)
                    py = min(y + dy, image_height - 1)
                    cell_sum += pixels[px, py]
                    cell_count += 1
            
            avg_intensity = cell_sum / cell_count
            dot_radius = (avg_intensity / 255.0) * (cell_size / 2.0)
            
            cell_center_x = x + cell_size / 2
            cell_center_y = y + cell_size / 2
            for dy in range(cell_size):
                for dx in range(cell_size):
                    px = min(x + dx, image_width - 1)
                    py = min(y + dy, image_height - 1)
                    
                    rel_x = (dx - cell_size / 2.0)
                    rel_y = (dy - cell_size / 2.0)
                    rot_x = rel_x * cos_a - rel_y * sin_a
                    rot_y = rel_x * sin_a + rel_y * cos_a
                    
                    dist = math.sqrt(rot_x**2 + rot_y**2)
                    
                    if dist <= dot_radius:
                        output_pixels[px, py] = 0
                    else:
                        output_pixels[px, py] = 255
    return output_image

def process_images(selected_images, add_cropmarks=False, add_halftones=False, split_channels=False):
    # uhhh uhhh whats the order here. um.
    # first we make sure there is a selection. actually dat happens in decide whether to go. 
    # cmyk version, split channels, crop marks, halftones
    # how do i make sure that once images are split i use split images for everything
    for img_path in selected_images:
        # hi
        print("im so hungry right now...")
    pass

def main():
    window = Tk() # i made a window
    window.geometry("800x500")
    window.title("CMYK Helper :D")
    frame = Frame(window, bg="skyblue", width=750, height=450)
    frame.pack(padx=0, pady=50)
    selected_images = []

    no_imgs_label = Label(frame, text="", bg="skyblue")
    no_imgs_label.pack()

    def if_nothing_selected():
        
        if not selected_images:
            no_imgs_label.config(text="No images selected.")
        else:
            no_imgs_label.config(text=f"{len(selected_images)} images selected.")
    
    def no_options_selected():
        no_imgs_label.config(text="No processing options selected. Please choose at least one option.")

    def decide_whether_to_go(selected_images, add_cropmarks, add_halftones, split_channels):
        if not selected_images:
            if_nothing_selected()
            return False
        if not (add_cropmarks or add_halftones or split_channels):
            no_options_selected()
            return False
        return True

    def store_images():
        nonlocal selected_images
        files = filedialog.askopenfilenames(title="Select images to process",
                filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if files:
            selected_images = list(files)
            no_imgs_label.config(text=f"{len(selected_images)} image(s) selected.")
        else:
            selected_images = []
            no_imgs_label.config(text="No images selected.")
        
            upload_button = Button(frame, text="Upload Images", command=store_images)
        upload_button.pack(pady=30)

        # the options
    whether_to_cropmark_var = IntVar()
    whether_to_halftone_var = IntVar()
    whether_to_split_var = IntVar()
    cropmark_checkbox = Checkbutton(frame, bg="skyblue", text="Add Crop Marks", variable=whether_to_cropmark_var)
    halftone_checkbox = Checkbutton(frame, bg="skyblue", text="Halftone", variable=whether_to_halftone_var)
    split_checkbox = Checkbutton(frame, bg="skyblue", text="Split into Channels", variable=whether_to_split_var)

    cropmark_checkbox.pack(anchor=W)
    halftone_checkbox.pack(anchor=W)
    split_checkbox.pack(anchor=W)

        
    go_button = Button(frame, text="Go", command=lambda: (
        decide_whether_to_go(
            selected_images,
            bool(whether_to_cropmark_var.get()),
            bool(whether_to_halftone_var.get()),
            bool(whether_to_split_var.get())
        ) and process_images(
            selected_images,
            add_cropmarks=bool(whether_to_cropmark_var.get()),
            add_halftones=bool(whether_to_halftone_var.get()),
            split_channels=bool(whether_to_split_var.get())
        )
    ))

if __name__ == "__main__":
    main()
