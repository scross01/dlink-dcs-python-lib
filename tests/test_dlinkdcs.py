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

    def test_set_email(self):
        # TODO
        self.assertTrue(False)

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

    def test_set_motion_detection_mode(self):
        r = self.ipcam.set_motion_detection_mode(ipcam.MOTION_DETECTION_SCHEDULE)
        self.assertTrue('MotionDetectionScheduleMode' in r)
        self.assertTrue(r['MotionDetectionScheduleMode'] == '1')
        r = self.ipcam.set_motion_detection_mode(ipcam.MOTION_DETECTION_ALWAYS)
        self.assertTrue('MotionDetectionScheduleMode' in r)
        self.assertTrue(r['MotionDetectionScheduleMode'] == '0')

    def test_set_motion_detection_schedule(self):
        r = self.ipcam.set_motion_detection_schedule(
            ipcam.MONDAY + ipcam.TUESDAY + ipcam.WEDNESDAY + ipcam.THURSDAY + ipcam.FRIDAY,
            '06:30:00', '20:15:00'
        )
        self.assertTrue(r['MotionDetectionScheduleDay'] == '62')
        self.assertTrue(r['MotionDetectionScheduleTimeStart'] == '06:30:00')
        self.assertTrue(r['MotionDetectionScheduleTimeStop'] == '20:15:00')
        r = self.ipcam.set_motion_detection_schedule(
            0, '00:00:00', '00:00:00'
        )
        self.assertTrue(r['MotionDetectionScheduleDay'] == '0')
        self.assertTrue(r['MotionDetectionScheduleTimeStart'] == '00:00:00')
        self.assertTrue(r['MotionDetectionScheduleTimeStop'] == '00:00:00')

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

    def test_set_sound_detection_mode(self):
        r = self.ipcam.set_sound_detection_mode(ipcam.SOUND_DETECTION_SCHEDULE)
        self.assertTrue('SoundDetectionScheduleMode' in r)
        self.assertTrue(r['SoundDetectionScheduleMode'] == '1')
        r = self.ipcam.set_sound_detection_mode(ipcam.SOUND_DETECTION_ALWAYS)
        self.assertTrue('SoundDetectionScheduleMode' in r)
        self.assertTrue(r['SoundDetectionScheduleMode'] == '0')

    def test_set_sound_detection_schedule(self):
        r = self.ipcam.set_sound_detection_schedule(
            ipcam.MONDAY + ipcam.TUESDAY + ipcam.WEDNESDAY + ipcam.THURSDAY + ipcam.FRIDAY,
            '06:30:00', '20:15:00'
        )
        self.assertTrue(r['SoundDetectionScheduleDay'] == '62')
        self.assertTrue(r['SoundDetectionScheduleTimeStart'] == '06:30:00')
        self.assertTrue(r['SoundDetectionScheduleTimeStop'] == '20:15:00')
        r = self.ipcam.set_sound_detection_schedule(
            0, '00:00:00', '00:00:00'
        )
        self.assertTrue(r['SoundDetectionScheduleDay'] == '0')
        self.assertTrue(r['SoundDetectionScheduleTimeStart'] == '00:00:00')
        self.assertTrue(r['SoundDetectionScheduleTimeStop'] == '00:00:00')

    def test_set_upload_server(self):
        r = self.ipcam.set_upload_server('ftpserver', 'username', 'password', '/path/', False, 2021)
        self.assertTrue(r['FTPHostAddress'] == 'ftpserver')
        self.assertTrue(r['FTPUserName'] == 'username')
        self.assertTrue(r['FTPPassword'] == 'password')
        self.assertTrue(r['FTPDirectoryPath'] == '/path/')
        self.assertTrue(r['FTPPassiveMode'] == '0')
        self.assertTrue(r['FTPPortNumber'] == '2021')
        r = self.ipcam.set_upload_server('', '', '', '/', True, 21)
        self.assertTrue(r['FTPHostAddress'] == '')
        self.assertTrue(r['FTPUserName'] == '')
        self.assertTrue(r['FTPPassword'] == '')
        self.assertTrue(r['FTPDirectoryPath'] == '/')
        self.assertTrue(r['FTPPassiveMode'] == '1')
        self.assertTrue(r['FTPPortNumber'] == '21')

    def test_set_upload_image(self):
        r = self.ipcam.set_upload_image(True)
        self.assertTrue(r['FTPScheduleEnable'] == '1')
        r = self.ipcam.set_upload_image(False)
        self.assertTrue(r['FTPScheduleEnable'] == '0')

    def test_set_upload_image_mode(self):
        r = self.ipcam.set_upload_image_mode(ipcam.FTP_MODE_DETECTION)
        self.assertTrue(r['FTPScheduleMode'] == '2')
        r = self.ipcam.set_upload_image_mode(ipcam.FTP_MODE_SCHEDULE)
        self.assertTrue(r['FTPScheduleMode'] == '1')
        r = self.ipcam.set_upload_image_mode(ipcam.FTP_MODE_ALWAYS)
        self.assertTrue(r['FTPScheduleMode'] == '0')

    def test_set_upload_image_settings(self):
        r = self.ipcam.set_upload_image_settings(
            filename='video',
            filename_mode=ipcam.UPLOAD_FILE_MODE_DATETIME,
            create_subfolder_minutes=30,
            frequency_mode=ipcam.FRAMES_PER_SECOND,
            frames_per_second=3,
        )
        self.assertTrue(r['FTPScheduleBaseFileName'] == 'video')
        self.assertTrue(r['FTPScheduleFileMode'] == '1')
        self.assertTrue(r['FTPCreateFolderInterval'] == '30')
        self.assertTrue(r['FTPScheduleVideoFrequencyMode'] == '0')
        self.assertTrue(r['FTPScheduleFramePerSecond'] == '3')

    def test_set_upload_image_schedule(self):
        r = self.ipcam.set_upload_image_schedule(
            ipcam.MONDAY + ipcam.TUESDAY + ipcam.WEDNESDAY + ipcam.THURSDAY + ipcam.FRIDAY,
            "06:00:00", "21:30:00"
        )
        self.assertTrue(r['FTPScheduleDay'] == '62')
        self.assertTrue(r['FTPScheduleTimeStart'] == '06:00:00')
        self.assertTrue(r['FTPScheduleTimeStop'] == '21:30:00')
        r = self.ipcam.set_upload_image_schedule(
            0, "00:00:00", "00:00:00"
        )
        self.assertTrue(r['FTPScheduleDay'] == '0')
        self.assertTrue(r['FTPScheduleTimeStart'] == '00:00:00')
        self.assertTrue(r['FTPScheduleTimeStop'] == '00:00:00')

    def test_set_upload_video(self):
        r = self.ipcam.set_upload_video(True)
        self.assertTrue(r['FTPScheduleEnableVideo'] == '1')
        r = self.ipcam.set_upload_video(False)
        self.assertTrue(r['FTPScheduleEnableVideo'] == '0')

    def test_set_upload_video_mode(self):
        r = self.ipcam.set_upload_video_mode(ipcam.FTP_MODE_DETECTION)
        self.assertTrue(r['FTPScheduleModeVideo'] == '2')
        r = self.ipcam.set_upload_video_mode(ipcam.FTP_MODE_SCHEDULE)
        self.assertTrue(r['FTPScheduleModeVideo'] == '1')
        r = self.ipcam.set_upload_video_mode(ipcam.FTP_MODE_ALWAYS)
        self.assertTrue(r['FTPScheduleModeVideo'] == '0')

    def test_set_upload_video_settings(self):
        r = self.ipcam.set_upload_video_settings(
            filename='video',
            file_limit_size=3072,
            file_limit_time=15,
        )
        self.assertTrue(r['FTPScheduleBaseFileNameVideo'] == 'video')
        self.assertTrue(r['FTPScheduleVideoLimitSize'] == '3072')
        self.assertTrue(r['FTPScheduleVideoLimitTime'] == '15')
        r = self.ipcam.set_upload_video_settings(
            filename='video',
        )
        self.assertTrue(r['FTPScheduleBaseFileNameVideo'] == 'video')
        self.assertTrue(r['FTPScheduleVideoLimitSize'] == '2048')
        self.assertTrue(r['FTPScheduleVideoLimitTime'] == '10')

    def test_set_upload_video_schedule(self):
        r = self.ipcam.set_upload_video_schedule(
            ipcam.MONDAY + ipcam.TUESDAY + ipcam.WEDNESDAY + ipcam.THURSDAY + ipcam.FRIDAY,
            "06:00:00", "21:30:00"
        )
        self.assertTrue(r['FTPScheduleDayVideo'] == '62')
        self.assertTrue(r['FTPScheduleTimeStartVideo'] == '06:00:00')
        self.assertTrue(r['FTPScheduleTimeStopVideo'] == '21:30:00')
        r = self.ipcam.set_upload_video_schedule(
            0, "00:00:00", "00:00:00"
        )
        self.assertTrue(r['FTPScheduleDayVideo'] == '0')
        self.assertTrue(r['FTPScheduleTimeStartVideo'] == '00:00:00')
        self.assertTrue(r['FTPScheduleTimeStopVideo'] == '00:00:00')


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("DlinkDCSCamera.send_command").setLevel(logging.DEBUG)
    unittest.main()
