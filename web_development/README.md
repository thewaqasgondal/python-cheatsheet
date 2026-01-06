# Web Development Examples

This directory contains comprehensive examples of modern web development using Python Flask, demonstrating best practices for building scalable web applications.

## 📁 Directory Structure

```
web_development/
├── flask_blog_app.py          # Main Flask application with full blog functionality
├── templates/                 # Jinja2 HTML templates
│   ├── base.html             # Base template with navigation and layout
│   ├── index.html            # Home page with post listings
│   ├── post.html             # Individual post view with comments
│   ├── login.html            # User login form
│   ├── register.html         # User registration form
│   ├── create_post.html      # Post creation/editing form
│   └── about.html            # About page with documentation
└── README.md                 # This file
```

## 🚀 Features Demonstrated

### Core Flask Features
- **Routing**: URL routing with parameters and HTTP methods
- **Templates**: Jinja2 templating with inheritance, filters, and macros
- **Forms**: WTForms integration with validation and CSRF protection
- **Database**: SQLAlchemy ORM with relationships and migrations
- **Authentication**: Flask-Login for user sessions and protected routes
- **Security**: Password hashing, CSRF protection, secure file uploads

### Advanced Features
- **REST API**: JSON API endpoints with proper HTTP status codes
- **Rate Limiting**: Flask-Limiter for API protection
- **CORS**: Cross-origin resource sharing for API access
- **File Uploads**: Secure file handling with validation
- **Search**: Full-text search across posts and content
- **Pagination**: Efficient pagination for large datasets
- **Error Handling**: Custom error pages and exception handling
- **CLI Commands**: Flask CLI integration for database management

### User Experience
- **Responsive Design**: Bootstrap 5 for mobile-friendly UI
- **Interactive Elements**: JavaScript for dynamic content
- **Flash Messages**: User feedback for actions
- **Modal Dialogs**: Confirmation dialogs for destructive actions
- **Loading States**: Visual feedback for async operations

## 🛠 Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager

### Installation
```bash
# Navigate to the web development directory
cd web_development

# Install dependencies
pip install flask flask-sqlalchemy flask-login flask-wtf flask-migrate flask-cors flask-limiter python-dotenv

# Or install from requirements.txt (if available)
pip install -r ../../requirements.txt
```

### Running the Application
```bash
# Run the Flask development server
python flask_blog_app.py

# Or use Flask CLI
export FLASK_APP=flask_blog_app.py
flask run
```

The application will be available at `http://localhost:5000`

## 👤 Demo Credentials

For testing purposes, the application includes demo data:
- **Username**: `demo`
- **Password**: `demo123`

## 📚 API Documentation

### Posts API
- `GET /api/posts` - Retrieve paginated list of posts
- `GET /api/posts?page=2&per_page=10` - Paginated posts
- `GET /api/posts?category=tech` - Filter by category
- `POST /api/posts` - Create new post (requires authentication)
- `GET /api/posts/<id>` - Get single post with comments

### Comments API
- `POST /api/posts/<id>/comments` - Add comment to post (requires authentication)

### Authentication
All POST/PUT/DELETE endpoints require authentication via session cookies.

## 🔧 Configuration

The application uses sensible defaults but can be configured via environment variables:

```bash
export FLASK_ENV=development  # or production
export SECRET_KEY=your-secret-key
export DATABASE_URL=sqlite:///app.db
```

## 📖 Code Examples

### Basic Route
```python
@app.route('/')
def index():
    return render_template('index.html')
```

### Database Model
```python
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
```

### Form Handling
```python
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
```

### API Endpoint
```python
@app.route('/api/posts', methods=['GET'])
def api_posts():
    posts = Post.query.all()
    return jsonify([post.to_dict() for post in posts])
```

### Protected Route
```python
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
```

## 🎯 Learning Objectives

After studying this example, you should understand:

1. **Flask Application Structure**: How to organize a Flask app with blueprints, models, and views
2. **Database Design**: Creating relationships, migrations, and efficient queries
3. **Security Best Practices**: Authentication, authorization, and input validation
4. **API Design**: RESTful API principles and JSON response formatting
5. **Frontend Integration**: Template inheritance, forms, and JavaScript interaction
6. **Deployment Considerations**: Configuration, error handling, and performance optimization

## 🔄 Database Management

### Initialize Database
```bash
flask db init
flask db migrate
flask db upgrade
```

### Create Admin User
```bash
flask create-admin
```

### Reset Database
```bash
rm app.db
flask db upgrade
python flask_blog_app.py  # This will create sample data
```

## 🚀 Production Deployment

For production deployment, consider:

1. **WSGI Server**: Use Gunicorn or uWSGI instead of Flask's development server
2. **Database**: Replace SQLite with PostgreSQL or MySQL
3. **Caching**: Add Redis for session storage and caching
4. **SSL/TLS**: Enable HTTPS with proper certificates
5. **Monitoring**: Add logging and error tracking
6. **Static Files**: Use CDN for static assets

## 📝 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://sqlalchemy.org/)
- [WTForms Documentation](https://wtforms.readthedocs.io/)
- [Flask-Login Documentation](https://flask-login.readthedocs.io/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)

## 🤝 Contributing

This example is designed to be educational. Feel free to:
- Add new features
- Improve the UI/UX
- Add more API endpoints
- Implement additional security measures
- Add unit tests

## 📄 License

This code is provided as an educational example and can be used freely for learning purposes.