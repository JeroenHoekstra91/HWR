Handwriting Recognition
=====================

**What it is:**

Python application for optical character recognition of characters from the dead sea scrolls. 

**Setup:**

* make sure you have Python 2.7.x. installed.
* [install pip](http://pip.readthedocs.org/en/latest/installing.html) for automatically installing dependencies.
* Make sure you have virtualenv installed (`pip install virtualenv`)
* run `virtualenv --python=python2.7 venv`
* run `source venv/bin/activate`
* run `pip install -r requirements.txt`

**requirements:**

* [Python](https://www.python.org/) 2.7.x.
* [pip](http://www.pip-installer.org)
* virtualenv

**adding dependencies:**

To add a new dependencies:

* run `pip install <package>`
* run `pip freeze > requirements.txt`

The first command will install the desired package, while the second updates the requirements.txt file.
