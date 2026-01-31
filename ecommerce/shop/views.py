from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json
from .models import Product


def home(request):
    # Get featured products from database (first 4 products)
    featured_products = Product.objects.all()[:4]
    
    # If no products in database, show empty message
    return render(request, "shop/home.html", {"products": featured_products})


def product_list(request):
    # Get all products from database
    products = Product.objects.all()
    return render(request, "shop/products.html", {"products": products})


def product_detail(request, product_id):
    """Display product detail page"""
    product = get_object_or_404(Product, id=product_id)
    return render(request, "shop/product_detail.html", {"product": product})


def get_cart(request):
    """Helper function to get cart from session"""
    if 'cart' not in request.session:
        request.session['cart'] = {}
    return request.session['cart']


def get_cart_items(request):
    """Helper function to get cart items with product details"""
    cart = get_cart(request)
    cart_items = []
    
    if not cart:
        return cart_items
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            price = float(product.price)
            cart_items.append({
                "id": product.id,
                "name": product.name,
                "price": price,
                "quantity": int(quantity),
                "total": price * int(quantity),
                "image": product.image_url if product.image_url else f"https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=100&h=100&fit=crop",
            })
        except (Product.DoesNotExist, ValueError, TypeError) as e:
            # Remove invalid product from cart
            if str(product_id) in cart:
                del cart[str(product_id)]
                request.session['cart'] = cart
                request.session.modified = True
    
    return cart_items


def cart(request):
    """Display shopping cart"""
    # Debug: Check session
    cart_session = request.session.get('cart', {})
    
    cart_items = get_cart_items(request)
    
    # Calculate totals using float for consistency
    subtotal = sum(item["price"] * item["quantity"] for item in cart_items) if cart_items else 0.0
    subtotal = float(subtotal)  # Ensure it's a float
    shipping = 9.99 if subtotal > 0 else 0.0
    tax = subtotal * 0.20  # 20% tax (using float instead of Decimal)
    total = subtotal + shipping + tax
    
    context = {
        "cart_items": cart_items,
        "subtotal": round(subtotal, 2),
        "shipping": round(shipping, 2),
        "tax": round(tax, 2),
        "total": round(total, 2),
        "cart_debug": cart_session,  # For debugging
    }
    return render(request, "shop/cart.html", context)


def add_to_cart(request, product_id):
    """Add product to cart"""
    if request.method == "POST":
        try:
            product = get_object_or_404(Product, id=product_id)
            
            # Ensure cart exists in session
            if 'cart' not in request.session:
                request.session['cart'] = {}
            
            cart = request.session['cart']
            product_id_str = str(product_id)
            quantity = int(request.POST.get('quantity', 1))
            
            # Update cart
            if product_id_str in cart:
                cart[product_id_str] += quantity
            else:
                cart[product_id_str] = quantity
            
            # Save cart to session
            request.session['cart'] = cart
            request.session.modified = True
            
            # Force session save
            request.session.save()
            
            messages.success(request, f"{product.name} added to cart!")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # AJAX request
                cart_count = sum(cart.values())
                return JsonResponse({
                    'success': True,
                    'message': f'{product.name} added to cart!',
                    'cart_count': cart_count
                })
            
            # Redirect to cart to show the item was added
            return redirect('cart')
            
        except Product.DoesNotExist:
            messages.error(request, "Product not found!")
            return redirect('product_list')
        except ValueError as e:
            messages.error(request, f"Invalid quantity: {str(e)}")
            return redirect('product_detail', product_id=product_id)
        except Exception as e:
            # Log the error for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error adding product {product_id} to cart: {str(e)}")
            messages.error(request, f"Error adding product to cart. Please try again.")
            return redirect('product_detail', product_id=product_id)
    else:
        # GET request - redirect to product detail
        return redirect('product_detail', product_id=product_id)


