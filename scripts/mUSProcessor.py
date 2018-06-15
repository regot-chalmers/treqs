#!/usr/bin/python
import getopt, os, fnmatch, re, sys, datetime


class USProcessor:
	log = open('logs/US_log_'+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.md',"w")

	#Sets for all ids
	storySet = set()
	duplicateStorySet = set()
		
	#NOTE: Not self-contained/effect-free. It uses and mutates the sets in which ids are stored (storySet,duplicateStorySet)
	def processStoryLine( self, line):
		"This process a single line in a user story file, extracting duplicate IDs and a list of all US ids."
	
		#Extracts the actual user story tag if there is one. Note that this requires the tag to be in a single line.
		m = re.search('\[userstory .*?\]', line)
		if m:
			self.log.write('New Story:\n')
			reqtag = m.group(0)
			self.log.write(reqtag+'\n')
	
			#Extract the id attribute from within the user story tag. Only user stories with id are processed.
			id = re.search('(?<=id=).*?(?=[ \]])', reqtag)
			if id:
				id = id.group(0)
				self.log.write(id+'\n')
	
				#Find duplicate ids. Note that currently, duplicate ids are still processed further.
				if id in self.storySet:
					self.log.write('Duplicate story id:'+id+'\n')
					self.duplicateStorySet.add(id)
				else:
					self.storySet.add(id)
			self.log.write('\n')
		return
	
	def processAllUS ( self, dir, recursive):
		
		#recursive traversion of root directory
		if recursive:
			for root, directories, filenames in os.walk(dir):
				#	for directory in directories:
				#		self.log.write os.path.join(root, directory)
		
				for filename in filenames:
					#Only markdown files starting with US are scanned
					pattern = "US_*.md"
					if fnmatch.fnmatch(filename, pattern):
						with open(os.path.join(root,filename), "r") as file:
							for line in file:
								self.processStoryLine(line)
		else:
			listOfFiles = os.listdir(dir)
		
			#Only markdown files starting with US are scanned
			pattern = "US_*.md"
			for entry in listOfFiles:
				if fnmatch.fnmatch(entry, pattern):
					with open(os.path.join(dir,entry), "r") as file:
						for line in file:
							self.processStoryLine(line)
		
		#Simple self.log.writeouts of all relevant sets.
		self.log.write('All stories:\n')
		for currentStory in self.storySet:
			self.log.write(currentStory+'\n')
		self.log.write('\n')
		
		self.log.write('Duplicate story IDs:\n')
		for currentID in self.duplicateStorySet:
			self.log.write(currentID+'\n')
			
		self.log.close()
		return