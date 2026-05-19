---
library: flask
version: 3.1
latest: true
category: backend
official_docs: https://flask.palletsprojects.com/
last_updated: 2026-03-21
last_checked: 2026-03-21
source: ai-enhanced from flask.palletsprojects.com + web research
---

# Flask v3.1

> Flask — A lightweight WSGI web application framework for Python. Micro but mighty.
> Current: v3.1.3 (Feb 2026) | Previous: v3.0 (Sep 2023)
> Docs: https://flask.palletsprojects.com/

## Version Comparison

| Feature | v2.x | v3.0 | v3.1 |
|:--------|:-----|:-----|:-----|
| Python minimum | 3.7 | 3.8 | **3.9+** |
| Werkzeug minimum | 2.x | 3.0 | **3.1** |
| Async views (`async def`) | ✅ | ✅ | ✅ |
| `__version__` attribute | ✅ | ⚠️ Deprecated | ❌ Removed |
| `config.from_json` | ✅ | ❌ Removed | ❌ |
| `safe_join` | ✅ | ❌ Removed | ❌ |
| Key rotation (`SECRET_KEY_FALLBACKS`) | ❌ | ❌ | ✅ |
| Partitioned cookies (CHIPS) | ❌ | ❌ | ✅ |
| Per-request `max_content_length` | ❌ | ❌ | ✅ |
| `MAX_FORM_MEMORY_SIZE` config | ❌ | ❌ | ✅ |
| `TRUSTED_HOSTS` config | ❌ | ❌ | ✅ |
| Resource `encoding` param | ❌ | ❌ | ✅ |

## Installation

```bash
# Install
pip install Flask          # latest (3.1.x)
pip install Flask==3.1.3   # pinned version

# With extras
pip install Flask[async]   # async support (installs asgiref)

# Development setup
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
pip install Flask

# Verify
python -c "import flask; print(flask.__name__)"
flask --version
```

## Configuration

```python
# config.py — common configuration pattern
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-me')
    # v3.1: key rotation — old keys still valid for unsigning
    SECRET_KEY_FALLBACKS = [
        'previous-secret-key-1',
        'previous-secret-key-2',
    ]
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # v3.1: Form limits
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB upload limit
    MAX_FORM_MEMORY_SIZE = 500_000          # 500KB for form fields
    MAX_FORM_PARTS = 1000

    # v3.1: Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_PARTITIONED = True       # v3.1: CHIPS support
    TRUSTED_HOSTS = ['example.com', '.example.com']


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'dev'
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    DEBUG = False

# app.py — loading config
app = Flask(__name__)
app.config.from_object('config.ProductionConfig')
# or from env var
app.config.from_envvar('APP_SETTINGS', silent=True)
```

## Core API

### App Factory Pattern

```python
from flask import Flask

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
```

### Routes & Views

```python
from flask import Flask, request, jsonify, abort, redirect, url_for

app = Flask(__name__)

# Basic routes
@app.route('/')
def index():
    return '<h1>Hello, World!</h1>'

# HTTP methods
@app.route('/api/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        data = request.get_json()
        # validate & create user
        return jsonify(user), 201
    return jsonify(get_all_users())

# URL parameters
@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

# Query parameters
@app.route('/api/search')
def search():
    q = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    return jsonify(search_results(q, page))

# File upload
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify(status='uploaded'), 201
    abort(400)
```

### Async Views (v2.0+)

```python
# Requires: pip install Flask[async]
@app.route('/api/data')
async def get_data():
    data = await fetch_from_external_api()
    return jsonify(data)

# ⚠️ Gotcha: Flask async runs in a thread with asyncio.run()
# For true ASGI, consider Quart (Flask-compatible)
```

### Request & Response

```python
from flask import request, make_response, Response

# Request attributes
request.method          # 'GET', 'POST', etc.
request.args            # URL query params (ImmutableMultiDict)
request.form            # form data (POST)
request.json            # parsed JSON body (or None)
request.get_json()      # parsed JSON (raises 400 on bad JSON)
request.files           # file uploads
request.headers         # HTTP headers
request.cookies         # cookies
request.remote_addr     # client IP
request.content_length  # body size

# v3.1: per-request max content length
class CustomRequest(Request):
    @property
    def max_content_length(self):
        if self.path.startswith('/upload'):
            return 100 * 1024 * 1024  # 100MB for uploads
        return 16 * 1024 * 1024       # 16MB default

app.request_class = CustomRequest

# Response
response = make_response(jsonify(data), 200)
response.headers['X-Custom'] = 'value'
response.set_cookie('key', 'value', httponly=True, samesite='Lax')
return response

# Streaming response
def generate():
    for row in query_large_dataset():
        yield f"{row}\n"

return Response(generate(), mimetype='text/plain')
```

