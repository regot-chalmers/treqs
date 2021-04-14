# DEPRECATION WARNING

TReqs has moved to its [new public home at gitlab](https://gitlab.com/treqs-on-git/treqs-ng). 

We keep the code in this repository unchanged, since it is referenced in our publications. Based on our learnings, we have however redisigned the command line interface and started to build a much more flexible tool.




# T-Reqs: Tool Support for Managing Requirements in Large-Scale Agile System Development

Requirements engineering is crucial to support agile development of large systems with long lifetimes. 
Agile cross-functional teams must be aware of requirements at system level and able to efficiently propose updates to those requirements. 

  - *Objective:* T-Reqs' objective is to offer lightweight tooling to __manage requirements in large-scale agile system development__.
  - *Philosophy:* __Bring requirements close to teams.__ T-Reqs aims to put requirements into the hands of teams and allows managing them together with changes of code and test.


Where many tools require an organization to adjust their process, T-Reqs aims to integrate into a particular organization's large-scale agile way of working.  
It supports proven solutions for requirements challenges in large-scale agile, for example updating system requirements based on using gerrit to review changes proposed by agile teams.

T-Reqs is currently in industrial use and based on its success, we are exploring whether providing its key concepts and infrastructure as open source is valuable. 
Regardless, we hope our experience helps to trigger a dialogue on how the changing landscape of requirements engineering in relation to agile system and software development affects needs for tooling support.

## About this project

T-Reqs is a living tool. Based on scripts, it integrates git and related tools into a powerful solution to support agile teams at scale. 
In this project, we give a minimal, working example based on gerrit and github.
Our scripts and setup may be reusable, e.g. through forking our project and using it to manage requirements. 
But generally, we assume that an organization may use this project as a template for their own setup. 
We have not tried, but are confident that for example instead of a gerrit-based flow, a pull-based flow may be used.
 
### Requirements

  Python 3.x


## Getting started

### Installation

Clone this repo, then from the root of repo directory, run

    pip install -e .

### Running scripts on example requirements

    treqs 


### Running test cases for the treqs package

    ./run_tests.sh

## Project structure

  - __requirements__ This folder contains a working example of requirements for T-Reqs, which we manage in T-Reqs. 
In many large-scale agile organizations, requirements originate from a different tool. 
To demo this situation, we maintain high-level use cases on github as issues. 
Replace these requirements with your own requirements.
  - __templates__ This folder contains templates that indicate the syntax for requirement and test ids that our scripts rely on.
Adjust these requirements to fit your context.
  - __tests__ This folder contains manual and automatic tests for T-Reqs. 
It also demonstrates how tests and requirements can be linked and managed together in git.
  - __treqs__ This folder contains scripts, e.g. to check if any user stories on github are not linked to from requirements, or if all requirements are covered by tests. 

T-Reqs combines these things together and encourages each part to evolve as you develop software. 
I.e. the scripts and templates should be evolved and adjusted to your organization's needs by the people that use them: The agile teams.


## Minimal setup
The minimal setup (as provided by the folders in this project) is as follows.
 
* An .md file containing requirements simulates system requirements. For instance, the following text would represent a single requirement with id REQ1 that has traces to user stories US1 and US2:

	```
	Some supplementary text
	[requirement id=REQ1 story=US1,US2]
	Requirement text
	[/requirement]
	More supplementary text
	```
* A test case file with test cases. Test cases can be markdown files (for manual test routines) or source files (here: python) (for automated test scripts). An example for a manual test case and a python test case are depicted below. In both cases, the [testcase] tag contains a test case id as well as tracing information to user stories and system requirements.

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

## Usage

    Usage:
      treqs [-u DIR] [-s DIR] [-t DIR] [--uspattern PATTERN] [--srpattern PATTERN] [--tcpattern PATTERN] [-r] [-q]

    Options:
      -u           directory to search for user stories [default: requirements/]
      -s           directory to search for system requirements [default: requirements/]
      -s           directory to search for test cases [default: tests/]
      --uspattern  pattern to match user story file names [default: US_.*?\.md]
      --srpattern  pattern to match system requirement file names [default: SR_.*?\.md]
      --tcpattern  pattern to match test file names [default: TC_.*?(\.py|\..md)]
      -r           traverse directories recursively
      -q           quiet; suppress console output

The treqs command produces a markdown log file (Summary_\*) in the logs folder (scripts/logs). 


## Further reading:
- [Requirements Challenges in Large-Scale Agile](https://oerich.wordpress.com/2017/06/28/re-for-large-scale-agile-system-development/)
- [T-Reqs: Key idea and User Stories](https://arxiv.org/abs/1805.02769)
