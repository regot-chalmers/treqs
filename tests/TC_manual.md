# Manual test cases 

## [testcase id=TC2 story=US6 req=REQ6]

Purpose: Test that a user story can be created in GitHub

### Setup


### Scenario / Steps

1. Go to https://github.com/regot-chalmers/treqs/issues
2. Press the New issue button
3. Select User story
4. Fill in the template
5. Press the Submit new issue button
6. Run "treqs"

### Expected outcome

1. The new user story is listed on https://github.com/regot-chalmers/treqs/issues
2. The new user story is listed in the file logs/US...

### Tear down

1. Go to the issue page for the newly created issue
2. Press Edit
3. Press Close issue

### Test result

Protocol of the result of executing this test, latest on top.



## [testcase id=TC3 story=US1a,US1b,US1c,US2,US4 req=REQ7,REQ9,REQ10]

Purpose: Editing a system requirement and putting the change up for review

### Setup


### Scenario / Steps

1. Make a change to a file containing requirements with a text editor
2. Run "treqs" 
3. Run "git add FILE"
4. Run "git commit -m 'test'"
5. Run "git push origin HEAD:refs/for/master" to push the commit to Gerrit
6. Go to https://review.gerrithub.io/dashboard/self
7. Click the new change
8. Add a reviewer (note: this can be either a developer (US1b), a system manager (US2,US4) or a test architect(US4))
9. Have that reviewer +2 the change
10. Submit the change

### Expected outcome

1. No errors are listed in the file logs/Summary...
2. The requirement file has been updated on https://github.com/regot-chalmers/treqs

### Tear down

1. Run "git log" and find the commit hash of the latest commit
2. Run "git revert HASH"
3. Push the new commit to Gerrit and submit it like above 

### Test result

Protocol of the result of executing this test, latest on top.



## [testcase id=TC4 story=US3 req=REQ8]

Purpose: Creating a new requirement on a branch

### Setup


### Scenario / Steps

1. Go to the root of the treqs repo
2. Run "git checkout -b experimentalbranch" to create a new branch and switch to it 
3. Create a new requirements file requirements/SR-temp.md
4. Add "[requirement id=REQtemp story=UStemp]" to the file and save
5. Run "git add requirements/SR-temp.md"
6. Run "git commit -m 'my message'"

### Expected outcome

1. After running "treqs" on the new branch, the new requirement is listed in logs/SysReq...
2. A running "treqs" on the master branch, the new requirement is not listed in logs/SysReq...

### Tear down

1. Run "git checkout master"
2. Run "git branch -D experimentalbranch"

### Test result

Protocol of the result of executing this test, latest on top.

