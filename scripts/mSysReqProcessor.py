#!/usr/bin/python
import getopt, os, fnmatch, re, sys, datetime

class SysReqsProcessor:
	log = open('logs/SysReq_log_'+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.md',"w")
	
	# Sets for all ids
	storySet = set()
	noUSTracingSet = set()
	reqIDSet = set()
	duplicateIDSet = set()
	
	# function defs
	# NOTE: Not self-contained/effect-free. It uses and mutates the sets in which ids are stored (storySet,noUSTracingSet,reqIDSet,duplicateIDSet)
	def processRequirementsLine(self, line):
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
			if id in self.reqIDSet:
				self.log.write('Duplicate requirement id:'+id+'\n')
				self.duplicateIDSet.add(id)
			else:
				self.reqIDSet.add(id)
	
			# Find all issue attributes. Supports also multiple issue attributes in theory.
			stories = re.findall('(?<=story=).*?(?=[ \]])', reqtag)
			# log.write(stories)
	
			# Find requirements without traces
			if len(stories) == 0:
				self.log.write('Warning: Requirement is not traced to a user story!\n')
				self.noUSTracingSet.add(id)
			else:
				for currentUS in stories:
					# Support potential commas in an issue attribute
					splitstories = re.split(',', currentUS)
					for currentStory in splitstories:
						self.log.write(currentStory+'\n')
						self.storySet.add(currentStory)
			self.log.write('\n')
		return
	
	
	def processAllLines (self, dir, recursive):
			
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
								self.processRequirementsLine(line)
		else:
			listOfFiles = os.listdir(dir)
		
			# Only files ending on sys-reqts.md are scanned
			pattern = "*sys-reqts.md"
			for entry in listOfFiles:
				if fnmatch.fnmatch(entry, pattern):
					with open(os.path.join(dir, entry), "r") as file:
						for line in file:
							self.processRequirementsLine(line)
		
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
		return
