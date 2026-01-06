"""
Web Development with Flask

This module demonstrates comprehensive web development using Flask,
including routing, templates, forms, authentication, and REST APIs.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, g
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import json
import secrets
from typing import List, Dict, Any, Optional
import tempfile
import uuid


# Configuration
class Config:
    SECRET_KEY = secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    WTF_CSRF_ENABLED = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)


# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
CORS(app)  # Enable CORS for API endpoints
limiter = Limiter(get_remote_address, app=app)

# Create upload folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# Database Models
class User(UserMixin, db.Model):
    """User model for authentication."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    posts = db.relationship('Post', backref='author', lazy=True)

    def set_password(self, password: str) -> None:
        """Set password hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check password against hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f'<User {self.username}>'


class Post(db.Model):
    """Blog post model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50), default='general')
    views = db.Column(db.Integer, default=0)

    def __repr__(self) -> str:
        return f'<Post {self.title}>'


class Comment(db.Model):
    """Comment model for posts."""
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    user = db.relationship('User', backref='comments')
    post = db.relationship('Post', backref='comments')


# Forms
class LoginForm(FlaskForm):
    """Login form."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    """User registration form."""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password',
                                   validators=[DataRequired(), EqualTo('password')])


class PostForm(FlaskForm):
    """Blog post form."""
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('general', 'General'),
        ('tech', 'Technology'),
        ('lifestyle', 'Lifestyle'),
        ('tutorial', 'Tutorial')
    ], default='general')


class CommentForm(FlaskForm):
    """Comment form."""
    content = TextAreaField('Comment', validators=[DataRequired(), Length(max=1000)])


class SearchForm(FlaskForm):
    """Search form."""
    query = StringField('Search', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('all', 'All Categories'),
        ('general', 'General'),
        ('tech', 'Technology'),
        ('lifestyle', 'Lifestyle'),
        ('tutorial', 'Tutorial')
    ], default='all')


# Flask-Login setup
@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
    """Load user for Flask-Login."""
    return User.query.get(int(user_id))


# Request hooks
@app.before_request
def before_request():
    """Set up request context."""
    g.user = current_user


@app.after_request
def after_request(response):
    """Clean up after request."""
    return response


# Routes
@app.route('/')
def index():
    """Home page with recent posts."""
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)

    return render_template('index.html', posts=posts, title='Home')


@app.route('/about')
def about():
    """About page."""
    return render_template('about.html', title='About')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))

        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))

        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
@login_required
def logout():
    """User logout."""
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    """User profile page."""
    posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.created_at.desc()).all()
    return render_template('profile.html', title='Profile', posts=posts)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    """Create new post."""
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                   content=form.content.data,
                   category=form.category.data,
                   author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('post', post_id=post.id))

    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@app.route('/post/<int:post_id>')
def post(post_id: int):
    """View individual post."""
    post = Post.query.get_or_404(post_id)
    post.views += 1
    db.session.commit()

    form = CommentForm()
    return render_template('post.html', title=post.title, post=post, form=form)


@app.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id: int):
    """Add comment to post."""
    post = Post.query.get_or_404(post_id)
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            author=current_user,
            post=post
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comment added successfully!', 'success')
        return redirect(url_for('post', post_id=post.id))

    return redirect(url_for('post', post_id=post.id))


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id: int):
    """Delete post."""
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('You cannot delete this post', 'error')
        return redirect(url_for('post', post_id=post.id))

    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    """Search posts."""
    form = SearchForm()
    posts = []
    query = None

    if form.validate_on_submit() or request.method == 'GET':
        if request.method == 'GET':
            query = request.args.get('q', '')
            category = request.args.get('category', 'all')
        else:
            query = form.query.data
            category = form.category.data

        if query:
            search_query = Post.query.filter(
                db.or_(
                    Post.title.contains(query),
                    Post.content.contains(query)
                )
            )

            if category != 'all':
                search_query = search_query.filter_by(category=category)

            posts = search_query.order_by(Post.created_at.desc()).all()

    return render_template('search.html', title='Search', form=form, posts=posts, query=query)


@app.route('/category/<category>')
def category_posts(category: str):
    """View posts by category."""
    posts = Post.query.filter_by(category=category).order_by(Post.created_at.desc()).all()
    return render_template('category.html', title=f'{category.title()} Posts',
                         posts=posts, category=category)


# API Routes
@app.route('/api/posts', methods=['GET'])
@limiter.limit("100 per minute")
def api_posts():
    """API endpoint for posts."""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 50)

    posts_query = Post.query.order_by(Post.created_at.desc())
    posts = posts_query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'posts': [{
            'id': post.id,
            'title': post.title,
            'content': post.content[:200] + '...' if len(post.content) > 200 else post.content,
            'author': post.author.username,
            'category': post.category,
            'created_at': post.created_at.isoformat(),
            'views': post.views
        } for post in posts.items],
        'total': posts.total,
        'pages': posts.pages,
        'current_page': posts.page
    })


@app.route('/api/posts/<int:post_id>', methods=['GET'])
def api_post(post_id: int):
    """API endpoint for single post."""
    post = Post.query.get_or_404(post_id)

    return jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'author': post.author.username,
        'category': post.category,
        'created_at': post.created_at.isoformat(),
        'updated_at': post.updated_at.isoformat(),
        'views': post.views,
        'comments': [{
            'id': comment.id,
            'content': comment.content,
            'author': comment.user.username,
            'created_at': comment.created_at.isoformat()
        } for comment in post.comments]
    })


@app.route('/api/posts', methods=['POST'])
@login_required
@limiter.limit("10 per minute")
def api_create_post():
    """API endpoint to create post."""
    data = request.get_json()

    if not data or not all(k in data for k in ['title', 'content']):
        return jsonify({'error': 'Missing required fields'}), 400

    post = Post(
        title=data['title'],
        content=data['content'],
        category=data.get('category', 'general'),
        author=current_user
    )

    db.session.add(post)
    db.session.commit()

    return jsonify({
        'id': post.id,
        'title': post.title,
        'message': 'Post created successfully'
    }), 201


@app.route('/api/posts/<int:post_id>/comments', methods=['POST'])
@login_required
@limiter.limit("30 per minute")
def api_add_comment(post_id: int):
    """API endpoint to add comment."""
    post = Post.query.get_or_404(post_id)
    data = request.get_json()

    if not data or 'content' not in data:
        return jsonify({'error': 'Comment content required'}), 400

    comment = Comment(
        content=data['content'],
        author=current_user,
        post=post
    )

    db.session.add(comment)
    db.session.commit()

    return jsonify({
        'id': comment.id,
        'content': comment.content,
        'author': current_user.username,
        'created_at': comment.created_at.isoformat()
    }), 201


# File upload routes
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    """File upload page."""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            # Add timestamp to avoid conflicts
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{int(datetime.utcnow().timestamp())}{ext}"

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            flash(f'File uploaded successfully: {filename}', 'success')
            return redirect(url_for('uploaded_files'))

    return render_template('upload.html', title='Upload File')


@app.route('/uploads')
@login_required
def uploaded_files():
    """View uploaded files."""
    files = []
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        files = os.listdir(app.config['UPLOAD_FOLDER'])

    return render_template('uploads.html', title='Uploaded Files', files=files)


# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return render_template('404.html', title='Page Not Found'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    db.session.rollback()
    return render_template('500.html', title='Internal Server Error'), 500


# Template filters
@app.template_filter('format_datetime')
def format_datetime(value: datetime, format='%Y-%m-%d %H:%M') -> str:
    """Format datetime in templates."""
    if value is None:
        return ""
    return value.strftime(format)


@app.template_filter('truncate')
def truncate_text(text: str, length: int = 100) -> str:
    """Truncate text in templates."""
    if len(text) <= length:
        return text
    return text[:length] + '...'


# Context processors
@app.context_processor
def inject_now():
    """Inject current datetime into all templates."""
    return {'now': datetime.utcnow()}


@app.context_processor
def inject_categories():
    """Inject post categories into all templates."""
    categories = ['general', 'tech', 'lifestyle', 'tutorial']
    return {'categories': categories}


# CLI commands
@app.cli.command('create-admin')
def create_admin():
    """Create admin user."""
    username = input('Username: ')
    email = input('Email: ')
    password = input('Password: ')

    if User.query.filter_by(username=username).first():
        print('User already exists')
        return

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    print('Admin user created')


@app.cli.command('init-db')
def init_db():
    """Initialize database."""
    db.create_all()
    print('Database initialized')


def create_sample_data():
    """Create sample data for demonstration."""
    # Create sample user
    if not User.query.filter_by(username='demo').first():
        user = User(username='demo', email='demo@example.com')
        user.set_password('demo123')
        db.session.add(user)
        db.session.commit()

        # Create sample posts
        posts_data = [
            {
                'title': 'Welcome to Flask Blog',
                'content': 'This is a sample blog post demonstrating Flask web development...',
                'category': 'general'
            },
            {
                'title': 'Python Best Practices',
                'content': 'Learn about Python best practices for web development...',
                'category': 'tech'
            },
            {
                'title': 'Getting Started with APIs',
                'content': 'Building REST APIs with Flask is straightforward...',
                'category': 'tutorial'
            }
        ]

        for post_data in posts_data:
            post = Post(**post_data, author=user)
            db.session.add(post)

        db.session.commit()
        print("Sample data created")


if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
        create_sample_data()

    print("Flask Web Development Examples")
    print("=" * 40)
    print("Starting Flask development server...")
    print("Visit http://localhost:5000 to see the application")
    print("\nFeatures demonstrated:")
    print("- User authentication and authorization")
    print("- CRUD operations for blog posts")
    print("- REST API endpoints")
    print("- File uploads")
    print("- Search functionality")
    print("- Rate limiting and CORS")
    print("- Database relationships")
    print("- Template inheritance and forms")
    print("\nSample login: demo / demo123")

    app.run(debug=True, host='0.0.0.0', port=5000)