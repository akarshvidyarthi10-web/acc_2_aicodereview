import uuid
import datetime
import random
import string
import json
import threading
import time

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
    def __init__(self, filename="automation.json"):
        self.filename = filename
        self.data = {"users": [], "projects": [], "tasks": []}
    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=2)
    def load(self):
        try:
            with open(self.filename, "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {"users": [], "projects": [], "tasks": []}
    def add_user(self, user):
        self.data["users"].append(user.to_dict())
        self.save()
    def add_project(self, project):
        self.data["projects"].append(project.to_dict())
        self.save()
    def add_task(self, task):
        self.data["tasks"].append(task.to_dict())
        self.save()
    def list_users(self):
        return self.data["users"]
    def list_projects(self):
        return self.data["projects"]
    def list_tasks(self):
        return self.data["tasks"]

class Scheduler:
    def __init__(self):
        self.jobs = []
    def schedule(self, func, delay):
        job_id = str(uuid.uuid4())
        def wrapper():
            time.sleep(delay)
            func()
        t = threading.Thread(target=wrapper)
        t.start()
        self.jobs.append({"id": job_id, "thread": t})
        return job_id
    def list_jobs(self):
        return [j["id"] for j in self.jobs]

class NotificationService:
    def __init__(self):
        self.sent = []
    def send(self, user, message):
        note = {"user": user.username, "email": user.email, "message": message, "time": str(datetime.datetime.now())}
        self.sent.append(note)
        return note
    def history(self):
        return self.sent

class ReportGenerator:
    def __init__(self, db):
        self.db = db
    def user_report(self):
        return [{"username": u["username"], "email": u["email"]} for u in self.db.list_users()]
    def project_report(self):
        return [{"name": p["name"], "owner": p["owner"], "task_count": len(p["tasks"])} for p in self.db.list_projects()]
    def task_report(self):
        return [{"title": t["title"], "assignee": t["assignee"], "status": t["status"], "deadline": t["deadline"]} for t in self.db.list_tasks()]

class AutomationEngine:
    def __init__(self):
        self.db = Database()
        self.db.load()
        self.scheduler = Scheduler()
        self.notifications = NotificationService()
        self.reports = ReportGenerator(self.db)
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
        self.db.add_task(task)
        return task
    def complete_task(self, task_id):
        for t in self.db.data["tasks"]:
            if t["id"] == task_id:
                t["status"] = "Completed"
        self.db.save()
    def notify_deadlines(self):
        now = datetime.datetime.now()
        for t in self.db.data["tasks"]:
            deadline = datetime.datetime.fromisoformat(t["deadline"])
            if t["status"] == "Pending" and deadline < now + datetime.timedelta(days=2):
                user = next((u for u in self.db.data["users"] if u["username"] == t["assignee"]), None)
                if user:
                    self.notifications.send(User(user["username"], user["email"]), f"Task {t['title']} is nearing deadline")
    def run_demo(self):
        u1 = self.create_user("akarsh", "akarsh@example.com")
        u2 = self.create_user("vidyarthi", "vidyarthi@example.com")
        p1 = self.create_project("Automation Core", u1)
        t1 = self.create_task(p1, "Build Engine", "Develop automation engine", u1, datetime.datetime.now() + datetime.timedelta(days=3))
        t2 = self.create_task(p1, "Write Docs", "Prepare documentation", u2, datetime.datetime.now() + datetime.timedelta(days=1))
        self.complete_task(t1.id)
        self.scheduler.schedule(lambda: self.notify_deadlines(), 2)
        print(self.reports.user_report())
        print(self.reports.project_report())
        print(self.reports.task_report())
        print(self.notifications.history())

def random_string(length=8):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

if __name__ == "__main__":
    engine = AutomationEngine()
    engine.run_demo()
