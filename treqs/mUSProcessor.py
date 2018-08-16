#!/usr/bin/python
import getopt, os, re, sys, datetime, requests


class USProcessor:

	def __init__(self):
		self.log = open('logs/US_log_'+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.md',"w")

	#Sets for all ids
	storySet = set()
	duplicateStorySet = set()
		
	#NOTE: Not self-contained/effect-free. It uses and mutates the sets in which ids are stored (storySet,duplicateStorySet)
	def processStoryLine( self, line):
		"This processes a single line in a user story file, extracting duplicate IDs and a list of all US ids."
	
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
	
	def processAllOnlineUS (self, repoURL='https://api.github.com/repos/regot-chalmers/treqs'):
		"This processes a github repo, querying all open issues and extracting the ones with users tory label. From those, the IDs are exctracted"
		
		#Get all open issues from the given github repo.
		r = requests.get(repoURL.rstrip() + '/issues?state=open')
		data = r.json()
		
		for currentItem in data:
			
			#Extract all labels and check whether "user story" is in there.
			labelSet = set()
			for currentLabel in currentItem['labels']:
				labelSet.add(currentLabel['name'])
			
			if 'user story' in labelSet:
				#Extracts the actual user story tag if there is one. Note that this requires the tag to be in a single line.
				m = re.search('\[userstory .*?\]', currentItem['body'])
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
		
	def processAllUSFiles ( self, dir, recursive, filePattern='US_.*?\.md'):
		"Processes all files containing user stories, extracting user story tag IDs."
		#recursive traversion of root directory
		if recursive:
			for root, directories, filenames in os.walk(dir):
				#	for directory in directories:
				#		self.log.write os.path.join(root, directory)
		
				for filename in filenames:
					#Only files matching the given pattern are scanned
					match = re.search(filePattern, filename)
					if match:
						with open(os.path.join(root,filename), "r") as file:
							for line in file:
								self.processStoryLine(line)
		else:
			listOfFiles = os.listdir(dir)
		
			for entry in listOfFiles:
				#Only files matching the given pattern are scanned
				match = re.search(filePattern, entry)
				if match:
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
		return
	
	def processAllUS (self, dir, recursive, filePattern='US_.*?\.md'):
		"Shorthand, executing helper methods for user story extraction."
		self.processAllOnlineUS()
		self.processAllUSFiles(dir, recursive, filePattern)
		
		self.log.close()
		return