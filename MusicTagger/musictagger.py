#!/usr/bin/python
#############################################################################################################
## MusicTagger, Waterstone Productions
## Music organization tool based on file names and directory names
##
## File name is the title
## Immediate folder is the album
## Folder above that is the artist
##
## Requires: EyeD3 and trim-app
#############################################################################################################
import os, sys
#############################################################################################################


#############################################################################################################
id3_base	= "eyeD3 "
id3_album	= " --album="
id3_artist	= " --artist="
id3_title	= " --title="
id3_removeall	= " --remove-all "
#############################################################################################################
trim_base	= "trim-app "
trim_rsrc	= " -r "
trim_junk	= " -d "
trim_print	= " -p "
#############################################################################################################
spacechars	= ["\'", "'", "\"", ":"]
hyphenchars	= []
andchars	= ["&"]
#############################################################################################################


#############################################################################################################
def GetArtist(path):
	parts = os.path.dirname(path).split("/")
	return "\"" + parts[len(parts) - 2] + "\""
#############################################################################################################
def GetAlbum(path):
	parts = os.path.dirname(path).split("/")
	return "\"" + parts[len(parts) - 1] + "\""
#############################################################################################################
def GetTitle(path):
	base = "\"" + os.path.splitext(os.path.basename(path))[0] + "\" "
	return base
#############################################################################################################
def GetFileName(path):
	return "\"" + path + "\""
#############################################################################################################
def Tag(directory):
	for root, dirs, files in os.walk(directory):
		for file in files:
			path = os.path.join(root, file)
			artist = GetArtist(path)
			album = GetAlbum(path)
			title = GetTitle(path)
			filename = GetFileName(path)
			command = id3_base + id3_artist + artist + id3_album + album + id3_title + title
			command = command + filename
			print command
			os.system(command)
#############################################################################################################
def UnTag(directory):
	command = id3_base + id3_removeall + directory
	print command
	os.system(command)
#############################################################################################################
def Clean(directory):
	os.chdir(directory)
	command = trim_base + trim_rsrc + trim_junk + trim_print
	print command
	os.system(command)
#############################################################################################################
def Fix(directory):
	for root, dirs, files in os.walk(directory):
		for file in files:
			newfile = file
			for char in spacechars:
				if char in file:
					newfile = newfile.replace(char, "")
					print file, newfile
			for char in hyphenchars:
				if char in file:
					newfile = newfile.replace(char, "-")
					print file, newfile
			for char in andchars:
				if char in file:
					newfile = newfile.replace(char, "And")
					print file, newfile
			oldfilename = os.path.join(root, file)
			newfilename = os.path.join(root, newfile)
			os.rename(oldfilename, newfilename)
#############################################################################################################
def Help():
	print "musictagger <command> <directory>"
	print "  commands:"
	print "    tag   = Tags all music with information from the recursive directory and file names"
	print "    untag = Removes the tags from all the files in the directory"
	print "    clean = Cleans the specified directory of junk files"
	print "    fix   = Fixes all the filenames to remove bad characters"
	sys.exit(0)
#############################################################################################################
def Error(message):
	print "ERROR: " + message
	sys.exit(0)
#############################################################################################################


#############################################################################################################
command = ""
directory = ""
#############################################################################################################
if len(sys.argv) != 3:
	Help()
else:
	command = sys.argv[1]
	directory = sys.argv[2]
#############################################################################################################
if not os.path.exists(directory):
	Error("Directory must exist already")
#############################################################################################################
if command == "tag":
	Tag(directory)
elif command == "untag":
	UnTag(directory)
elif command == "clean":
	Clean(directory)
elif command == "fix":
	Fix(directory)
else:
	Help()
#############################################################################################################
