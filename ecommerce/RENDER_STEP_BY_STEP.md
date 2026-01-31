# 🚀 Render Deployment - Step by Step (Get Your Frontend Live!)

Follow these steps **exactly** to get your frontend working on Render.

## 📋 Before You Start

1. Make sure your code is pushed to GitHub
2. Have a Render account (sign up at https://render.com if needed)

## 🎯 Step-by-Step Instructions

### Step 1: Create PostgreSQL Database

1. Go to https://dashboard.render.com
2. Click **"New +"** (top right)
3. Select **"PostgreSQL"**
4. Configure:
   - **Name**: `ecommerce-db`
   - **Database**: `ecommerce` (auto-filled)
   - **User**: `ecommerce_user` (auto-filled)
   - **Region**: Choose closest to you
   - **PostgreSQL Version**: Latest (14 or 15)
   - **Plan**: **Free**
5. Click **"Create Database"**
6. ⚠️ **IMPORTANT**: Wait for it to be ready (green status)
7. Click on the database
8. Go to **"Connections"** tab
9. **Copy the "Internal Database URL"** - you'll need this!

### Step 2: Create Web Service

1. In Render Dashboard, click **"New +"**
2. Select **"Web Service"**
3. Connect your GitHub account (if not already)
4. Select your repository
5. Click **"Connect"**

### Step 3: Configure Web Service

Fill in these settings **exactly**:

#### Basic Settings
- **Name**: `ecommerce-app` (or any name you like)
- **Environment**: `Python 3`
- **Region**: Same as your database
- **Branch**: `main` (or your default branch)

#### ⚠️ CRITICAL: Root Directory
- **Root Directory**: `ecommerce`
  - This tells Render where your `manage.py` file is!
  - If your repo structure is `Devops/ecommerce/`, set this to `ecommerce`
  - If your repo root IS the ecommerce folder, leave this empty

#### Build & Start Commands

**Build Command**:
```bash
pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput
```

**Start Command**:
```bash
gunicorn ecommerce.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

**Important Notes**:
- Must use `$PORT` (Render provides this dynamically)
- Must use `0.0.0.0` (not 127.0.0.1)
- The command must be exactly as shown above

### Step 4: Set Environment Variables

Click **"Environment"** tab, then click **"Add Environment Variable"** for each:

1. **SECRET_KEY**
   - Generate one by running locally:
     ```bash
     python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
     ```
   - Copy the output and paste as the value

2. **DEBUG**
   - Value: `False`
   - Must be False for production

3. **DATABASE_URL**
   - Value: Paste the **Internal Database URL** from Step 1
   - Should look like: `postgresql://user:password@host:5432/dbname`

4. **DJANGO_SETTINGS_MODULE**
   - Value: `ecommerce.settings`

5. **PYTHON_VERSION**
   - Value: `3.12.3`

6. **RENDER**
   - Value: `true`
   - This helps Django detect it's running on Render

### Step 5: Deploy

1. Scroll down and click **"Create Web Service"**
2. Wait for the build to start (you'll see logs)
3. **Watch the build logs** - look for:
   - ✅ "Installing dependencies..."
   - ✅ "Running migrations..."
   - ✅ "Collecting static files..."
   - ✅ "Build successful"

### Step 6: Check for Errors

1. Go to **"Logs"** tab
2. Look for any red error messages
3. Common issues:
   - **"No such file: manage.py"** → Root Directory is wrong
   - **"ModuleNotFoundError"** → Check requirements.txt
   - **"Database connection failed"** → Check DATABASE_URL

### Step 7: Run Migrations (If Needed)

If migrations didn't run automatically:

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

### Step 8: Verify It's Working

1. Check service status - should be **"Live"** (green)
2. Click on your service URL (or visit `https://your-app-name.onrender.com`)
3. You should see your homepage!
4. Test these URLs:
   - `/` - Homepage
   - `/products/` - Products page
   - `/cart/` - Cart page

## ✅ Success Checklist

- [ ] Build completed successfully (green checkmark)
- [ ] Service status is "Live"
- [ ] Can access homepage at your Render URL
- [ ] Static files loading (CSS, images)
- [ ] Can navigate to `/products/`
- [ ] Can add items to cart

## 🐛 If Still Getting "Not Found"

### Check These in Order:

1. **Root Directory**: Is it set to `ecommerce`?
   - Go to Settings → Root Directory
   - Should be: `ecommerce`

2. **Start Command**: Does it use `$PORT`?
   - Go to Settings → Start Command
   - Should be: `gunicorn ecommerce.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120`

3. **Build Logs**: Any errors?
   - Go to Logs tab
   - Look for red errors
   - Most common: "No such file: manage.py" = wrong Root Directory

4. **Runtime Logs**: Is the app starting?
   - After build, check Logs tab
   - Should see: "Listening at: http://0.0.0.0:XXXX"
   - If you see errors, they'll tell you what's wrong

5. **Environment Variables**: All set?
   - Go to Environment tab
   - Verify: SECRET_KEY, DEBUG=False, DATABASE_URL, RENDER=true

6. **Database**: Is it running?
   - Check PostgreSQL service status (should be green)
   - Verify DATABASE_URL is correct

## 📞 Need More Help?

1. **Check the Logs** - Most errors are there
2. **Read RENDER_FIX_NOT_FOUND.md** - Detailed troubleshooting
3. **Run check_render.py locally** - Diagnose issues:
   ```bash
   cd ecommerce
   python check_render.py
   ```

## 🎉 You're Done!

Once you see your homepage, your frontend is live! 🚀

---

**Pro Tip**: Free tier spins down after 15 min inactivity. First request after spin-down takes 30-60 seconds.

