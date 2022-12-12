from database import db
import datetime

class Project(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(200))
    text = db.Column("text", db.String(100))
    deadline = db.Column("deadline", db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    comments = db.relationship("Comment", backref="project", cascade = "all, delete-orphan", lazy=True)
    
    def __init__(self, title, text, deadline, user_id):
        self.title = title
        self.text = text
        self.deadline = deadline
        self.user_id = user_id

# Added phone field
class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    first_name = db.Column("first_name", db.String(30))
    last_name = db.Column("last_name", db.String(30))
    email = db.Column("email", db.String(100))
    phone = db.Column("phone", db.String(10))
    name = db.Column("name", db.String(20))
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    project = db.relationship("Project", backref="user", lazy=True)
    comments = db.relationship("Comment", backref="user", lazy=True)

    def __init__(self, first_name, last_name, email, phone, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.password = password
        self.registered_on = datetime.date.today()

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.VARCHAR, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, content, project_id, user_id):
        self.date_posted = datetime.date.today()
        self.content = content
        self.project_id = project_id
        self.user_id = user_id