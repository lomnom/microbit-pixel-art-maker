from microbit import * #import needed library

def parseImage(image): #function to make display easier to work with
	output=""
	for row in range(0,5): #iterate thru rows
		currRow=image[row]
		for column in range(0,5): #iterate thru column in current row
			currColumn=image[row][column]
			output+=str(currColumn)
		output+=":"
	output=output[:-1]
	return output

#display pixel at top left
img=[[6,0,0,0,0], 
     [0,0,0,0,0],
     [0,0,0,0,0],
     [0,0,0,0,0],
     [0,0,0,0,0]]
display.show(Image(parseImage(img)))

#needed vars
buttonState=None #0=none pressed 1=a 2=b 3=both
direction=1 #2=upDown 1=leftRight
coords=[0,0] #[0]=leftRight [1]=upDown currently at top left of screen
prevHold=False
lastClickB=0
lastClickA=0
img=[[0,0,0,0,0], 
     [0,0,0,0,0],
     [0,0,0,0,0],
     [0,0,0,0,0],
     [0,0,0,0,0]]
iteration=0
cursor=0
previouslyPressed=False

#main loop
while True: #controls
	iteration+=1#increment iteration
	#update buttonState
	if pin1.read_analog()>700: #detect if pin1 touched (up)
		buttonState=0
		sleep(200)
		if not coords[1]==4: #check if at edge
			coords[1]+=1 #move coords to up by 1
		else:
			coords[1]=0
		display.set_pixel(coords[0],coords[1],3)
		iteration=0
	if pin0.read_analog()>700: #detect if pin0 touched (down)
		buttonState=3
		sleep(200)
		if not coords[1]==0: #check if at edge
			coords[1]-=1 #move coords to down by 1
		else:
			coords[1]=4
		display.set_pixel(coords[0],coords[1],3)
		iteration=0
	if button_b.was_pressed(): #detect if button b pressed(right)
		buttonState=2
		sleep(100)
		if not coords[0]==4: #check if at edge
			coords[0]+=1 #move coords to right by 1
		else:
			coords[0]=0
		display.set_pixel(coords[0],coords[1],3)
		iteration=0
	if button_a.was_pressed(): #detect if button a pressed(left)
		buttonState=1
		sleep(100)
		if not coords[0]==0: #check if at edge
			coords[0]-=1 #move coords to left by 1
		else:
			coords[0]=4
	if iteration==7: #display cursor
		iteration=0
		display.set_pixel(coords[0],coords[1],3)
		iteration=0
		display.set_pixel(coords[0],coords[1],3)
	display.show(Image(parseImage(img)))
	if pin2.read_analog()>700 : 
		buttonState=3
		sleep(300)
		iteration=0
		if img[coords[1]][coords[0]]==9:
			img[coords[1]][coords[0]]=0
		else:
			img[coords[1]][coords[0]]+=1

