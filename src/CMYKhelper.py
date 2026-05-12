from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageDraw
import math
import numpy as np

def get_split_image_into_channels(img):
    img_CMYK = img.convert("CMYK")
    cyan, magenta, yellow, key = img_CMYK.split()
    return cyan, magenta, yellow, key

def give_cropmarked_images(img, padding=150):
    w, h = img.size
    new_size = (w + padding*2, h + padding*2)
    new_img = Image.new("CMYK", new_size, (0, 0, 0, 0))
    new_img.paste(img.convert("CMYK"), (padding, padding))

    draw = ImageDraw.Draw(new_img)
    black = (0, 0, 0, 255)

    corners = [
        (padding, padding),           # top left
        (padding + w, padding),       # top right
        (padding, padding + h),       # bottom left
        (padding + w, padding + h),   # bottom right
    ]

    for cx, cy in corners:
        mark_thickness = 3
        mark_length = 50
        dx = -1 if cx == padding else 1
        draw.line(
            [(cx, cy), (cx + dx * mark_length, cy)],
            fill=black, width=mark_thickness
        )

        dy = -1 if cy == padding else 1
        draw.line(
            [(cx, cy), (cx, cy + dy * mark_length)],
            fill=black, width=mark_thickness
        )
    
    return new_img

def halftone_whole_image(img, cell_size):
    img = img.convert("CMYK")
    cyan, magenta, yellow, key = img.split()
    cyan_halftone = halftone_one_channel(cyan, cell_size, 15)
    magenta_halftone = halftone_one_channel(magenta, cell_size, 75)
    yellow_halftone = halftone_one_channel(yellow, cell_size, 0)
    key_halftone = halftone_one_channel(key, cell_size, 45)
    merged = Image.merge(
        "CMYK",
        (
            cyan_halftone,
            magenta_halftone,
            yellow_halftone,
            key_halftone
        )
    )
    return merged

def halftone_one_channel(channel_img, cell_size, grid_angle_degrees):

    image_width, image_height = channel_img.size
    # switched to numpy for array &faster processing 
    img_array = np.array(channel_img, dtype=np.float32)
    output = np.ones((image_height, image_width), dtype=np.float32)

    angle_rad = math.radians(grid_angle_degrees)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)

    cell_range = np.arange(cell_size)
    dx_grid, dy_grid = np.meshgrid(cell_range - cell_size / 2.0, cell_range - cell_size / 2.0)

    # stupid sin cos rotation for dist calc
    rot_x = dx_grid * cos_a - dy_grid * sin_a
    rot_y = dx_grid * sin_a + dy_grid * cos_a
    dist_grid = np.sqrt(rot_x**2 + rot_y**2) # no loops needed. grid of distance from cell center for each pixel
    # determines whether to draw dot or nah

    for y in range(0, image_height, cell_size):
        for x in range(0, image_width, cell_size):
            cell = img_array[y:y+cell_size, x:x+cell_size]
            avg_intensity = cell.mean()
            dot_radius = (1.0 - avg_intensity / 255.0) * (cell_size / 2.0)

            cell_h, cell_w = cell.shape
            dot_mask = dist_grid[:cell_h, :cell_w] <= dot_radius
            output[y:y+cell_size, x:x+cell_size] = np.where(dot_mask, 0.0, 1.0)
    return Image.fromarray((output * 255).astype(np.uint8), mode="L")

def process_images(selected_images, add_cropmarks=False, add_halftones=False, split_channels=False, cell_size=10):
    for img_path in selected_images:
        img_name = img_path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
        img = Image.open(img_path)
        img_CMYK = img.convert("CMYK")

        processed_img = img_CMYK

        if split_channels:
            cyan, magenta, yellow, key = get_split_image_into_channels(img_CMYK)

        if add_cropmarks:
            if split_channels:
                cropmarked = give_cropmarked_images(img_CMYK)
                cyan, magenta, yellow, key = cropmarked.split()
            else:
                processed_img = give_cropmarked_images(processed_img)

        if add_halftones:
            if split_channels:
                cyan_halftone = halftone_one_channel(cyan, cell_size, 15)
                magenta_halftone = halftone_one_channel(magenta, cell_size, 75)
                yellow_halftone = halftone_one_channel(yellow, cell_size, 0)
                key_halftone = halftone_one_channel(key, cell_size, 45)
            else:
                processed_img = halftone_whole_image(processed_img, cell_size)

        # a less chopped save system

        suffix = ""
        if add_cropmarks:
            suffix += "_cropmarked"
        if add_halftones:
            suffix += "_halftoned"

        if split_channels:
            channels = (cyan_halftone, magenta_halftone, yellow_halftone, key_halftone) if add_halftones else (cyan, magenta, yellow, key)
            for channel, name in zip(channels, ("cyan", "magenta", "yellow", "key")):
                channel.save(f"{img_name}_{name}{suffix}.pdf", resolution=300.0)
        else:
            processed_img.save(f"{img_name}_CMYK{suffix}.pdf", resolution=300.0)
            
