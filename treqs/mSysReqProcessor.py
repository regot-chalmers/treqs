#!/usr/bin/python
import getopt, os, re, sys, datetime

class SysReqsProcessor:

	# Sets for all ids
	storySet = set()
	noUSTracingSet = set()
	reqIDSet = set()
	duplicateIDSet = set()

	def __init__(self):
		self.log = open('logs/SysReq_log_'+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.md',"w+")

	# function defs
	# NOTE: Not self-contained/effect-free. It uses and mutates the sets in which ids are stored (storySet,noUSTracingSet,reqIDSet,duplicateIDSet)
	def processRequirementsLine(self, line):
		"This process a single line in a requirements file, extracting duplicate IDs, missing US traces, and a list of all traces to US."
	
		success = True
		
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
			if id in self.reqIDSet:
				self.log.write('Duplicate requirement id:'+id+'\n')
				self.duplicateIDSet.add(id)
				success = False
			else:
				self.reqIDSet.add(id)
	
			# Find all issue attributes. Supports also multiple issue attributes in theory.
			stories = re.findall('(?<=story=).*?(?=[ \]])', reqtag)
			# log.write(stories)
	
			# Find requirements without traces
			if len(stories) == 0:
				self.log.write('Warning: Requirement is not traced to a user story!\n')
				self.noUSTracingSet.add(id)
				success = False
			else:
				for currentUS in stories:
					# Support potential commas in an issue attribute
					splitstories = re.split(',', currentUS)
					for currentStory in splitstories:
						self.log.write(currentStory+'\n')
						self.storySet.add(currentStory)
			self.log.write('\n')
		return success
	
	
	def processAllLines (self, dir, recursive, filePattern='SR_.*?\.md'):

		success = True 

		# recursive traversion of root directory
		if recursive:
			for root, directories, filenames in os.walk(dir):
				# for directory in directories
				for filename in filenames:
					#Only files matching the given pattern are scanned
					match = re.search(filePattern, filename)
					if match:
						entry = os.path.join(root, filename)
						with open(entry, "r") as file:
							for line in file:
								success = self.processRequirementsLine(line) and success
		else:
			listOfFiles = os.listdir(dir)
			for entry in listOfFiles:
				#Only files matching the given pattern are scanned
				match = re.search(filePattern, entry)
				if match:
					with open(os.path.join(dir, entry), "r") as file:
						for line in file:
							success = self.processRequirementsLine(line) and success

		# Simple log.writeouts of all relevant sets.
		self.log.write('All stories:\n')
		for currentStory in self.storySet:
			self.log.write(currentStory+'\n')
		self.log.write('\n')
		
		self.log.write('Requirements without traces to stories:\n')
		for currentID in self.noUSTracingSet:
			self.log.write(currentID+'\n')
		self.log.write('\n')
		
		self.log.write('Duplicate requirements IDs:\n')
		for currentID in self.duplicateIDSet:
			self.log.write(currentID+'\n')
			
		self.log.close()
		return success
