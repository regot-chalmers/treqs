#!/usr/bin/python
import getopt, os, fnmatch, re, sys, datetime

#function defs
#NOTE: Not self-contained/effect-free. It uses and mutates the sets in which ids are stored (storySet,noUSTracingSet,reqSet,noReqTracingSet,testIDSet,duplicateIDSet)
def processTestCaseLine( line ):
	"This process a single line in a test case file, extracting duplicate IDs, missing traces, and a list of all traces to US and requirements."

	#Extracts the actual test case tag if there is one. Note that this requires the tag to be in a single line.
	m = re.search('\[testcase .*?\]', line)
	if m:
		log.write('New Test Case:\n')
		reqtag = m.group(0)
		log.write(reqtag+'\n')

		#Extract the id attribute from within the test case tag. Only test cases with id are processed.
		id = re.search('(?<=id=).*?(?=[ \]])', reqtag)
		if id:
			id = id.group(0)
			log.write(id+'\n')

			#Find duplicate ids. Note that currently, duplicate ids are still processed further.
			if id in testIDSet:
				log.write('Duplicate TC id:'+id+'\n')
				duplicateIDSet.add(id)
			else:
				testIDSet.add(id)

			#Find all story attributes. Supports also multiple storu attributes in theory.
			stories = re.findall('(?<=story=).*?(?=[ \]])', reqtag)

			#Find test cases without user story traces
			if len(stories)==0:
				log.write('Warning: Test is not traced to a user story!\n')
				noUSTracingSet.add(id)
			else:
				for currentUS in stories:
					#Support potential commas in an issue attribute
					splitstories = re.split(',', currentUS)
					for currentStory in splitstories:
						log.write(currentStory+'\n')
						storySet.add(currentStory)

			#Find all req attributes.
			reqs = re.findall('(?<=req=).*?(?=[ \]])', reqtag)

			#Find test cases without requirement traces
			if len(reqs)==0:
				log.write('Warning: Test is not traced to a requirement!\n')
				noReqTracingSet.add(id)
			else:
				for currentReq in reqs:
					#Support potential commas in an req attribute
					splitreqs = re.split(',', currentReq)
					for currentReq in splitreqs:
						log.write(currentReq)
						reqSet.add(currentReq)
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
	print('Usage: '+sys.argv[0]+' -d <directory> -r')
	sys.exit(2)
for opt, arg in opts:
	if opt in ("-d", "--dir"):
		dir = os.path.normpath(arg)
	elif opt in ("-r"):
		recursive = True
#log.write 'Directory is', dir
#log.write 'Recursive is', recursive

log = open('logs/TC_log_'+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.md',"w")
#Sets for all ids
storySet = set()
noUSTracingSet = set()
testIDSet = set()
duplicateIDSet = set()
reqSet = set()
noReqTracingSet = set()

#recursive traversion of root directory
if recursive:
	for root, directories, filenames in os.walk(dir):
		#	for directory in directories:
		#		log.write os.path.join(root, directory)
		for filename in filenames:
			#Only files ending on sys-reqts.md are scanned
			patternA = "TC_*.md"
			patternB = "TC_*.py"
			if fnmatch.fnmatch(filename, patternA) or fnmatch.fnmatch(filename, patternB):
				with open(os.path.join(root,filename), "r") as file:
					for line in file:
						processTestCaseLine(line)
else:
	listOfFiles = os.listdir(dir)

	#Only python or markdown files starting with TC are scanned
	patternA = "TC_*.md"
	patternB = "TC_*.py"
	for entry in listOfFiles:
		if fnmatch.fnmatch(entry, patternA) or fnmatch.fnmatch(entry, patternB):
			with open(os.path.join(dir,entry), "r") as file:
				for line in file:
					processTestCaseLine(line )

#Simple log.writeouts of all relevant sets.
log.write('All story traces:\n')
for currentStory in storySet:
	log.write(currentStory+'\n')
log.write('\n')

log.write('All requirement traces:\n')
for currentReq in reqSet:
	log.write(currentReq+'\n')
log.write('\n')

log.write('Test cases without traces to stories:\n')
for currentID in noUSTracingSet:
	log.write(currentID+'\n')
log.write('\n')

log.write('Test cases without traces to requirements:\n')
for currentID in noReqTracingSet:
	log.write(currentID+'\n')
log.write('\n')

log.write('Duplicate test IDs:\n')
for currentID in duplicateIDSet:
	log.write(currentID+'\n')
	
log.close() 