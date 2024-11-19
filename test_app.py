import unittest
from app import app, db, User

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
        # Create database and tables
        with app.app_context():
            db.create_all()
            user = User(first_name="John", last_name="Doe", image_url="http://example.com/image.png")
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index_redirect(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)  # Redirects to /users
        self.assertIn(b'You should be redirected automatically to target URL:', response.data)

    def test_list_users(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Doe', response.data)  # Check if the user is listed

    def test_new_user(self):
        response = self.app.post('/users/new', data=dict(
            first_name='Jane',
            last_name='Smith',
            image_url='http://example.com/jane.png'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Jane Smith', response.data)  # Check if the new user is listed

    def test_user_detail(self):
        user = User.query.first()
        response = self.app.get(f'/users/{user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Doe', response.data)  # Check if the user details are shown

if __name__ == '__main__':
    unittest.main()
