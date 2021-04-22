# Code For PDX Open Stream Data Package Tool

This tool takes meta data from the user about a proposed PDX Open Stream dataset and produce the datapackage.json. In addition it creates a work area in the the local github repository, and populate it with a dcat1.1 meta data file, the original dataset file, and an empty scripts directory. Any scripts develed to alter the original dataset in any way should be stored in the scripts directory. 

To launch the tool use the following comand from the data-package-tool directory on your local machine
python -m flask run

The user interface is available at localhost:5000 with your browser.
