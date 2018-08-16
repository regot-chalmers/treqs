import os
import shutil
import tempfile
import unittest
from contextlib import contextmanager

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

    def test_list_all_artefacts_in_folder(self):
        """
        [testcase id=TC6 story=US1c req=REQ1,REQ2,REQ11]

        Ensure that all test cases, user stories and requirements
        retrieved by treqs are listed in the log files
        """
        # Arrange
        with open('US_all.md', 'w+') as f:
            f.write('[userstory id=UStemp]')
        with open('TC_all.md', 'w+') as f:
            f.write('[testcase id=TCtemp]')
        with open('SR_all.md', 'w+') as f:
            f.write('[requirement id=REQtemp]')

        # Act
        main('treqs -u . -s . -t .'.split())

        # Assert
        for start_of_filename, artefact_name in [('TC', 'TCtemp'),
                                                 ('SysReq', 'REQtemp'),
                                                 ('US', 'UStemp')]:
            with self.subTest(artefact_name):
                with _open_file_in_directory_starting_with('logs', start_of_filename) as f:
                    self.assertIn(artefact_name, f.read())

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
        with _open_file_in_directory_starting_with('logs', 'Summary') as f:
            self.assertIn('UStemp', f.read())

@contextmanager
def _open_file_in_directory_starting_with(directory, starts_with):
    filename = next(filter(lambda x: x.startswith(starts_with), os.listdir(directory)))
    file_path = os.path.join('logs', filename)
    with open(file_path) as f:
        yield f
