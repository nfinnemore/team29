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
from forms import LoginForm
from models import Comment as Comment
from forms import RegisterForm, LoginForm, CommentForm

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
    if session.get('user'):
        return render_template('index.html', user = session['user'])
    return render_template("index.html")

# View your projects link
@app.route('/projects')
def get_projects():
    # retreive user from data base
    # check if a user is saved in session
    if(session.get('user')):
        # retrieve projects from database
        projects = db.session.query(Project).filter_by(user_id=session['user_id']).all()
        
        return render_template('projects.html', projects = projects, user=session['user'])
    else:
        return redirect(url_for('login'))

# View single project link
@app.route('/projects/<project_id>')
def get_project(project_id):
    if session.get('user'):
        project = db.session.query(Project).filter_by(id=project_id, user_id=session['user_id']).one()
        form=CommentForm()
        return render_template('project.html', project=project, user=session['user_id'], form=form)
    else:
        return redirect(url_for('login'))

# Add new project link
@app.route('/projects/new', methods=['GET', 'POST'])
def new_project():
    # Check method used for request
    if session.get('user'):
        if request.method =='POST':
            title = request.form['title']
            text = request.form['projectText']
            deadline = request.form['deadline']
            from datetime import date
            today = date.today()
            today = today.strftime("%m-%d-%Y")
            new_record = Project(title, text, deadline, session['user_id'])
            db.session.add(new_record)
            db.session.commit()
            return redirect(url_for('get_project', project_id=new_record.id))
        else:
            return render_template('new.html', user=session['user'])
    else:
        return redirect(url_for('login'))

# edit project
@app.route('/projects/edit/<project_id>', methods=['GET', 'POST'])
def update_project(project_id):
    if session.get('user'):
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
            project = db.session.query(Project).filter_by(id=project_id).one()
            return render_template('new.html', project=project, user=session['user'])
    else:
        return redirect(url_for('login'))

@app.route('/projects/delete/<project_id>', methods=['POST'])
def delete_project(project_id):
    if session.get('user'):
        my_project = db.session.query(Project).filter_by(id=project_id).one()
        db.session.delete(my_project)
        db.session.commit()
        return redirect(url_for('get_projects'))
    else:
        return redirect(url_for('login'))

# New feature in register: phone is a new field for when registering
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
        phone = request.form['phone']
        # create user model
        new_user = User(first_name, last_name, request.form['email'], phone, h_password)
        # add user to database and commit
        db.session.add(new_user)
        db.session.commit()
        # save the user's name to the session
        session['user'] = first_name
        session['user_id'] = new_user.id  # access id value from user model of this newly added user
        # show user dashboard view
        return redirect(url_for('index'))

    # something went wrong - display register view
    return render_template('register.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    # validate_on_submit only validates using POST
    if login_form.validate_on_submit():
        # we know user exists. We can use one()
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        # user exists check password entered matches stored password
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            # password match add user info to session
            session['user'] = the_user.first_name
            session['user_id'] = the_user.id
            # render view
            return redirect(url_for('index'))

        # password check failed
        # set error message to alert user
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("login.html", form=login_form)
    else:
        # form did not validate or GET request
        return render_template("login.html", form=login_form)

@app.route('/logout')
def logout():
    # check if a user is saved in session
    if session.get('user'):
        session.clear()

    return redirect(url_for('index'))

@app.route('/projects/<project_id>/comment', methods=['POST'])
def new_comment(project_id):
    if session.get('user'):
        comment_form = CommentForm()
        # validate_on_submit only validates using POST
        if comment_form.validate_on_submit():
            # get comment data
            comment_text = request.form['comment']
            new_record = Comment(comment_text, int(project_id), session['user_id'])
            db.session.add(new_record)
            db.session.commit()

        return redirect(url_for('get_project', project_id=project_id))

    else:
        return redirect(url_for('login'))

# New Feature 1: all projects
# View all projects link
@app.route('/all_projects')
def all_projects():
    # if user is logged in, they can see all projects
    if(session.get('user')):
        # retrieve all projects from database
        projects = db.session.query(Project).all()
        
        return render_template('all_projects.html', projects = projects, user=session['user'])
    else:
        return redirect(url_for('login'))

# New Feature 2: View other projects
# View someone's project link
@app.route('/all_projects/<project_id>')
def view_project(project_id):

    if session.get('user'):
        project = db.session.query(Project).filter_by(id=project_id).one()
        return render_template('view_project.html', project=project, user=session['user_id'])
    else:
        return redirect(url_for('login'))
        
# New Feature 3: View account details or perform actions (either change password or delete account)
@app.route('/account')
def view_account():

    if session.get('user'):
        user = db.session.query(User).filter_by(id=session['user_id']).one()
        return render_template('account.html', user=user, user_id=session['user_id'])
    else:
        return redirect(url_for('login'))

# New Feature 4: See all the users in a table to get reference on name, contact email
@app.route('/all_users')
def all_users():
    # retreive user from data base
    # check if a user is saved in session
    if session.get('user'):
        users = db.session.query(User).all()
        
        return render_template('all_users.html', users = users, user=session['user'])
    else:
        return redirect(url_for('login'))

app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000