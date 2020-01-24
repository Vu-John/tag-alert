#!/usr/bin/env python
import unittest
from app import create_app, db
from app.models import User, Tag, Subreddit
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='john')
        u.set_password('password')
        self.assertFalse(u.check_password('not_a_password'))
        self.assertTrue(u.check_password('password'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    def test_tag(self):
        u1 = User(username='john', email='john@example.com')
        db.session.add(u1)
        db.session.commit()
        self.assertEqual(u1.tags.all(), [])

        # Add Tag
        tag = Tag(text='first')
        db.session.add(tag)
        u1.tags.append(tag)
        db.session.commit()

        self.assertTrue(u1.tags.all() == [tag])
        self.assertEqual(u1.tags.count(), 1)
        self.assertEqual(u1.tags.first().text, 'first')

        # Delete Tag
        u1.tags.remove(tag)
        db.session.commit()
        self.assertEqual(u1.tags.all(), [])

    def test_subreddit(self):
        u1 = User(username='john', email='john@example.com')
        db.session.add(u1)
        db.session.commit()
        self.assertEqual(u1.subreddits.all(), [])

        # Add Subreddit
        subreddit = Subreddit(sub='popular')
        db.session.add(subreddit)
        u1.subreddits.append(subreddit)
        db.session.commit()

        self.assertTrue(u1.subreddits.all() == [subreddit])
        self.assertEqual(u1.subreddits.count(), 1)
        self.assertEqual(u1.subreddits.first().sub, 'popular')

        # Delete Subreddit
        u1.subreddits.remove(subreddit)
        db.session.commit()
        self.assertEqual(u1.subreddits.all(), [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
