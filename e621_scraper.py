from sys import platform as _os
import requests
import re
import wget
import time
import argparse
import os

resp = requests.get
foundImg = []
foundLinks = []
debugging = True
workdir = os.getcwd()
baseUrl = "https://e621.net/post/index/"

def motd():
print "					  "
print "		   __ ___  __ "
print "  	  / /|__ \/_ |"
print "	 ___ / /_   ) || |"
print " / _ \ '_ \ / / | |"
print "|  __/ (_) / /_ | |"
print " \___|\___/____||_|"
print "	 .:.Scraper.:.	  "

def getImgz_e621():
	
	response = resp(baseUrl).text
	linkz = re.compile(ur'"file_url":"https:\/\/static1.e621.net\/data\S{39}.[jpg|png|jpeg|gif]+')
	loot = re.findall(linkz, response)
	urlID  = args.search

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
		 
	for j in os.listdir("../"+urlID):
			foundImg.append(j)

	for j in loot:
		clean = j.replace('"file_url":"', '')
		foundLinks.append(clean)

	for links in foundLinks:
		try:  
			loot2 = links[36:]
			img_name = str(loot2)
			print img_name
			foundImg.index(img_name)

		except ValueError as valueerr:           
				if debugging:
					print("Value Error: {0}".format(valueerr))   

				print "input wget", links
				print (wget.download(links))
				print "\n"		


	os.chdir(workdir)
	if debugging:            
		print "len(clean)",  len(clean)
	
parser = argparse.ArgumentParser()
parser.add_argument("--search")
parser.add_argument("--pages")
args = parser.parse_args()

motd()
for j in range(1,int(args.pages)):
	compiledUrl = baseUrl+str(j)+str("/")+args.search
	getImgz_e621()
