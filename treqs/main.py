#!/usr/bin/env python

import getopt, sys, datetime, os
from treqs import mUSProcessor, mSysReqProcessor, mTCProcessor

def main(argv):

    #Default paths for respective files (user stories, test cases, system requirements). Can be provided as function arguments.
    usDir = 'requirements'
    tcDir = 'tests'
    sysReqDir = 'requirements'

    #Default patterns for respective filenames (user stories, test cases, system requirements). Can be provided as function arguments.
    usPattern = 'US_.*?\.md'
    tcPattern = 'TC_.*?(\.py|\.md)$'
    sysReqPattern = 'SR_.*?\.md'

    recursive = False
        # argument options for this script. Only accepts the option d (root dir) and r (recursive)
    try:
        opts, args = getopt.getopt(argv[1:], "hu:s:t:r", ["help","usdir=","sysreqdir=","tcdir=","uspattern=","srpattern=","tcpattern="])
    except getopt.GetoptError:
        print('Usage: ' + argv[0] + ' -u <user story directory> -s <system requirements directory> -t <test case directory> -r')
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
            print('Usage: ' + argv[0] + ' -u <user story directory> -s <system requirements directory> -t <test case directory> [-r]')
            sys.exit(2)

    try:
        os.makedirs('logs')
    except OSError:
        if not os.path.isdir('logs'):
            raise

    #Do all the data processing here
    reqProcessor = mSysReqProcessor.SysReqsProcessor()
    success = reqProcessor.processAllLines(sysReqDir, recursive, sysReqPattern)

    usProcessor = mUSProcessor.USProcessor()
    success = usProcessor.processAllUS(usDir, recursive, usPattern) and success

    tcProcessor = mTCProcessor.TCProcessor()
    success = tcProcessor.processAllTC(tcDir, recursive, tcPattern) and success

    #Get all the user stories and traces to them
    existingStories = usProcessor.storySet
    tracedStoriesFromReqs = reqProcessor.storySet
    tracedStoriesFromTests = tcProcessor.storySet
    #Calculate which story IDs are not traced to
    diffUSReq = existingStories.difference(tracedStoriesFromReqs)
    diffUSTests = existingStories.difference(tracedStoriesFromTests)
    #Calculate whether there are any traces to non-existing stories
    nonExistingUSReqs = tracedStoriesFromReqs.difference(existingStories)
    nonExistingUSTests = tracedStoriesFromTests.difference(existingStories)

    #Get all the requirements and traces to them
    existingReqs = reqProcessor.reqIDSet
    tracedReqsFromTests = tcProcessor.reqSet
    #Calculate which Req IDs are not traced to
    diffReqTests = existingReqs.difference(tracedReqsFromTests)
    #Calculate which Req IDs are traced to but do not exist
    nonExistingReqTC = tracedReqsFromTests.difference(existingReqs)

    #Get all duplicate IDs
    duplicateUS = usProcessor.duplicateStorySet
    duplicateTC = tcProcessor.duplicateIDSet
    duplicateReq = reqProcessor.duplicateIDSet

    #Get all IDs of artifacts missing traces
    reqsWithoutUSTraces = reqProcessor.noUSTracingSet
    testsWithoutUSTraces = tcProcessor.noUSTracingSet
    testsWithoutReqTraces = tcProcessor.noReqTracingSet
    
    if success and (len(nonExistingUSReqs)>0 or len(nonExistingUSTests)>0 or len(nonExistingReqTC)>0):
        success = False

    filename = 'logs/Summary_log_'+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.md'
    log = open(filename,"w")

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
        
    log.write('\n')
    log.write('### Missing items ###\n')
    log.write('The following user stories are referenced by requirements, but do not exist:\n\n')
    for currentID in nonExistingUSReqs:
        log.write('* User Story ' + currentID + '\n')
        
    log.write('\n')
    log.write('The following user stories are referenced by test cases, but do not exist:\n\n')
    for currentID in nonExistingUSTests:
        log.write('* User Story ' + currentID + '\n')
        
    log.write('\n')
    log.write('The following requirements are referenced by test cases, but do not exist:\n\n')
    for currentID in nonExistingReqTC:
        log.write('* Requirement ' + currentID + '\n')
        
    log.close()
    
    #Return -1 if the validation has failed, and print the log to the console
    if not success:
        print('Validation failed with the following output:\n')
        with open(filename, 'r') as f:
            print(f.read())
        return -1

if __name__ == '__main__':
    main(sys.argv)
