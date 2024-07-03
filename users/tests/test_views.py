from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .test_serializers import generate_test_image
from ..models import Employee, Customer

User = get_user_model()


class RegisterEmployeeViewTest(APITestCase):

    def test_register_employee(self):
        url = reverse('register-employee')
        photo = SimpleUploadedFile("test_photo.jpg", generate_test_image(), content_type="jpeg")
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'test@example.com',
            'name': 'Test User',
            'phone': '+375441112233',
            'photo': photo
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=f"Employee didn't create. {response.data}")
        self.assertIn('access', response.data, msg="Access token not created")
        self.assertIn('refresh', response.data, msg="Refresh token not created")

    class RegisterEmployeeViewTest(APITestCase):

        def test_register_employee_without_photo(self):
            url = reverse('register-employee')
            data = {
                'username': 'testuser',
                'password': 'testpassword123',
                'email': 'test@example.com',
                'name': 'Test User',
                'phone': '+375441112233',
            }
            response = self.client.post(url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('photo', response.data)
            self.assertEqual(response.data['photo'][0], 'No file was submitted.')


class CurrentUserViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('current-user')

    def get_jwt_token(self):
        refresh = RefreshToken.for_user(self.user)
        return str(refresh.access_token)

    def test_get_current_user_authenticated(self):
        token = self.get_jwt_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_get_current_user_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserDetailViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser1', password='testpassword1',
                                             email='testuser1@example.com')
        self.other_user = User.objects.create_user(username='otheruser1', password='otherpassword1',
                                                   email='otheruser1@example.com')
        self.url = reverse('user-detail', kwargs={'pk': self.user.pk})

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_get_user_detail_authenticated(self):
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser1')

    def test_get_user_detail_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_other_user_detail_authenticated(self):
        token = self.get_jwt_token(self.user)
        other_user_url = reverse('user-detail', kwargs={'pk': self.other_user.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(other_user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'otheruser1')


class UserListViewTest(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='password',
                                                   email='admin@example.com', role=User.Role.ADMIN)
        self.employee_user = Employee.objects.create(username='employee', password='password',
                                                          email='email2@example.com', role=User.Role.EMPLOYEE)
        self.customer_user = Customer.objects.create(username='customer', password='password',
                                                          email='email3@example.com', role=User.Role.CUSTOMER)

        self.url = reverse('user-list')

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_filter_by_employee_role(self):
        token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = self.client.get(self.url, {'role': 'employee'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['role'], 'EMPLOYEE')

    def test_filter_by_customer_role(self):
        token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = self.client.get(self.url, {'role': 'customer'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['role'], 'CUSTOMER')

    def test_filter_by_unknown_role(self):
        token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = self.client.get(self.url, {'role': 'unknown'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['count'], 0,)

    def test_without_filter_role(self):
        token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['count'], 3, msg=f'{response.data}')
