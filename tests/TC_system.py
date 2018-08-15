import os
import shutil
import tempfile
import unittest

from treqs.main import main


class TestSystem(unittest.TestCase):
    def setUp(self):
        self.temp_directory = tempfile.mkdtemp()
        self.old_directory = os.getcwd()
        os.chdir(self.temp_directory)

    def tearDown(self):
        os.chdir(self.old_directory)
        shutil.rmtree(self.temp_directory)

    def test_logs_directory_is_created(self):
        """
        [testcase id=TC1 story=US1d req=REQ5]

        Ensure that a logs/ directory is created in the current
        directory when treqs is run.
        """
        # Act
        main('treqs -u . -s . -t .'.split())

        # Assert
        self.assertTrue(os.path.isdir('logs'))

    def test_list_user_stories_without_requirements(self):
        """
        [testcase id=TC5 story=US1d req=REQ3]

        Ensure that user stories without system requirements
        are listed in the Summary file
        """
        # Arrange
        with open('US_all.md', 'w+') as f:
            f.write('[userstory id=UStemp]')

        # Act
        main('treqs -u . -s . -t .'.split())

        # Assert
        filename = next(filter(lambda x: x.startswith('Summary'), os.listdir('logs')))
        file_path = os.path.join(self.temp_directory, 'logs', filename)
        with open(file_path) as f:
            self.assertIn('UStemp', f.read())
