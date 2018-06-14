#!/usr/bin/python
import getopt, os, fnmatch, re, sys


# function defs
# NOTE: Not self-contained/effect-free. It uses and mutates the sets in which ids are stored (storySet,noUSTracingSet,reqIDSet,duplicateIDSet)
def processRequirementsLine(line):
	"This process a single line in a requirements file, extracting duplicate IDs, missing US traces, and a list of all traces to US."

	# Extracts the actual requirement tag if there is one. Note that this requires the tag to be in a single line.
	m = re.search('\[requirement .*?\]', line)
	if m:
		# print('New requirement:')
		reqtag = m.group(0)
		# print(reqtag)

		# Extract the id attribute from within the requirement tag. Only requirements with id are processed.
		id = re.search('(?<=id=).*?(?=[ \]])', reqtag)
		if id:
			id = id.group(0)
		# print(id)

		# Find duplicate ids. Note that currently, duplicate ids are still processed further.
		if id in reqIDSet:
			print('Duplicate requirement id:', id)
			duplicateIDSet.add(id)
		else:
			reqIDSet.add(id)

		# Find all issue attributes. Supports also multiple issue attributes in theory.
		stories = re.findall('(?<=issue=).*?(?=[ \]])', reqtag)
		# print(stories)

		# Find requirements without traces
		if len(stories) == 0:
			print('Warning: Requirement is not traced to a user story!')
			noUSTracingSet.add(id)
		else:
			for currentUS in stories:
				# Support potential commas in an issue attribute
				splitstories = re.split(',', currentUS)
				for currentStory in splitstories:
					print(currentStory)
					storySet.add(currentStory)
		print('')
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
# print('Directory is', dir)
# print('Recursive is', recursive)

# Sets for all ids
storySet = set()
noUSTracingSet = set()
reqIDSet = set()
duplicateIDSet = set()

# recursive traversion of root directory
if recursive:
	for root, directories, filenames in os.walk(dir):
		# for directory in directories:
		# 	print os.path.join(root, directory)

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

# Simple printouts of all relevant sets.
print('All stories:')
for currentStory in storySet:
	print(currentStory)
print('')

print('Requirements without traces to stories:')
for currentID in noUSTracingSet:
	print(currentID)
print('')

print('Duplicate requirements IDs:')
for currentID in duplicateIDSet:
	print(currentID)
