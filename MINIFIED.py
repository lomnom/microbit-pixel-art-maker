k='group.txt'
j='0'
i=True
h=open
d=None
c='art'
b='saveSlot.txt'
a=int
Z=range
I=str
from microbit import pin0 as O,pin1 as T,pin2 as P,button_a as U,button_b as K,display as Q,Image as Y,sleep as V
W=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
def D(data):Q.scroll(data)
def L(file,backup):
	A=backup
	try:
		with h(file)as B:return B.read()
	except OSError:J(file,A);return A
def J(file,data):
	with h(file,'w')as A:A.write(I(data));return i
def H(image):
	B=image;A=''
	for C in Z(0,5):
		F=B[C]
		for D in Z(0,5):E=B[C][D];A+=I(E)
		A+=':'
	A=A[:-1];return A
def R(image):
	A=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]];B=0
	for C in Z(0,5):
		for D in Z(0,5):B=C*6+D;A[C][D]=a(image[B])
	return A
def M():V(200)
def S(coords):A=coords;Q.set_pixel(A[0],A[1],3)
E=a(L(b,j))
F=c+I(E)
B=R(L(F,'00000:00000:00000:00000:00000'))
N=a(L(k,j))
from radio import on,config as e,send,receive as f
on()
e(group=N)
A=[0,0]
G=0
l=0
X=d
C=770
while i:
	G+=1
	if T.read_analog()>C:
		M()
		if not A[1]==4:A[1]+=1
		else:A[1]=0
		S(A);G=0
	if O.read_analog()>C:
		M()
		if not A[1]==0:A[1]-=1
		else:A[1]=4
		S(A);G=0
	if K.is_pressed():
		M()
		if not A[0]==4:A[0]+=1
		else:A[0]=0
		S(A);G=0
	if U.is_pressed():
		M()
		if not A[0]==0:A[0]-=1
		else:A[0]=4
		S(A);G=0
	if G%7==0:S(A)
	if G%50==0:
		g=f()
		if not g==d:Q.show(Y('66666:66066:60606:60006:66666'));V('300');X=R(receivedString)
	if P.read_analog()>C and O.read_analog()>C:J(F,H(B));D('saved')
	if T.read_analog()>C and P.read_analog()>C:B=R(L(F,W));D('loaded')
	if P.read_analog()>C and U.is_pressed():X=B;M();D('copied')
	if T.read_analog()>C and O.read_analog()>C:
		if not X==d:B=X
		M();D('pasted')
	if O.read_analog()>C and K.is_pressed():J(F,H(B));E-=1;D(I(E));F=c+I(E);B=R(L(F,H(W)));J(b,E)
	if O.read_analog()>C and U.is_pressed():J(F,H(B));E+=1;D(I(E));F=c+I(E);B=R(L(F,H(W)));J(b,E)
	if P.read_analog()>C and K.is_pressed():send(H(B));D('sent')
	if U.is_pressed()and K.is_pressed():
		if N==255:N=0
		else:N+=1
		D(I(N));V(500);J(k,I(N))
	if T.read_analog()>C and K.is_pressed():
		G=0;D('Hold B to confirm.')
		if K.is_pressed():B=W;D('screen cleared.')
	Q.show(Y(H(B)))
	if P.read_analog()>C:
		G=0
		if B[A[1]][A[0]]==9:B[A[1]][A[0]]=0
		else:B[A[1]][A[0]]=a(B[A[1]][A[0]])+1
		Q.show(Y(H(B)));V(500)
