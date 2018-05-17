import tkinter
from PIL import ImageTk, Image
import numpy
import os

# Listener callbacks
def listenClick(event):
	global current
	print('Clicking', event.x, event.y)
	for pt in new:
		point = w.coords(pt)
		if (event.x >= point[0] and event.x <= point[2]) and (event.y >= point[1] and event.y <= point[3]):
			print('Exists', w.type(pt))
			current = pt
			return
	print('Creating point')
	createPoint(event)
def listenDrag(event):
	global current
	print('Dragging', event.x, event.y)
	print(current != None)
	if current != None:
		print('Dragging it!', event.x, event.y)
		movePoint(event)
		for pt in range(len(new)):
			if current == new[pt]:
				new_coords = getActualCoords(new[pt])
				orig_coords = getActualCoords(original[pt])
				old_coords = w.coords(arrows[pt])
				w.coords(arrows[pt], old_coords[0], old_coords[1], new_coords[0], new_coords[1])
def listenRelease(event):
	global current
	print('Releasing', event.x, event.y)
	current = None

# Create points
def createPoint(event):
	original.append(w.create_oval(event.x-9, event.y-9, event.x+9, event.y+9, width=0, fill="#ff0000",activefill="#ff0000",disabledfill="#ff0000"))
	new.append(w.create_oval(event.x-9, event.y-9, event.x+9, event.y+9, width=0, fill="#00ff00"))
	arrow = w.create_line(event.x, event.y, event.x, event.y, width=2, arrow=tkinter.LAST)
	arrows.append(arrow)
# Move point
def movePoint(event):
	w.coords(current, event.x-9, event.y-9, event.x+9, event.y+9)
# Get points
def getPoints():
	return original, new
# Get picture
def getPicture():
	return numpy.asarray(rimg1)
def getActualCoords(point):
	coords = w.coords(point)
	return coords[0]+9, coords[1]+9

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

# Create points
current = None
new = []
original = []
arrows = []

# w.pack(expand="yes", fill="both")
w.pack()
top.mainloop()	