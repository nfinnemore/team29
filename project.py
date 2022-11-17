# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template
from flask import request
from flask import redirect, url_for 

app = Flask(__name__)     # create an app

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
a_user = {'name' : 'Geoffrey', 'email' : 'gcloud@uncc.edu'}
projects = { 1: {'title' : 'My Project', 'text' : 'This is a description', 'deadline' : '11/15/22'},
            2: {'title' : 'My Project2', 'text' : 'This is a description', 'deadline' : '11/16/22'},
            3: {'title' : 'My Project3', 'text' : 'This is a description', 'deadline' : '11/17/22'} }

# Home link
@app.route('/')
@app.route('/index')
def index():
   return render_template('index.html', user = a_user)

# View all projects link
@app.route('/projects')
def get_projects():

    return render_template('projects.html', user=a_user, projects=projects)

# View single project link
@app.route('/projects/<project_id>')
def get_project(project_id):

   return render_template('project.html', user=a_user, project = projects[int(project_id)])

# Add new project link
@app.route('/projects/new', methods=['GET', 'POST'])
def new_project():
    # Check method used for request
    if request.method == 'POST':
        # get title data
        title = request.form['title']
        # get project data
        text = request.form['projectText']
        # get deadline data
        deadline = request.form['deadline']
        # get the last ID used and increment by 1
        id = len(projects)+1
        #create new project entry
        projects[id] = {'title' : title, 'text' : text, 'deadline' : deadline}
        # ready to render response - redirect to projects view
        return redirect(url_for('get_projects'))
    else:
        # Get request - show new note form
        return render_template('new.html', user=a_user)
    

app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000