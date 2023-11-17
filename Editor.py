import tkinter as tk
from tkinter import Tk, LabelFrame, Button, Canvas, filedialog, colorchooser
from PIL import Image, ImageTk, ImageFilter, ImageColor, ImageOps, ImageEnhance
from tkinter import ttk
import os

# start code
root = tk.Tk()
root.geometry("1000x600")
root.title("Photo Editor")
root.config(bg="white")

pen_color = "black"
pen_size = 5
file_path = ""
color1 = '#020f12'
color2 = '#05d7ff'
color3 = '#65e7ff'
color4 = 'BLACK'

# functions

def add_image():
    global file_path
    global image# usable outside the function
    file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png"),
                                                      ("JPEG files", "*.jpg"),
                                                      ("All files", "*.*")])
    image = Image.open(file_path)


    width_factor = canvas_width/image.width
    height_factor = canvas_height/image.height

    min_factor = min(width_factor, height_factor)
    global new_width, new_height
    new_width = int(image.width * min_factor)
    new_height = int(image.height * min_factor)

    image = image.resize((new_width, new_height), Image.ANTIALIAS)
    global x_position, y_position
    x_position = (canvas_width - new_width) // 2
    y_position = (canvas_height - new_height) // 2


    image = ImageTk.PhotoImage(image)

    canvas.image = image
    canvas.create_image(x_position,y_position,image=image, anchor="nw")

def draw(event):
    x1,y1 = (event.x-pen_size), (event.y-pen_size)
    x2,y2 = (event.x+pen_size), (event.y+pen_size)
    canvas.create_oval(x1,y1,x2,y2, fill=pen_color, outline="")

def change_color():
    global pen_color
    pen_color = colorchooser.askcolor(title="Select Pen Color")[1]

def change_size(size):
    global pen_size
    pen_size = size

def clear_canvas():
   canvas.delete("all")
   canvas.create_image(x_position, y_position, image=image, anchor="nw")

def apply_filter(filter):
    image = Image.open(file_path)
    image = image.resize((new_width, new_height), Image.ANTIALIAS)
    if filter == "Black and White":
        image = ImageOps.grayscale(image=image)
    elif filter == "Sharpen":
        image = image.filter(ImageFilter.UnsharpMask(radius=5))
    elif filter == "Blur":
        image = image.filter(ImageFilter.BLUR)
    elif filter == "Emboss":
        image = image.filter(ImageFilter.EMBOSS)
    elif filter == "Smooth":
        image = image.filter(ImageFilter.SMOOTH)
    elif filter == "Invert":
        image = ImageOps.invert(image)
    elif filter == "Autocontrast":
        image = ImageOps.autocontrast(image=image, cutoff=5)
    elif filter == "Auto":
        image = ImageEnhance.Color(image).enhance(1.2)
        image = ImageEnhance.Contrast(image).enhance(1)
        image = image.filter(ImageFilter.UnsharpMask(radius=1.5))
        image = ImageEnhance.Brightness(image).enhance(1.2)
        image = image.filter(ImageFilter.GaussianBlur(radius=0.5))
    image = ImageTk.PhotoImage(image)
    canvas.image = image
    canvas.create_image(x_position, y_position, image=image, anchor="nw")

def blend_image():
    file_path2 = filedialog.askopenfilename(filetypes=[("PNG files", "*.png"),
                                                      ("JPEG files", "*.jpg"),
                                                      ("All files", "*.*")])
    image1 = Image.open(file_path)
    image1 = image1.resize((new_width, new_height), Image.ANTIALIAS)
    image2 = Image.open(file_path2)
    image2 = image2.resize((image1.size[0], image1.size[1]), Image.ANTIALIAS)

    blended_image = Image.composite(image1,image2,Image.new('L', image1.size,100))

    blended_image = ImageTk.PhotoImage(blended_image)
    canvas.image = blended_image
    canvas.create_image(x_position, y_position, image=blended_image, anchor="nw")

