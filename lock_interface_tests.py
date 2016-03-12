#! /usr/bin/env python

import os
import tempfile
import unittest

import lock_interface


class LockInterfaceTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, lock_interface.app.config['DATABASE'] = tempfile.mkstemp()
        lock_interface.app.config['TESTING'] = True
        self.app = lock_interface.app.test_client()
        lock_interface.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(lock_interface.app.config['DATABASE'])

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_index_page(self):
        rv = self.app.get('/')
        assert rv.status_code == 302
        rv = self.login('admin', 'default')
        assert 'Add User' in rv.data.decode("utf-8")

    def test_logout(self):
        rv = self.login('admin', 'default')
        assert 'Add User' in rv.data.decode("utf-8")
        rv = self.logout()
        assert 'You were logged out' in rv.data.decode("utf-8")

    def test_404(self):
        rv = self.app.get('/random_url')
        assert rv.status_code == 404

    def test_login_page(self):
        rv = self.app.get('/login')
        assert rv.status_code == 200
        rv = self.login('badusername', lock_interface.PASSWORD)
        assert 'Invalid username' in rv.data.decode("utf-8")
        rv = self.login(lock_interface.USERNAME, 'badpassword')
        assert 'Invalid password' in rv.data.decode("utf-8")
        rv = self.login(lock_interface.USERNAME, lock_interface.PASSWORD)
        assert 'You were logged in' in rv.data.decode("utf-8")

    def test_adding_entry(self):
        self.login(lock_interface.USERNAME, lock_interface.PASSWORD)
        self.app.post('/add', data=dict(
            name='Joe Shmoe',
            note='test node',
            binary='00000010010101'))
        rv = self.app.get('/')
        assert 'New entry was successfully posted' in rv.data.decode("utf-8")
        self.app.post('/add', data=dict(
            name='Joe Shmoe',
            note='test node',
            binary='not binary data'))
        rv = self.app.get('/')
        assert 'is not binary' in rv.data.decode("utf-8")
        self.app.post('/delete', data=dict(
            user_id=1))
        rv = self.app.get('/')
        assert 'User deleted successfully.' in rv.data.decode("utf-8")
        self.app.post('/add', data=dict(
            name='',
            note='',
            binary=''))
        rv = self.app.get('/')
        assert ('name is below min value' and
                'binary is below min value') in rv.data.decode("utf-8")

    def test_status_page(self):
        self.login(lock_interface.USERNAME, lock_interface.PASSWORD)
        rv = self.app.get('/status')
        assert 'Status Page' in rv.data.decode("utf-8")

    def test_log_page(self):
        self.login(lock_interface.USERNAME, lock_interface.PASSWORD)
        rv = self.app.get('/log')
        assert 'Door Lock Access Log' in rv.data.decode("utf-8")

if __name__ == '__main__':
    unittest.main()
