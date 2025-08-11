import pytest
from django.test import client, TestCase
from django.urls import reverse

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None
from modules.api.models import Category, Product
from modules.authentication.models import UserProfile as User


class TestCatalogView(TestCase):
    """Test cases for the catalog HTML page"""

    def setUp(self):
        """Set up test data"""
        self.client = client.Client()

        # Create sample user
        self.sample_user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        # Create categories
        self.category1 = Category.objects.create(
            name="Electronics", description="Electronic devices and gadgets"
        )
        self.category2 = Category.objects.create(
            name="Clothing", description="Fashion and apparel"
        )
        self.category3 = Category.objects.create(
            name="Empty Category", description="Category with no products"
        )

        # Create products
        prod = Product.objects.create(
            name="Smartphone", description="Latest smartphone", price=599.99, stock=10
        )
        prod.categories.add(self.category1)
        prod.save()

        prod = Product.objects.create(
            name="Laptop", description="Gaming laptop", price=1299.99, stock=5
        )
        prod.categories.add(self.category1)
        prod.save()

        prod = Product.objects.create(
            name="T-Shirt", description="Cotton t-shirt", price=29.99, stock=20
        )
        prod.categories.add(self.category2)
        prod.save()

        prod = Product.objects.create(
            name="Jeans", description="Blue jeans", price=79.99, stock=15
        )
        prod.categories.add(self.category2)
        prod.save()

    def test_catalog_page_loads_successfully(self):
        """Test that the catalog page loads with 200 status"""
        url = reverse("catalog")  # Adjust URL name as needed
        response = self.client.get(url)
        assert response.status_code == 200

    def test_catalog_uses_correct_template(self):
        """Test that the catalog view uses the correct template"""
        url = reverse("catalog")
        response = self.client.get(url)
        assert "api/product/catalog.html" in [t.name for t in response.templates]

    def test_catalog_extends_base_template(self):
        """Test that catalog template extends base_generic.html"""
        url = reverse("catalog")
        response = self.client.get(url)

        # Check for base template elements
        assert "base_generic.html" in str(response.templates[0].source)

    def test_catalog_includes_required_css_and_js(self):
        """Test that required CSS and JS files are included"""
        url = reverse("catalog")
        response = self.client.get(url)
        content = response.content.decode("utf-8")

        # Check for CSS
        assert "api/css/styles.css" in content
        # Check for JS
        assert "api/js/toggleDropdown.js" in content

    def test_catalog_title_is_correct(self):
        """Test that the page title is correct"""
        url = reverse("catalog")
        response = self.client.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        title = soup.find("title").get_text()
        assert title and "Catalog" in title

        # Also check h2 title
        h2_title = soup.find("h2", class_="cart-title")
        assert h2_title and h2_title.get_text().strip() == "Catalog"

    def test_catalog_displays_categories(self):
        """Test that categories are displayed correctly"""
        url = reverse("catalog")
        response = self.client.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Check categories container exists
        categories_div = soup.find("div", class_="categories")
        assert categories_div

        # Check dropdown buttons for categories
        dropdown_buttons = soup.find_all("button", class_="dropdown-btn")
        assert len(dropdown_buttons) == 3  # We created 3 categories

        # Check category names
        category_names = [btn.get_text().strip() for btn in dropdown_buttons]
        assert "Electronics" in category_names
        assert "Clothing" in category_names
        assert "Empty Category" in category_names

    def test_catalog_displays_products_in_categories(self):
        """Test that products are displayed within their categories"""
        url = reverse("catalog")
        response = self.client.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all dropdown content areas
        dropdown_contents = soup.find_all("ul", class_="dropdown-content")

        # Check that we have dropdown content for each category
        assert len(dropdown_contents) == 3

        # Check specific products are linked correctly
        product_links = soup.find_all("a", class_="product-link")
        product_names = [
            link.get_text().strip()
            for link in product_links
            if "View All" not in link.get_text()
        ]

        assert "Smartphone" in product_names
        assert "Laptop" in product_names
        assert "T-Shirt" in product_names
        assert "Jeans" in product_names

    def test_catalog_product_links_are_correct(self):
        """Test that product links have correct URLs"""
        url = reverse("catalog")
        response = self.client.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find product links (excluding "View All" links)
        product_links = soup.find_all("a", class_="product-link")
        product_detail_links = [
            link for link in product_links if "View All" not in link.get_text()
        ]

        # Check that links contain product detail URLs
        for link in product_detail_links:
            href = link.get("href")
            assert href and (
                "/catalog/" in href or "product_detail" in href
            )  # Adjust based on your URL pattern

    def test_catalog_category_view_all_links(self):
        """Test that 'View All' links are present and correct"""
        url = reverse("catalog")
        response = self.client.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find "View All" links
        view_all_links = soup.find_all("a", string="View All")
        assert len(view_all_links) == 3  # One for each category

        # Check that links have correct URLs
        for link in view_all_links:
            href = link.get("href")
            assert href and "categories" in href

    def test_catalog_empty_category_message(self):
        """Test that empty categories show appropriate message"""
        url = reverse("catalog")
        response = self.client.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the empty category dropdown
        dropdown_contents = soup.find_all("ul", class_="dropdown-content")

        # Check for "No products in this category" message
        empty_messages = soup.find_all("li", string="No products in this category")
        assert len(empty_messages) == 1  # Should have one empty category

    def test_catalog_dropdown_functionality_attributes(self):
        """Test that dropdown elements have correct attributes for functionality"""
        url = reverse("catalog")
        response = self.client.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Check dropdown buttons have onclick attribute
        dropdown_buttons = soup.find_all("button", class_="dropdown-btn")
        for button in dropdown_buttons:
            onclick = button.get("onclick")
            assert onclick and "toggleDropdown" in onclick

        # Check dropdown content has correct initial style
        dropdown_contents = soup.find_all("ul", class_="dropdown-content")
        for content in dropdown_contents:
            style = content.get("style")
            assert "display: none" in style

    def test_catalog_html_structure(self):
        """Test the overall HTML structure of the catalog page"""
        url = reverse("catalog")
        response = self.client.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Check main container
        container = soup.find("main", class_="container")
        assert container

        # Check title structure
        title = container.find("h2", class_="cart-title")
        assert title and title.get_text().strip() == "Catalog"

        # Check categories structure
        categories_div = container.find("div", class_="categories")
        assert categories_div

        # Check dropdown structure
        dropdowns = categories_div.find_all("div", class_="dropdown")
        assert len(dropdowns) > 0

        for dropdown in dropdowns:
            # Each dropdown should have a button and ul
            button = dropdown.find("button", class_="dropdown-btn")
            ul = dropdown.find("ul", class_="dropdown-content")
            assert button and ul
