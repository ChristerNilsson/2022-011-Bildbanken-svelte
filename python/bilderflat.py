# Om bilder eller kataloger saknas i small, skapas dessa och bilder.js uppdateras
# Se till att katalogen small existerar
# En nyare bild i Home än i small tvingar fram en ny small.

import json
import time
from os import scandir,mkdir,remove
from os.path import exists,getsize
from PIL import Image # Pillow

WARNING = 50 # MB. Större filer listas.
WIDTH = 475

ROOT = "C:\\github\\2022-011-Bildbanken-svelte\\"
Home = ROOT + "public\\Home"
small = ROOT + "public\\small"
JSON = ROOT + "src\\json\\"

res = {}

def frekvens(s):
	for letter in '-,[]{}.;_"0123456789':
		s = s.replace(letter,' ')
	words = s.split(' ')
	hash = {}
	for word in words:
		if word in hash:
			hash[word] += 1
		else:
			hash[word] = 1
	keys = list(hash.keys())
	keys.sort()
	for word in keys:
		if hash[word] == 1:
			print(word)

def dumpjson(data,f):
	s = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
	s = s.replace("],","],\n") # Varje key på egen rad.
	s = s.replace("{","{\n")
	s = s.replace('}','\n}')
	s = s.replace('},','},\n')
	# frekvens(s)
	f.write(s)

def pop(path):
	arr = path.split('\\')
	arr.pop()
	return "\\".join(arr)

def flat(root, res={}, parent=""):
	ensurePath(root, parent)
	for name in [f for f in scandir(root + "\\" + parent)]:
		namn = name.name
		if name.is_dir():
			flat(root, res, parent + "\\" + namn)
		elif namn.endswith('.jpg') or namn.endswith('.JPG'):
			stat = name.stat()
			res[parent + "\\" + namn] = stat.st_mtime
			if stat.st_size > WARNING * 1000000:
				print("*** Size Warning:", stat.st_size, root + parent + '\\' + namn)
		else:
			print("*** Ignored file:",root + parent + '\\' + namn)
	return res

def ensurePath(root,path):
	arr = path.split("\\")
	for i in range(len(arr)):
		p = root + "\\" + "\\".join(arr[0:i])
		if not exists(p): mkdir(p)

def dump(a):
	for key in a:
		print(key,a[key])

def patch(tree,path,data):
	arr = path.split("\\")
	ptr = tree
	for key in arr[1:len(arr)]:
		if key not in ptr: ptr[key] = {}
		if key != arr[-1]: ptr = ptr[key]
	if data:
		ptr[key] = data
	else:
		del ptr[key]

def makeSmall(a,b,name):
	big = Image.open(a+name)
	bigSize = getsize(a+name)
	small = big.resize((WIDTH, round(WIDTH*big.height/big.width)))
	ensurePath(b,name)
	small.save(b + name)
	patch(tree, name, [small.width, small.height, bigSize, big.width, big.height])

def cleanCache(node, a, path="", key=""):
	if type(node) is list:
		if a.get(path + key) == None:
			delKand.append(path+key)
			print('remove',path+key)
	else:
		if len(node) == 0:
			delKand.append(path+key)
			print('remove',path+key)
		for k in node:
			cleanCache(node[k], a, path + key + "\\", k)
start = time.time()

a = flat(Home,{})
b = flat(small,{})

print('Images in Home',len(a))
print('Images in small',len(b))

if exists(JSON + '\\bilder.json'):
	with open(JSON + '\\bilder.json', 'r', encoding="utf8") as f:
		tree = json.loads(f.read())
else:
	tree = {}

antal = 0
# utöka small och bilder.js
for key in a.keys():
	if key not in b or a[key] > b[key]:
		antal += 1
		print('adding image',antal,round(time.time() - start,3), key)
		b[key] = makeSmall(Home,small,key)

# minska small och bilder.js
for key in b.keys():
	if key not in a:
		print('removing image',key)
		remove(small + key)
		patch(tree, key, None)

# remove även från bilder
# minska bilder.js
# tag bort de som inte förekommer i Home
delKand = []
cleanCache(tree,a)
for item in delKand:
	patch(tree,item,None)

with open(JSON + '\\bilder.json', 'w', encoding="utf8") as f:
	dumpjson(tree,f)

print(round(time.time() - start,3),'seconds')
