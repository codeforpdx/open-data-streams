# Code For PDX Open Stream Data Package Tool

This tool takes meta data from the user about a proposed PDX Open Stream dataset and produces the datapackage.json with accompanying artifacts. The tool creates a work area, currently in https://github.com/codeforpdx/open-data-streams/tree/main/source-data/<project_name>. <project_name> is derived from the name field in the apps form data.

A DCAT meta datafile called DCAT1.1.json  is generated from the form data and written https://github.com/codeforpdx/open-data-streams/tree/main/source-data/<project_name>. Finally the original dataset file, and an empty scripts directory. Any scripts developed to alter the original dataset in any way should be stored in the scripts directory. 

To launch the tool use the following command from the data-package-tool directory on your local machine
python -m flask run. The user interface is available at http://localhost:5000 with your browser.
