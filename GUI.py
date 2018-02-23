from Tkinter import *
import RPi.GPIO as gpio
import time
import cv2
from PIL import Image, ImageTk
from imutils.video import VideoStream
import threading
import imutils

# width, height = 800, 600
# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

def init():
	gpio.setmode(gpio.BOARD)
	gpio.setup(7,gpio.OUT)
	gpio.setup(11,gpio.OUT)
	gpio.setup(13,gpio.OUT)
	gpio.setup(15,gpio.OUT)
	gpio.setup(10,gpio.OUT)
	gpio.setup(12,gpio.OUT)
	gpio.setup(16,gpio.OUT)
	gpio.setup(18,gpio.OUT)
def move_forward(t):
        init()
	gpio.output(7,True)
	gpio.output(11,True)
	gpio.output(13,True)
	gpio.output(15,True)
	gpio.output(10,True)
	gpio.output(12,True)
	gpio.output(16,True)
	gpio.output(18,True)
	
	time.sleep(t)
	gpio.cleanup()
def move_backward(t):
        init()
	gpio.output(7,True)
	gpio.output(11,True)
	gpio.output(13,True)
	gpio.output(15,True)
	
	gpio.output(10,False)
	gpio.output(12,False)
	gpio.output(16,False)
	gpio.output(18,False)
	
	time.sleep(t)
	gpio.cleanup()

def turn_left(t):
        init()
	gpio.output(7,True)
	gpio.output(11,False)
	gpio.output(13,False)
	gpio.output(15,True)
	
	gpio.output(10,True)
	gpio.output(18,True)
	
	time.sleep(t)
	gpio.cleanup()
def turn_right(t):
        init()
	gpio.output(7,False)
	gpio.output(11,True)
	gpio.output(13,True)
	gpio.output(15,False)
	
	gpio.output(12,True)
	gpio.output(16,True)
	
	time.sleep(t)
	gpio.cleanup()

def pivot_left(t):
        init()
	gpio.output(7,True)
	gpio.output(11,True)
	gpio.output(13,True)
	gpio.output(15,True)
	
	gpio.output(10,True)
	gpio.output(18,True)
	gpio.output(12,False)
	gpio.output(16,False)
	
	time.sleep(t)
	gpio.cleanup()
def pivot_right(t):
        init()
	gpio.output(7,True)
	gpio.output(11,True)
	gpio.output(13,True)
	gpio.output(15,True)
	
	gpio.output(10,False)
	gpio.output(18,False)
	gpio.output(12,True)
	gpio.output(16,True)
	
	time.sleep(t)
	gpio.cleanup()
def stop(t):
    init()
    gpio.output(7,False)
    gpio.output(11,False)
    gpio.output(13,False)
    gpio.output(15,False)
    
    time.sleep(t)
    gpio.cleanup()
def key_input(event):
	print "key: ",event.char
	key_press = event.char
	sleep_time = 0.3
	if key_press.lower() == "w":
		move_forward(sleep_time)
	elif key_press.lower() == "s":
		move_backward(sleep_time)
	elif key_press.lower() == "d":
		turn_right(sleep_time)
	elif key_press.lower() == "a":
		turn_left(sleep_time)
	elif key_press.lower() == "q":
		pivot_left(sleep_time)
	elif key_press.lower() == "e":
		pivot_right(sleep_time)
	else:
		stop(sleep_time)


root = Tk()

root.bind('<Escape>', lambda e: root.quit())
root.attributes('-fullscreen', True)
root.configure(background='black')
root.bind('<KeyPress>',key_input)
'''
canvas = Canvas(root, width=500, height=420,bg='red')
canvas.place(x = 400,y=200)
'''
frame = None
thread = None
stopEvent = None
panel = None
vs = VideoStream(0).start()

def exit():
        global root,vs,stopEvent
        vs.stop()
        stopEvent.set()
        stop(0.3)
        root.quit()

# root.title("Controll the Auto")
# root.geometry("600x400")
def videoLoop():
        global frame,stopEvent,panel,vs,root
        try:
                # keep looping over frames until we are instructed to stop
                while not stopEvent.is_set():
                        # grab the frame from the video stream and resize it to
                        # have a maximum width of 300 pixels
                        frame = vs.read()
                        frame = imutils.resize(frame, width=700,height=600)

                        # OpenCV represents images in BGR order; however PIL
                        # represents images in RGB order, so we need to swap
                        # the channels, then convert to PIL and ImageTk format
                        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        image = Image.fromarray(image)
                        image = ImageTk.PhotoImage(image)

                        # if the panel is not None, we need to initialize it
                        if panel is None:
                                panel = Label(image=image)
                                panel.image = image
                                panel.place(x = 250 ,y=150)

                        # otherwise, simply update the panel
                        else:
                                panel.configure(image=image)
                                panel.image = image

        except RuntimeError, e:
                print("[INFO] caught a RuntimeError")

