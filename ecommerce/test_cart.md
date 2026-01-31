# Testing Cart Functionality

## Steps to Test:

1. **Make sure you have products in the database:**
   ```bash
   python manage.py create_dummy_products
   ```

2. **Start the server:**
   ```bash
   python manage.py runserver
   ```

3. **Test the cart:**
   - Go to http://localhost:8000/
   - Click "Add to Cart" on any product
   - You should be redirected to /cart/ and see the product
   - Check the debug message at the top of the cart page

## Common Issues:

### Issue: Cart is empty after adding items
**Solution:** Check:
- Is the session middleware enabled? (It should be in settings.py)
- Are you using the same browser session?
- Check browser console for any JavaScript errors

### Issue: Products not showing in cart
**Possible causes:**
- Products don't exist in database (run create_dummy_products)
- Session not persisting (check SESSION settings)
- Product ID mismatch

## Debug Information:

The cart page now shows debug information at the top showing how many items are in the session.

