#!/usr/bin/env python
#!encoding=utf-8

# http://www.file-recovery.com/ogg-signature-format.htm
# http://www.digitalpreservation.gov/formats/fdd/fdd000026.shtml

import sys

x = 0

def handle_ogg(filein, n_in, directoire):

	global x
	x += 1
	print x
	
	#thisogg = "OggS\x00\x02"
	thisogg = ""
	
	this_pos = filein.tell()
	filein.seek(this_pos - 6)
	
	finished = False
	
	while (finished != True):

		# get header; append to thisogg.
		header = filein.read(27)
		thisogg += header

		# check whether this is the last page.
		finished = (((ord(header[5]) & 0x04) != 0) or (ord(header[26]) == 0x00))

		# get number of segments
		num_segments = ord(header[26])
		
		# get total size of all segments
		section_length = 0
		for i in range(num_segments):
			this_section_length = filein.read(1)
			thisogg += this_section_length
			section_length += ord(this_section_length)
		
		# read and append that many segments
		thisogg += filein.read(section_length)
	
	#write out ogg
	f = open(directoire + str(x) + ".ogg", "wb")
	f.write(thisogg)
	f.close()
	
	#read next few bytes.
	return filein.read(n)


def is_ogg_header(header_in):
	return (header_in[:6] == "OggS\x00\x02")

if (len(sys.argv) < 3):
	sys.exit("Yo gimme some args you chucklefuck.")
	
file_path_in = sys.argv[1]
directory_path_out = sys.argv[2]
if (directory_path_out[-1] != "/"):
	directory_path_out += "/"

with open(file_path_in, "rb") as f:
	
	n = 6
	sloorp = f.read(n)

	while(len(sloorp) == n):
		
		if (is_ogg_header(sloorp)):
			sloorp = handle_ogg(f, n, directory_path_out)
		else:
			sloorp = sloorp[1:] + f.read(1)


print "Found a total of " + str(x) + " instances. "
