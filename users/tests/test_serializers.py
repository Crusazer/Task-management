from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from users.serializers import RegisterCustomerSerializer, RegisterEmployeeSerializer
from PIL import Image
import io


def generate_test_image():
    image = Image.new('RGB', (100, 100), color=(73, 109, 137))
    byte_arr = io.BytesIO()
    image.save(byte_arr, format='JPEG')
    return byte_arr.getvalue()


class RegisterEmployeeSerializerTest(TestCase):
    def test_serializer_with_valid_data(self):
        photo = SimpleUploadedFile("test_photo.jpg", generate_test_image(), content_type="jpeg")
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'test@example.com',
            'name': 'Test User',
            'phone': '+375441112233',
            'photo': photo,
        }
        serializer = RegisterEmployeeSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_with_missing_photo(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'test@example.com',
            'name': 'Test User',
            'phone': '+375441112233',
        }
        serializer = RegisterEmployeeSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_with_invalid_phone(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'test@example.com',
            'name': 'Test User',
            'phone': '+1234567890',
        }
        serializer = RegisterEmployeeSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class RegisterCustomerSerializerTest(TestCase):
    def test_serializer_with_valid_data(self):
        photo = SimpleUploadedFile("test_photo.jpg", generate_test_image(), content_type="jpeg")
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'test@example.com',
            'name': 'Test User',
            'phone': '+375441112233',
            'photo': photo,
        }
        serializer = RegisterCustomerSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_with_missing_photo(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'test@example.com',
            'name': 'Test User',
            'phone': '+375441112233',
        }
        serializer = RegisterCustomerSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_with_invalid_phone(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'test@example.com',
            'name': 'Test User',
            'phone': '+1234567890',
        }
        serializer = RegisterCustomerSerializer(data=data)
        self.assertFalse(serializer.is_valid())
