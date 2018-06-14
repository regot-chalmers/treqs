#!/usr/bin/python
import getopt, os, fnmatch, re, sys

#function defs
#NOTE: Not self-contained/effect-free. It uses and mutates the sets in which ids are stored (storySet,duplicateStorySet)
def processStoryLine( line ):
	"This process a single line in a user story file, extracting duplicate IDs and a list of all US ids."
        
	#Extracts the actual user story tag if there is one. Note that this requires the tag to be in a single line.
	m = re.search('\[us .*?\]', line)
	if m:
		print ('New Story:')
		reqtag = m.group(0)
		print (reqtag)
                
		#Extract the id attribute from within the user story tag. Only user stories with id are processed.
		id = re.search('(?<=id=).*?(?=[ \]])', reqtag)
		if id:
			id = id.group(0)
			print (id)

			#Find duplicate ids. Note that currently, duplicate ids are still processed further.
			if id in storySet:
				print ('Duplicate story id:',id)
				duplicateStorySet.add(id)
			else:
				storySet.add(id)
		print ''
	return

#MAIN
#default values for directory and recursive traversion.
dir='./'
recursive=False

#argument options for this script. Only accepts the option d (root dir) and r (recursive)
try:
	opts, args = getopt.getopt(sys.argv[1:],"hd:r",["dir="])
except getopt.GetoptError:
	print ('Usage: ',sys.argv[0],' -d <directory> -r')
	sys.exit(2)
for opt, arg in opts:
	if opt in ("-d", "--dir"):
		dir = os.path.normpath(arg)
	elif opt in ("-r"):
		recursive = True
#print 'Directory is', dir
#print 'Recursive is', recursive 

#Sets for all ids
storySet = set()
duplicateStorySet = set()

#recursive traversion of root directory
if recursive:
	for root, directories, filenames in os.walk(dir):
		#	for directory in directories:
		#		print os.path.join(root, directory) 

		for filename in filenames: 
			entry=os.path.join(root,filename) 
			
			#Only files ending on user-stories.md are scanned
			pattern = "*user-stories.md"  
			if fnmatch.fnmatch(entry, pattern):
				with open(entry, "r") as file:
					for line in file: 
						processStoryLine(line)
else:
	listOfFiles = os.listdir(dir)
	
	#Only files ending on user-stories.md are scanned
	pattern = "*user-stories.md"  
	for entry in listOfFiles:	
		if fnmatch.fnmatch(entry, pattern):
			with open(os.path.join(dir,entry), "r") as file:
				for line in file:
					processStoryLine(line)

#Simple printouts of all relevant sets.
print ('All stories:')
for currentStory in storySet:
	print (currentStory)
print ('')

print ('Duplicate story IDs:')
for currentID in duplicateStorySet:
	print (currentID)
