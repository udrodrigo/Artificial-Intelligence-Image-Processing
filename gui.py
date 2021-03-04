from tkinter import *
from tkinter import filedialog
import PIL.Image, PIL.ImageTk
import cv2
import numpy as np
from Stitch import join_horizontal, join_vertical, shuffle, split
from copy import deepcopy


class popupWindow(object):
    def __init__(self,master):
        top=self.top=Toplevel(master)
        self.l=Label(top,text="Enter Rows")
        self.l.pack()
        self.e=Entry(top)
        self.e.pack()
        self.l2=Label(top,text="Enter Cols")
        self.l2.pack()
        self.e2=Entry(top)
        self.e2.pack()
        self.b=Button(top,text='Ok',command=self.cleanup)
        self.b.pack()
    def cleanup(self):
        self.value=(int(self.e.get()), int(self.e2.get()))
        self.top.destroy()



class MainWindow:

    def __init__(self):
       
        self.window = Tk()
        self.window.geometry("800x400")
        self.window.title("Stitching Image")

        self.image = None
        self.parts = None
        self.is_shuffled = False

        res_frame = Frame(self.window, height=400)
        res_frame.pack(side=LEFT, anchor='n', pady=16)

        self.res_canvas = Canvas(res_frame, width=400, height=300, bg='gray')
        self.res_canvas.pack(side=TOP)

        inp_frame = Frame(self.window)
        inp_frame.pack(side=LEFT, anchor='n', pady=16)

        self.inp_canvas = Canvas(inp_frame, width=400, height=300, bg='gray')
        self.inp_canvas.pack(side=TOP)

        button_frame = Frame(inp_frame)
        button_frame.pack(side=BOTTOM, pady=16)

        stitch_button = Button(button_frame, text='<<', command=self.stitch)
        stitch_button.pack(side=LEFT, padx=16)

        shuffle_button = Button(button_frame, text='Shuffle', command = self.shuffle)
        shuffle_button.pack(side=LEFT, padx=16)

        cut_button = Button(button_frame, text='Cut', command=self.cut)
        cut_button.pack(side=LEFT, padx=16)
        
        load_button = Button(button_frame, text='File', command=self.load)
        load_button.pack(side=LEFT, padx=16)
    

    def display_inp(self, image):
        b,g,r = cv2.split(cv2.resize(image,(400,300)))
        img = cv2.merge((r,g,b))
        im = PIL.Image.fromarray(img)
        self.inp_imgtk = PIL.ImageTk.PhotoImage(image=im) 
        self.inp_canvas.create_image(0,0,image=self.inp_imgtk, anchor='nw')


    def display_res(self, image):

        b,g,r = cv2.split(cv2.resize(image,(400,300)))
        img = cv2.merge((r,g,b))
        im = PIL.Image.fromarray(img)
        self.res_imgtk = PIL.ImageTk.PhotoImage(image=im) 
        self.res_canvas.create_image(0,0,image=self.res_imgtk, anchor='nw')

    
    def load(self):
        filename = filedialog.askopenfilename()
        self.image = cv2.imread(filename)
        self.display_inp(self.image)

    
    def cut(self):
        self.popup()


    def popup(self):
        self.w=popupWindow(self.window)
        self.window.wait_window(self.w.top)
        self.r, self.c = self.w.value


    def shuffle(self):
        self.is_shuffled = True
        self.parts = shuffle(split(self.image, self.r, self.c))
        height, width, _ = self.image.shape
        image = deepcopy(self.image)
        row = self.r
        col = self.c
        h = height//row
        w = width//col    
        x = 0
        for i in range(row):
            for j in range(col):
                image[i*h:(i+1)*h,j*w:(j+1)*w,:] = self.parts[x]
                x += 1
        self.display_inp(image)


    def stitch(self):
        if self.is_shuffled:
            self.display_res(join_horizontal(join_vertical(self.parts, self.r*self.c, self.r), self.c))
            self.is_shuffled = False

    def run(self):
        self.window.mainloop()



MainWindow().run()