### Error Handling

```python
from flask import jsonify
from werkzeug.exceptions import HTTPException

# Custom error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify(error='Not found'), 404

@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return jsonify(error='Internal server error'), 500

# Catch all HTTP errors as JSON
@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify(
        code=e.code,
        name=e.name,
        description=e.description,
    ), e.code

# Custom exceptions
class ValidationError(Exception):
    def __init__(self, message, field=None):
        self.message = message
        self.field = field

@app.errorhandler(ValidationError)
def handle_validation(e):
    return jsonify(error=e.message, field=e.field), 422
```

### Blueprints & Modular Structure

```python
# app/api/__init__.py
from flask import Blueprint

bp = Blueprint('api', __name__, url_prefix='/api')

from app.api import users, posts  # import routes

# app/api/users.py
from app.api import bp

@bp.route('/users')
def list_users():
    return jsonify(users=[])

@bp.before_request
def authenticate():
    token = request.headers.get('Authorization')
    if not verify_token(token):
        abort(401)

# Recommended project structure:
# project/
# ├── app/
# │   ├── __init__.py      # create_app factory
# │   ├── models.py         # SQLAlchemy models
# │   ├── main/
# │   │   ├── __init__.py   # Blueprint
# │   │   └── routes.py
# │   ├── api/
# │   │   ├── __init__.py   # Blueprint
# │   │   ├── users.py
# │   │   └── auth.py
# │   └── templates/
# ├── config.py
# ├── requirements.txt
# └── wsgi.py
```

### Templates (Jinja2)

```python
from flask import render_template

@app.route('/profile/<username>')
def profile(username):
    user = get_user_or_404(username)
    return render_template('profile.html', user=user)
```

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html>
<head><title>{% block title %}{% endblock %}</title></head>
<body>
  {% block content %}{% endblock %}
</body>
</html>

<!-- templates/profile.html -->
{% extends "base.html" %}
{% block title %}{{ user.name }}{% endblock %}
{% block content %}
  <h1>{{ user.name }}</h1>
  <!-- ⚠️ Autoescaped by default — safe from XSS -->
  <p>{{ user.bio }}</p>

  <!-- To render raw HTML (careful!): -->
  {{ user.html_content | safe }}
  <!-- Or in Python: Markup('<b>safe</b>') -->
{% endblock %}
```

### CLI Commands

```python
import click

@app.cli.command('init-db')
@click.option('--seed', is_flag=True, help='Seed sample data')
def init_db(seed):
    """Initialize the database."""
    db.create_all()
    if seed:
        create_sample_data()
    click.echo('Database initialized.')

# Usage: flask init-db --seed
```

### Extensions (Common Stack)

```python
# Database: Flask-SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(80))

# Migrations: Flask-Migrate
from flask_migrate import Migrate
migrate = Migrate()
# flask db init / flask db migrate / flask db upgrade

# Auth: Flask-Login
from flask_login import LoginManager, login_required, current_user
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/dashboard')
@login_required
def dashboard():
    return f"Hello, {current_user.name}"

# CORS: Flask-CORS
from flask_cors import CORS
CORS(app, resources={r"/api/*": {"origins": "https://example.com"}})

# Caching: Flask-Caching
from flask_caching import Cache
cache = Cache(config={'CACHE_TYPE': 'redis'})

@app.route('/expensive')
@cache.cached(timeout=300)
def expensive_view():
    return compute_expensive()
```

## Common Patterns

```python
# 1. Before/After request hooks
@app.before_request
def before_request():
    g.start_time = time.time()
    g.db = get_db_connection()

@app.after_request
def after_request(response):
    duration = time.time() - g.start_time
    response.headers['X-Response-Time'] = str(duration)
    return response

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# 2. Middleware pattern
class RequestLogger:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO')
        app.logger.info(f"Request: {path}")
        return self.app(environ, start_response)

