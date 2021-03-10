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

def unParseImage(image): #unparse parsed image
	output=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
	char=0
	for row in range(0,5):
		for column in range(0,5):
			char=(row*6)+column
			output[row][column]=int(image[char])
	return output

def read(file):#read file function
	try: #load slot
		with open(file) as content: #save save slot
			return content.read()
	except OSError:
		return None

def write(file,data): #function to write to file
	with open(file, 'w') as content: #save save slot
		content.write(str(data))


#load images
try: #load slot
	with open("saveSlot.txt") as slot: #save save slot
		saveSlot=int(slot.read())
except OSError: #make file if nonexistent
	with open("saveSlot.txt", 'w') as slot:
		slot.write(str(0))
		saveSlot=0

currFile="art"+str(saveSlot) #update current file

try: #load image
	with open(currFile) as art:
		img = unParseImage(art.read())
except OSError:
	with open(currFile,'w') as art:
		img=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
		art.write(parseImage(img))
		


#needed vars
coords=[0,0] 
iteration=0
cursor=0
clipBoard=None

#2+0 save
#2+1 load
#2+a save slot +
#2+b save slot -

#main loop
while True: #controls

	iteration+=1#increment iteration

	if pin1.read_analog()>770: #detect if pin1 touched (up)
		sleep(200)
		if not coords[1]==4: #check if at edge
			coords[1]+=1 #move coords to up by 1
		else:
			coords[1]=0 #if at edge, move to other side
		display.set_pixel(coords[0],coords[1],3)#print cursor to make moving more obvious
		iteration=0 #make sure cursor doesnt flash instantly after move

	if pin0.read_analog()>770: #detect if pin0 touched (down)
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

	if (iteration%7)==0: #display cursor if idle for 7 iterations
		display.set_pixel(coords[0],coords[1],3)

	#loading and saving
	if pin2.read_analog()>770 and pin0.read_analog()>770: #save 2+0
		with open(currFile, 'w') as art:
			display.scroll("saved")
			art.write(parseImage(img))

	if pin1.read_analog()>770 and pin2.read_analog()>770: #load 2+1
		try:
			with open(currFile) as art:
				display.scroll("loaded")
				img = unParseImage(art.read())
		except OSError:
			display.scroll("File not found. Try saving.")

	if pin2.read_analog()>770 and button_a.is_pressed(): #copy
		clipBoard=img
		sleep(200)
		display.scroll("copied")

	if pin1.read_analog()>770 and pin0.read_analog()>770: #paste
		if not clipBoard==None:
			img=clipBoard
		sleep(200)
		display.scroll("pasted")

	if pin0.read_analog()>770 and button_b.is_pressed(): #go down and load state
		with open(currFile, 'w') as art: #save
			art.write(parseImage(img))

		saveSlot-=1 #increment save slot
		display.scroll(str(saveSlot)) #show slot
		currFile="art"+str(saveSlot) #update current file

		try: #load state
			with open(currFile) as art:
				img = unParseImage(art.read())
		except OSError: #if file doesnt exist, write empty and load
			with open(currFile,'w') as art:
				img=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
				art.write(parseImage(img))
				
		with open("saveSlot.txt", 'w') as slot: #save save slot
			slot.write(str(saveSlot))

	if pin0.read_analog()>770 and button_a.is_pressed(): #go up and load
		with open(currFile, 'w') as art: #save
			art.write(parseImage(img))

		saveSlot+=1 #increment save slot
		display.scroll(str(saveSlot)) #show slot
		currFile="art"+str(saveSlot) #update current file

		try: #load state
			with open(currFile) as art:
				img = unParseImage(art.read())
		except OSError: #if file doesnt exist, write empty and load
			with open(currFile,'w') as art:
				img=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
				art.write(parseImage(img))
				

		with open("saveSlot.txt", 'w') as slot: #save save slot
			slot.write(str(saveSlot))


	#others
	if pin1.read_analog()>770 and button_b.is_pressed(): #clear screen (requires confrmation)
		iteration=0
		display.scroll("Do you want to clear screen? Hold B to confirm.")
		if button_b.is_pressed():
			img=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
			display.scroll("screen cleared.")

	display.show(Image(parseImage(img))) #refresh display

	if pin2.read_analog()>770 : 
		iteration=0 #make sure cursor doesnt flash during color changing
		if img[coords[1]][coords[0]]==9: #make color 0 if currently 9
			img[coords[1]][coords[0]]=0
		else:
			img[coords[1]][coords[0]]=int(img[coords[1]][coords[0]])+1 #increment color
		display.show(Image(parseImage(img))) #refresh display
		sleep(500) #longer delay for easier color control

