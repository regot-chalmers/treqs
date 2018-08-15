import os
import shutil
import tempfile
import unittest

from treqs.main import main

class TestSystem(unittest.TestCase):
    def test_logs_directory_is_created(self):
        """
        [testcase id=TC1 story=US4 req=REQ3]

        Ensure that a logs/ directory is created in the current
        directory when treqs is run.
        """
        temp_directory = tempfile.mkdtemp()
        old_directory = os.getcwd()
        os.chdir(temp_directory)
        main('treqs -u . -s . -t .'.split())

        self.assertTrue(os.path.isdir('logs'))

        os.chdir(old_directory)
        shutil.rmtree(temp_directory)


