#!/usr/bin/python

import getopt
import json
import os
import subprocess
import sys
import time

COOKIEURL = "http://cartoon.media.daum.net/webtoon/viewer/"
VIEWER = "http://cartoon.media.daum.net/webtoon/viewer_images.js?webtoon_episode_id="

def usage():
	print
	print "Usage:"
	print
	print "options:"
	print "-e <episode range>         (default: 0-3)"
	print "-r <RSS address>"
	print "-o <output directory>      (default: ./)"
	print
	print "sample:"
	print "daumwebtoon.py -e 0-999 -r http://cartoon.media.daum.net/webtoon/rss/petermon (episode 0 ~ 999 download)"
	print
	sys.exit(2)

def parsing_rss(rss):
	idlist = []
	item = False

	if os.path.isfile('.\\out.output'):
		os.system('del .\\out.output')
	curl_cmd = 'curl -s -o .\\out.output '+rss
	curl = subprocess.Popen(curl_cmd, shell=True)
	for i in range(0,50):	# 5 seconds
		time.sleep(0.1)
		if curl.poll() != None:
			break
	if not os.path.isfile('.\\out.output'):
		print '[ERROR] Failed download RSS file.'
		sys.exit(2)

	output_file = open('.\\out.output', 'r')
	for line in output_file.readlines():
		line = line.strip()
		if line.find("<item>") == 0:
			item = True
		if item == True:
			# Get ID
			if line.find("<link>") == 0:
				idx = line.find("</link>")
				line = line[:idx]
				idx = line.rfind('/')
				if idx < 0:
					print '[ERROR] Failed parsing RSS file'
					idlist = []
					break
				id = line[idx+1:]
				# push ID to idlist
				idlist.append(id)
			if line.find("</item>") == 0:
				item = False
	output_file.close()
	return idlist

def get_cookie(id):
	cookie = '.\\cookie.jar'

	if os.path.isfile(cookie):
		os.system('del '+cookie)

	curl_cmd = 'curl -s -o ./out.output --cookie-jar '+cookie+' '+COOKIEURL+id
	curl = subprocess.Popen(curl_cmd, shell=True)
	for i in range(0,50):	# 5 seconds
		time.sleep(0.1)
		if curl.poll() != None:
			break

	if os.path.getsize(cookie) > 0:
		return cookie

	print '[ERROR] Failed get cookie'
	sys.exit(1)

def get_imginfo(id, cookie):
	if os.path.isfile('.\\out.output'):
		os.system('del .\\out.output')
	curl_cmd = 'curl -s -o .\\out.output --cookie '+cookie+' '+VIEWER+id
	curl = subprocess.Popen(curl_cmd, shell=True)
	for i in range(0,50):	# 5 seconds
		time.sleep(0.1)
		if curl.poll() != None:
			break
	if not os.path.isfile('.\\out.output'):
		print '[ERROR] Failed download page.'
		sys.exit(2)

	dict = {}
	output_file = open('.\\out.output', 'r')
	dict = json.loads(output_file.read(), encoding='utf8')
	output_file.close()

	return dict

def main(argv):
	rss = ''
	title = None
	episode_start = 0
	episode_end = 9999
	output_dir = '.\\'
	finish = False

	try:
		opts, args = getopt.getopt(argv, "he:r:t:o:")
	except getopt.GetoptError, e:
		print "[ERROR] GetoptError: "+str(e)
		sys.exit(2)

	for opt, arg in opts:
		if opt == "-h":
			usage()
		elif opt == "-e":
			try:
				parse = arg.split("-")
				episode_start = int(parse[0])
				episode_end = int(parse[1])
			except:
				print "[ERROR] Incorrect episode range"
				usage()
		elif opt == "-r":
			rss = arg
		elif opt == "-t":
			title = arg
		elif opt == "-o":
			output_dir = arg
			if output_dir[-1] != '\\':
				output_dir += '\\'

	if rss == '':
		usage()

	if (episode_start >= episode_end):
		print "[ERROR] Incorrect episode range"
		sys.exit(1)

	idlist = parsing_rss(rss)
	idlist.reverse()
	if len(idlist) < 1:
		print '[ERROR] Not found episode in RSS'
		sys.exit(1)

	episode = -1
	cookie = None
	for id in idlist:
		if cookie is None:
			cookie = get_cookie(id)

		episode += 1
		if episode_start > episode:
			continue
		if episode_end < episode:
			break

		info = get_imginfo(id, cookie)

		if title is None:
			title = info['title'].encode('euc-kr')
		
		title = title.translate(None, '\\/:*?"<>|').strip()
		if not os.path.isdir(output_dir+title):
			os.makedirs(output_dir+title)
			
		sequence = 0
		for img in info['images']:
			sequence += 1
			episode_title = info['episodeTitle'].encode('euc-kr')
			episode_title = episode_title.translate(None, '\\/:*?"<>|').strip()
			
			output_name = "%s%s\\%s_%03d_%s_%03d.jpg" %\
							(output_dir, title, title, episode,
							 episode_title, sequence)
			wget_cmd = 'wget -O "'+output_name.decode('euc-kr')+'" '+img['url']
			result = os.system(wget_cmd.encode('euc-kr'))
			if result != 0:
				print '[ERROR] Failed download'
				sys.exit(1)

	print '[INFO] Finish download !! Bye~'

if __name__ == '__main__':
	main(sys.argv[1:])