app.wsgi_app = RequestLogger(app.wsgi_app)

# 3. API versioning
v1 = Blueprint('v1', __name__, url_prefix='/api/v1')
v2 = Blueprint('v2', __name__, url_prefix='/api/v2')

# 4. Configuration-based feature flags
@app.route('/beta-feature')
def beta():
    if not app.config.get('ENABLE_BETA'):
        abort(404)
    return render_template('beta.html')

# 5. Deployment (Production)
# gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"
# or with gevent:
# gunicorn -w 4 -k gevent -b 0.0.0.0:8000 "app:create_app()"
```

## Gotchas & Breaking Changes

### General Gotchas

- ⚠️ **Application context required**: Accessing `current_app`, `g`, or DB outside request context raises `RuntimeError`.
  ```python
  # Wrong: calling outside context
  with app.app_context():
      db.create_all()  # ✅ Correct
  ```

- ⚠️ **Jinja macro context**: Macros don't have access to `request`, `session`, `g` by default.
  ```html
  {# Wrong — request is undefined #}
  {% macro nav() %}{{ request.path }}{% endmacro %}
  {# Fix: import with context #}
  {% from "macros.html" import nav with context %}
  ```

- ⚠️ **`app.run()` is NOT for production**: Use Gunicorn, uWSGI, or Waitress.
  ```bash
  # Development only
  flask run --debug
  # Production
  gunicorn -w 4 "app:create_app()"
  ```

- ⚠️ **Thread safety of `g`**: `g` is per-request, NOT shared between requests. Don't store persistent data.

- ⚠️ **`request.json` vs `request.get_json()`**: `.json` returns None for bad Content-Type; `.get_json(force=True)` ignores Content-Type.

- ⚠️ **Circular imports**: App factory pattern avoids this — always use `create_app()` + blueprints.

- ⚠️ **Flask-Migrate auto-detection**: Alembic may miss some changes (indexes, constraints). Always review migration scripts.

- ⚠️ **Autoescaping**: Enabled by default in `.html` templates only. `.txt` and other templates are NOT autoescaped.

### v3.1 Breaking Changes

- ⚠️ **Python 3.9+ required**: Dropped Python 3.8 support.
- ⚠️ **Werkzeug >= 3.1 required**: Update dependencies simultaneously.
- ⚠️ **`SECRET_KEY_FALLBACKS` arg order bug** (fixed in 3.1.1): v3.1.0 had incorrect order — **upgrade to 3.1.3+**.
- ⚠️ **Session cache vulnerability** (fixed in 3.1.3): Session object cached sensitive info — **upgrade to 3.1.3+**.

### v3.0 Breaking Changes

- ⚠️ **`config.from_json` removed**: Use `config.from_file("config.json", json.load)`.
- ⚠️ **`safe_join` removed**: Use `werkzeug.utils.safe_join`.
- ⚠️ **`__version__` deprecated**: Use `importlib.metadata.version("flask")`.

## Migration

### From Flask 2.x → 3.0
1. Update Python to 3.8+
2. Update Werkzeug to 3.0+
3. Replace `safe_join` → `werkzeug.utils.safe_join`
4. Replace `config.from_json(file)` → `config.from_file(file, json.load)`
5. Replace `flask.__version__` → `importlib.metadata.version("flask")`
6. Test all extensions for v3 compatibility

### From Flask 3.0 → 3.1
1. Update Python to 3.9+
2. Update Werkzeug to 3.1+, ItsDangerous to 2.2+, Blinker to 1.9+
3. Adopt `SECRET_KEY_FALLBACKS` for key rotation
4. Set `TRUSTED_HOSTS` for production security
5. Consider `SESSION_COOKIE_PARTITIONED` for CHIPS compliance
6. **Upgrade directly to 3.1.3+** (3.1.0 has vulnerabilities)

<!--
BM25 DESIGN RULES:
- H1 = library name (root search anchor)
- H2 = feature category, add (vN) suffix for version matching
- Code:prose ratio ≥ 70:30
- Use ⚠️ diff notes for version disambiguation
- Keep 5-30KB per file, H2 sections ~50 lines each
-->
