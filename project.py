# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template

app = Flask(__name__)     # create an app

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
a_user = {'name' : 'Geoffrey', 'email' : 'gcloud@uncc.edu'}
a_note = { 1: {'title' : 'My Project', 'text' : 'This is a description', 'date' : '11/15/22'},
            2: {'title' : 'My Project2', 'text' : 'This is a description', 'date' : '11/16/22'},
            3: {'title' : 'My Project3', 'text' : 'This is a description', 'date' : '11/17/22'} }

# Home link
@app.route('/')
@app.route('/index')
def index():
   return render_template('index.html', user = a_user)

# View all projects link
@app.route('/projects')
def get_projects():

    return render_template('projects.html', user=a_user, note=a_note)

# View single project link
@app.route('/project')
def get_project():
   return render_template('project.html', user=a_user, note = a_note)

@app.route('/new')
def new_note():
    return render_template('new.html', user=a_user, note=a_note)
    

app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000