#############################
# will make it cleaner later#
#############################
import requests
import argparse
import shutil
#import ffmpy
import time
import sys
import re
import os

resp = requests.get
foundImg = []
foundLinks = []
foundID = []	
debugging = False
workdir = os.getcwd()
baseUrl = "https://e621.net/post/index/"


def motd():
	print ("e621")
	print (".:.Scraper.:.\n")

def getImgz_e621(url, counter=0):
	
	response = resp(url).text
	if args.animated:
		linkz = re.compile(ur'"file_url":"https:\/\/static1.e621.net\/data\S{39}.[gif|swf|webm]+')

	elif args.images:
		linkz = re.compile(ur'"file_url":"https:\/\/static1.e621.net\/data\S{39}.[jpg|png|jpeg]+')

	elif args.all:
		linkz = re.compile(ur'"file_url":"https:\/\/static1.e621.net\/data\S{39}.[jpg|png|jpeg|gif|swf|webm]+')		

	idz = re.compile(ur'"id":\d{6,}')
	linksLoot = re.findall(linkz, response)
	idLoot = re.findall(idz, response)
	urlID  = args.search or str(args.pool)

	if not os.path.exists(urlID) or os.path.exists("../"+urlID):
	
			try:
					os.mkdir(urlID)
			except OSError as oserr_mkdir:
					if debugging:
							print (("OS Error: {0}".format(oserr_mkdir)))
			else:   
					os.chdir(urlID)

	elif os.path.exists(urlID):
			os.chdir(urlID)
		 
	for ls in os.listdir("../"+urlID):
			foundImg.append(ls)

	del(foundLinks[:])
	for dirtyLink in linksLoot:
		cleanLink = dirtyLink.replace('"file_url":"', '').encode('utf-8')
		foundLinks.append(cleanLink)

	del(foundID[:])
	for dirtyID in idLoot:
		cleanID = dirtyID.replace('"id":', '').encode('utf-8')
		foundID.append(cleanID)

	if not foundID and not foundLinks:
		sys.exit(1)
	elif foundID and foundLinks:
		pass
	else:
		print ("Something that wasn't supposed to happend, \n happend please make issue at github.. thanks")

	IDpLink_Dict = dict(zip(foundID, foundLinks))

	for ID, LINK in IDpLink_Dict.items():
		try:
				fileExtension = LINK[-4:]
				if fileExtension == "webm":
					fileExtension = ".webm"
				name = ID+fileExtension
				foundImg.index(name)

		except ValueError as valueerr:           
					if debugging:
						print(("Value Error: {0}".format(valueerr)))
					
					stream = resp(LINK, stream=True)
					start = time.time()

					with open(name, 'wb') as file:
						shutil.copyfileobj(stream.raw, file)
						counter += 1
					print ("Downloaded: {0}     Count: {1}     Seconds: {2:4f}     Filesize: {3:d}KB     ".format(name, counter, (time.time()-start), (os.stat(name).st_size >> 10)))

		else:
			print ("Found IT: {0}     Filesize: {1:d}KB ".format(name, (os.stat(name).st_size >> 10)))

	os.chdir(workdir)
	
parser = argparse.ArgumentParser(prog='e621Scraper.py', usage='%(prog)s [--search cum] [--pages 10] [--pool 6090] [--images True] [--animated True] [--all True]')
parser.add_argument("--search", help='downloads images based on what you searched for')
parser.add_argument("--pages", help='how many pages do you want to download from')
parser.add_argument("--pool", help='downloads images from pool, give it the id of the pool')
parser.add_argument("--images", help='downloads only images')
parser.add_argument("--animated", help='downloads only animations')
parser.add_argument("--all", help='downloads both images and animations')
args = parser.parse_args()

motd()

if args.search and args.pages:
	for pages in range(1,int(args.pages)+1):
		compiledUrl = baseUrl+str(pages)+str("/")+args.search
		print ("\nURL: {0}".format(compiledUrl))
		getImgz_e621(compiledUrl)

if args.pool: 
	#while True:
	for pool in range(1,9999):
		compiledUrl = baseUrl.replace('post', 'pool').replace('index','show')+str(args.pool)+"?page="+str(pool)
		print ("\nURL: {0}".format(compiledUrl))
		getImgz_e621(compiledUrl)
