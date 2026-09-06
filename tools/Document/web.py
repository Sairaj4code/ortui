#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Complex web application built with web.py.
Features:
- User registration & login with password hashing
- Session-based authentication
- CRUD operations for tasks (Create, Read, Update, Delete)
- RESTful JSON API for tasks
- Simple HTML templates (inline)
- SQLite database storage
- Basic static file serving

Install dependencies: pip install web.py
Run: python web.py
"""

import web
import hashlib
import json
import os
import time
from web import template

# ----------------------------------------------------------------------
# Database configuration (SQLite)
# ----------------------------------------------------------------------
db = web.database(dbn='sqlite', db='tasks.db')
db.printing = False

# Create tables if they do not exist
db.query('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

db.query('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''')

# ----------------------------------------------------------------------
# URL mappings
# ----------------------------------------------------------------------
urls = (
    '/', 'Index',
    '/login', 'Login',
    '/register', 'Register',
    '/logout', 'Logout',
    '/dashboard', 'Dashboard',
    '/tasks/new', 'NewTask',
    '/tasks/edit/(.*)', 'EditTask',
    '/tasks/delete/(.*)', 'DeleteTask',
    '/api/tasks', 'TasksAPI',
    '/static/(.*)', 'StaticFiles'
)

# ----------------------------------------------------------------------
# Application & Session
# ----------------------------------------------------------------------
app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'))

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def hash_password(password):
    """Return SHA-256 hash of the password."""
    return hashlib.sha256(password.encode()).hexdigest()


def get_user_id():
    """Return the ID of the currently logged-in user or None."""
    if 'user_id' in session:
        return session.user_id
    return None


def html_response(title, body, status=200):
    """Generate a simple HTML page."""
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f4f4f4; }}
        .container {{ max-width: 800px; margin: auto; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; }}
        a {{ color: #007bff; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .form-group {{ margin-bottom: 15px; }}
        label {{ display: block; margin-bottom: 5px; }}
        input[type="text"], input[type="password"], textarea {{ width: 100%; padding: 8px; box-sizing: border-box; }}
        button {{ background: #007bff; color: #fff; border: none; padding: 10px 15px; cursor: pointer; border-radius: 4px; }}
        button:hover {{ background: #0056b3; }}
        .task {{ border-bottom: 1px solid #ddd; padding: 10px 0; }}
        .completed {{ text-decoration: line-through; color: #888; }}
        .error {{ color: red; }}
    </style>
</head>
<body>
    <div class="container">
        {body}
    </div>
</body>
</html>"""
    return web.HTTPError(status, page) if status != 200 else page


def require_login():
    """Redirect to login if not authenticated."""
    if not get_user_id():
        raise web.seeother('/login')


# ----------------------------------------------------------------------
# Page Handlers
# ----------------------------------------------------------------------
class Index:
    def GET(self):
        body = """
        <h1>Welcome to the Task Manager</h1>
        <p><a href="/login">Login</a> | <a href="/register">Register</a></p>
        """
        return html_response('Home', body)


class Login:
    def GET(self):
        body = """
        <h1>Login</h1>
        <form method="POST" action="/login">
            <div class="form-group">
                <label>Username</label>
                <input type="text" name="username" required>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit">Login</button>
        </form>
        <p>Don't have an account? <a href="/register">Register here</a></p>
        """
        return html_response('Login', body)

    def POST(self):
        data = web.input(username='', password='')
        username = data.username.strip()
        password = data.password
        user = db.select('users', where='username=$username', vars=locals()).limit(1)
        if user and user[0].password == hash_password(password):
            session.user_id = user[0].id
            session.username = user[0].username
            raise web.seeother('/dashboard')
        return html_response('Login', '<p class="error">Invalid credentials.</p><p><a href="/login">Try again</a></p>', status=200)


class Register:
    def GET(self):
        body = """
        <h1>Register</h1>
        <form method="POST" action="/register">
            <div class="form-group">
                <label>Username</label>
                <input type="text" name="username" required>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit">Register</button>
        </form>
        <p>Already have an account? <a href="/login">Login here</a></p>
        """
        return html_response('Register', body)

    def POST(self):
        data = web.input(username='', password='')
        username = data.username.strip()
        password = hash_password(data.password)
        try:
            db.insert('users', username=username, password=password)
            raise web.seeother('/login')
        except web.IntegrityError:
            return html_response('Register', '<p class="error">Username already taken.</p><p><a href="/register">Try again</a></p>')


class Logout:
    def GET(self):
        session.kill()
        raise web.seeother('/')


