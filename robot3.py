import RPi.GPIO as gpio
import time
import Tkinter as tk

def init():
	gpio.setmode(gpio.BOARD)
	gpio.setup(7,gpio.OUT)
	gpio.setup(11,gpio.OUT)
	gpio.setup(13,gpio.OUT)
	gpio.setup(15,gpio.OUT)
def move_forward(t):
	gpio.output(7,False)
	gpio.output(11,True)
	gpio.output(13,True)
	gpio.output(15,False)
	time.sleep(t)
	gpio.cleanup()
def move_backward(t):
	gpio.output(7,True)
	gpio.output(11,False)
	gpio.output(13,False)
	gpio.output(15,True)
	time.sleep(t)
	gpio.cleanup()

def turn_left(t):
	gpio.output(7,True)
	gpio.output(11,True)
	gpio.output(13,True)
	gpio.output(15,False)
	time.sleep(t)
	gpio.cleanup()
def turn_right(t):
	gpio.output(7,False)
	gpio.output(11,True)
	gpio.output(13,False)
	gpio.output(15,False)
	time.sleep(t)
	gpio.cleanup()

def pivot_left(t):
	gpio.output(7,True)
	gpio.output(11,False)
	gpio.output(13,True)
	gpio.output(15,False)
	time.sleep(t)
	gpio.cleanup()
def pivot_right(t):
	gpio.output(7,False)
	gpio.output(11,True)
	gpio.output(13,False)
	gpio.output(15,True)
	time.sleep(t)
	gpio.cleanup()

def key_input(event):
	init()
	print "key: ",event.char
	key_press = event.char
	if key_press.lower() == "w":
		move_forward()
	elif key_press.lower() == "s":
		move_backward()
	elif key_press.lower() == "d":
		turn_right()
	elif key_press.lower() == "a":
		turn_left()
	elif key_press.lower() == "q":
		pivot_left()
	elif key_press.lower() == "e":
		pivot_right()
	else:
		pass

root = tk.TK()
root.bind('<KeyPress>',key_input)
root.mainloop()
