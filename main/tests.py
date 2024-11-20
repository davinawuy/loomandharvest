from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product

class MainAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        self.product = Product.objects.create(
            name="Test Product",
            price=10.99,
            description="A test product",
            stock=5,
            category="Test Category",
            user=self.user
        )


    def test_delete_product(self):
        response = self.client.post(reverse('main:delete_Product', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)

    def test_show_xml(self):
        response = self.client.get(reverse('main:show_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

    def test_show_json(self):
        response = self.client.get(reverse('main:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_show_xml_by_id(self):
        response = self.client.get(reverse('main:show_xml_by_id', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

    def test_show_json_by_id(self):
        response = self.client.get(reverse('main:show_json_by_id', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')


    def test_login_user(self):
        response = self.client.post(reverse('main:login'), {
            'username': 'testuser',
            'password': 'password',
        })
        self.assertEqual(response.status_code, 302)



    def test_add_product_ajax(self):
        response = self.client.post(reverse('main:add_Product_ajax'), {
            'name': 'AJAX Product',
            'price': 5.99,
            'description': 'AJAX description',
            'stock': 10,
            'category': 'AJAX Category',
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 201)
