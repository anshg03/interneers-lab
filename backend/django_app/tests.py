from django.test import TestCase,Client
from django.urls import reverse
import json

class HelloNameTests(TestCase):
    def setUp(self):
        self.client=Client()
    
    def test_valid_name(self):
        response=self.client.get(reverse('hello_world')+"?name=Bobdon")
        self.assertEqual(response.status_code,200)
        self.assertEqual(response['Content-Type'],'application/json')
        
        data=json.loads(response.content)
        self.assertEqual(data["message"],f'Hello, Bobdon!')
    
    def test_empty_name(self):
        response = self.client.get(reverse('hello_world') + "?name=")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response['Content-Type'],'application/json')
        
        data=json.loads(response.content)
        self.assertEqual(data["error"], "Invalid name. Name cannot be empty.")

    def test_hello_name_too_long(self):
        response = self.client.get(reverse('hello_world') + "?name=BobdonBobdon")
        self.assertEqual(response.status_code, 400) 
        self.assertEqual(response['Content-Type'], 'application/json')

        data = json.loads(response.content)
        self.assertEqual(data['error'], "Invalid name. Length must be less than 10.")
    
    def test_name_with_special(self):
        response = self.client.get(reverse('hello_world') + "?name=Don123@")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response['Content-Type'],'application/json')
        
        data=json.loads(response.content)
        self.assertEqual(data["error"], "Invalid name. Only letters are allowed.")
        