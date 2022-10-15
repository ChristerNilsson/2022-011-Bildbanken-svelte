# Om small eller bilder.js saknas produceras små bilder i den katalogen och dimension uppdateras
# Därefter sammanställs bilder.js som omfattar ALLA kataloger, i variabeln total.

import json
import time
from os import scandir,mkdir
from os.path import exists
from PIL import Image

WIDTH = 432
ROOT = "C:\\github\\2022-011-Bildbanken-svelte\\public\\database\\"

total = [] # Samlar på sig hela strukturen
data = {}

def pop(path):
	arr = path.split('\\')
	arr.pop()
	return "\\".join(arr)

def makeSmall(js,entry):
	print('.',end="")
	big = Image.open(entry.path)
	small = big.resize((WIDTH, round(WIDTH*big.height/big.width)))
	p = pop(entry.path)
	if not exists(p + '\\small'):
		mkdir(p + '\\small')
	small.save(pop(entry.path) + '\\small\\' + entry.name)
	js[entry.name] = [small.width,small.height]

def readrecurs(curr, parent):
	js = {}

	if exists(parent + "\\small\\bilder.js"):
		keys = list(curr[-2].keys())
		key = keys[-1]
		with open(parent + '\\small\\bilder.js', 'r', encoding="utf8") as f:
			curr[-2][key] = json.loads(f.read())
	else:
		names = [f for f in scandir(parent)]
		for name in names:
			if name.name != 'small' and name.name != 'bilder.js':
				if name.is_dir():
					nextcurr = {}
					curr[-1][name.name] = nextcurr
					readrecurs(curr+[nextcurr],name.path)
				else:
					makeSmall(js,name)
		if len(js) > 0:
			print(len(js),'\nthumbnails written for',parent.split('\\')[-1])
			with open(parent+'\\small\\bilder.js', 'w', encoding="utf8") as f:
				json.dump(js,f)

			keys = list(curr[-2].keys())
			key = keys[-1]
			curr[-2][key] = js

start = time.time()
total = {}
readrecurs([total],ROOT)

with open(ROOT + "bilder.js", 'w', encoding="utf8") as f:
	f.write('data = ')
	json.dump(total, f, ensure_ascii=False)

print(total)
print(round(time.time() - start,3),'seconds')
