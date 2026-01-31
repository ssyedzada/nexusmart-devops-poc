"""
Management command to create dummy products with images
Run with: python manage.py create_dummy_products
"""
from django.core.management.base import BaseCommand
from shop.models import Product


class Command(BaseCommand):
    help = 'Creates dummy products with images for testing'

    def handle(self, *args, **options):
        products_data = [
            {
                "name": "Premium Wireless Headphones",
                "price": 129.99,
                "description": "Noise-cancelling over-ear headphones with 30-hour battery life. Premium sound quality with active noise cancellation technology. Perfect for travel, work, and entertainment.",
                "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            },
            {
                "name": "Ultra-Thin Laptop",
                "price": 899.99,
                "description": "Lightweight laptop with 16GB RAM and 512GB SSD. High-performance processor, stunning display, and all-day battery life. Perfect for professionals and students.",
                "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            },
            {
                "name": "Smart Fitness Watch",
                "price": 249.99,
                "description": "Track heart rate, sleep, and workouts with GPS. Water-resistant design with 7-day battery life. Monitor your health and fitness goals with advanced sensors.",
                "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            },
            {
                "name": "Wireless Charging Pad",
                "price": 39.99,
                "description": "Fast charging pad compatible with all Qi-enabled devices. Sleek design with LED indicator. Supports up to 15W fast charging for compatible devices.",
                "image_url": "https://images.unsplash.com/photo-1563013544-824ae1b704d3?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            },
            {
                "name": "Wireless Earbuds Pro",
                "price": 89.99,
                "description": "Premium wireless earbuds with active noise cancellation. Crystal clear sound quality with 8-hour battery life. Perfect for music lovers and commuters.",
                "image_url": "https://images.unsplash.com/photo-1590658165737-15a0472108b8?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            },
            {
                "name": "Bluetooth Speaker",
                "price": 59.99,
                "description": "Portable Bluetooth speaker with 360-degree sound. Waterproof design with 12-hour battery life. Perfect for outdoor adventures and parties.",
                "image_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            },
            {
                "name": "Gaming Headset",
                "price": 79.99,
                "description": "Professional gaming headset with 7.1 surround sound. Noise-cancelling microphone and RGB lighting. Comfortable for long gaming sessions.",
                "image_url": "https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            },
            {
                "name": "USB-C Hub",
                "price": 49.99,
                "description": "Multi-port USB-C hub with HDMI, USB 3.0, and SD card reader. Compact design perfect for laptops and tablets. Supports 4K video output.",
                "image_url": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            },
            {
                "name": "Mechanical Keyboard",
                "price": 119.99,
                "description": "RGB mechanical keyboard with Cherry MX switches. Programmable keys and customizable lighting. Perfect for gaming and typing enthusiasts.",
                "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            },
            {
                "name": "Wireless Mouse",
                "price": 34.99,
                "description": "Ergonomic wireless mouse with precision tracking. Long battery life and comfortable grip. Perfect for work and gaming.",
                "image_url": "https://images.unsplash.com/photo-1527814050087-3793815479db?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            },
            {
                "name": "4K Monitor",
                "price": 349.99,
                "description": "27-inch 4K UHD monitor with HDR support. Ultra-thin bezels and adjustable stand. Perfect for work, gaming, and content creation.",
                "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            },
            {
                "name": "Portable SSD",
                "price": 99.99,
                "description": "1TB portable SSD with USB-C connectivity. Fast transfer speeds up to 1050MB/s. Compact and durable design perfect for on-the-go storage.",
                "image_url": "https://images.unsplash.com/photo-1591488320449-11f0a6c8f08d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            }
        ]

        created_count = 0
        updated_count = 0

        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data["name"],
                defaults={
                    "price": product_data["price"],
                    "description": product_data["description"],
                    "image_url": product_data["image_url"]
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created: {product.name}')
                )
            else:
                # Update existing product
                product.price = product_data["price"]
                product.description = product_data["description"]
                product.image_url = product_data["image_url"]
                product.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'↻ Updated: {product.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Successfully created {created_count} products'
            )
        )
        if updated_count > 0:
            self.stdout.write(
                self.style.WARNING(f'↻ Updated {updated_count} existing products')
            )

