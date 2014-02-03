#!/usr/bin/python

import getopt
import os
import subprocess
import sys
import time

import merge_image

def usage():
	print
	print "Usage:"
	print
	print "options:"
	print "-e <episode range>         (default: 1-1)"
	print "-t <title id>"
	print "-n <title string>          (optional)"
	print "-o <output directory>      (default: .\\)"
	print
	print "sample:"
	print "webtoon.py -e 1-10 -t 22897   (episode 1 ~ 10 download)"
	print
	sys.exit(2)

def main(argv):
	title_id = ''
	title = ''
	episode_start = 1
	episode_end = 2
	output_dir = '.\\'
	finish = False

	try:
		opts, args = getopt.getopt(argv, "he:t:n:o:")
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
				episode_end = int(parse[1]) + 1
			except:
				print "[ERROR] Incorrect episode range"
				usage()
		elif opt == "-t":
			title_id = arg
		elif opt == "-n":
			title = arg
		elif opt == "-o":
			output_dir = arg
			if output_dir[-1] != '/':
				output_dir += '/'

	if title_id == '':
		usage()

	if (episode_start > episode_end):
		print "[ERROR] Incorrect episode range"

	if not os.path.isdir(output_dir+title):
		cmd = 'md "%s"'%(output_dir+title)
		os.system(cmd)

	find_string = ['http://imgcomic.naver.com/webtoon/'+title_id+'/', 'http://imgcomic.naver.net/webtoon/'+title_id+'/']

	for episode in range(episode_start, episode_end):
		if os.path.isfile('.\\output.output'):
			os.system('del .\\output.output')
		page_url = '"http://comic.naver.com/webtoon/detail.nhn?titleId=%s&no=%d"'%(title_id, episode)
		curl_cmd = 'curl -o .\\output.output '+page_url
		print 'curl cmd: '+curl_cmd

		curl = subprocess.Popen(curl_cmd, shell=True)

		for i in range(0,30):	# 3 seconds
			time.sleep(0.1)
			if curl.poll() != None:
				break

		if not os.path.isfile('.\\output.output'):
			print '[INFO] Finish!'
			break

		output_file = open('.\\output.output', 'r')

		img_list = []
		img_output = "%s%s/%s_%03d.jpg" % (output_dir, title, title, episode)
		seq = 0
		for line in output_file.readlines():
			line = line.strip()
			s_idx = line.find(find_string[0])
			if s_idx == -1:
				s_idx = line.find(find_string[1])
			if s_idx != -1:
				seq += 1
				e_idx = line[s_idx:].find('"')
				url = line[s_idx:s_idx+e_idx]
				url_split = url.split('/')
				output_name = "%s%s/%s_%03d_%03d.jpg" %\
							(output_dir, title, title, episode, seq)
				referer='http://comic.naver.com/webtoon/detail.nhn?titleId=%s&no=%d'%(title_id, episode)
				wget_cmd = 'wget -O '+output_name+' --header="Referer: '+referer+'" '+url
				print wget_cmd
				result = os.system(wget_cmd)
				if result != 0:
					print '[ERROR] Failed download'					
				img_list.append(output_name)
	
		output_file.close()
		
		# merge image files
		merge_image.merge_image(img_output, img_list)
		
		# delete image files
		for img in img_list:
			os.remove(img)

if __name__ == '__main__':
	main(sys.argv[1:])

