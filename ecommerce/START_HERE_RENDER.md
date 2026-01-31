# 🚀 START HERE - Get Your Frontend Live on Render

## ⚡ Quick Fix (5 Minutes)

The **#1 reason** for "Not Found" is **wrong Root Directory**. Follow these steps:

### 1. In Render Dashboard → Your Service → Settings

Set **Root Directory** to:
```
ecommerce
```

### 2. Verify Start Command

Should be:
```bash
gunicorn ecommerce.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

### 3. Verify Build Command

Should be:
```bash
pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput
```

### 4. Check Environment Variables

Must have:
- `SECRET_KEY` (generate one)
- `DEBUG=False`
- `DATABASE_URL` (from your PostgreSQL)
- `RENDER=true`

### 5. Redeploy

Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## 📚 Full Instructions

See **RENDER_STEP_BY_STEP.md** for complete step-by-step guide.

## 🐛 Still Not Working?

See **RENDER_FIX_NOT_FOUND.md** for detailed troubleshooting.

---

## ✅ What You Should See When It Works

1. **Build Status**: ✅ Green checkmark
2. **Service Status**: "Live" (green)
3. **Your URL**: Shows your homepage (not "Not Found")
4. **Logs**: Show "Listening at: http://0.0.0.0:XXXX"

---

**Most Common Issue**: Root Directory not set to `ecommerce`!

Fix it and redeploy. Your frontend will be live! 🎉

