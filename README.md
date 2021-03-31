
![action](https://github.com/JackWolf24/ithilfe/actions/workflows/python-app.yml/badge.svg) ![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/JackWolf24/5dfef24b289a9890e7d579140ca0ae15/raw/test.json)


Ithilfe is a simple program to help a It Department keeping track of devices in house. 

Available as console or gui app (check out corresponding branches). 

## disclaimer
The content of this readme focuses on Windows(win 10 tested only). 

Latest docs and exe can be found in artifacts of last ci run.

## dependencies
- python 3.7 https://www.python.org/downloads/release/python-379/
- git installed https://git-scm.com/downloads
- pip installed https://pip.pypa.io/en/stable/installing/
- content of requirements.txt

## installation 
on https://github.com/JackWolf24/ithilfe choose a version (different branches)

`git clone --single-branch --branch <branchname> https://github.com/JackWolf24/ithilfe.git`


in your terminal:

  ```
  git clone https://github.com/JackWolf24/ithilfe.git
  ```
  
  cd in repo
  
  ```
  pip install -r requirements.txt
  ```
  
## usage
in your terminal:
  cd into a directory where it_hilfe is located
  
  if cloned main branch:
  
  ```
  pyhton it_hilfe_gui2.py
  ```
  
  else a file that starts with it_hilfe.py:
  
  ```
  python <a file that starts with it_hilfe>.py
  ```
  
  The programs itself are self-explanatory. 
  
## build exe

  cd into ithilfe/
  
  ```
  pyinstaller it_hilfe.spec
  ```
  
  after process beeing finished, the exe file is located in 
  
  ```
  ithilfe/dist
  ```
  
  the latest exe ci built can be found: 
  ```
  actions/Ci/<last workfolwrun> 
  ```
  scroll down to find artifacts
  
## generate latest documentation as html

  cd into ithilfe/docs
  
  ```
  make <Builder>
  ```
  
  This will update the docs according to existing docstrings. The file can be found in:
  
  ```
  it_hilfe/docs/_build/<Builder>
  ```
  
  Available builders can be found at https://www.sphinx-doc.org/en/master/man/sphinx-build.html
  
  Most common is html

  
  the latest ci built docs can be found: 
  ```
  actions/Ci/<last workfolwrun> 
  ```
  scroll down to find artifacts
  
