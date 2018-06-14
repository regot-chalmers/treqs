#!/usr/bin/python
import getopt, os, fnmatch, re, sys, datetime

#function defs
#NOTE: Not self-contained/effect-free. It uses and mutates the sets in which ids are stored (storySet,duplicateStorySet)
def processStoryLine( line ):
	"This process a single line in a user story file, extracting duplicate IDs and a list of all US ids."

	#Extracts the actual user story tag if there is one. Note that this requires the tag to be in a single line.
	m = re.search('\[userstory .*?\]', line)
	if m:
		log.write('New Story:\n')
		reqtag = m.group(0)
		log.write(reqtag+'\n')

		#Extract the id attribute from within the user story tag. Only user stories with id are processed.
		id = re.search('(?<=id=).*?(?=[ \]])', reqtag)
		if id:
			id = id.group(0)
			log.write(id+'\n')

			#Find duplicate ids. Note that currently, duplicate ids are still processed further.
			if id in storySet:
				log.write('Duplicate story id:'+id+'\n')
				duplicateStorySet.add(id)
			else:
				storySet.add(id)
		log.write('\n')
	return

#MAIN
#default values for directory and recursive traversion.
dir='./'
recursive=False

#argument options for this script. Only accepts the option d (root dir) and r (recursive)
try:
	opts, args = getopt.getopt(sys.argv[1:],"hd:r",["dir="])
except getopt.GetoptError:
	print('Usage: ',sys.argv[0],' -d <directory> -r')
	sys.exit(2)
for opt, arg in opts:
	if opt in ("-d", "--dir"):
		dir = os.path.normpath(arg)
	elif opt in ("-r"):
		recursive = True
#log.write 'Directory is', dir
#log.write 'Recursive is', recursive

log = open('logs/US_log_'+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.md',"w")
#Sets for all ids
storySet = set()
duplicateStorySet = set()

#recursive traversion of root directory
if recursive:
	for root, directories, filenames in os.walk(dir):
		#	for directory in directories:
		#		log.write os.path.join(root, directory)

		for filename in filenames:
			#Only markdown files starting with US are scanned
			pattern = "US_*.md"
			if fnmatch.fnmatch(filename, pattern):
				with open(os.path.join(root,filename), "r") as file:
					for line in file:
						processStoryLine(line)
else:
	listOfFiles = os.listdir(dir)

	#Only markdown files starting with US are scanned
	pattern = "US_*.md"
	for entry in listOfFiles:
		if fnmatch.fnmatch(entry, pattern):
			with open(os.path.join(dir,entry), "r") as file:
				for line in file:
					processStoryLine(line)

#Simple log.writeouts of all relevant sets.
log.write('All stories:\n')
for currentStory in storySet:
	log.write(currentStory+'\n')
log.write('\n')

log.write('Duplicate story IDs:\n')
for currentID in duplicateStorySet:
	log.write(currentID+'\n')
	
log.close()
