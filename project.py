# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template
from flask import request
from flask import redirect, url_for
from database import db
from models import Project as Project
from models import User as User

app = Flask(__name__)     # create an app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db.init_app(app)
# Setup models
with app.app_context():
    db.create_all() 

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
# Home link
@app.route('/')
@app.route('/index')
def index():
    a_user = db.session.query(User).filter_by(email='gcloud@uncc.edu').one()
    return render_template('index.html', user = a_user)

# View all projects link
@app.route('/projects')
def get_projects():
    a_user = db.session.query(User).filter_by(email='gcloud@uncc.edu').one()
    projects = db.session.query(Project).all()
    return render_template('projects.html', projects = projects, user=a_user)

# View single project link
@app.route('/projects/<project_id>')
def get_project(project_id):
    a_user = db.session.query(User).filter_by(email='gcloud@uncc.edu').one()
    project = db.session.query(Project).filter_by(id=project_id)
    return render_template('project.html', user=a_user, project = project[int(0)])

# Add new project link
@app.route('/projects/new', methods=['GET', 'POST'])
def new_project():
    # Check method used for request
    if request.method =='POST':
        a_user = db.session.query(User).filter_by(email='gcloud@uncc.edu').one()
        title = request.form['title']
        text = request.form['projectText']
        deadline = request.form['deadline']
        from datetime import date
        today = date.today()
            
        today = today.strftime("%m-%d-%Y")
        new_record = Project(title, text, deadline, a_user.id)
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('get_project', project_id=new_record.id))
    else:
        a_user = db.session.query(User).filter_by(email='gcloud@uncc.edu').one()
        return render_template('new.html', user=a_user)
    

app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000