def update_cart(request, product_id):
    """Update quantity of item in cart"""
    if request.method == "POST":
        cart = get_cart(request)
        product_id_str = str(product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        if product_id_str in cart:
            if quantity > 0:
                cart[product_id_str] = quantity
                messages.success(request, "Cart updated!")
            else:
                # Remove if quantity is 0
                del cart[product_id_str]
                messages.success(request, "Item removed from cart!")
            
            request.session['cart'] = cart
            request.session.modified = True
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # AJAX request - return updated totals
                cart_items = get_cart_items(request)
                subtotal = sum(item["price"] * item["quantity"] for item in cart_items)
                shipping = 9.99 if subtotal > 0 else 0
                tax = subtotal * 0.20
                total = subtotal + shipping + tax
                
                return JsonResponse({
                    'success': True,
                    'subtotal': round(subtotal, 2),
                    'shipping': round(shipping, 2),
                    'tax': round(tax, 2),
                    'total': round(total, 2)
                })
        
        return redirect('cart')
    
    return redirect('cart')


def remove_from_cart(request, product_id):
    """Remove item from cart"""
    if request.method == "POST":
        cart = get_cart(request)
        product_id_str = str(product_id)
        
        if product_id_str in cart:
            try:
                product = Product.objects.get(id=product_id)
                product_name = product.name
            except Product.DoesNotExist:
                product_name = "Item"
            
            del cart[product_id_str]
            request.session['cart'] = cart
            request.session.modified = True
            
            messages.success(request, f"{product_name} removed from cart!")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # AJAX request
                cart_items = get_cart_items(request)
                subtotal = sum(item["price"] * item["quantity"] for item in cart_items)
                shipping = 9.99 if subtotal > 0 else 0
                tax = subtotal * 0.20
                total = subtotal + shipping + tax
                
                return JsonResponse({
                    'success': True,
                    'subtotal': round(subtotal, 2),
                    'shipping': round(shipping, 2),
                    'tax': round(tax, 2),
                    'total': round(total, 2),
                    'cart_count': sum(cart.values())
                })
        
        return redirect('cart')
    
    return redirect('cart')


def checkout(request):
    """Fake checkout process"""
    cart_items = get_cart_items(request)
    
    if not cart_items:
        messages.warning(request, "Your cart is empty!")
        return redirect("cart")
    
    if request.method == "POST":
        # In a real app, this would process the order
        # Clear cart after successful checkout
        request.session['cart'] = {}
        request.session.modified = True
        messages.success(request, "Order placed successfully! (This is a demo)")
        return redirect("home")
    
    # Calculate order summary from cart
    subtotal = sum(item["price"] * item["quantity"] for item in cart_items)
    shipping = 9.99 if subtotal > 0 else 0
    tax = subtotal * 0.20
    total = subtotal + shipping + tax
    
    order_summary = {
        "subtotal": round(subtotal, 2),
        "shipping": round(shipping, 2),
        "tax": round(tax, 2),
        "total": round(total, 2),
        "items": cart_items,
    }
    return render(request, "shop/checkout.html", {"order_summary": order_summary})


@require_http_methods(["GET", "POST"])
def admin_login(request):
    """Hidden admin login page (password: devops2025)"""
    if request.method == "POST":
        password = request.POST.get("password", "")
        if password == "devops2025":
            # Create or get a superuser for admin access
            from django.contrib.auth.models import User
            user, created = User.objects.get_or_create(
                username="admin",
                defaults={"email": "admin@nexusmart.com", "is_staff": True, "is_superuser": True}
            )
            if created:
                user.set_password("devops2025")
                user.save()
            else:
                # Update existing user to ensure they have correct password
                user.set_password("devops2025")
                user.is_staff = True
                user.is_superuser = True
                user.save()
            
            # Authenticate and login
            user = authenticate(request, username="admin", password="devops2025")
            if user:
                login(request, user)
                messages.success(request, "Admin login successful!")
                return redirect("admin_dashboard")
            else:
                messages.error(request, "Authentication failed. Please try again.")
        else:
            messages.error(request, "Incorrect password. Access denied.")
    
    return render(request, "shop/admin_login.html")


def admin_dashboard(request):
    """Hidden admin dashboard (only accessible after login)"""
    if not request.user.is_authenticated:
        messages.warning(request, "Please login to access the admin dashboard.")
        return redirect("admin_login")
    
    # Get statistics
    total_products = Product.objects.count()
    recent_products = Product.objects.all()[:5]
    
    context = {
        "total_products": total_products,
        "recent_products": recent_products,
        "user": request.user,
    }
    return render(request, "shop/admin_dashboard.html", context)
