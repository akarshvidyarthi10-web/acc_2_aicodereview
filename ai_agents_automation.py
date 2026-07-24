import uuid
import datetime
import random
import string
import threading
import time
import json

class BaseAgent:
    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name
        self.created_at = datetime.datetime.now()
    def run(self, *args, **kwargs):
        raise NotImplementedError

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
    def __init__(self, filename="agents.json"):
        self.filename = filename
        self.data = {"users": [], "projects": [], "tasks": [], "logs": []}
    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=2)
    def load(self):
        try:
            with open(self.filename, "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {"users": [], "projects": [], "tasks": [], "logs": []}
    def log(self, entry):
        self.data["logs"].append({"time": str(datetime.datetime.now()), "entry": entry})
        self.save()

class SchedulerAgent(BaseAgent):
    def __init__(self):
        super().__init__("SchedulerAgent")
        self.jobs = []
    def run(self, func, delay):
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

class NotificationAgent(BaseAgent):
    def __init__(self):
        super().__init__("NotificationAgent")
        self.sent = []
    def run(self, user, message):
        note = {"user": user.username, "email": user.email, "message": message, "time": str(datetime.datetime.now())}
        self.sent.append(note)
        return note
    def history(self):
        return self.sent

class ReportingAgent(BaseAgent):
    def __init__(self, db):
        super().__init__("ReportingAgent")
        self.db = db
    def run(self):
        return {"users": self.db.data["users"], "projects": self.db.data["projects"], "tasks": self.db.data["tasks"], "logs": self.db.data["logs"]}

class AnomalyAgent(BaseAgent):
    def __init__(self, db):
        super().__init__("AnomalyAgent")
        self.db = db
    def run(self):
        anomalies = []
        now = datetime.datetime.now()
        for t in self.db.data["tasks"]:
            deadline = datetime.datetime.fromisoformat(t["deadline"])
            if t["status"] == "Pending" and deadline < now:
                anomalies.append({"task": t["title"], "assignee": t["assignee"], "issue": "Missed deadline"})
        return anomalies

class WorkflowAgent(BaseAgent):
    def __init__(self, db, scheduler, notifier, reporter, anomaly):
        super().__init__("WorkflowAgent")
        self.db = db
        self.scheduler = scheduler
        self.notifier = notifier
        self.reporter = reporter
        self.anomaly = anomaly
    def run(self):
        anomalies = self.anomaly.run()
        for a in anomalies:
            user = next((u for u in self.db.data["users"] if u["username"] == a["assignee"]), None)
            if user:
                self.notifier.run(User(user["username"], user["email"]), f"Task {a['task']} has missed deadline")
        return self.reporter.run()

class AutomationEngine:
    def __init__(self):
        self.db = Database()
        self.db.load()
        self.scheduler = SchedulerAgent()
        self.notifier = NotificationAgent()
        self.reporter = ReportingAgent(self.db)
        self.anomaly = AnomalyAgent(self.db)
        self.workflow = WorkflowAgent(self.db, self.scheduler, self.notifier, self.reporter, self.anomaly)
    def create_user(self, username, email):
        user = User(username, email)
        self.db.data["users"].append(user.to_dict())
        self.db.save()
        return user
    def create_project(self, name, owner):
        project = Project(name, owner)
        self.db.data["projects"].append(project.to_dict())
        self.db.save()
        return project
    def create_task(self, project, title, description, assignee, deadline):
        task = Task(title, description, assignee, deadline)
        project.add_task(task)
        self.db.data["tasks"].append(task.to_dict())
        self.db.save()
        return task
    def complete_task(self, task_id):
        for t in self.db.data["tasks"]:
            if t["id"] == task_id:
                t["status"] = "Completed"
        self.db.save()
    def run_workflow(self):
        return self.workflow.run()

def random_string(length=8):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def demo():
    engine = AutomationEngine()
    u1 = engine.create_user("akarsh", "akarsh@example.com")
    u2 = engine.create_user("vidyarthi", "vidyarthi@example.com")
    p1 = engine.create_project("AI Agents Automation", u1)
    t1 = engine.create_task(p1, "Build Core", "Develop automation core", u1, datetime.datetime.now() + datetime.timedelta(seconds=3))
    t2 = engine.create_task(p1, "Test Agents", "Run agent tests", u2, datetime.datetime.now() - datetime.timedelta(days=1))
    engine.complete_task(t1.id)
    engine.scheduler.run(lambda: engine.workflow.run(), 2)
    time.sleep(4)
    print("Reports:", engine.reporter.run())
    print("Notifications:", engine.notifier.history())
    print("Anomalies:", engine.anomaly.run())

if __name__ == "__main__":
    demo()
class BaseAgent:
    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name
        self.created_at = datetime.datetime.now()
    def run(self, *args, **kwargs):
        raise NotImplementedError

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
    def __init__(self, filename="agents.json"):
        self.filename = filename
        self.data = {"users": [], "projects": [], "tasks": [], "logs": []}
    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=2)
    def load(self):
        try:
            with open(self.filename, "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {"users": [], "projects": [], "tasks": [], "logs": []}
    def log(self, entry):
        self.data["logs"].append({"time": str(datetime.datetime.now()), "entry": entry})
        self.save()

class SchedulerAgent(BaseAgent):
    def __init__(self):
        super().__init__("SchedulerAgent")
        self.jobs = []
    def run(self, func, delay):
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

class NotificationAgent(BaseAgent):
    def __init__(self):
        super().__init__("NotificationAgent")
        self.sent = []
    def run(self, user, message):
        note = {"user": user.username, "email": user.email, "message": message, "time": str(datetime.datetime.now())}
        self.sent.append(note)
        return note
    def history(self):
        return self.sent

class ReportingAgent(BaseAgent):
    def __init__(self, db):
        super().__init__("ReportingAgent")
        self.db = db
    def run(self):
        return {"users": self.db.data["users"], "projects": self.db.data["projects"], "tasks": self.db.data["tasks"], "logs": self.db.data["logs"]}

class AnomalyAgent(BaseAgent):
    def __init__(self, db):
        super().__init__("AnomalyAgent")
        self.db = db
    def run(self):
        anomalies = []
        now = datetime.datetime.now()
        for t in self.db.data["tasks"]:
            deadline = datetime.datetime.fromisoformat(t["deadline"])
            if t["status"] == "Pending" and deadline < now:
                anomalies.append({"task": t["title"], "assignee": t["assignee"], "issue": "Missed deadline"})
        return anomalies

class WorkflowAgent(BaseAgent):
    def __init__(self, db, scheduler, notifier, reporter, anomaly):
        super().__init__("WorkflowAgent")
        self.db = db
        self.scheduler = scheduler
        self.notifier = notifier
        self.reporter = reporter
        self.anomaly = anomaly
    def run(self):
        anomalies = self.anomaly.run()
        for a in anomalies:
            user = next((u for u in self.db.data["users"] if u["username"] == a["assignee"]), None)
            if user:
                self.notifier.run(User(user["username"], user["email"]), f"Task {a['task']} has missed deadline")
        return self.reporter.run()

class AutomationEngine:
    def __init__(self):
        self.db = Database()
        self.db.load()
        self.scheduler = SchedulerAgent()
        self.notifier = NotificationAgent()
        self.reporter = ReportingAgent(self.db)
        self.anomaly = AnomalyAgent(self.db)
        self.workflow = WorkflowAgent(self.db, self.scheduler, self.notifier, self.reporter, self.anomaly)
    def create_user(self, username, email):
        user = User(username, email)
        self.db.data["users"].append(user.to_dict())
        self.db.save()
        return user
    def create_project(self, name, owner):
        project = Project(name, owner)
        self.db.data["projects"].append(project.to_dict())
        self.db.save()
        return project
    def create_task(self, project, title, description, assignee, deadline):
        task = Task(title, description, assignee, deadline)
        project.add_task(task)
        self.db.data["tasks"].append(task.to_dict())
        self.db.save()
        return task
    def complete_task(self, task_id):
        for t in self.db.data["tasks"]:
            if t["id"] == task_id:
                t["status"] = "Completed"
        self.db.save()
    def run_workflow(self):
        return self.workflow.run()

def random_string(length=8):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def cli():
    engine = AutomationEngine()
    while True:
        print("\nAI Agents Automation CLI")
        print("1. Create User")
        print("2. Create Project")
        print("3. Create Task")
        print("4. Complete Task")
        print("5. Run Workflow")
        print("6. Show Reports")
        print("7. Show Notifications")
        print("8. Show Anomalies")
        print("9. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            u = engine.create_user(input("Username: "), input("Email: "))
            print("User created:", u.to_dict())
        elif choice == "2":
            uname = input("Owner username: ")
            owner = next((User(u["username"], u["email"]) for u in engine.db.data["users"] if u["username"] == uname), None)
            if owner:
                p = engine.create_project(input("Project name: "), owner)
                print("Project created:", p.to_dict())
        elif choice == "3":
            pname = input("Project name: ")
            project = next((Project(p["name"], User(p["owner"], "owner@example.com")) for p in engine.db.data["projects"] if p["name"] == pname), None)
            aname = input("Assignee username: ")
            assignee = next((User(u["username"], u["email"]) for u in engine.db.data["users"] if u["username"] == aname), None)
            if project and assignee:
                t = engine.create_task(project, input("Title: "), input("Description: "), assignee, datetime.datetime.now() + datetime.timedelta(days=2))
                print("Task created:", t.to_dict())
        elif choice == "4":
            tid = input("Task ID: ")
            engine.complete_task(tid)
            print("Task completed")
        elif choice == "5":
            print("Workflow run:", engine.run_workflow())
        elif choice == "6":
            print("Reports:", engine.reporter.run())
        elif choice == "7":
            print("Notifications:", engine.notifier.history())
        elif choice == "8":
            print("Anomalies:", engine.anomaly.run())
        elif choice == "9":
            break

if __name__ == "__main__":
    cli()