def main():
    window = Tk()
    window.geometry("500x400")
    window.title("CMYK Helper :D")
    window.configure(bg="#8fffda")

    selected_images = []
    # frame
    frame = Frame(window, bg="white", padx=20, pady=20)
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    # title
    Label(frame, text="CMYK Helper", font=("Helvetica", 16, "bold"), bg="white").pack(anchor=W)
    Label(frame, text="Prepare images for screenprinting", font=("Helvetica", 9), fg="gray", bg="white").pack(anchor=W)
    
    def no_options_selected():
        no_imgs_label.config(text="No processing options selected. Please choose at least one option.")

    def toggle_halftone_entry(*args):
        if whether_to_halftone_var.get():
            halftone_size_frame.pack(anchor=W, padx=(22, 0), pady=(2, 4))
        else:
            halftone_size_frame.pack_forget()

    def decide_whether_to_go(selected_images, add_cropmarks, add_halftones, split_channels):
        if not selected_images:
            no_imgs_label.config(text="No images selected.")
            return False
        elif not (add_cropmarks or add_halftones or split_channels):
            no_options_selected()
            return False
        else:
            return True
        
    def on_go():
        try:
            cell_size = int(halftone_size_entry.get()) if whether_to_halftone_var.get() else 10
        except ValueError:
            cell_size = 10
            no_imgs_label.config(text="Invalid cell size, using default of 10.")
        decide_whether_to_go(
            selected_images,
            bool(whether_to_cropmark_var.get()),
            bool(whether_to_halftone_var.get()),
            bool(whether_to_split_var.get())
        ) and process_images(
            selected_images,
            add_cropmarks=bool(whether_to_cropmark_var.get()),
            add_halftones=bool(whether_to_halftone_var.get()),
            split_channels=bool(whether_to_split_var.get()),
            cell_size=cell_size
        )

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
        
    Frame(frame, bg="#e0e0e0", height=1).pack(fill=X, pady=10)  # divider

    # upload 

    upload_button = Button(frame, text="+ Upload Images", command=store_images,
        bg="#4a90d9", fg="white", relief=FLAT, padx=12, pady=6, cursor="hand2")
    upload_button.pack(fill=X)

    no_imgs_label = Label(frame, text="No images selected.", font=("Helvetica", 8),
        fg="gray", bg="white")
    no_imgs_label.pack(anchor=W, pady=(4, 0))

    Frame(frame, bg="#e0e0e0", height=1).pack(fill=X, pady=10)  # divider

    # options
    Label(frame, text="Processing Options", font=("Helvetica", 10, "bold"), bg="white").pack(anchor=W, pady=(0,6))

    whether_to_cropmark_var = IntVar()
    whether_to_halftone_var = IntVar()
    whether_to_split_var = IntVar()

    check_style = {"bg": "white", "activebackground": "white", "font": ("Helvetica", 10)}
    cropmark_checkbox = Checkbutton(frame, text="Add Crop Marks", variable=whether_to_cropmark_var, **check_style)
    halftone_checkbox = Checkbutton(frame, text="Halftone", variable=whether_to_halftone_var, **check_style)
    halftone_size_frame = Frame(frame, bg="white")
    Label(halftone_size_frame, text="Cell size:", font=("Helvetica", 9), fg="gray", bg="white").pack(side=LEFT)

    halftone_size_entry = Entry(halftone_size_frame, width=5, relief=SOLID)
    halftone_size_entry.insert(0, "10")
    halftone_size_entry.pack(side=LEFT, padx=(4,0))

    split_checkbox = Checkbutton(frame, text="Split into Channels", variable=whether_to_split_var, **check_style)
    cropmark_checkbox.pack(anchor=W)
    halftone_checkbox.pack(anchor=W)

    whether_to_halftone_var.trace_add("write", toggle_halftone_entry)

    split_checkbox.pack(anchor=W)

    Frame(frame, bg="#e0e0e0", height=1).pack(fill=X, pady=10)  # divider

    go_button = Button(frame, text="Go", command=on_go,
        bg="#2ecc71", fg="white", relief=FLAT, padx=12, pady=6, cursor="hand2", font=("Helvetica", 10, "bold"))
    go_button.pack(fill=X)
    window.mainloop() # i can open it now. im scared.

if __name__ == "__main__":
    main()