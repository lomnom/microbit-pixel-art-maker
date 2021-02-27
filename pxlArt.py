from microbit import * #import needed library

def parseImage(image): #function to make display easier to work with by converting list of pixels to valid format
	output=""
	for row in range(0,5): #iterate thru rows
		currRow=image[row] #update row of pixels var
		for column in range(0,5): #iterate thru column in current row
			currColumn=image[row][column] #update pixel var
			output+=str(currColumn) #addd current pixel to string to output
		output+=":" #add colon to back of current row
	output=output[:-1] #remove last extra colon
	return output

#display pixel at top left
img=[[6,0,0,0,0], 
     [0,0,0,0,0],
     [0,0,0,0,0],
     [0,0,0,0,0],
     [0,0,0,0,0]]
display.show(Image(parseImage(img)))

#needed vars
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

	if pin1.read_analog()>550: #detect if pin1 touched (up)
		sleep(200)
		if not coords[1]==4: #check if at edge
			coords[1]+=1 #move coords to up by 1
		else:
			coords[1]=0 #if at edge, move to other side
		display.set_pixel(coords[0],coords[1],3)#print cursor to make moving more obvious
		iteration=0 #make sure cursor doesnt flash instantly after move

	if pin0.read_analog()>550: #detect if pin0 touched (down)
		sleep(200) #delay
		if not coords[1]==0: #check if at edge
			coords[1]-=1 #move coords to down by 1
		else:
			coords[1]=4 #if at egde,move to other side
		display.set_pixel(coords[0],coords[1],3)#print cursor to make moving more obvious
		iteration=0#make sure cursor doesnt flash instantly after move

	if button_b.is_pressed(): #detect if button b pressed(right)
		sleep(200) #delay
		if not coords[0]==4: #check if at edge
			coords[0]+=1 #move coords to right by 1
		else:
			coords[0]=0 #if at edge,move to other side
		display.set_pixel(coords[0],coords[1],3)#print cursor to make moving more obvious
		iteration=0#make sure cursor doesnt flash instantly after move

	if button_a.is_pressed(): #detect if button a pressed(left)
		sleep(200) #delay
		if not coords[0]==0: #check if at edge
			coords[0]-=1 #move coords to left by 1
		else:
			coords[0]=4 #if at edge, move to other side
		display.set_pixel(coords[0],coords[1],3) #print cursor to make moving more obvious
		iteration=0 #make sure cursor doesnt flash instantly after move

	if iteration==7: #display cursor if idle for 7 iterations
		iteration=0 #move iteration back to 0
		display.set_pixel(coords[0],coords[1],3)

	display.show(Image(parseImage(img))) #refresh display

	if pin2.read_analog()>550 : 
		sleep(300) #longer delay for easier color control
		iteration=0 #make sure cursor doesnt flash during color changing
		if img[coords[1]][coords[0]]==9: #make color 0 if currently 9
			img[coords[1]][coords[0]]=0
		else:
			img[coords[1]][coords[0]]+=1 #increment color

