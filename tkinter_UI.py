import numpy as np
import cv2
import tkinter as tk
from tkinter import messagebox as mb
from PIL import Image, ImageTk, ImageOps
import tensorflow.keras
import time

np.set_printoptions(suppress=True)
# Load the model
model = tensorflow.keras.models.load_model('keras_model.h5')
#Set up GUI
window = tk.Tk()  #Makes main window
window.wm_title("Home security")
window.config(background="#FFFFFF")

#Graphics window
imageFrame = tk.Frame(window, width=600, height=500)
imageFrame.grid(row=0, column=0, padx=10, pady=2)
imageFrame.pack()

#Capture video frames
lmain = tk.Label(imageFrame)
lmain.grid(row=0, column=0)
cap = cv2.VideoCapture(0)
def prediction():
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    size = (224, 224)
    image = Image.open('upload1.jpg')
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    class1=prediction[0][0]
    class2=prediction[0][1]
    return class1>class2
def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    cv2.imwrite('upload1.jpg',frame)
    p=prediction()
    global start
    global end_time
    if p==True:
        if(start==True):
            start=False
            end_time = time.time() + 3
        canvas.itemconfig(oval_red, fill="white")
        canvas.itemconfig(oval_green, fill="green")
        if time.time() > end_time:
            MsgBox = mb.showinfo('Welcome', 'You can come in :)))')
            start=True
            end_time=0

    else:
        canvas.itemconfig(oval_red, fill="red")
        canvas.itemconfig(oval_green, fill="white")
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame) 



#Slider window (slider controls stage position)

sliderFrame = tk.Frame(window, width=600, height=100)
canvas = tk.Canvas(window, width=600, height=100, bg="white")
oval_red = canvas.create_oval(10, 10, 100, 100, fill="white")
oval_green = canvas.create_oval(110, 10, 200, 100, fill="white")
canvas.pack()

start = True
end_time=0
show_frame()  #Display 2
window.mainloop()  #Starts GUI
