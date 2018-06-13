#!/usr/bin/python
import getopt, os, fnmatch, re, sys

dir='./'
recursive=False

try:
	opts, args = getopt.getopt(sys.argv[1:],"hd:r",["dir="])
except getopt.GetoptError:
      print 'Usage: '+sys.argv[0]+' -d <directory> -r'
      sys.exit(2)
for opt, arg in opts:
	if opt in ("-d", "--dir"):
        	dir = os.path.normpath(arg)
	elif opt in ("-r"):
        	recursive = True
print 'Directory is', dir
print 'Recursive is', recursive 

storySet = set()
noUSTracingSet = set()
reqIDSet = set()
duplicateIDSet = set()

if recursive:
	for root, directories, filenames in os.walk(dir):
	#	for directory in directories:
	#		print os.path.join(root, directory) 

		for filename in filenames: 
			entry=os.path.join(root,filename) 
			pattern = "*sys-reqts.md"  
    			if fnmatch.fnmatch(entry, pattern):
				file = open(entry, "r")
				for line in file: 
					#if line.find('<requirement',0,len(line))!=-1:
					#	print line      
					m = re.search('<requirement .*?>', line)
					if m:
						print 'New requirement:'
						reqtag = m.group(0)
						print reqtag
						id = re.search('(?<=id=).*?(?=[ >])', reqtag)
						if id:
							id = id.group(0)
							print id
							if id in reqIDSet:
								print 'Duplicate requirement id:',id
								duplicateIDSet.add(id)
							else:
								reqIDSet.add(id) 
							stories = re.findall('(?<=issue=).*?(?=[ >])', reqtag)
							if len(stories)==0:
								print 'Warning: Requirement is not traced to a user story!'
								noUSTracingSet.add(id)
							for currentUS in stories:
								splitstories = re.split(',', currentUS)
								for currentStory in splitstories:
									print currentStory
									storySet.add(currentStory)
							print ''
else:
	listOfFiles = os.listdir(dir)
	pattern = "*sys-reqts.md"  
	for entry in listOfFiles:	
		if fnmatch.fnmatch(entry, pattern):
                	file = open(os.path.join(dir,entry), "r")
                        for line in file:
	                        #if line.find('<requirement',0,len(line))!=-1:
                                #       print line
                                m = re.search('<requirement .*?>', line)
                                if m:
        	                        print 'New requirement:'
                                        reqtag = m.group(0)
                                        print reqtag
                                        id = re.search('(?<=id=).*?(?=[ >])', reqtag)
                                        if id:
						id = id.group(0)
                                                print id
                                                if id in reqIDSet:
                                                	print 'Duplicate requirement id:',id
                                                        duplicateIDSet.add(id)
                                                else:
                                                        reqIDSet.add(id)	                                        
						stories = re.findall('(?<=issue=).*?(?=[ >])', reqtag)
        	                                if len(stories)==0:
                	        	                print 'Warning: Requirement is not traced to a user story!'
							noUSTracingSet.add(id)
                        	                for currentUS in stories:
                                		        splitstories = re.split(',', currentUS)
                                        	        for currentStory in splitstories:
                                        		        print currentStory
                                                        	storySet.add(currentStory)
						print ''

print 'All stories:'
for currentStory in storySet:
	print currentStory
print''
print 'Requirements without traces to stories:'
for currentID in noUSTracingSet:
	print currentID
print''
print 'Duplicate requirements IDs:'
for currentID in duplicateIDSet:
	print currentID
