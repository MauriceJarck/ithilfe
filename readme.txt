
![action](https://github.com/JackWolf24/ithilfe/actions/workflows/python-app.yml/badge.svg)
# ithilfe
## description
Ithilfe is a simple programm to help a It Department keeping track of devices in house. 
Available as console or gui app (check out corresponding branches). 

## dependencies
- this readme is only tested with win 10 latest and python 3.7 https://www.python.org/downloads/release/python-379/
- git installed https://git-scm.com/downloads
- pip installed https://pip.pypa.io/en/stable/installing/
- content of requirements.txt

## installation 
on https://github.com/JackWolf24/ithilfe choose version (different branches = branchname)
`git clone --single-branch --branch <branchname> https://github.com/JackWolf24/ithilfe.git`

or if you choose main branch just
`git clone https://github.com/JackWolf24/ithilfe.git`


in your terminal:
  `git clone https://github.com/JackWolf24/ithilfe.git`
  cd in repo
  `pip instal -r requirements.txt`
  
## usage
in your terminal:
  cd into directory where it_hilfe is installed
  ```cd it_hilfe
  
  if cloned main branch:
  
  pyhton it_hilfe_gui2_logic
  
  
  else a file that starts with it_hilfe.py:
  
  python <a file that starts with it_hilfe>.py
  ```
  the programs itselfs are self-explanatory
  
## build exe

  cd into ithilfe/it_hilfe
  
  `PyInstaller --noconsole --onefile --icon "..data/favicon.ico" <fileSupposedToBeConverted>.py`
  
  after process beeing finished, the exe file is in ithilfe/dist
  

## generate latest docmentation as html

  cd into ithilfe/docs
  
  `make html`
