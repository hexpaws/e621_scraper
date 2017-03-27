import requests
import argparse
import shutil
import time
import sys
import re
import os

resp = requests.get
foundImg = []
foundLinks = []
foundID = []
debugging = True
workdir = os.getcwd()
baseUrl = "https://e621.net/post/index/"

def motd():
	print "e621"
	print ".:.Scraper.:.\n"

def getImgz_e621(url, counter=0):
	
	response = resp(url).text
	linkz = re.compile(ur'"file_url":"https:\/\/static1.e621.net\/data\S{39}.[jpg|png|jpeg|gif]+')
	idz = re.compile(ur'"id":\d{6,}')
	linksLoot = re.findall(linkz, response)
	idLoot = re.findall(idz, response)
	urlID  = args.search or str(args.pool)

	if not os.path.exists(urlID) or os.path.exists("../"+urlID):
	
			try:
					os.mkdir(urlID)
			except OSError as oserr_mkdir:
					if debugging:
							print ("OS Error: {0}".format(oserr_mkdir))
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

	IDpLink_Dict = dict(zip(foundID, foundLinks))
	


	for ID, LINK in IDpLink_Dict.items():
		try:
				foundImg.index(ID)
				print foundID

		except ValueError as valueerr:           
					if debugging:
						print("Value Error: {0}".format(valueerr))

					
					stream = resp(LINK, stream=True)
					fileExtension = LINK[-4:]
					start = time.time()
					name = ID+fileExtension
					with open(name, 'wb') as file:
						shutil.copyfileobj(stream.raw, file)
						counter += 1
					print "Downloaded: {0} \t Count: {1} \t Seconds: {2:4f} \t Filesize: {3:d}KB \t".format(name, counter, (time.time()-start), (os.stat(name).st_size >> 10))

	os.chdir(workdir)
	if debugging:            
		print "len(clean)",  len(clean)
	
parser = argparse.ArgumentParser()
parser.add_argument("--search")
parser.add_argument("--pages")
parser.add_argument("--pool")
args = parser.parse_args()

motd()
"""
while resp():
	for pool in range(5,9999):
		compiledUrl = baseUrl.replace('post', 'pool').replace('index','show')+str('6960')+"?page="+str(pool)
		print "URL: {0}".format(compiledUrl)
		getImgz_e621(compiledUrl)
"""	

if args.search and args.pages:
	for pages in range(1,int(args.pages)):
		compiledUrl = baseUrl+str(pages)+str("/")+args.search
		
		print "URL: {0}".format(compiledUrl)
		getImgz_e621(compiledUrl)

if args.pool: 
	while True:
		for pool in range(1,9999):
			compiledUrl = baseUrl.replace('post', 'pool').replace('index','show')+str(args.pool)+"?page="+str(pool)
			print "URL: {0}".format(compiledUrl)
			getImgz_e621(compiledUrl)
