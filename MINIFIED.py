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
from microbit import pin0 as N,pin1 as O,pin2 as U,button_a as P,button_b as Q,display as R,Image as Y,sleep as V
W=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
def D(data):R.scroll(data)
def K(file,backup):
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
def S(image):
	A=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]];B=0
	for C in Z(0,5):
		for D in Z(0,5):B=C*6+D;A[C][D]=a(image[B])
	return A
def L():V(200)
def T(coords):A=coords;R.set_pixel(A[0],A[1],3)
E=a(K(b,j))
F=c+I(E)
B=S(K(F,'00000:00000:00000:00000:00000'))
M=a(K(k,j))
from radio import on,config as e,send,receive as f
on()
e(group=M)
A=[0,0]
G=0
l=0
X=d
C=770
while i:
	G+=1
	if O.read_analog()>C:
		L()
		if not A[1]==4:A[1]+=1
		else:A[1]=0
		T(A);G=0
	if N.read_analog()>C:
		L()
		if not A[1]==0:A[1]-=1
		else:A[1]=4
		T(A);G=0
	if Q.is_pressed():
		L()
		if not A[0]==4:A[0]+=1
		else:A[0]=0
		T(A);G=0
	if P.is_pressed():
		L()
		if not A[0]==0:A[0]-=1
		else:A[0]=4
		T(A);G=0
	if G%7==0:T(A)
	if G%50==0:
		g=f()
		if not g==d:R.show(Y('66666:66066:60606:60006:66666'));V('300');X=S(receivedString)
	if U.read_analog()>C and N.read_analog()>C:J(F,H(B));D('saved')
	if O.read_analog()>C and U.read_analog()>C:B=S(K(F,W));D('loaded')
	if U.read_analog()>C and P.is_pressed():X=B;L();D('copied')
	if O.read_analog()>C and N.read_analog()>C:
		if not X==d:B=X
		L();D('pasted')
	if N.read_analog()>C and Q.is_pressed():J(F,H(B));E-=1;D(I(E));F=c+I(E);B=S(K(F,H(W)));J(b,E)
	if N.read_analog()>C and P.is_pressed():J(F,H(B));E+=1;D(I(E));F=c+I(E);B=S(K(F,H(W)));J(b,E)
	if O.read_analog()>C and P.is_pressed():send(H(B));D('sent')
	if P.is_pressed()and Q.is_pressed():
		if M==255:M=0
		else:M+=1
		D(I(M));V(500);J(k,I(M))
	if O.read_analog()>C and Q.is_pressed():
		G=0;D('Hold B to confirm.')
		if Q.is_pressed():B=W;D('screen cleared.')
	R.show(Y(H(B)))
	if U.read_analog()>C:
		G=0
		if B[A[1]][A[0]]==9:B[A[1]][A[0]]=0
		else:B[A[1]][A[0]]=a(B[A[1]][A[0]])+1
		R.show(Y(H(B)));V(500)
