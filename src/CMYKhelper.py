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

def halftone_one_channel(channel_img, img_name, cell_size, grid_angle_degrees):
    image_width, image_height = channel_img.size
    output_image = Image.new("L", (image_width, image_height), 255)
    
    image_center_x = image_width / 2
    image_center_y = image_height / 2

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

def main():
    window = Tk() # i made a window
    window.geometry("800x500")
    window.title("CMYK Helper :D")
    window.mainloop() # i can open it now. im scared.

if __name__ == "__main__":
    main()
