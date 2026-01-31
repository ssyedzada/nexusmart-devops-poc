# Docker Setup Guide

## Quick Start

### Using Docker Compose (Recommended)

1. **Build and start services:**
   ```bash
   docker-compose up --build
   ```

2. **Run migrations (first time only):**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. **Create superuser (optional):**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

4. **Create dummy products:**
   ```bash
   docker-compose exec web python manage.py create_dummy_products
   ```

5. **Access the application:**
   - Web: http://localhost:8000
   - Database: localhost:5432

### Using Docker Only

1. **Build the image:**
   ```bash
   docker build -t nexusmart-app .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8000:8000 \
     -e DEBUG=True \
     -e SECRET_KEY=your-secret-key \
     -e DATABASE_URL=postgres://user:pass@host:5432/dbname \
     nexusmart-app
   ```

## Services

- **web**: Django application (port 8000)
- **db**: PostgreSQL database (port 5432)

## Environment Variables

Set these in `docker-compose.yml` or as environment variables:

- `DEBUG`: Set to `False` in production
- `SECRET_KEY`: Django secret key
- `DATABASE_URL`: PostgreSQL connection string (auto-set in docker-compose)

## Troubleshooting

### Database connection errors
- Wait for database to be ready (healthcheck handles this)
- Check database credentials in docker-compose.yml

### Static files not loading
- Run: `docker-compose exec web python manage.py collectstatic`

### Container won't start
- Check logs: `docker-compose logs web`
- Verify Docker and docker-compose are installed

## Production Deployment

For production:
1. Set `DEBUG=False`
2. Use a strong `SECRET_KEY`
3. Configure proper `ALLOWED_HOSTS`
4. Use environment variables for sensitive data
5. Set up proper database backups

