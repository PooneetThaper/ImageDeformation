import tkinter
from PIL import ImageTk, Image
import numpy as np
import os
from deformation import deform

# Listener callbacks
def listenClick(event):
        global w, current, new
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
        global w, current, new, original, arrows
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
        global current, img2
        print('Releasing', event.x, event.y)
        current = None
        # Deform picture
        # img2 = arrayToPicture(deformation.deform(getPicture(rimg1), original, new))
        # w.create_image(width,0, image=img2, anchor="nw")
def listenHover(event):
        updateMouseCoord(event)
def deformPicture():
        global rimg1, img2, img2_canvas
        p, q = getPoints()
        print("List of points p:", p)
        print("List of points q:", q)
        image = getPicture(rimg1)
        real_p = np.array(p).astype(np.int)
        real_q = np.array(q).astype(np.int)
        deformed = deform(image, p, q)
        img2 = ImageTk.PhotoImage(arrayToPicture(deformed))
        w.itemconfigure(img2_canvas, image=img2)
# Create points
def createPoint(event):
        global w, width, height, new, coord
        if event.x < 0 or event.x > width or event.y < 0 or event.y > height:
                w.itemconfigure(coord, text=w.itemcget(coord, 'text')+' Out of bounds')
                return
        x = event.x
        y = event.y
        original.append(w.create_oval(x-9, y-9, x+9, y+9, width=0, fill="#ff0000",activefill="#ff0000",disabledfill="#ff0000"))
        new.append(w.create_oval(x-9, y-9, x+9, y+9, width=0, fill="#00ff00"))
        arrow = w.create_line(x, y, x, y, width=2, arrow=tkinter.LAST)
        arrows.append(arrow)
# Move point
def movePoint(event):
        global width, height
        if event.x < 0:
                x = 0
        elif event.x > width:
                x = width
        else:
                x = event.x
        if event.y < 0:
                y = 0
        elif event.y > height:
                y = height
        else:
                y = event.y
        error_msg = ' Out of bounds' if x != event.x or y != event.y else ''
        w.coords(current, x-9, y-9, x+9, y+9)
        w.itemconfigure(coord, text='%d, %d'%(event.x, event.y) + error_msg)
# Get points
def getPoints():
        global original, new
        return list(map(getActualCoords, original)), list(map(getActualCoords, new))
# Get picture
def getPicture(pic):
        return np.asarray(pic)
def arrayToPicture(arr):
        return Image.fromarray(np.uint8(arr))
def getActualCoords(point):
        coords = w.coords(point)
        return coords[0]+9, coords[1]+9
def updateMouseCoord(event):
        global w, coord
        w.itemconfigure(coord, text='%d, %d'%(event.x, event.y))
def main():
        global w, width, height, new, original, arrows, coord, rimg1, img2, img2_canvas
        # Initialize window and canvas
        top = tkinter.Tk()
        w = tkinter.Canvas(top)
        # Event Listeners
        w.bind('<Button-1>', listenClick)
        w.bind('<B1-Motion>', listenDrag)
        w.bind('<ButtonRelease-1>', listenRelease)
        w.bind('<Motion>', listenHover)

        # Open Image
        rimg1 = Image.open("./dorabenny.jpg")
        [width, height] = rimg1.size

        # Set window to twice width to fit two pictures
        w.config(width=width*2, height=height)
        img1 = ImageTk.PhotoImage(rimg1)

        # Figure out transformation matrix/calculations here
        # a = 1
        # b = 0.5
        # c = 1
        # d = 0
        # e = 0.5
        # f = 0
        # rimg2 = rimg1.transform((width, height), Image.AFFINE, (a,b,c,d,e,f), Image.BICUBIC)
        # img2 = ImageTk.PhotoImage(rimg2)
        #rimg2 = None
        # Create images
        w.create_image(0, 0, image=img1, anchor="nw")
        w.create_line(width, 0, width, height)
        img2 = None
        img2_canvas = w.create_image(width,0, image=img2, anchor="nw")

        deformButton = tkinter.Button(text="deform", command=deformPicture)

        w.create_window(width*2, 0, window=deformButton, anchor="nw")

        # Create points
        current = None
        new = []
        original = []
        arrows = []

        # Coordinate indicator
        coord = w.create_text(10, height)
        w.itemconfigure(coord, text='0 0', anchor="sw")
        # w.pack(expand="yes", fill="both")
        w.pack()
        top.mainloop()

if __name__ == '__main__':
        main()
