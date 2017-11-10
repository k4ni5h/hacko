def find_between( s, first, last ):
	try:
		check=False
		start=i=0
		while(i!=len(s)):
			if check==False and s[i:i+len(first)]==first:
				check=True
				start=i+len(first)
				i+=len(first)
			elif check and s[i:i+len(last)]==last:
				check=False
				f=open('chat.txt','a+')
				f.write(s[start:i]+'\n')
				f.close()
				start=0
				i+=len(last)
			elif check and s[i:i+len(first)]==first:
				check=False
				start=0
				i+=len(last)
			if check and s[i]=="<" and i==start+1:
				print("@#$%^&^%$#@#$%^&^%$#@#$%^&*&^%$#")
				check=False
				start=0
			i+=1
	except ValueError:
		return ""

import glob, os
os.chdir("chat")
for fil in glob.glob("*.html"):
	with open(fil, 'r', encoding='utf-8') as infile:
		for s in infile:
			find_between( s, '</span></div></div><p></span></div></div><p></span></div></div><p></span></div></div><p>', '</p><div' )