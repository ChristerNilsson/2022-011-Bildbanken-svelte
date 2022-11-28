# Om bilder eller kataloger saknas i Small, skapas dessa och Cache uppdateras

import time
import json
from os import scandir, mkdir, remove, rmdir
from os.path import exists, getsize
from PIL import Image

WIDTH = 475

ROOT = "C:\\github\\2022-011-Bildbanken-svelte\\"
Home = ROOT + "public\\Home"
small = ROOT + "public\\small"
JSON = ROOT + "public\\json\\"


def is_jpg(key): return key.endswith('.jpg') or key.endswith('.JPG')


def is_tif(key): return key.endswith('.tif') or key.endswith('.TIF')


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
	s = json.dumps(data, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
	s = s.replace("],","],\n") # Varje key (katalog,fil) på egen rad.
	s = s.replace(":{",":\n{")
	s = s.replace(',"',',\n"')
	# frekvens(s)
	f.write(s)

# def pop(path):
# 	arr = path.split('\\')
# 	arr.pop()
# 	return "\\".join(arr)

# def dump(a):
# 	for key in a:
# 		print(key,a[key])


def loadCache():
	if not exists(JSON + '\\bilder.json'): return {}
	with open(JSON + '\\bilder.json', 'r', encoding="utf8") as f:
		return json.loads(f.read())


def pruneCache():
	antal = {'files':0, 'folders':0}
	keys = list(c.keys())
	keys = reversed(keys)
	for key in keys:
		if key not in a:
			if is_jpg(key):
				antal['files'] += 1
			else:
				antal['folders'] += 1
			patch(cache, key, None)
	return antal


def ensurePath(root,path):
	arr = path.split("\\")
	for i in range(len(arr)):
		p = root + "\\" + "\\".join(arr[0:i])
		if not exists(p): mkdir(p)


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
	patch(cache, name, [small.width, small.height, bigSize, big.width, big.height])
	return [small.width, small.height, bigSize, big.width, big.height]


# utöka Small och Cache
def expandSmall():
	antal = {'files':0, 'folders':0}
	for key in a.keys():
		if key not in b:
			if is_jpg(key):
				antal['files'] += 1
				print('.', end="")
				b[key] = makeSmall(Home,small,key)
			else:
				print('D', end="")
				antal['folders'] += 1
	print()
	return antal


# minska Small och Cache
def shrinkSmall():
	antal = {'files':0, 'folders':0, 'keys':0}
	keys = list(b.keys())
	keys = reversed(keys)
	for key in keys:
		if key not in a:
			small0 = small + key
			if is_jpg(key):
				remove(small0)
				antal['files'] += 1
			else:
				rmdir(small0)
				antal['folders'] += 1
			if key in cache:
				del cache[key]
				antal['keys'] += 1
	return antal

# def getInfo(path):
# 	info = Image.open(path)
# 	size = getsize(path)
# 	return [info.width, info.height, size]


def flat(root, res={}, path=""):
	ensurePath(root, path)
	for name in [f for f in scandir(root + "\\" + path)]:
		namn = name.name
		path1 = path + "\\" + namn
		if name.is_dir():
			res[path1] = ""
			flat(root, res, path1)
		elif is_jpg(namn):
			res[path1] = ""
		else:
			print("*** Ignored file:", "public\\Home" + path1)
	return res


def flatten(node, res={}, path=''):
	for key in node:
		path1 = path + "\\" + key
		res[path1] = ""
		if not type(node[key]) is list:
			flatten(node[key],res, path1)
	return res


def compare(a,b,message):
	res = {}
	cfiles = 0
	cfolders = 0
	for path in a:
		if path not in b:
			if is_jpg(path):
				if cfiles == 0: res[path] = 0
				cfiles += 1
			else:
				res[path] = 0
				cfolders += 1
	if cfolders > 0 or cfiles > 0:
		print(message, cfolders, 'folders +', cfiles, 'files')
	return res


def compare2(message,x,y):
	res = {}
	res['missing'] = compare(x, y, 'Home vs ' + message + ': missing')
	res['surplus'] = compare(y, x, 'Home vs ' + message + ': surplus')
	return res


def countFolders(arr):
	antal = 0
	for key in arr:
		if not is_jpg(key): antal += 1
	return antal


hash = {}
letters = list("+!§()0123456789_,.-¤")
stoppord = 'aasen adepterr adersson jpg lowres och på adrian allan alsamarrai amalie amen analyse anmästearen anzambi autografskrvning ble blixte calm campo cat ceremonie coh dah dax deltagran do during ea edvin eisler ellen enricsson entre exteriöre frisys fö föräldrarl fötäldrar galleriet ggr gm hampus hanna hasselbacken his hurry huvudnonader idar ingertz interiiör interiö interiöri intervjuvar intrvjuas istället jadoube joakim jonathan jouni jubileuml junioer juniotturneringen jöberg kafeet kafffet kankse khalili klari koentatorsrummet kollar kollekt kommentatorr kommentatorrummet kommentatorsrummeti kommentatro kommenttorsrummet kommpisar kompisarpg lagdledare lagledate larsson lennart lexander linnea linus livesändningl livesåndning lokander lottnig lågstadet lögdahl mallanstadiet malmö mediaansvari miniior morellr mourad muntean mästartklassen näringsllivet oc ocb ocg ochh ocj oh olk ollefsén ostafiev ove pannka pch pettersson prisutdelnineng prisutdelningl prisutdelningr prize producenr profiiler publiparti qi radd raden resultatapportering resultatrapporteing reultatrapportering reultatredovisning rmorgondagens rondpausl rånby santiago sara schackinstruktio schackyouga seo severingen sgnerer simultanspell sk slutforsering snabbschacksdm solemn solomia some spealre spelaregistrering speling spellokaleni spleare sponsorerrond steinitz stromästarna stsningsgruppen ter the thordur tran trino triumvirat truskavetska träder tuomainen utanföt vallatorpsskolan vatn vede ver veteranallmän vilolaäge waeli wedberg wernberg with wweb xunming xxxxx åskådarei åskådarer åsådare af amassadör emanuel exteriörr klaas klas kolobok line livesädningen lottnib ooch prisutdelnigen pågåender shah sllutspel stasik to träbingsparti årfest års årsjubileum rondl tränongsparti vt it problemlösnings ron xuanming la mter and bokförsälning rrond highres cafeét veterner avlutningen of ans gr an'.split(' ')

def flatWords(node):
	for key in node:
		words = key
		for letter in letters:
			words = words.replace(letter," ")
		for word in words.split(' '):
			wordLower = word.lower()
			if len(word) > 1 and wordLower not in stoppord and wordLower == word:
				hash[word] = hash[word]+1 if word in hash else 1
		if type(node[key]) is dict: flatWords(node[key])

def convert(hash):
	arr = []
	for key in hash.keys():
		arr.append([hash[key],key])
	arr = sorted(arr)
	return arr

######################


cache = loadCache()

start = time.time()
flatWords(cache)
keys = convert(hash)
print(len(keys),'words in', round(time.time()-start,3),'seconds')
print()
for [count,key] in keys:
	print(key + ':' + str(count))

a = flat(Home, {})
b = flat(small, {})
c = flatten(cache, {})

print()
ca = countFolders(a)
cb = countFolders(b)
cc = countFolders(c)
print('Home: ', ca, 'folders +', len(a) - ca,'files')
print('Small:', cb, 'folders +', len(b) - cb,'files')
print('Cache:', cc, 'folders +', len(c) - cc,'files')

print()
resSmall = compare2('Small',a,b)
resCache = compare2('Cache',a,c)

print()
for key in resSmall['missing'].keys(): print('Small missing:', key)
print()
for key in resSmall['surplus'].keys(): print('Small surplus:', key)
print()
for key in resCache['missing'].keys(): print('Cache missing:', key)
print()
for key in resCache['surplus'].keys(): print('Cache surplus:', key)

print()
update = input('Update Small and Cache? (NO/Yes)').upper()
update = update.startswith('Y')

if update:

	start = time.time()
	print()
	antal = expandSmall()
	print()
	if antal['folders'] > 0 or antal['files'] > 0: print('Small: Added',   antal['folders'],'folders and', antal['files'], 'files')
	antal = shrinkSmall()
	if antal['folders'] > 0 or antal['files'] > 0: print('Small: Deleted', antal['folders'],'folders and', antal['files'], 'files')
	if antal['keys'] > 0: print('Cache: Deleted', antal['keys'], 'keys')
	antal = pruneCache()
	if antal['folders'] > 0 or antal['files'] > 0: print('Cache: Pruned',  antal['folders'], 'folders and', antal['files'], 'files')

	with open(JSON + '\\bilder.json', 'w', encoding="utf8") as f: dumpjson(cache,f)
	print()
	print(round(time.time() - start,3),'seconds')
