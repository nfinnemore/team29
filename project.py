# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template
from flask import request
from flask import redirect, url_for
from database import db
from models import Project as Project
from models import User as User
from forms import RegisterForm
from flask import session
import bcrypt

app = Flask(__name__)     # create an app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SECRET_KEY'] = 'SE3155'

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
    # retreive user from data base
    # check if a user is saved in session
    if(session.get('user')):
        # retrieve projects from database
        projects = db.session.query(Project).filter_by(user_id=session['user_id'].all)
        
        return render_template('projects.html', projects = projects, user=session['user'])
    else:
        return render_template(url_for('login'))

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

# edit project
@app.route('/projects/edit/<project_id>', methods=['GET', 'POST'])
def update_project(project_id):
    # check method used for request
    if request.method == 'POST':
        # get title data
        title = request.form['title']
        # get text data
        text = request.form['projectText']
        # get deadline data
        deadline = request.form['deadline']
        project = db.session.query(Project).filter_by(id=project_id).one()
        # update project data
        project.title = title
        project.text = text
        project.deadline = deadline
        # update project in DB
        db.session.add(project)
        db.session.commit()

        return redirect(url_for('get_projects'))
    
    else:
        # GET request - show new project form to edit note
        # retrieve user from database
        a_user = db.session.query(User).filter_by(email='gcloud@uncc.edu').one()
        #retrieve note from database
        my_project = db.session.query(Project).filter_by(id=project_id).one()

        return render_template('new.html', project=my_project, user=a_user)

@app.route('/projects/delete/<project_id>', methods=['POST'])
def delete_project(project_id):
    my_project = db.session.query(Project).filter_by(id=project_id).one()
    db.session.delete(my_project)
    db.session.commit()

    return redirect(url_for('get_projects'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        # salt and hash password
        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        # get entered user data
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        # create user model
        new_user = User(first_name, last_name, request.form['email'], h_password)
        # add user to database and commit
        db.session.add(new_user)
        db.session.commit()
        # save the user's name to the session
        session['user'] = first_name
        session['user_id'] = new_user.id  # access id value from user model of this newly added user
        # show user dashboard view
        return redirect(url_for('get_notes'))

    # something went wrong - display register view
    return render_template('register.html', form=form)


app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000