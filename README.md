# T-Reqs: Tool Support for Managing Requirements in Large-Scale Agile System Development

Requirements engineering is crucial to support agile development of large systems with long lifetimes. 
Agile cross-functional teams must be aware of requirements at system level and able to efficiently propose updates to those requirements. 

T-Reqs' objective is to offer lightweight tooling to manage requirements in large-scale agile system development.
It supports proven solutions for many known requirements challenges in large-scale agile, for example updating system requirements based on using gerrit to review changes proposed by agile teams.

T-Reqs is currently in industrial use and based on its success, we are exploring whether providing its key concepts and infrastructure as open source is valuable. 
Regardless, we hope our experience helps to trigger a dialogue on how the changing landscape of requirements engineering in relation to agile system and software development affects needs for tooling support.

Further reading:
- [Requirements Challenges in Large-Scale Agile](https://oerich.wordpress.com/2017/06/28/re-for-large-scale-agile-system-development/)
- [T-Reqs: Key idea and User Stories](https://arxiv.org/abs/1805.02769)

## Requirements

  Python 3.x

## Running test cases for the treqs package

From root of the treqs git repo directory, run

    pip install -e .
    ./run_tests.sh

