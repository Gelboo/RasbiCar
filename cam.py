# from Tkinter import *
import cv2

def start_video():
	cap = cv2.VideoCapture(0)

	while(True):
		_,frame = cap.read()

		#gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

		cv2.imshow('frame',frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()
start_video()
'''
root = Tk()
root.title("Controll the Auto")
root.geometry("600x400")

button1 = Button(root,text="button1")
button2 = Button(root,text="button2")
button3 = Button(root,text="button3")

button1.pack()
button2.place(x=200,y=200)
button3.place(x=10,y=30)

root.mainloop()

'''
