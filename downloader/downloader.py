#!/usr/bin/python

import getopt
import json
import os
import subprocess
import sys
import time

import merge_image

COOKIEURL = "http://cartoon.media.daum.net/webtoon/viewer/"
VIEWER = "http://cartoon.media.daum.net/webtoon/viewer_images.js?webtoon_episode_id="

def usage():
	print
	print "Usage:"
	print
	print "options:"
	print "-e <episode range>         (default: 1-1)"	
	print "-o <output directory>      (default: .\\)"
	print "-w <daum or naver>         (default: naver)"
	print "-m                         (Do merge)"
	print "-p                         (Save PNG file type. (only use with '-m')"
	print "for Naver:"
	print "		-t <title id>"
	print "		-n <title string>     (optional)"
	print "for daum:"
	print "		-r <RSS address>"	
	print
	print
	print "sample:"
	print "		webtoon.py -e 1-10 -t 22897 -w naver (episode 1 ~ 10 download)"
	print "		webtoon.py -e 1-3 -t 22897 -w daum (episode 1 ~ 3 download)"
	print
	sys.exit(2)
	
###############################################################################
#for daum
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
	
def daum_main(rss, title, episode_start, episode_end, output_dir, merge, png):
	idlist = parsing_rss(rss)
	idlist.reverse()
	if len(idlist) < 1:
		print '[ERROR] Not found episode in RSS'
		sys.exit(1)

	episode = 0
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
		
		# get episode title 
		episode_title = info['episodeTitle'].encode('euc-kr')
		episode_title = episode_title.translate(None, '\\/:*?"<>|').strip()

		# get image
		img_list = []
		img_output = "%s%s\\%s_%03d_%s.jpg" %\
					(output_dir, title, title, episode, episode_title)
		sequence = 0
		for img in info['images']:
			sequence += 1
			
			output_name = "%s%s\\%s_%03d_%03d.jpg" %\
							(output_dir, title, title, episode, sequence)
			wget_cmd = 'wget -O "'+output_name.decode('euc-kr')+'" '+img['url']
			result = os.system(wget_cmd.encode('euc-kr'))
			if result != 0:
				print '[ERROR] Failed download'
				sys.exit(1)
			img_list.append(output_name)

		# merge image files
		if merge:
			if img_output[-4:] == '.jpg':
				img_output = img_output[:-4]
			if merge_image.merge_image(img_output, img_list, png):
				# delete image files
				for img in img_list:
					os.remove(img)			
	
###############################################################################
#for Naver
WEEKLY_WEBTOON = 1
CHALLENGE_BEST = 2
def naver_main(title_id, title, episode_start, episode_end, output_dir, merge, png, best):
	if title_id == '':
		usage()
		
	if title == None:
		title = ''

	if (episode_start > episode_end):
		print "[ERROR] Incorrect episode range"

	if not os.path.isdir(output_dir+title):
		cmd = 'md "%s"'%(output_dir+title)
		os.system(cmd)

	find_string = ['http://imgcomic.naver.com/webtoon/'+title_id+'/', 'http://imgcomic.naver.net/webtoon/'+title_id+'/']
	find_string_for_best = ['http://imgcomic.naver.net/nas/user_contents_data/challenge_comic', '']
	
	retry_episode = 0
	page_url = ''
	webtoon_type = WEEKLY_WEBTOON
	if best:
		webtoon_type = CHALLENGE_BEST
	for episode in range(episode_start, episode_end + 1):
		if os.path.isfile('.\\output.output'):
			os.system('del .\\output.output')
		if webtoon_type == WEEKLY_WEBTOON:
			print 'Try to start WEEKLY webtoon download..'
			page_url = '"http://comic.naver.com/webtoon/detail.nhn?titleId=%s&no=%d"'%(title_id, episode)
		elif webtoon_type == CHALLENGE_BEST:
			print 'Try to start BEST challenge webtoon download..'
			page_url = '"http://comic.naver.com/bestChallenge/detail.nhn?titleId=%s&no=%d"' % (title_id, episode)
		else:
			break
		curl_cmd = 'curl -o .\\output.output '+page_url
		print 'curl cmd: '+curl_cmd

		curl = subprocess.Popen(curl_cmd, shell=True)

		for i in range(0,30):	# 3 seconds
			time.sleep(0.1)
			if curl.poll() != None:
				break
		if not os.path.isfile('.\\output.output'):
			if retry_episode < 2:
				retry_episode += 1
				continue
			print '[INFO] Finish!'
			break

		retry_episode = 0

		output_file = open('.\\output.output', 'r')

		img_list = []
		seq = 0
		s_idx = -1
		for line in output_file.readlines():
			line = line.strip()
			if webtoon_type == WEEKLY_WEBTOON:
				s_idx = line.find(find_string[0])
				if s_idx == -1:
					s_idx = line.find(find_string[1])
			else: # webtoon_type == CHALLENGE_BEST:
				s_idx = line.find(find_string_for_best[0])

			if s_idx != -1:
				seq += 1
				e_idx = line[s_idx:].find('"')
				url = line[s_idx:s_idx+e_idx]
				if url[-4:].lower() == ".jpg" or url[-4:].lower() == ".png":
					output_name = "%s%s/%s_%03d_%03d.jpg" %\
								(output_dir, title, title, episode, seq)
					if webtoon_type == WEEKLY_WEBTOON:
						referer='http://comic.naver.com/webtoon/detail.nhn?titleId=%s&no=%d'%(title_id, episode)
						wget_cmd = 'wget -O '+output_name+' --header="Referer: '+referer+'" '+url
					else: # webtoon_type == CHALLENGE_BEST:
						referer='http://comic.naver.com/bestChallenge/detail.nhn?titleId=%s&no=%d'%(title_id, episode)
						wget_cmd = 'wget -O '+output_name+' --header="Referer: '+referer+'" '+url
					
					print wget_cmd
					result = os.system(wget_cmd)
					if result != 0:
						print '[ERROR] Failed download'	
					img_list.append(output_name)
	
		output_file.close()
		
		# merge image files
		if merge:
			img_output = "%s%s/%s_%03d" % (output_dir, title, title, episode)
			if merge_image.merge_image(img_output, img_list, png):
				# delete image files
				for img in img_list:
					os.remove(img)


###############################################################################
#for common
def main(argv):
	title_id = ''
	title = None
	rss = ''
	episode_start = 1
	episode_end = 1
	output_dir = '.\\'
	finish = False
	webtoon_type = "naver"
	merge = False
	png = False
	best = False

	try:
		opts, args = getopt.getopt(argv, "he:t:n:o:r:w:mpb")
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
			title_id = arg
		elif opt == "-n":
			title = arg
		elif opt == "-o":
			output_dir = arg
			if output_dir[-1] != '\\':
				output_dir += '\\'
		elif opt == "-w":
			webtoon_type = arg
		elif opt == "-m":
			merge = True
		elif opt == "-p":
			png = True
		elif opt == "-b":
			best = True

	try:
		if webtoon_type == 'naver':
			naver_main(title_id, title, episode_start, episode_end, output_dir, merge, png, best)
		elif webtoon_type == 'daum':
			daum_main(rss, title, episode_start, episode_end, output_dir, merge, png)
		else:
			print "Unknown webtoon type: " + webtoon_type
			usage()
		print '[INFO] Finish download !! Bye~'
	except Exception, e:
		print '[ERROR] ', e
	
if __name__ == '__main__':
	main(sys.argv[1:])

