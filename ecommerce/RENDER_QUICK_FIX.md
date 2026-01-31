# 🚨 Quick Fix for "Not Found" Error on Render

## Most Common Causes & Fixes

### ✅ Fix 1: Correct Start Command
**Problem**: Using wrong port or command

**Solution**: In Render Dashboard → Your Service → Settings → Start Command:
```bash
gunicorn ecommerce.wsgi:application --bind 0.0.0.0:$PORT
```

**Important**: 
- Must use `$PORT` (not 8000)
- Must use `0.0.0.0` (not 127.0.0.1)

---

### ✅ Fix 2: Set Root Directory
**Problem**: Render can't find your `manage.py`

**Solution**: In Render Dashboard → Your Service → Settings:
- Set **Root Directory** to: `ecommerce`
- (Only if your code is in the `ecommerce` folder)

---

### ✅ Fix 3: Environment Variables
**Problem**: Missing required environment variables

**Solution**: In Render Dashboard → Your Service → Environment → Add:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Generate one: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | `False` |
| `DATABASE_URL` | From your PostgreSQL service (Internal Database URL) |
| `DJANGO_SETTINGS_MODULE` | `ecommerce.settings` |

---

### ✅ Fix 4: Build Command
**Problem**: Static files not collected

**Solution**: In Render Dashboard → Your Service → Settings → Build Command:
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

---

### ✅ Fix 5: Run Migrations
**Problem**: Database not set up

**Solution**: 
1. Go to your service in Render
2. Click "Shell" tab
3. Run:
   ```bash
   python manage.py migrate
   ```

---

### ✅ Fix 6: Check Logs
**Problem**: Need to see actual error

**Solution**:
1. Go to your service in Render
2. Click "Logs" tab
3. Look for red error messages
4. Common errors:
   - `ModuleNotFoundError` → Check requirements.txt
   - `Database connection failed` → Check DATABASE_URL
   - `Port already in use` → Use $PORT in start command

---

## 🎯 Quick Checklist

Before deploying, ensure:
- [ ] Start command uses `$PORT`
- [ ] Root Directory is set correctly (if needed)
- [ ] `SECRET_KEY` environment variable is set
- [ ] `DATABASE_URL` environment variable is set
- [ ] Build command includes `collectstatic`
- [ ] Migrations have been run
- [ ] All code is pushed to GitHub

---

## 📞 Still Not Working?

1. **Check the Logs** - Most errors are visible there
2. **Verify Build Succeeded** - Green checkmark in Render
3. **Test Locally First** - Make sure it works with: `gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8000`
4. **Check Render Status Page** - https://status.render.com

---

**Pro Tip**: After making changes, click "Manual Deploy" → "Deploy latest commit" to redeploy immediately.

