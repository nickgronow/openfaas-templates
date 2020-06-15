import os
import unittest
import base
from unittest.mock import Mock, call
from testfixtures import TempDirectory


class ActionHandlerTest(unittest.TestCase):

    def setUp(self):
        self.event = Mock()
        self.event.body = {}
        self.event.headers = {}
        self.context = Mock()

        self.temp_dir = TempDirectory()

        os.environ['appname'] = 'appname'
        os.environ['secrets'] = self.temp_dir.path

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_secret(self):
        self.temp_dir.write('test-secret', b'top-secret-info')
        secret = base.secret('test-secret')
        self.assertEqual('top-secret-info', secret)
