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

### high-level user requirements
We aim for using Github issues as work packages/user stories/etc. In the example below we use “#1” to refer to https://github.com/regot-chalmers/treqs/issues/1 .
 
## Template
Regarding the minimal template, I would say
 
A .md file containing requirements:
 
Some supplementary text
<requirement id=”REQ1” issue=”#1”>
Requirement text
</requirement>
More supplementary text
 
A test case file with test cases. Now, there are a thousand ways of writing test cases. We encode the needed metadata in a docstring:
 
//*=================================
//test case: TC1__test_case_name
//
//Purpose of the test case
//
//#Feature#
//    #1
//
//#Requirement#
//    REQ1
//
//=================================
testcase TC1__test_case_name() {
...
}
 
There are probably more modern and better formats; this is close to the industrial application case.
 

## Scripts to include
Scripts for verifying the tracing, e.g. verifying you haven’t traced your test case to a requirement that does not exist.
A CI test runner running those scripts for every commit. https://travis-ci.org/ is a popular choice.
 
