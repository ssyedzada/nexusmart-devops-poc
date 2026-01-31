from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from .models import Product


class ProductModelTest(TestCase):
    """Test Product model"""
    
    def setUp(self):
        Product.objects.create(
            name="Test Product",
            price=29.99,
            description="Test description",
            image_url="https://example.com/image.jpg"
        )

    def test_product_creation(self):
        """Test that product is created correctly"""
        product = Product.objects.get(name="Test Product")
        self.assertEqual(product.price, Decimal('29.99'))
        self.assertEqual(product.description, "Test description")
        self.assertEqual(str(product), "Test Product")

    def test_product_str(self):
        """Test product string representation"""
        product = Product.objects.get(name="Test Product")
        self.assertEqual(str(product), "Test Product")


class ViewTests(TestCase):
    """Test views"""
    
    def setUp(self):
        self.client = Client()
        Product.objects.create(
            name="Test Product",
            price=29.99,
            description="Test description"
        )

    def test_home_view(self):
        """Test home page loads"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "NexusMart")

    def test_product_list_view(self):
        """Test product list page loads"""
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view(self):
        """Test product detail page loads"""
        product = Product.objects.first()
        response = self.client.get(reverse('product_detail', args=[product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, product.name)

    def test_cart_view(self):
        """Test cart page loads"""
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)

    def test_checkout_view_get(self):
        """Test checkout page loads"""
        # Add items to cart first (checkout requires items in cart)
        product = Product.objects.first()
        if product:
            # Add product to cart via session
            session = self.client.session
            session['cart'] = {str(product.id): 1}
            session.save()
            response = self.client.get(reverse('checkout'))
            self.assertEqual(response.status_code, 200)
        else:
            # If no products, checkout should redirect to cart
            response = self.client.get(reverse('checkout'))
            self.assertEqual(response.status_code, 302)

    def test_checkout_view_post(self):
        """Test checkout form submission"""
        response = self.client.post(reverse('checkout'), {})
        # Should redirect after successful checkout
        self.assertEqual(response.status_code, 302)

    def test_admin_login_view_get(self):
        """Test admin login page loads"""
        response = self.client.get(reverse('admin_login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Admin Access")

    def test_admin_login_view_post_correct_password(self):
        """Test admin login with correct password"""
        response = self.client.post(reverse('admin_login'), {
            'password': 'devops2025'
        })
        # Should redirect to dashboard
        self.assertEqual(response.status_code, 302)

    def test_admin_login_view_post_incorrect_password(self):
        """Test admin login with incorrect password"""
        response = self.client.post(reverse('admin_login'), {
            'password': 'wrongpassword'
        })
        # Should stay on login page
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Incorrect password")

    def test_admin_dashboard_requires_login(self):
        """Test admin dashboard requires authentication"""
        response = self.client.get(reverse('admin_dashboard'))
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
