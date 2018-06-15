import getopt, sys, mUSProcessor, mSysReqProcessor, mTCProcessor, datetime, os

#Default paths for respective files (user stories, test cases, system requirements). Can be provided as function arguments.
usDir = '../treqs-reqts'
tcDir = '../treqs-reqts'
sysReqDir = '../treqs-reqts'

#Default patterns for respective filenames (user stories, test cases, system requirements). Can be provided as function arguments.
usPattern = 'US_.*?\.md'
tcPattern = 'TC_.*?(\.py|\.md)'
sysReqPattern = 'SR_.*?\.md'

recursive = False

# argument options for this script. Only accepts the option d (root dir) and r (recursive)
try:
    opts, args = getopt.getopt(sys.argv[1:], "hu:s:t:r", ["help","usdir=","sysreqdir=","tcdir=","uspattern=","srpattern=","tcpattern="])
except getopt.GetoptError:
    print('Usage: ' + sys.argv[0] + ' -u <user story directory> -s <system requirements directory> -t <test case directory> -r')
    sys.exit(2)
for opt, arg in opts:
    if opt in ("-u", "--usdir"):
        usDir = os.path.normpath(arg)
    elif opt in ("-s", "--sysreqdir"):
        sysReqDir = os.path.normpath(arg)
    elif opt in ("-t", "--tcdir"):
        tcDir = os.path.normpath(arg)
    elif opt in ("--uspattern"):
        usPattern = os.path.normpath(arg)
    elif opt in ("--srpattern"):
        sysReqPattern = os.path.normpath(arg)
    elif opt in ("--tcpattern"):
        tcPattern = os.path.normpath(arg)
    elif opt in ("-r"):
        recursive = True
    elif opt in ("-h", "--help"):
        print('Usage: ' + sys.argv[0] + ' -u <user story directory> -s <system requirements directory> -t <test case directory> [-r]')
        sys.exit(2)
#Do all the data processing here
reqProcessor = mSysReqProcessor.SysReqsProcessor()
reqProcessor.processAllLines(sysReqDir, recursive, sysReqPattern)

usProcessor = mUSProcessor.USProcessor()
usProcessor.processAllUS(usDir, recursive, usPattern)

tcProcessor = mTCProcessor.TCProcessor()
tcProcessor.processAllTC(tcDir, recursive, tcPattern)

#Get all the user stories and traces to them
existingStories = usProcessor.storySet
tracedStoriesFromReqs = reqProcessor.storySet
tracedStoriesFromTests = tcProcessor.storySet
#Calculate which story IDs are not traced to
diffUSReq = existingStories.difference(tracedStoriesFromReqs)
diffUSTests = existingStories.difference(tracedStoriesFromTests)

#Get all the requirements and traces to them
existingReqs = reqProcessor.reqIDSet
tracedReqsFromTests = tcProcessor.reqSet
#Calculate which Req IDs are not traced to
diffReqTests = existingReqs.difference(tracedReqsFromTests)

#Get all duplicate IDs
duplicateUS = usProcessor.duplicateStorySet
duplicateTC = tcProcessor.duplicateIDSet
duplicateReq = reqProcessor.duplicateIDSet

#Get all IDs of artifacts missing traces
reqsWithoutUSTraces = reqProcessor.noUSTracingSet
testsWithoutUSTraces = tcProcessor.noUSTracingSet
testsWithoutReqTraces = tcProcessor.noReqTracingSet

try: 
    os.makedirs('logs')
except OSError:
    if not os.path.isdir('logs'):
        raise

log = open('logs/Summary_log_'+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.md',"w")

log.write('# T-Reqs commit report #\n\n')
log.write('### Duplicate IDs ###\n')
log.write('The following duplicate User Story IDs exist:\n\n')
for currentID in duplicateUS:
    log.write('* User Story ' + currentID + '\n')
    
log.write('\n')
log.write('The following duplicate System Requirement IDs exist:\n\n')
for currentID in duplicateReq:
    log.write('* System Requirement ' + currentID + '\n')
    
log.write('\n')
log.write('The following duplicate Test Case IDs exist:\n\n')
for currentID in duplicateTC:
    log.write('* Test Case ' + currentID + '\n')
    
log.write('\n')

log.write('### Items without traces ###\n')
log.write('The following System Requirements lack traces to user stories:\n\n')
for currentID in reqsWithoutUSTraces:
    log.write('* System Requirement ' + currentID + '\n')
    
log.write('\n')
log.write('The following Test Cases lack traces to user stories:\n\n')
for currentID in testsWithoutUSTraces:
    log.write('* Test Case ' + currentID + '\n')

log.write('\n')
log.write('The following Test Cases lack traces to system requirements:\n\n')
for currentID in testsWithoutReqTraces:
    log.write('* Test Case ' + currentID + '\n')

log.write('\n')

log.write('### Missing traces ###\n')
log.write('The following user stories are not referenced by any system requirement:\n\n')
for currentID in diffUSReq:
    log.write('* User Story ' + currentID + '\n')
    
log.write('\n')
log.write('The following user stories are not referenced by any test case:\n\n')
for currentID in diffUSTests:
    log.write('* User Story ' + currentID + '\n')
    
log.write('\n')
log.write('The following system requirements are not referenced by any test case:\n\n')
for currentID in diffReqTests:
    log.write('* System Requirement ' + currentID + '\n')
    
log.close()