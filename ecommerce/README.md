📘 DevOps E-commerce PoC: NexusMart
🎯 Project Overview
NexusMart is a modern e-commerce Proof of Concept (PoC) application built with Django 6.0, demonstrating comprehensive DevOps principles and practices for Ipswich Retail's digital transformation.

📊 Key Features
✅ Modern Django MVT Architecture (Model-View-Template)
✅ Complete CI/CD Pipeline with GitHub Actions
✅ Containerization with Docker & Docker Compose
✅ Automated Testing and Deployment
✅ Professional UI/UX with Bootstrap 5
✅ Hidden Admin Dashboard for management
✅ Interactive Shopping Cart with Session Management
✅ Product Management System
✅ Management Commands for Dummy Data
✅ DevOps Monitoring ready (Prometheus/Grafana)

🚀 Quick Start Guide

Prerequisites
- Python 3.12+ (Django 6.0+ requires Python 3.12+)
- Git
- Docker & Docker Compose (optional)
- GitHub Account

1. Local Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/nexusmart-devops.git
cd nexusmart-devops/ecommerce

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database
python manage.py makemigrations
python manage.py migrate

# Create dummy products (optional but recommended)
python manage.py create_dummy_products

# Create superuser (optional)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Run development server
python manage.py runserver
```

Access the application: http://localhost:8000

🔧 Docker Setup

Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Run migrations (first time only)
docker-compose exec web python manage.py migrate

# Create dummy products
docker-compose exec web python manage.py create_dummy_products

# Create superuser (optional)
docker-compose exec web python manage.py createsuperuser
```

The application will be available at http://localhost:8000

Using Docker Only

```bash
# Build Docker image
docker build -t nexusmart-app .

# Run container
docker run -p 8000:8000 \
  -e DEBUG=True \
  -e SECRET_KEY=your-secret-key \
  -e DATABASE_URL=postgres://user:pass@host:5432/dbname \
  nexusmart-app
```

Dockerfile Overview

The Dockerfile includes:
- Python 3.10 slim base image
- Automatic migrations on container start
- Static file collection
- Gunicorn for production
- Health checks and proper entrypoint

See `DOCKER_SETUP.md` for detailed Docker documentation.

🌐 Deployment

Option A: Render (Recommended)

1. Push code to GitHub
2. Sign up at render.com
3. Connect GitHub repository
4. Deploy as Web Service
5. Set environment variables:
   - `SECRET_KEY` - Django secret key
   - `DEBUG=False` - Production mode
   - `DATABASE_URL` - Provided by Render
   - `ALLOWED_HOSTS` - Your domain

Option B: Railway

1. Connect GitHub repository to Railway
2. Railway auto-detects Django
3. Set environment variables
4. Deploy automatically

Option C: PythonAnywhere

1. Upload files via Git
2. Configure virtual environment
3. Install requirements: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Configure web app

🔗 URLs & Access

Public Pages
- **Home**: `/` - Modern e-commerce homepage with featured products
- **Products**: `/products/` - Complete product catalog
- **Product Details**: `/product/<id>/` - Individual product page
- **Cart**: `/cart/` - Interactive shopping cart with quantity management
- **Checkout**: `/checkout/` - Checkout process (demo mode)

Cart Operations
- **Add to Cart**: `/cart/add/<product_id>/` - Add product to cart
- **Update Cart**: `/cart/update/<product_id>/` - Update item quantity
- **Remove from Cart**: `/cart/remove/<product_id>/` - Remove item

Hidden Admin (Not linked from site)
- **Admin Login**: `/admin-login/` (Password: `devops2025`)
- **Admin Dashboard**: `/admin-dashboard/` - Custom admin interface
- **Django Admin**: `/admin/` - Standard Django admin (superusers only)

⚙️ DevOps Pipeline Features

1. CI/CD Pipeline (GitHub Actions)

The pipeline includes:
- **Test Job**: Runs unit tests, integration tests, and coverage reports
- **Lint Job**: Code quality checks with flake8, black, and pylint
- **Docker Build**: Builds and validates Docker image
- **Deploy Job**: Placeholder for deployment automation

Triggered on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

2. Automated Testing

- Unit tests for models (`Product`)
- View tests for all pages
- Integration tests for cart functionality
- Admin login tests
- Test coverage reporting

Run tests locally:
```bash
python manage.py test
```

3. Containerization

- **Dockerfile**: Production-ready container configuration
- **docker-compose.yml**: Multi-service setup with PostgreSQL
- **entrypoint.sh**: Automatic migrations and static file collection
- Health checks and dependency management

