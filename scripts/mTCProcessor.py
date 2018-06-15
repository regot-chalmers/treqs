#!/usr/bin/python
import getopt, os, re, sys, datetime

class TCProcessor:
	try: 
		os.makedirs('logs')
	except OSError:
		if not os.path.isdir('logs'):
			raise
	log = open('logs/TC_log_'+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.md',"w")

	#Sets for all ids
	storySet = set()
	noUSTracingSet = set()
	testIDSet = set()
	duplicateIDSet = set()
	reqSet = set()
	noReqTracingSet = set()

	#NOTE: Not self-contained/effect-free. It uses and mutates the sets in which ids are stored (storySet,noUSTracingSet,reqSet,noReqTracingSet,testIDSet,duplicateIDSet)
	def processTestCaseLine( self, line):
		"This process a single line in a test case file, extracting duplicate IDs, missing traces, and a list of all traces to US and requirements."
	
		#Extracts the actual test case tag if there is one. Note that this requires the tag to be in a single line.
		m = re.search('\[testcase .*?\]', line)
		if m:
			self.log.write('New Test Case:\n')
			reqtag = m.group(0)
			self.log.write(reqtag+'\n')
	
			#Extract the id attribute from within the test case tag. Only test cases with id are processed.
			id = re.search('(?<=id=).*?(?=[ \]])', reqtag)
			if id:
				id = id.group(0)
				self.log.write(id+'\n')
	
				#Find duplicate ids. Note that currently, duplicate ids are still processed further.
				if id in self.testIDSet:
					self.log.write('Duplicate TC id:'+id+'\n')
					self.duplicateIDSet.add(id)
				else:
					self.testIDSet.add(id)
	
				#Find all story attributes. Supports also multiple storu attributes in theory.
				stories = re.findall('(?<=story=).*?(?=[ \]])', reqtag)
	
				#Find test cases without user story traces
				if len(stories)==0:
					self.log.write('Warning: Test is not traced to a user story!\n')
					self.noUSTracingSet.add(id)
				else:
					for currentUS in stories:
						#Support potential commas in an issue attribute
						splitstories = re.split(',', currentUS)
						for currentStory in splitstories:
							self.log.write(currentStory+'\n')
							self.storySet.add(currentStory)
	
				#Find all req attributes.
				reqs = re.findall('(?<=req=).*?(?=[ \]])', reqtag)
	
				#Find test cases without requirement traces
				if len(reqs)==0:
					self.log.write('Warning: Test is not traced to a requirement!\n')
					self.noReqTracingSet.add(id)
				else:
					for currentReq in reqs:
						#Support potential commas in an req attribute
						splitreqs = re.split(',', currentReq)
						for currentReq in splitreqs:
							self.log.write(currentReq)
							self.reqSet.add(currentReq)
			self.log.write('\n')
		return
	
	def processAllTC (self, dir, recursive, filePattern='TC_.*?(py|md)'):	
		#recursive traversion of root directory
		if recursive:
			for root, directories, filenames in os.walk(dir):
				#	for directory in directories:
				#		self.log.write os.path.join(root, directory)
				for filename in filenames:
					#Only files matching the given pattern are scanned
					match = re.search(filePattern, entry)
					if match:
						with open(os.path.join(root,filename), "r") as file:
							for line in file:
								self.processTestCaseLine(line)
		else:
			listOfFiles = os.listdir(dir)
			#Only files matching the given pattern are scanned
			for entry in listOfFiles:
				match = re.search(filePattern, entry)
				if match:
					with open(os.path.join(dir,entry), "r") as file:
						for line in file:
							self.processTestCaseLine(line)
		
		#Simple self.log.writeouts of all relevant sets.
		self.log.write('All story traces:\n')
		for currentStory in self.storySet:
			self.log.write(currentStory+'\n')
		self.log.write('\n')
		
		self.log.write('All requirement traces:\n')
		for currentReq in self.reqSet:
			self.log.write(currentReq+'\n')
		self.log.write('\n')
		
		self.log.write('Test cases without traces to stories:\n')
		for currentID in self.noUSTracingSet:
			self.log.write(currentID+'\n')
		self.log.write('\n')
		
		self.log.write('Test cases without traces to requirements:\n')
		for currentID in self.noReqTracingSet:
			self.log.write(currentID+'\n')
		self.log.write('\n')
		
		self.log.write('Duplicate test IDs:\n')
		for currentID in self.duplicateIDSet:
			self.log.write(currentID+'\n')
			
		self.log.close()
		return