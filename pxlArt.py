from microbit import pin0,pin1,pin2,button_a,button_b,display,Image,sleep #import needed library

blank=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]

#define needed functions
def say(data):
	display.scroll(data)

def read(file,backup):#read file function
	try: #load slot
		with open(file) as content: #save save slot
			return content.read()
	except OSError:
		write(file,backup)
		return backup

def write(file,data): #function to write to file
	with open(file, 'w') as content: #save save slot
		content.write(str(data))
		return True

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

def delay():
	sleep(200)

def displayCursor(coords):
	display.set_pixel(coords[0],coords[1],3)

#load images
saveSlot=int(read("saveSlot.txt","0"))

currFile="art"+str(saveSlot) #update current file

img=unParseImage(read(currFile,"00000:00000:00000:00000:00000")) #read art
		
group=int(read("group.txt","0")) #read group

#init radio
from radio import on, config, send, receive

on() #on radio

config(group=group) #cahnge this manually

#needed vars
coords=[0,0] 
iteration=0
cursor=0
clipBoard=None
base=770

#2+0 save
#2+1 load
#2+a save slot +
#2+b save slot -

#main loop
while True: #controls

	iteration+=1#increment iteration

	if pin1.read_analog()>base: #detect if pin1 touched (up)
		delay()
		if not coords[1]==4: #check if at edge
			coords[1]+=1 #move coords to up by 1
		else:
			coords[1]=0 #if at edge, move to other side
		displayCursor(coords)#print cursor to make moving more obvious
		iteration=0 #make sure cursor doesnt flash instantly after move

	if pin0.read_analog()>base: #detect if pin0 touched (down)
		delay() #delay
		if not coords[1]==0: #check if at edge
			coords[1]-=1 #move coords to down by 1
		else:
			coords[1]=4 #if at egde,move to other side
		displayCursor(coords)#print cursor to make moving more obvious
		iteration=0#make sure cursor doesnt flash instantly after move

	if button_b.is_pressed(): #detect if button b pressed(right)
		delay() #delay
		if not coords[0]==4: #check if at edge
			coords[0]+=1 #move coords to right by 1
		else:
			coords[0]=0 #if at edge,move to other side
		displayCursor(coords)#print cursor to make moving more obvious
		iteration=0#make sure cursor doesnt flash instantly after move

	if button_a.is_pressed(): #detect if button a pressed(left)
		delay() #delay
		if not coords[0]==0: #check if at edge
			coords[0]-=1 #move coords to left by 1
		else:
			coords[0]=4 #if at edge, move to other side
		displayCursor(coords) #print cursor to make moving more obvious
		iteration=0 #make sure cursor doesnt flash instantly after move

	if (iteration%7)==0: #display cursor if idle for 7 iterations
		displayCursor(coords)

	if (iteration%50)==0: #check messages
		message=receive()
		try:
			image=unParseImage(message)
			clipBoard=image #put in clipboard
			display.show(Image("66666:66066:60606:60006:66666")) #mail symbol
			sleep(1000)
		except:
			pass

	#loading and saving
	if pin2.read_analog()>base and pin0.read_analog()>base: #save 2+0
		write(currFile,parseImage(img))
		say("saved")

	if pin1.read_analog()>base and pin2.read_analog()>base: #load 2+1
		img=unParseImage(read(currFile,blank))
		say("loaded")

	if pin2.read_analog()>base and button_a.is_pressed(): #copy
		clipBoard=img
		delay()
		say("copied")

	if pin1.read_analog()>base and pin0.read_analog()>base: #paste
		if not clipBoard==None: 
			img=clipBoard
		delay()
		say("pasted")

	if pin0.read_analog()>base and button_b.is_pressed(): #go down and load state
		write(currFile,parseImage(img))

		saveSlot-=1 #increment save slot
		say(str(saveSlot)) #show slot
		currFile="art"+str(saveSlot) #update current file

		img=unParseImage(read(currFile,parseImage(blank)))
				
		write("saveSlot.txt",saveSlot)

	if pin0.read_analog()>base and button_a.is_pressed(): #go up and load
		write(currFile,parseImage(img))

		saveSlot+=1 #increment save slot
		say(str(saveSlot)) #show slot
		currFile="art"+str(saveSlot) #update current file

		img=unParseImage(read(currFile,parseImage(blank)))
				
		write("saveSlot.txt",saveSlot)

	#radio
	if pin1.read_analog()>base and button_a.is_pressed(): #transmit
		send(parseImage(img))
		say("sent")

	if button_a.is_pressed() and button_b.is_pressed(): #change group
		if group==255: #make group 0 if currently 255
			group=0
		else:
			group+=1 #increment group
		say(str(group))
		sleep(500) #longer delay for easier group control
		write("group.txt",str(group))

	#others
	if pin1.read_analog()>base and button_b.is_pressed(): #clear screen (requires confrmation)
		iteration=0
		say("Hold B to confirm.")
		if button_b.is_pressed():
			img=blank
			say("screen cleared.")

	display.show(Image(parseImage(img))) #refresh display

	if pin2.read_analog()>base : 
		iteration=0 #make sure cursor doesnt flash during color changing
		if img[coords[1]][coords[0]]==9: #make color 0 if currently 9
			img[coords[1]][coords[0]]=0
		else:
			img[coords[1]][coords[0]]=int(img[coords[1]][coords[0]])+1 #increment color
		display.show(Image(parseImage(img))) #refresh display
		sleep(500) #longer delay for easier color control
