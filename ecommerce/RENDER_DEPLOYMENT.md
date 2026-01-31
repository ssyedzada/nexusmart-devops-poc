# 🚀 Render Deployment Guide

This guide will help you deploy your Django ecommerce application to Render.

## 📋 Prerequisites

1. A GitHub account with your code pushed to a repository
2. A Render account (sign up at https://render.com)

## 🔧 Step-by-Step Deployment

### Option 1: Using render.yaml (Automatic - Recommended)

If you're using the `render.yaml` file, Render will automatically configure everything:

1. **Push your code to GitHub** (if not already done)
   ```bash
   git add .
   git commit -m "Add Render deployment configuration"
   git push origin main
   ```

2. **Go to Render Dashboard**
   - Visit https://dashboard.render.com
   - Click "New +" → "Blueprint"

3. **Connect GitHub Repository**
   - Select your repository
   - Render will detect the `render.yaml` file
   - Click "Apply"

4. **Wait for Deployment**
   - Render will automatically:
     - Create a PostgreSQL database
     - Build your application
     - Run migrations
     - Deploy your app

### Option 2: Manual Setup (If render.yaml doesn't work)

1. **Create a PostgreSQL Database**
   - Go to Render Dashboard
   - Click "New +" → "PostgreSQL"
   - Name it: `ecommerce-db`
   - Select "Free" plan
   - Click "Create Database"
   - **Copy the Internal Database URL** (you'll need this)

2. **Create a Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure the service:
     - **Name**: `ecommerce-app` (or any name you prefer)
     - **Environment**: `Python 3`
     - **Build Command**: 
       ```bash
       pip install -r requirements.txt && python manage.py collectstatic --noinput
       ```
     - **Start Command**:
       ```bash
       gunicorn ecommerce.wsgi:application --bind 0.0.0.0:$PORT
       ```
     - **Root Directory**: `ecommerce` (if your code is in the ecommerce folder)

3. **Set Environment Variables**
   Click "Environment" tab and add:
   - `SECRET_KEY`: Generate a secure key (you can use: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
   - `DEBUG`: `False`
   - `DATABASE_URL`: Paste the Internal Database URL from step 1
   - `DJANGO_SETTINGS_MODULE`: `ecommerce.settings`
   - `PYTHON_VERSION`: `3.12.3`

4. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy your app
   - Wait for the build to complete (usually 2-5 minutes)

5. **Run Migrations**
   - Once deployed, go to your service
   - Click "Shell" tab
   - Run:
     ```bash
     python manage.py migrate
     ```
   - (Optional) Create dummy products:
     ```bash
     python manage.py create_dummy_products
     ```

## 🔍 Troubleshooting "Not Found" Error

If you see "Not Found" when accessing your Render URL, check:

### 1. Check Build Logs
- Go to your service in Render Dashboard
- Click "Logs" tab
- Look for errors during build or startup

### 2. Verify Start Command
Make sure your start command is:
```bash
gunicorn ecommerce.wsgi:application --bind 0.0.0.0:$PORT
```
**Important**: Must use `$PORT` (not 8000) - Render provides this dynamically

### 3. Check Environment Variables
- Ensure `SECRET_KEY` is set
- Ensure `DEBUG=False` for production
- Ensure `DATABASE_URL` is set correctly

### 4. Verify Root Directory
- If your `manage.py` is in `/ecommerce/`, set Root Directory to `ecommerce`
- If it's in the root, leave Root Directory empty

### 5. Check ALLOWED_HOSTS
The settings.py should allow Render domains. It's already configured, but verify:
- `ALLOWED_HOSTS` includes `*` when `RENDER` environment variable is set
- Or manually add your Render URL: `your-app-name.onrender.com`

### 6. Check Static Files
- Ensure `collectstatic` runs during build
- Verify `whitenoise` is in `MIDDLEWARE` (already configured)

### 7. Check Database Connection
- Verify `DATABASE_URL` is correct
- Check database is running (green status in Render)
- Run migrations: `python manage.py migrate` in Shell

## 📝 Common Issues and Solutions

### Issue: "Application Error"
**Solution**: Check logs for specific error. Common causes:
- Missing environment variables
- Database connection issues
- Import errors

### Issue: Static Files Not Loading
**Solution**: 
- Ensure build command includes: `python manage.py collectstatic --noinput`
- Verify `whitenoise` is installed and in `MIDDLEWARE`

### Issue: Database Errors
**Solution**:
- Run migrations: `python manage.py migrate` in Shell
- Verify `DATABASE_URL` is set correctly
- Check database is running

### Issue: Port Already in Use
**Solution**: 
- Always use `$PORT` in start command (Render provides this)
- Never hardcode port numbers

## ✅ Verification Checklist

After deployment, verify:

- [ ] Build completed successfully (check logs)
- [ ] Application is running (green status)
- [ ] Can access homepage at your Render URL
- [ ] Database migrations ran successfully
- [ ] Static files are loading (CSS, images)
- [ ] Can add products to cart
- [ ] Admin login works (if configured)

## 🔗 Your Render URL

Once deployed, your app will be available at:
```
https://your-app-name.onrender.com
```

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Django on Render](https://render.com/docs/deploy-django)
- [Render Environment Variables](https://render.com/docs/environment-variables)

## 🆘 Still Having Issues?

1. Check Render logs for specific error messages
2. Verify all files are committed and pushed to GitHub
3. Ensure `requirements.txt` includes all dependencies
4. Check that `runtime.txt` specifies Python 3.12.3
5. Verify `manage.py` is in the correct location

---

**Note**: Free tier on Render spins down after 15 minutes of inactivity. First request after spin-down may take 30-60 seconds to respond.

