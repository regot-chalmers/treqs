# Vision for T-Reqs demonstrator

This file is supposed to collect some ideas on how to build the demonstrator.

## Example Requirements

For a demonstrator, we need example (system) requirements, high-level use cases / user stories / features, and tests. 
Potentially even software.

### Domain
Our current idea is to use requirements of T-Reqs as this example. 
Thus, building the open source flavour of T-Reqs within itself.

We will then maintain requirements and tests for scripts (see below).

We believe that could make a good and limited real world-example. That would be somewhat like making a compiler for a programming language in the programming language itself.

### High-level user requirements
We aim for using Github issues as work packages/user stories/etc. In the example below we use “#1” to refer to https://github.com/regot-chalmers/treqs/issues/1 .
 
## Template
The minimal template is as follows.
 
* An .md file containing requirements simulates system requirements. For instance, the following text would represent a single requirement with id REQ1 that has traces to user stories US1 and US2:

	```
	Some supplementary text
	[requirement id=REQ1 story=US1,US2]
	Requirement text
	[/requirement]
	More supplementary text
	```
* A test case file with test cases. Test cases in our case are both markdown files (for manual test routines) and python files (for automated test scripts). An example for a manual test case and a python test case are depicted below. In both cases, the [testcase] tag contains a test case id as well as tracing information to user stories and system requirements.

	```
	[testcase id=TC1TestCaseName story=US1 req=REQ1]
	Purpose: Purpose of the test case without linebreak.
	
	## Setup
	Describe any steps that must be done before performing the test.
	
	## Scenario / Steps
	
	## Expected outcome
	
	## Tear down
	Describe what to do after the test
	
	## Test result
	Protocol of the result of executing this test, latest on top.
	```

	```
	#==================================
	# [testcase id=TC_python_test1 story=US4 req=REQ3]
	# 
	# <Purpose of the test case>
	# 
	#==================================
	testcase TC1__test_case_name() {
	...
	}
	```	
* A list of user stories. Currently, both issues in the github project labeled "user story" and markdown files are accepted. In both cases, the [userstory] tag is required to obtain a unique id for each story. An example for a markdown file containing user stories is depicted below.

	```
	[userstory id=US2]
	As a system manager, I want to make sure that proposed updates to requirements are of good quality, do not conflict with each other, or with the product mission. 
	
	[userstory id=US3]
	As member of an experimenting team, I want to experiment with new requirements and features so that I can better assess their business value and cost. This must not affect existing requirements during the experiment or block the requirements database afterwards. 
	
	[userstory id=US4]
	As a test architect or system manager, I want to be aware of new requirements for the test infrastructure early on so that I can plan verification and validation pro-actively. 
```

The formats are here mainly chosen for convenience, but can easily be adapted to any company standard. 

## Scripts
Python scripts are included (in the scripts directory) that verify the tracing between user stories, system requirements, as well as test cases. Furthermore, they verify that ids are unique and that there are no user stories or test cases that lack traces.

The main.py script is the overall execution script, invoking all required modules and producing a markdown log file (Summary_*) in the logs folder (scripts/logs). The script can be provided with several command line arguments (directories for all artifact types, file name patterns, recursive directory traversion).

The scripting currently assumes that all tags ([userstory], [testcase] and [requirement]) and the attributes are as described above. Furthermore, without command line argmuents, main.py assumes that all files are under treqs-reqts, that user story files are markdown files starting with "US\_", that system requirement files are markdown files starting with "SR\_", and that test case files are either markdown or python files starting with "TC\_".

An instance of Travis-CI will be added that executes this script for every commit and publishes the report.