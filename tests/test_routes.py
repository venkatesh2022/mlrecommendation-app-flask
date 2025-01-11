import unittest
from app import app

class FlaskTestCase(unittest.TestCase):
    def test_home(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(username='testuser', password='testpassword'), follow_redirects=True)
        self.assertIn(b'Logged in successfully!', response.data)
        
    def test_recommend(self):
        tester = app.test_client(self)
        response = tester.post('/recommend', data=dict(movie_id=1), follow_redirects=True)
        self.assertIn(b'Movie recommendations:', response.data)
        
if __name__ == '__main__':
    unittest.main()