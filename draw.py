import tkinter
from PIL import ImageTk, Image
import os

# Listener callbacks
def listenClick(event):
	print('Clicking', event.x, event.y)
def listenDrag(event):
	print('Dragging', event.x, event.y)
def listenRelease(event):
	print('Releasing', event.x, event.y)

# Initialize window and canvas
top = tkinter.Tk()
w = tkinter.Canvas(top)
# Event Listeners
w.bind('<Button-1>', listenClick)
w.bind('<B1-Motion>', listenDrag)
w.bind('<ButtonRelease-1>', listenRelease)

# Open Image
rimg1 = Image.open("./dorabenny.jpg")
[width, height] = rimg1.size

# Set window to twice width to fit two pictures
w.config(width=width*2, height=height)
img1 = ImageTk.PhotoImage(rimg1)

# Figure out transformation matrix/calculations here
a = 1
b = 0.5
c = 1
d = 0
e = 0.5
f = 0
rimg2 = rimg1.transform((width, height), Image.AFFINE, (a,b,c,d,e,f), Image.BICUBIC)
img2 = ImageTk.PhotoImage(rimg2)

# Create images
w.create_image(0, 0, image=img1, anchor="nw")
w.create_image(width,0, image=img2, anchor="nw")
# w.pack(expand="yes", fill="both")
w.pack()
top.mainloop()	