# 🚨 Fix "Not Found" Error on Render - Step by Step

## ⚠️ Most Common Issue: Root Directory

If your `manage.py` is in the `ecommerce` folder (not at repository root), Render needs to know this!

## ✅ Solution 1: Manual Setup (Recommended for First Time)

### Step 1: Create Web Service in Render

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Fill in these settings:

### Step 2: Configure Settings

**Name**: `ecommerce-app` (or any name)

**Environment**: `Python 3`

**Region**: Choose closest to you

**Branch**: `main` (or your default branch)

**Root Directory**: ⚠️ **THIS IS CRITICAL** ⚠️
```
ecommerce
```
*(This tells Render where your `manage.py` file is)*

**Build Command**:
```bash
pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput
```

**Start Command**:
```bash
gunicorn ecommerce.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

### Step 3: Create PostgreSQL Database

1. In Render Dashboard, click **"New +"** → **"PostgreSQL"**
2. Name: `ecommerce-db`
3. Plan: **Free**
4. Click **"Create Database"**
5. **Copy the "Internal Database URL"** (you'll need this)

### Step 4: Set Environment Variables

In your Web Service → **Environment** tab, add:

| Key | Value | Notes |
|-----|-------|-------|
| `SECRET_KEY` | Generate one | See below |
| `DEBUG` | `False` | Must be False for production |
| `DATABASE_URL` | Paste from step 3 | The Internal Database URL |
| `DJANGO_SETTINGS_MODULE` | `ecommerce.settings` | |
| `PYTHON_VERSION` | `3.12.3` | |
| `RENDER` | `true` | Helps with settings detection |

**Generate SECRET_KEY**:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 5: Deploy

1. Click **"Create Web Service"**
2. Wait for build to complete (2-5 minutes)
3. Check the **"Logs"** tab for any errors

### Step 6: Run Migrations (If Not Done Automatically)

1. Go to your service
2. Click **"Shell"** tab
3. Run:
   ```bash
   python manage.py migrate
   ```
4. (Optional) Create dummy products:
   ```bash
   python manage.py create_dummy_products
   ```

## ✅ Solution 2: Using render.yaml (If Repo Root is ecommerce folder)

If your repository root IS the `ecommerce` folder (not `Devops`), then:

1. Make sure `render.yaml` is at the repository root
2. Push to GitHub
3. In Render: **"New +"** → **"Blueprint"**
4. Connect repository
5. Render will auto-configure everything

**BUT** if your repo root is `Devops` and Django is in `Devops/ecommerce`, then use **Solution 1** (manual setup) with Root Directory set to `ecommerce`.

## 🔍 Troubleshooting Checklist

### ❌ Still Getting "Not Found"?

Check each of these:

#### 1. Root Directory
- [ ] Is Root Directory set to `ecommerce`?
- [ ] Can Render find `manage.py`? (Check build logs)

#### 2. Start Command
- [ ] Does it use `$PORT` (not 8000)?
- [ ] Does it use `0.0.0.0` (not 127.0.0.1)?
- [ ] Is the command: `gunicorn ecommerce.wsgi:application --bind 0.0.0.0:$PORT`?

#### 3. Build Logs
- [ ] Check "Logs" tab in Render
- [ ] Look for red error messages
- [ ] Common errors:
  - `ModuleNotFoundError` → Check requirements.txt
  - `No such file: manage.py` → Wrong Root Directory
  - `Database connection failed` → Check DATABASE_URL

#### 4. Runtime Logs
- [ ] After build, check "Logs" tab
- [ ] Look for: `Listening at: http://0.0.0.0:XXXX`
- [ ] If you see errors, they'll tell you what's wrong

#### 5. Environment Variables
- [ ] `SECRET_KEY` is set
- [ ] `DATABASE_URL` is set (from PostgreSQL service)
- [ ] `DEBUG=False`
- [ ] `DJANGO_SETTINGS_MODULE=ecommerce.settings`

#### 6. Database
- [ ] PostgreSQL service is running (green status)
- [ ] Migrations have been run
- [ ] `DATABASE_URL` is correct

#### 7. Static Files
- [ ] Build command includes `collectstatic`
- [ ] Check logs for "Static files collected"

## 🐛 Common Errors & Fixes

### Error: "ModuleNotFoundError: No module named 'ecommerce'"
**Fix**: Set Root Directory to `ecommerce` in Render settings

### Error: "No such file: manage.py"
**Fix**: Set Root Directory to `ecommerce` in Render settings

### Error: "Database connection failed"
**Fix**: 
1. Check PostgreSQL is running
2. Verify `DATABASE_URL` is correct (use Internal Database URL)
3. Run migrations: `python manage.py migrate` in Shell

### Error: "DisallowedHost at /"
**Fix**: 
1. Set `RENDER=true` environment variable
2. Or manually add your Render URL to `ALLOWED_HOSTS`

### Error: "Static files not found"
**Fix**: 
1. Ensure build command includes `collectstatic`
2. Check `STATIC_ROOT` in settings.py
3. Verify `whitenoise` is in `MIDDLEWARE`

## ✅ Verification Steps

After deployment, verify:

1. **Build Status**: Green checkmark ✅
2. **Service Status**: "Live" (not "Stopped")
3. **Homepage**: Visit your Render URL - should show homepage
4. **Products Page**: Visit `/products/` - should show products
5. **Static Files**: CSS should load (check page source)

## 📞 Still Not Working?

1. **Check Logs First**: Most errors are visible in the Logs tab
2. **Test Locally**: Make sure it works with:
   ```bash
   cd ecommerce
   gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8000
   ```
3. **Run Diagnostic**: Use the `check_render.py` script:
   ```bash
   cd ecommerce
   python check_render.py
   ```

## 🎯 Quick Reference

**Root Directory**: `ecommerce`  
**Build Command**: `pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput`  
**Start Command**: `gunicorn ecommerce.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120`

---

**Remember**: The #1 cause of "Not Found" is **wrong Root Directory**. Make sure it's set to `ecommerce`!

