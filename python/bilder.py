# Om small eller bilder.js saknas produceras små bilder i den katalogen och dimension uppdateras
# Därefter sammanställs bilder.js som omfattar ALLA kataloger, i variabeln Home.

import json
import time
from os import scandir,mkdir
from os.path import exists,getsize
from PIL import Image # Pillow
from PyPDF2 import PdfReader

USE_CACHE = True

WIDTH = 475
ROOT = "C:\\github\\2022-011-Bildbanken-svelte\\public\\"

antal = 0

Home = [] # Samlar på sig hela strukturen
data = {}

def dumpjson(data,f):
	json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

def pop(path):
	arr = path.split('\\')
	arr.pop()
	return "\\".join(arr)

def makeSmall(js,entry):
	print('.',end="")
	big = Image.open(entry.path)
	bigSize = getsize(entry.path)

	small = big.resize((WIDTH, round(WIDTH*big.height/big.width)))
	p = pop(entry.path)
	if not exists(p):	mkdir(p)
	small.save(pop(entry.path).replace("Home","small") + '\\' + entry.name)
	js[entry.name] = [small.width, small.height, bigSize, big.width, big.height]

def readrecurs(curr, parent):
	global antal
	js = {}

	# if not exists(ROOT + "\\small"): mkdir(ROOT + "\\small")
	if not exists(ROOT + "\\small\\"+parent): mkdir(ROOT + "\\small\\"+parent)

	if USE_CACHE and exists(ROOT + "\\small" + parent +  "\\bilder.js"):

		keys = list(curr[-2].keys())
		key = keys[-1]
		with open(ROOT + "\\small" + parent + '\\bilder.js', 'r', encoding="utf8") as f:
			curr[-2][key] = json.loads(f.read())
			antal += len(curr[-2][key])

	else:
		names = [f for f in scandir(ROOT + "Home" + parent)]
		# print(names)
		for name in names:
			# if name.name != 'small' and name.name != 'bilder.js' and name.name != 'bilder.json':
			if name.is_dir():
				nextcurr = {}
				curr[-1][name.name] = nextcurr
				readrecurs(curr+[nextcurr],parent + "\\" + name.name) # path
			else:
				makeSmall(js,name)
		if len(js) > 0:
			print('\n',len(js),'thumbnails written for',parent.split('\\')[-1])
			with open(ROOT + '\\small' + parent + '\\bilder.js', 'w', encoding="utf8") as f:
				dumpjson(js,f)

			keys = list(curr[-2].keys())
			key = keys[-1]
			curr[-2][key] = js

start = time.time()
Home = {}
readrecurs([Home],"\\")

with open(ROOT + "bilder.js", 'w', encoding="utf8") as f:
	f.write('Home=')
	dumpjson(Home, f)

#print(Home)
print(antal)
print(round(time.time() - start,3),'seconds')







def read_pdf() :
	#reader = PdfReader("Swade_PhD.pdf")
	reader = PdfReader("SSF.pdf")
	hash = {}
	for page in reader.pages:
		words = page.extract_text()
		words = words.replace("(", " ")
		words = words.replace(")", " ")
		words = words.replace("[", " ")
		words = words.replace("]", " ")
		words = words.replace(".", " ")
		words = words.replace(",", " ")
		words = words.replace("'", " ")
		words = words.replace("-", " ")

		words = words.replace("/", " ")
		words = words.replace('"', " ")
		words = words.replace("`", " ")
		words = words.replace(":", " ")
		words = words.replace("?", " ")
		words = words.replace("!", " ")

		words = words.lower()

		for word in words.split():
			if word in hash:
				hash[word] = hash[word]+1
			else:
				hash[word] = 1


	print(len(hash))
	print(hash)
	s =""
	for key in hash:
		s += ' ' + key

	print(len(s))
	print(s)

# read_pdf()
