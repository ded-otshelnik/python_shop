# python_shop

A simple Python shop application built with Django

## Features

- Product catalog with categories
- Shopping cart functionality
- User authentication and registration
- Order management
- Admin panel for inventory management
- Search and filtering capabilities

## How to Run

1. Clone the repository:

    ```bash
    git clone <repository-url>
    cd python_shop
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run migrations:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser (optional):

    ```bash
    python manage.py createsuperuser
    ```

6. Start the development server:

    ```bash
    python manage.py runserver
    ```

The application will be available at `http://localhost:8000`

## API Endpoints

### Products & Categories

- `GET /api/products/` - List catalog
- `GET /api/products/{id}/` - Get product details
- `POST /api/products/` - Create new product (admin only)
- `PUT /api/products/{id}/` - Update product (admin only)
- `DELETE /api/products/{id}/` - Delete product (admin only)
- `GET /api/categories/{id}/` - Get category details

### Cart

- `GET /api/cart/` - Get user's cart
- `POST /api/cart/add/` - Add item to cart
- `PUT /api/cart/update/{id}/` - Update cart item quantity
- `DELETE /api/cart/remove/{id}/` - Remove item from cart

### Orders

- `GET /api/orders/` - List user's orders
- `POST /api/orders/` - Create new order
- `GET /api/orders/{id}/` - Get order details

### Authentication

- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile
