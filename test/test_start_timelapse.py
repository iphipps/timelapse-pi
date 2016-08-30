import unittest
import mock
import sys
sys.path.append(r"../")
from timelapsepi.start_timelapse import *


class MyTest(unittest.TestCase):

    def test_read_json(self):
        """
        Example test that runs against known input and asserts a specific fact
        """
        config = read_json('trivial_config.json')
        self.assertEquals(config['email']['from'], 'api@mydomain.com')
        pass


    def test_take_clip(self):
        """
        Example test that requires a specific method to be called once
        """
        camera = mock.MagicMock()
        file_name = 'test_file.jpg'
        take_clip(camera, file_name, clip_length=5)
        camera.capture.assert_called_once_with(file_name)


    def send_email(self):
        config = read_json('trivial_config.json')
        subject = 'hi'
        body = 'hello world'
        # needs a patch of smtplib.SMTP into a mock so it can run offline
        send_email(subject, body, config)


    def test_make_video(self):
        #make_video(working_dir)
        #do note that 'pass' here does NOT indicate test passing, it's just a filler word in python
        pass


    def test_update_dropbox(self):
        #update_dropbox(file, config)
        pass


    def test_update_all_dropbox(self):
        #update_all_dropbox(config)
        pass


    def test_start_timelapse(self):
        #start_timelapse(config)
        pass


if __name__ == '__main__':
    """
    Run with defaults if called as a script.
    TODO: pass command line argument allowing someone to specify different json
    """
    start_timelapse(read_json())