class Dashboard:
    def GET(self):
        require_login()
        user_id = get_user_id()
        tasks = db.select('tasks', where='user_id=$user_id', vars=locals(), order='created_at DESC')
        task_list = ''.join(
            f'<div class="task {'completed' if t.completed else ''}">'
            f'<strong>{t.title}</strong>: {t.description} '
            f'<a href="/tasks/edit/{t.id}">Edit</a> | '
            f'<form method="POST" action="/tasks/delete/{t.id}" style="display:inline;">'
            f'<button type="submit">Delete</button></form></div>'
            for t in tasks
        )
        body = f"""
        <h1>Dashboard (Welcome, {session.get('username', 'User')})</h1>
        <a href="/">Home</a> | <a href="/logout">Logout</a>
        <h2>Your Tasks</h2>
        {task_list if task_list else '<p>No tasks yet.</p>'}
        <h3>Add a new task</h3>
        <form method="POST" action="/tasks/new">
            <div class="form-group"><label>Title</label><input type="text" name="title" required></div>
            <div class="form-group"><label>Description</label><textarea name="description"></textarea></div>
            <button type="submit">Add Task</button>
        </form>
        <h3>API</h3>
        <p>Access JSON tasks via <a href="/api/tasks">/api/tasks</a></p>
        """
        return html_response('Dashboard', body)


class NewTask:
    def POST(self):
        require_login()
        data = web.input(title='', description='')
        if data.title.strip():
            db.insert('tasks', user_id=get_user_id(), title=data.title.strip(), description=data.description.strip())
        raise web.seeother('/dashboard')


class EditTask:
    def GET(self, task_id):
        require_login()
        task = db.select('tasks', where='id=$task_id AND user_id=$user_id', vars={'task_id': task_id, 'user_id': get_user_id()}, limit=1)
        if not task:
            raise web.notfound()
        t = task[0]
        body = f"""
        <h1>Edit Task: {t.title}</h1>
        <form method="POST" action="/tasks/edit/{t.id}">
            <div class="form-group"><label>Title</label><input type="text" name="title" value="{t.title}" required></div>
            <div class="form-group"><label>Description</label><textarea name="description">{t.description}</textarea></div>
            <div class="form-group"><label>Completed</label><input type="checkbox" name="completed" {'checked' if t.completed else ''}></div>
            <button type="submit">Update</button>
        </form>
        <p><a href="/dashboard">Back to Dashboard</a></p>
        """
        return html_response('Edit Task', body)

    def POST(self, task_id):
        require_login()
        data = web.input(title='', description='', completed='')
        task = db.select('tasks', where='id=$task_id AND user_id=$user_id', vars={'task_id': task_id, 'user_id': get_user_id()}, limit=1)
        if not task:
            raise web.notfound()
        db.update('tasks', where='id=$task_id', title=data.title.strip(), description=data.description.strip(), completed=1 if data.completed else 0, vars={'task_id': task_id})
        raise web.seeother('/dashboard')


class DeleteTask:
    def POST(self, task_id):
        require_login()
        db.delete('tasks', where='id=$task_id AND user_id=$user_id', vars={'task_id': task_id, 'user_id': get_user_id()})
        raise web.seeother('/dashboard')


class TasksAPI:
    def GET(self):
        if not get_user_id():
            return web.HTTPError(401, json.dumps({'error': 'Unauthorized'}))
        user_id = get_user_id()
        tasks = db.select('tasks', where='user_id=$user_id', vars=locals())
        task_list = [{'id': t.id, 'title': t.title, 'description': t.description, 'completed': bool(t.completed), 'created_at': str(t.created_at)} for t in tasks]
        return web.HTTPError(200, json.dumps(task_list, indent=2))

    def POST(self):
        if not get_user_id():
            return web.HTTPError(401, json.dumps({'error': 'Unauthorized'}))
        data = web.input(title='', description='')
        if not data.title.strip():
            return web.HTTPError(400, json.dumps({'error': 'Title required'}))
        task_id = db.insert('tasks', user_id=get_user_id(), title=data.title.strip(), description=data.description.strip())
        return web.HTTPError(201, json.dumps({'id': task_id, 'status': 'created'}))


class StaticFiles:
    def GET(self, path):
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
        file_path = os.path.join(static_dir, path)
        if os.path.isfile(file_path):
            ext = os.path.splitext(file_path)[1]
            content_type = {'.css': 'text/css', '.js': 'application/javascript', '.png': 'image/png', '.jpg': 'image/jpeg', '.gif': 'image/gif', '.ico': 'image/x-icon'}.get(ext, 'text/plain')
            with open(file_path, 'rb') as f:
                content = f.read()
            return web.HTTPError(200, content, {'Content-Type': content_type})
        raise web.notfound()


# ----------------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------------
if __name__ == '__main__':
    app.run()
