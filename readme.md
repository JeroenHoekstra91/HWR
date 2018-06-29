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
* MATLAB R2018a
* [MATLAB Engine API for Python](https://nl.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html)

**adding dependencies:**

To add a new dependencies:

* run `pip install <package>`
* run `pip freeze > requirements.txt`

The first command will install the desired package, while the second updates the requirements.txt file.

**removing a dependency:**

To remove an installed dependency:

* run `pip uninstall <package>`
* run `pip freeze > requirements.txt`

The first command will uninstall the desired package, while the second updates the requirements.txt file.

**installing MATLAB Engine API for Python:**

* Make sure the virtual environment is activated: `source venv/bin/activate`

* run `cd [Matlab installation directory]/extern/engines/python`

* run `sudo python setup.py install`

**running the pipeline:**

From the project root directory:

* run `python pipeline.py [input directory] [output directory]`

This will segment the words for each of the images in the input directory. It will create a directory under output directory path for each of the images in the input directory named after the image name. In the generated folders, the images with the detected words will be stored.

Only grayscale images are supported. If a color image is found in the input directory, it will be converted to grayscale. Word segmentation is computationally expensive, a run for a single image take around 4 minutes.