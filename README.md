# CMYK Helper :D

## Demo
Demo Video: https://youtu.be/l6FEfKLy_K8

## GitHub Repository
GitHub Repo: https://github.com/Samaya-V/Final-Project

## Description

CMYK Helper is a Python-based desktop application designed to simplify image preparation for screen printing workflows. The program provides an easy-to-use graphical interface that allows users to upload images and automatically process them for print production. It can add crop marks, split images into CMYK channels, and generate halftone versions of images.

The project was created using Python with the Tkinter library for the user interface, Pillow for image processing, and NumPy for fast pixel calculations. The interface is simple so users can quickly upload files, select processing options, and export print-ready images without needing advanced image editing software.

One of the main features of the program is CMYK channel separation. Uploaded images are converted into the CMYK color space and split into cyan, magenta, yellow, and key/black channels. These channels can then be saved individually for printing purposes. The application can also generate halftones for each channel using customizable cell sizes and different screen angles to reduce moiré patterns during printing.

Another feature is crop mark generation. The program creates padded images with crop marks placed around the edges to help align prints during the screen printing process. Crop marks are drawn using Pillow’s drawing tools.

The program structure is divided into several functions. `get_split_image_into_channels()` handles CMYK conversion and channel separation. `give_cropmarked_images()` creates crop marks and padding around images. `halftone_one_channel()` generates halftone patterns for individual channels using NumPy arrays for improved performance. `halftone_whole_image()` applies halftones across all CMYK channels and recombines them into a final image. Finally, `process_images()` manages the export workflow and saves processed files as PDFs.

There are several areas for future improvement, like live image previews, drag-and-drop uploading, and GPU-accelerated halftone rendering for faster processing of large images. Something to work on is the order of operations, as the added cropmarks end up getting halftoned at present.

Overall, CMYK Helper is a lightweight application for preparing images for screen printing.
