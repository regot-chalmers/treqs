#!/usr/bin/python
import getopt, os, fnmatch, re, sys, datetime


# function defs
# NOTE: Not self-contained/effect-free. It uses and mutates the sets in which ids are stored (storySet,noUSTracingSet,reqIDSet,duplicateIDSet)
def processRequirementsLine(line):
	"This process a single line in a requirements file, extracting duplicate IDs, missing US traces, and a list of all traces to US."

	# Extracts the actual requirement tag if there is one. Note that this requires the tag to be in a single line.
	m = re.search('\[requirement .*?\]', line)
	if m:
		# log.write('New requirement:')
		reqtag = m.group(0)
		# log.write(reqtag)

		# Extract the id attribute from within the requirement tag. Only requirements with id are processed.
		id = re.search('(?<=id=).*?(?=[ \]])', reqtag)
		if id:
			id = id.group(0)
		# log.write(id)

		# Find duplicate ids. Note that currently, duplicate ids are still processed further.
		if id in reqIDSet:
			log.write('Duplicate requirement id:'+id+'\n')
			duplicateIDSet.add(id)
		else:
			reqIDSet.add(id)

		# Find all issue attributes. Supports also multiple issue attributes in theory.
		stories = re.findall('(?<=story=).*?(?=[ \]])', reqtag)
		# log.write(stories)

		# Find requirements without traces
		if len(stories) == 0:
			log.write('Warning: Requirement is not traced to a user story!\n')
			noUSTracingSet.add(id)
		else:
			for currentUS in stories:
				# Support potential commas in an issue attribute
				splitstories = re.split(',', currentUS)
				for currentStory in splitstories:
					log.write(currentStory+'\n')
					storySet.add(currentStory)
		log.write('\n')
	return


# MAIN
# default values for directory and recursive traversion.
dir = './'
recursive = False

# argument options for this script. Only accepts the option d (root dir) and r (recursive)
try:
	opts, args = getopt.getopt(sys.argv[1:], "hd:r", ["dir="])
except getopt.GetoptError:
	print('Usage: ' + sys.argv[0] + ' -d <directory> -r')
	sys.exit(2)
for opt, arg in opts:
	if opt in ("-d", "--dir"):
		dir = os.path.normpath(arg)
	elif opt in ("-r"):
		recursive = True
# log.write('Directory is', dir)
# log.write('Recursive is', recursive)
try: 
    os.makedirs('logs')
except OSError:
    if not os.path.isdir('logs'):
        raise
log = open('logs/SysReq_log_'+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.md',"w")
# Sets for all ids
storySet = set()
noUSTracingSet = set()
reqIDSet = set()
duplicateIDSet = set()

# recursive traversion of root directory
if recursive:
	for root, directories, filenames in os.walk(dir):
		# for directory in directories:
		# 	log.write os.path.join(root, directory)

		for filename in filenames:
			entry = os.path.join(root, filename)

			# Only files ending on sys-reqts.md are scanned
			pattern = "*sys-reqts.md"
			if fnmatch.fnmatch(entry, pattern):
				with open(entry, "r") as file:
					for line in file:
						processRequirementsLine(line)
else:
	listOfFiles = os.listdir(dir)

	# Only files ending on sys-reqts.md are scanned
	pattern = "*sys-reqts.md"
	for entry in listOfFiles:
		if fnmatch.fnmatch(entry, pattern):
			with open(os.path.join(dir, entry), "r") as file:
				for line in file:
					processRequirementsLine(line)

# Simple log.writeouts of all relevant sets.
log.write('All stories:\n')
for currentStory in storySet:
	log.write(currentStory+'\n')
log.write('\n')

log.write('Requirements without traces to stories:\n')
for currentID in noUSTracingSet:
	log.write(currentID+'\n')
log.write('\n')

log.write('Duplicate requirements IDs:\n')
for currentID in duplicateIDSet:
	log.write(currentID+'\n')
	
log.close()