def save():
    if canvas:
        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"),
                                                            ("All files", "*.*")])
        if save_path:
            # Create a postscript file
            canvas.postscript(file=save_path + ".ps", colormode='color')

            # Convert the postscript file to an image file
            img = Image.open(save_path + ".ps")
            img.save(save_path, format="png")

            # Remove the temporary postscript file
            os.remove(save_path + ".ps")



# left_frame #

left_frame = tk.Frame(root, width=200,height=600, bg="purple")
left_frame.pack(side="left", fill ="y")



# canvas #
canvas_width, canvas_height =800,600
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()


# buttons #
image_button = tk.Button(left_frame,
                         background='PURPLE',
                         foreground=color4,
                         activebackground= color3,
                         activeforeground=color4,
                         highlightthickness=2,
                         highlightbackground='PURPLE',
                         highlightcolor='WHITE',
                         cursor='hand1',
                         text="Upload",
                         font=('Arial',13, 'bold'),
                         command=add_image, bg="white")
image_button.pack(pady=15)

color_button = tk.Button(left_frame,
                         background='PURPLE',
                         foreground=color4,
                         activebackground= color3,
                         activeforeground=color4,
                         highlightthickness=2,
                         highlightbackground='PURPLE',
                         highlightcolor='WHITE',
                         cursor='hand1',
                         text="Change Pen Color",
                         font=('Arial',13, 'bold'),
                         command=change_color, bg="white")
color_button.pack(pady=15)

# pen_size_frame

pen_size_frame = tk.Frame(left_frame, bg="white")
pen_size_frame.pack(pady=5)

# radio buttons #
pen_size_1 = tk.Radiobutton(pen_size_frame, text="Small", value=3, command=lambda: change_size(3), bg="white")
pen_size_1.pack(side="left")
pen_size_2 = tk.Radiobutton(pen_size_frame, text="Medium", value=5, command=lambda: change_size(5), bg="white")
pen_size_2.pack(side="left")
pen_size_2.select()
pen_size_3 = tk.Radiobutton(pen_size_frame, text="Large", value=7, command=lambda: change_size(7), bg="white")
pen_size_3.pack(side="left")

# clear button

clear_button = tk.Button(left_frame,
                         background='PURPLE',
                         foreground=color4,
                         activebackground=color3,
                         activeforeground=color4,
                         highlightthickness=2,
                         highlightbackground='PURPLE',
                         highlightcolor='WHITE',
                         cursor='hand1',
                         text="Clear",
                         font=('Arial',13,'bold'),
                         command=clear_canvas, bg="#FF9797")
clear_button.pack(pady=10)

# filter section #

filter_label = tk.Label(left_frame, text="Select Filter", fg='white', bg="purple")
filter_label.pack(pady=0)
arrow_label = tk.Label(left_frame, text="↓↓↓", fg='white', bg="purple")
arrow_label.pack(pady=0)
filter_combobox = ttk.Combobox(left_frame, values=["Black and White", "Blur", "Emboss",
                                                  "Sharpen", "Smooth", "Invert",
                                                  "Autocontrast", "Auto"])
filter_combobox.pack()

# combobox functions #
filter_combobox.bind("<<ComboboxSelected>>", lambda event: apply_filter(filter_combobox.get()))

canvas.bind("<B1-Motion>",draw)

# blend button #
blend_button = tk.Button(left_frame,
                         background='PURPLE',
                         foreground=color4,
                         activebackground=color3,
                         activeforeground=color4,
                         highlightthickness=2,
                         highlightbackground='PURPLE',
                         highlightcolor='WHITE',
                         cursor='hand1',
                         text="Blend",
                         font=('Arial', 13, 'bold'),
                         command=blend_image, bg="White" )
blend_button.pack(pady=10)

# save button #
save_button = tk.Button(left_frame,
                        background='PURPLE',
                        foreground=color4,
                        activebackground=color3,
                        activeforeground=color4,
                        highlightthickness=2,
                        highlightbackground='PURPLE',
                        highlightcolor='WHITE',
                        cursor='hand1',
                        text="Save",
                        font=('Arial', 13, 'bold'),
                        command=save, bg="White")
save_button.pack(pady=10)



root.mainloop()

