import json
import uuid
import datetime
import random
import string

class User:
    def __init__(self, username, email):
        self.id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.created_at = datetime.datetime.now()
    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email, "created_at": str(self.created_at)}

class Project:
    def __init__(self, name, owner):
        self.id = str(uuid.uuid4())
        self.name = name
        self.owner = owner
        self.tasks = []
        self.created_at = datetime.datetime.now()
    def add_task(self, task):
        self.tasks.append(task)
    def to_dict(self):
        return {"id": self.id, "name": self.name, "owner": self.owner.username, "tasks": [t.to_dict() for t in self.tasks], "created_at": str(self.created_at)}

class Task:
    def __init__(self, title, description, assignee, deadline):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.assignee = assignee
        self.deadline = deadline
        self.status = "Pending"
        self.created_at = datetime.datetime.now()
    def complete(self):
        self.status = "Completed"
    def to_dict(self):
        return {"id": self.id, "title": self.title, "description": self.description, "assignee": self.assignee.username, "deadline": str(self.deadline), "status": self.status, "created_at": str(self.created_at)}

class Database:
    def __init__(self, filename="data.json"):
        self.filename = filename
        self.data = {"users": [], "projects": []}
    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=2)
    def load(self):
        try:
            with open(self.filename, "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {"users": [], "projects": []}
    def add_user(self, user):
        self.data["users"].append(user.to_dict())
        self.save()
    def add_project(self, project):
        self.data["projects"].append(project.to_dict())
        self.save()
    def list_users(self):
        return self.data["users"]
    def list_projects(self):
        return self.data["projects"]

class ReportGenerator:
    def __init__(self, db):
        self.db = db
    def user_report(self):
        return [{"username": u["username"], "email": u["email"], "created_at": u["created_at"]} for u in self.db.list_users()]
    def project_report(self):
        return [{"name": p["name"], "owner": p["owner"], "task_count": len(p["tasks"])} for p in self.db.list_projects()]
    def task_report(self):
        tasks = []
        for p in self.db.list_projects():
            for t in p["tasks"]:
                tasks.append({"title": t["title"], "assignee": t["assignee"], "status": t["status"], "deadline": t["deadline"]})
        return tasks

class TaskManager:
    def __init__(self):
        self.db = Database()
        self.db.load()
    def create_user(self, username, email):
        user = User(username, email)
        self.db.add_user(user)
        return user
    def create_project(self, name, owner):
        project = Project(name, owner)
        self.db.add_project(project)
        return project
    def create_task(self, project, title, description, assignee, deadline):
        task = Task(title, description, assignee, deadline)
        project.add_task(task)
        self.db.save()
        return task
    def complete_task(self, project, task_id):
        for t in project.tasks:
            if t.id == task_id:
                t.complete()
        self.db.save()

def random_string(length=8):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def demo():
    manager = TaskManager()
    u1 = manager.create_user("akarsh", "akarsh@example.com")
    u2 = manager.create_user("vidyarthi", "vidyarthi@example.com")
    p1 = manager.create_project("AI Research", u1)
    p2 = manager.create_project("Web Development", u2)
    t1 = manager.create_task(p1, "Build Model", "Train AI model", u1, datetime.datetime.now() + datetime.timedelta(days=7))
    t2 = manager.create_task(p1, "Write Paper", "Draft research paper", u2, datetime.datetime.now() + datetime.timedelta(days=14))
    t3 = manager.create_task(p2, "Frontend", "Develop UI", u1, datetime.datetime.now() + datetime.timedelta(days=10))
    t4 = manager.create_task(p2, "Backend", "Setup API", u2, datetime.datetime.now() + datetime.timedelta(days=12))
    manager.complete_task(p1, t1.id)
    manager.complete_task(p2, t3.id)
    report = ReportGenerator(manager.db)
    print(report.user_report())
    print(report.project_report())
    print(report.task_report())

if __name__ == "__main__":
    demo()