4. Monitoring Setup

- Logging configured for application and shop app
- Ready for Prometheus/Grafana integration
- Error tracking in place
- Debug logging for development

📁 Project Structure

```
nexusmart-devops/
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # CI/CD Pipeline
├── shop/                       # Main Django app
│   ├── management/
│   │   └── commands/
│   │       └── create_dummy_products.py  # Management command
│   ├── migrations/             # Database migrations
│   ├── templates/shop/         # HTML templates
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── products.html
│   │   ├── product_detail.html
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   ├── admin_login.html
│   │   └── admin_dashboard.html
│   ├── static/shop/            # Static files
│   ├── models.py               # Database models (Product)
│   ├── views.py                # Business logic & cart management
│   ├── tests.py                # Unit tests
│   ├── urls.py                 # URL routing
│   ├── admin.py                # Django admin configuration
│   └── context_processors.py   # Cart context processor
├── ecommerce/                  # Django project
│   ├── settings.py             # Configuration
│   ├── urls.py                # Main URLs
│   └── wsgi.py                # WSGI config
├── Dockerfile                  # Container configuration
├── docker-compose.yml          # Multi-service setup
├── entrypoint.sh               # Container entrypoint
├── requirements.txt            # Python dependencies
├── runtime.txt                 # Python version for deployment
├── .dockerignore               # Docker ignore file
├── .gitignore                  # Git ignore file
├── QUICKSTART.md               # Quick start guide
├── DOCKER_SETUP.md             # Docker documentation
└── README.md                   # This file
```

🛠️ Management Commands

Create Dummy Products

Populate the database with 12 sample products with images:

```bash
python manage.py create_dummy_products
```

This creates products like:
- Premium Wireless Headphones
- Ultra-Thin Laptop
- Smart Fitness Watch
- Wireless Charging Pad
- And 8 more products!

🎓 Learning Objectives Met

DevOps Principles Demonstrated:
- ✅ **Continuous Integration** - Automated testing on every commit
- ✅ **Continuous Deployment** - Automated deployment pipeline
- ✅ **Infrastructure as Code** - Docker & docker-compose configuration
- ✅ **Monitoring & Logging** - Application performance tracking
- ✅ **Collaboration** - Team workflows and communication tools
- ✅ **Version Control** - Git branching strategy

Technical Skills Showcased:
- ✅ Django MVT architecture
- ✅ Session-based cart management
- ✅ Containerization with Docker
- ✅ CI/CD pipeline design
- ✅ Cloud deployment ready
- ✅ Automated testing
- ✅ Security best practices
- ✅ Management commands
- ✅ Context processors

📈 Screenshots for Report

Required Screenshots:
1. GitHub repository with branches
2. GitHub Actions pipeline passing
3. Docker build and run
4. Application running locally
5. Deployed application (Render/PythonAnywhere)
6. Admin dashboard
7. Shopping cart functionality
8. CI/CD workflow logs
9. Test results
10. Product catalog

⚠️ Troubleshooting

Common Issues:

**Static files not loading:**
```bash
python manage.py collectstatic
```
Check `STATICFILES_DIRS` in `settings.py`

**Docker build fails:**
- Check Dockerfile syntax
- Ensure `requirements.txt` exists
- Verify `entrypoint.sh` has execute permissions

**Database errors:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Cart not working:**
- Ensure sessions are enabled (check `MIDDLEWARE` in settings)
- Check browser cookies are enabled
- Verify products exist in database

**Admin access denied:**
- Use password: `devops2025` at `/admin-login/`
- Or create superuser: `python manage.py createsuperuser`

**Docker Compose issues:**
- Ensure Docker and docker-compose are installed
- Check ports 8000 and 5432 are not in use
- View logs: `docker-compose logs web`

**CI/CD pipeline fails:**
- Check GitHub Actions tab for error details
- Verify all required files are committed
- Ensure `requirements.txt` is up to date

📝 Additional Documentation

- **QUICKSTART.md** - Detailed quick start guide
- **DOCKER_SETUP.md** - Complete Docker documentation
- **test_cart.md** - Cart functionality testing guide

🔒 Security Notes

- Change `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Use environment variables for sensitive data
- Configure proper `ALLOWED_HOSTS`
- Use HTTPS in production
- Keep dependencies updated

📄 License

This is a Proof of Concept project for educational purposes.

---

**Built with ❤️ using Django, Docker, and DevOps best practices**
