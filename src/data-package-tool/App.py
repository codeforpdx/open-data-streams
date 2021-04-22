from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import Form, StringField, SubmitField, TextAreaField, validators
from pymongo import MongoClient
import os, io
#import os.path
import json
# will need to externally config this later
datalakepath = '../../datalake/'
dcatMeta = dict([
    ('conformsTo','https://project-open-data.cio.gov/v1.1/schema/'),

    ])
if not os.path.exists(datalakepath):
    os.mkdir(datalakepath);

client = MongoClient()
db = client.openData

DEBUG=True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class dataPackageForm(Form):
    name = StringField('name',[validators.required()])
    title = StringField('title',[validators.required()])
    homepage = StringField('title',[])
    description = TextAreaField('description',[])
    submit = StringField('submit')

@app.route('/', methods=['GET', 'POST'])
def data_package():
    form = dataPackageForm(request.form)
    if request.method == 'POST':
        name=request.form['name']
        title = request.form['title']
        homepage = request.form['homepage']
        # keyword = request.form['keywords']
        # modified = request.form['modified']
        # publisher= request.form['publisher']
        # contactPoint= request.form['contactPoint']
        # identifier= request.form['identifier']
        # accessLevel= request.form['accessLevel']
        # bureau= request.form['bureau']
        # license= request.form['license']
    if form.validate():
        # Save the comment here.
        print('Processing Data')
        processFormData(request.form)
    else:
        flash('All the form fields are required. ')
    
    return render_template('datapackage.html', form=form)

def processFormData(formData):
    dcatMeta = dict([
        ('conformsTo','https://project-open-data.cio.gov/v1.1/schema/'),
        ('describedBy','blah blah blah')
        ])
    keyword = formData['keyword'].split(', ')
    dcatMeta["dataset"] = dict(formData)
    dcatMeta["dataset"]["keyword"] = keyword
    dcatMeta["dataset"]["@type"] = "dcat:Dataset"


    f = io.StringIO()
    json.dump(dcatMeta,fp=f, indent=4)
    print(f.getvalue())
# create project directory and files
# will need to externally config this later
    datalakepath = '../../source-data'
    if not os.path.exists(datalakepath):
        os.mkdir(datalakepath)
    workingPath=datalakepath+formData["name"]
    if not os.path.exists(workingPath):
        os.mkdir(workingPath);
        os.mkdir(workingPath +"/scripts")
    os.system('cp ' + formData["file"] + ' ' + workingPath)
    fp = open(workingPath+"/DCAT1.1.json","w")
    json.dump(dcatMeta,fp,indent=4)

#     workingPath=datalakepath+name+'/'
#     if not os.path.exists(workingPath):
#         os.mkdir(workingPath);
#         f = open(workingPath+"DCAT1.1.json","w")
#         formData = {
#             "name":name,
#             "title":title,
#             "homepage":homepage
#             }
#         dcatContent[dataset]=formData
#  #       json.dump({"name":name, "title":title, "homepage":homepage},f, indent=4)
#  #       json.dump(dcatContent,f,indent=4)
#         print(dcatContent)