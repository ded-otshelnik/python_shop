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

6. Set environment variables:

    Create a `.env.conf` file in the `src/config/` directory and add the following line:

    ```env
    DJANGO_ENV=dev
    ```

7. Start the development server:

    ```bash
    python src/bin/manage.py runserver
    ```

The application will be available at `http://localhost:8000`

## Web API Endpoints

### Products & Categories

- `GET /catalog/` - Catalog of products ordered by categories
- `GET /catalog/{id}/` - Product details by ID
- `GET /categories/{id}/` - Products in a specific category

### Cart

- `GET /cart/` - Get user's cart
- `POST /cart/{id}` - Add item to user's cart

### Orders

- `GET /orders/` - List user's orders
- `POST /orders/` - Create new order
- `GET /orders/{id}/` - Get order details

### Authentication

- `POST /auth/login/` - User login
- `POST /auth/signup/` - User registration
- `GET /auth/profile/` - Get user profile
