import os.path
import sys
import unittest
import logging

from configparser import ConfigParser
from dlinkdcs import DlinkDCSCamera as ipcam

config = ConfigParser()
config_filepath = os.path.join(os.path.dirname(__file__), 'camtest.cfg')

if os.path.exists(config_filepath):
    config.read([config_filepath])

config_defaults = config.defaults()

CAM_HOST = config_defaults.get('host') or ''
CAM_PORT = int(config_defaults.get('port')) or 80
CAM_USER = config_defaults.get('user') or 'admin'
CAM_PASS = config_defaults.get('password') or ''


class TestDlinkDCSCam(unittest.TestCase):
    def setUp(self):
        self.ipcam = ipcam(CAM_HOST, CAM_USER, CAM_PASS, CAM_PORT)

    def test_get_cgi_version(self):
        r = self.ipcam.get_cgi_version()
        self.assertTrue('CGIVersion' in r)

    def test_get_date_time(self):
        r = self.ipcam.get_date_time()
        self.assertTrue('DateTimeMode' in r)

    def test_get_day_night(self):
        r = self.ipcam.get_day_night()
        self.assertTrue('DayNightMode' in r)

    def test_get_email(self):
        r = self.ipcam.get_email()
        self.assertTrue('EmailSMTPServerAddress' in r)

    def test_get_iimage(self):
        r = self.ipcam.get_iimage()
        self.assertTrue('VideoResolution' in r)

    def test_get_inetwork(self):
        r = self.ipcam.get_inetwork()
        self.assertTrue('IPAddress' in r)

    def test_get_isystem(self):
        r = self.ipcam.get_isystem()
        self.assertTrue('CameraName' in r)

    def test_get_iwireless(self):
        r = self.ipcam.get_iwireless()
        self.assertTrue('ConnectionMode' in r)

    def test_get_motion_detection(self):
        r = self.ipcam.get_motion_detection()
        self.assertTrue('MotionDetectionEnable' in r)

    def test_get_network(self):
        r = self.ipcam.get_network()
        self.assertTrue('IPAddress' in r)

    def test_get_sound_detection(self):
        r = self.ipcam.get_sound_detection()
        self.assertTrue('SoundDetectionEnable' in r)

    def test_get_user(self):
        r = self.ipcam.get_user()
        self.assertTrue('AccessControlEnable' in r)

    def test_get_upload(self):
        r = self.ipcam.get_upload()
        self.assertTrue('FTPHostAddress' in r)

    def test_get_user_list(self):
        r = self.ipcam.get_user_list()
        self.assertTrue('UserName' in r)

    def test_set_date_time(self):
        # TODO
        self.assertTrue(False)

    def test_set_day_night(self):
        r = self.ipcam.set_day_night(ipcam.DAY_NIGHT_MANUAL)
        self.assertTrue('DayNightMode' in r)
        self.assertTrue(r['DayNightMode'] == ipcam.DAY_NIGHT_MANUAL)
        r = self.ipcam.set_day_night(ipcam.DAY_NIGHT_AUTO)
        self.assertTrue('DayNightMode' in r)
        self.assertTrue(r['DayNightMode'] == ipcam.DAY_NIGHT_AUTO)

    def test_set_day_night_sensor(self):
        r = self.ipcam.set_day_night_sensor(ipcam.DAY_NIGHT_LIGHT_SENSOR_LOW)
        self.assertTrue('LightSensorControl' in r)
        self.assertTrue(r['LightSensorControl'] == ipcam.DAY_NIGHT_LIGHT_SENSOR_LOW)
        r = self.ipcam.set_day_night_sensor(ipcam.DAY_NIGHT_LIGHT_SENSOR_MEDIUM)
        self.assertTrue('LightSensorControl' in r)
        self.assertTrue(r['LightSensorControl'] == ipcam.DAY_NIGHT_LIGHT_SENSOR_MEDIUM)

    def test_set_email(self):
        # TODO
        self.assertTrue(False)

    def test_set_day_night_schedule(self):
        r = self.ipcam.set_day_night_schedule(
            '01:00', '13:00',  # SUNDAY
            '02:00', '14:00',  # MONDAY
            '03:00', '15:00',  # TUESDAY
            '04:00', '16:00',  # WEDNESDAY
            '05:00', '17:00',  # THURSDAY
            '06:00', '18:00',  # FRIDAY
            '07:00', '19:00',  # SATURDAY
        )
        self.assertTrue(r['IRLedScheduleSunStart'] == '01:00')
        self.assertTrue(r['IRLedScheduleMonStart'] == '02:00')
        self.assertTrue(r['IRLedScheduleTueStart'] == '03:00')
        self.assertTrue(r['IRLedScheduleWedStart'] == '04:00')
        self.assertTrue(r['IRLedScheduleThuStart'] == '05:00')
        self.assertTrue(r['IRLedScheduleFriStart'] == '06:00')
        self.assertTrue(r['IRLedScheduleSatStart'] == '07:00')
        self.assertTrue(r['IRLedScheduleSunEnd'] == '13:00')
        self.assertTrue(r['IRLedScheduleMonEnd'] == '14:00')
        self.assertTrue(r['IRLedScheduleTueEnd'] == '15:00')
        self.assertTrue(r['IRLedScheduleWedEnd'] == '16:00')
        self.assertTrue(r['IRLedScheduleThuEnd'] == '17:00')
        self.assertTrue(r['IRLedScheduleFriEnd'] == '18:00')
        self.assertTrue(r['IRLedScheduleSatEnd'] == '19:00')
        r = self.ipcam.set_day_night_schedule(
            '00:00', '00:00',  # SUNDAY
            '00:00', '00:00',  # MONDAY
            '00:00', '00:00',  # TUESDAY
            '00:00', '00:00',  # WEDNESDAY
            '00:00', '00:00',  # THURSDAY
            '00:00', '00:00',  # FRIDAY
            '00:00', '00:00',  # SATURDAY
        )
        self.assertTrue(r['IRLedScheduleSunStart'] == '00:00')
        self.assertTrue(r['IRLedScheduleMonStart'] == '00:00')
        self.assertTrue(r['IRLedScheduleTueStart'] == '00:00')
        self.assertTrue(r['IRLedScheduleWedStart'] == '00:00')
        self.assertTrue(r['IRLedScheduleThuStart'] == '00:00')
        self.assertTrue(r['IRLedScheduleFriStart'] == '00:00')
        self.assertTrue(r['IRLedScheduleSatStart'] == '00:00')
        self.assertTrue(r['IRLedScheduleSunEnd'] == '00:00')
        self.assertTrue(r['IRLedScheduleMonEnd'] == '00:00')
        self.assertTrue(r['IRLedScheduleTueEnd'] == '00:00')
        self.assertTrue(r['IRLedScheduleWedEnd'] == '00:00')
        self.assertTrue(r['IRLedScheduleThuEnd'] == '00:00')
        self.assertTrue(r['IRLedScheduleFriEnd'] == '00:00')
        self.assertTrue(r['IRLedScheduleSatEnd'] == '00:00')

    def test_set_motion_detection(self):
        r = self.ipcam.set_motion_detection(True)
        self.assertTrue('MotionDetectionEnable' in r)
        self.assertTrue(r['MotionDetectionEnable'] == '1')
        r = self.ipcam.set_motion_detection(False)
        self.assertTrue('MotionDetectionEnable' in r)
        self.assertTrue(r['MotionDetectionEnable'] == '0')

    def test_set_motion_detection_sensitivity(self):
        r = self.ipcam.set_motion_detection_sensitivity(90)
        self.assertTrue('MotionDetectionSensitivity' in r)
        self.assertTrue(r['MotionDetectionSensitivity'] == '90')
        r = self.ipcam.set_motion_detection_sensitivity(50)
        self.assertTrue('MotionDetectionSensitivity' in r)
        self.assertTrue(r['MotionDetectionSensitivity'] == '50')

    def test_set_motion_detection_blockset(self):
        r = self.ipcam.set_motion_detection_blockset('1111100000111110000011111')
        self.assertTrue('MotionDetectionBlockSet' in r)
        self.assertTrue(r['MotionDetectionBlockSet'] == '1111100000111110000011111')
        r = self.ipcam.set_motion_detection_blockset('0000000000000000000000000')
        self.assertTrue('MotionDetectionBlockSet' in r)
        self.assertTrue(r['MotionDetectionBlockSet'] == '0000000000000000000000000')

    def test_set_motion_detection_schedule(self):
        # TODO
        self.assertTrue(False)

    def test_set_sound_detection(self):
        r = self.ipcam.set_sound_detection(True)
        self.assertTrue('SoundDetectionEnable' in r)
        self.assertTrue(r['SoundDetectionEnable'] == '1')
        r = self.ipcam.set_sound_detection(False)
        self.assertTrue('SoundDetectionEnable' in r)
        self.assertTrue(r['SoundDetectionEnable'] == '0')

    def test_set_sound_detection_decibels(self):
        r = self.ipcam.set_sound_detection_sensitivity(90)
        self.assertTrue('SoundDetectionDB' in r)
        self.assertTrue(r['SoundDetectionDB'] == '90')
        r = self.ipcam.set_sound_detection_sensitivity(50)
        self.assertTrue('SoundDetectionDB' in r)
        self.assertTrue(r['SoundDetectionDB'] == '50')

    def test_set_sound_detection_schedule(self):
        # TODO
        self.assertTrue(False)

    def test_set_upload(self):
        # TODO
        self.assertTrue(False)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("DlinkDCSCamera.send_command").setLevel(logging.DEBUG)
    unittest.main()