def onClose():
        global stopEvent,vs,root  
        # set the stop event, cleanup the camera, and allow the rest of
        # the quit process to continue
        print("[INFO] closing...")
        stopEvent.set()
        vs.stop()
        root.quit()

# start a thread that constantly pools the video sensor for
# the most recently read frame
stopEvent = threading.Event()
thread = threading.Thread(target=videoLoop, args=())
thread.start()

# set a callback to handle when the window is closed
root.wm_title("PyImageSearch PhotoBooth")
root.wm_protocol("WM_DELETE_WINDOW", onClose)




running = False
jobid = None


def start_motor(direction):
    print("starting motor...(%s)" % direction)
    
    Moving_direction = Label(root,text='Moving'+direction+" ")
    Moving_direction.place(x=500,y=200)
    move(direction)


def stop_motor():
    global jobid
    root.after_cancel(jobid)
    stop(0.3)
    print("stopping motor...")

def move(direction):
    global jobid
    print("Moving (%s)" % direction)
    t = 0.3
    if direction == "up":
    	move_forward(t)
    elif direction == "right":
    	turn_right(t)
    elif direction == "down":
    	move_backward(t)
    elif direction == "left":
    	turn_left(t)
    elif direction == "clockwise":
    	pivot_right(t)
    elif direction == "counterclockwise":
    	pivot_left(t)
    else:
    	stop(t)
    jobid = root.after(5, move, direction)






up_button = Button(root,bg='black')
right_button = Button(root,bg='black')
down_button = Button(root,bg='black')
left_button = Button(root,bg='black')
left_button = Button(root,bg='black')
left_button = Button(root,bg='black')
clockwise_button = Button(root,bg='black')
counterclcokwise_button = Button(root,bg='black')

up_image = ImageTk.PhotoImage(file="up_arrow.png")
right_image = ImageTk.PhotoImage(file="right_arrow.png")
down_image = ImageTk.PhotoImage(file="down_arrow.png")
left_image = ImageTk.PhotoImage(file="left_arrow.png")
clockwise_image = ImageTk.PhotoImage(file="clockwise-arrow.png")
counterclockwise_image = ImageTk.PhotoImage(file="Counterclockwise-arrow.png")

up_button.config(image = up_image)
right_button.config(image = right_image)
down_button.config(image = down_image)
left_button.config(image = left_image)
clockwise_button.config(image = clockwise_image)
counterclcokwise_button.config(image = counterclockwise_image)

up_button.place(x=1100,y=400)
right_button.place(x=1200,y=450)
down_button.place(x=1100,y=500)
left_button.place(x=1000,y=450)
clockwise_button.place(x = 1200, y = 300)
counterclcokwise_button.place(x = 1000 , y = 300)

up_button.bind('<ButtonPress-1>', lambda event, direction="up": start_motor(direction))
up_button.bind('<ButtonRelease-1>', lambda event: stop_motor())

right_button.bind('<ButtonPress-1>', lambda event, direction="right": start_motor(direction))
right_button.bind('<ButtonRelease-1>', lambda event: stop_motor())

down_button.bind('<ButtonPress-1>', lambda event, direction="down": start_motor(direction))
down_button.bind('<ButtonRelease-1>', lambda event: stop_motor())

left_button.bind('<ButtonPress-1>', lambda event, direction="left": start_motor(direction))
left_button.bind('<ButtonRelease-1>', lambda event: stop_motor())

clockwise_button.bind('<ButtonPress-1>', lambda event, direction="clockwise": start_motor(direction))
clockwise_button.bind('<ButtonRelease-1>', lambda event: stop_motor())

counterclcokwise_button.bind('<ButtonPress-1>', lambda event, direction="counterclockwise": start_motor(direction))
counterclcokwise_button.bind('<ButtonRelease-1>', lambda event: stop_motor())


title = Label(root, text='Controll the Vehicle', font='Calibri 22 ',bg='black',fg='gray')
title.place(x = 450 , y = 50)

Instruction = Label(root,text = 'You can use HotKey \n\n    w ==> forward \n  d ==> right \n s ==> back \n a ==> left \n    q ==> counter \n  e ==> clock ',
	bg = 'black',fg='red',font = 'Calibri 12')
Instruction.place(x = 100,y = 50)

distance = Label(root,text= 'Distance \n  23 cm',font='Calibri 12',fg='red',bg='black' )
distance.place(x=100,y=500)
root.mainloop()
