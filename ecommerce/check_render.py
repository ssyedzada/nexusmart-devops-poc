#!/usr/bin/env python
"""
Quick diagnostic script to check if the app is configured correctly for Render.
Run this locally to verify your setup before deploying.
"""
import os
import sys

def check_settings():
    """Check if settings are configured correctly"""
    print("🔍 Checking Django Settings...")
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
    
    try:
        import django
        django.setup()
        
        from django.conf import settings
        
        print("✅ Django settings loaded successfully")
        print(f"   DEBUG: {settings.DEBUG}")
        print(f"   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        print(f"   Database: {settings.DATABASES['default']['ENGINE']}")
        print(f"   Static Root: {settings.STATIC_ROOT}")
        print(f"   WSGI Application: {settings.WSGI_APPLICATION}")
        
        return True
    except Exception as e:
        print(f"❌ Error loading settings: {e}")
        return False

def check_urls():
    """Check if URLs are configured"""
    print("\n🔍 Checking URL Configuration...")
    
    try:
        from django.urls import get_resolver
        from django.conf import settings
        
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
        import django
        django.setup()
        
        resolver = get_resolver()
        url_patterns = resolver.url_patterns
        
        print("✅ URL patterns loaded")
        print(f"   Root URL patterns: {len(url_patterns)}")
        
        # Check if home route exists
        try:
            from django.urls import reverse
            home_url = reverse('home')
            print(f"   ✅ Home URL configured: {home_url}")
        except Exception as e:
            print(f"   ⚠️  Home URL issue: {e}")
        
        return True
    except Exception as e:
        print(f"❌ Error checking URLs: {e}")
        return False

def check_requirements():
    """Check if requirements are installed"""
    print("\n🔍 Checking Requirements...")
    
    required_packages = [
        'django',
        'gunicorn',
        'whitenoise',
        'dj_database_url',
        'psycopg2',
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    return True

def check_files():
    """Check if required files exist"""
    print("\n🔍 Checking Required Files...")
    
    required_files = [
        'manage.py',
        'requirements.txt',
        'ecommerce/wsgi.py',
        'ecommerce/settings.py',
        'ecommerce/urls.py',
        'shop/urls.py',
        'shop/views.py',
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - NOT FOUND")
            all_exist = False
    
    return all_exist

def main():
    print("=" * 60)
    print("🚀 Render Deployment Diagnostic Tool")
    print("=" * 60)
    
    results = []
    
    results.append(("Files", check_files()))
    results.append(("Requirements", check_requirements()))
    results.append(("Settings", check_settings()))
    results.append(("URLs", check_urls()))
    
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All checks passed! Your app should work on Render.")
        print("\n📝 Next steps:")
        print("   1. Push code to GitHub")
        print("   2. Deploy on Render using render.yaml or manual setup")
        print("   3. Set environment variables in Render dashboard")
        print("   4. Run migrations: python manage.py migrate")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
    print("=" * 60)

if __name__ == '__main__':
    main()

