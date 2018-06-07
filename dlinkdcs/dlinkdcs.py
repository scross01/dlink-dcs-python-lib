"""
DLINK DCS IP Camera Python SDK.

Tested with DLINK DCS 5025L.
"""

import requests
import logging

from datetime import datetime


class DlinkDCSCamera(object):
    """DLINK DCS IP Camera Control."""

    DAY_NIGHT_AUTO = '0'
    DAY_NIGHT_MANUAL = '1'
    DAY_NIGHT_ALWAYS_DAY = '2'
    DAY_NIGHT_ALWAYS_NIGHT = '3'
    DAY_NIGHT_SCHEDULE = '4'

    DAY_NIGHT_LIGHT_SENSOR_LOW = '1'
    DAY_NIGHT_LIGHT_SENSOR_MEDIUM = '3'
    DAY_NIGHT_LIGHT_SENSOR_HIGH = '5'

    MOTION_DETECTION_ALWAYS = '0'
    MOTION_DETECTION_SCHEDULE = '1'

    SOUND_DETECTION_ALWAYS = '0'
    SOUND_DETECTION_SCHEDULE = '1'

    SUNDAY = 1
    MONDAY = 2
    TUESDAY = 4
    WEDNESDAY = 8
    THURSDAY = 16
    FRIDAY = 32
    SATURDAY = 64

    FTP_MODE_ALWAYS = 0
    FTP_MODE_SCHEDULE = 1
    FTP_MODE_DETECTION = 2

    FRAMES_PER_SECOND = 0
    SECONDS_PER_FRAME = 1

    UPLOAD_FILE_MODE_OVERWRITE = 0
    UPLOAD_FILE_MODE_DATETIME = 1
    UPLOAD_FILE_MODE_SEQUENCE = 3

    UPLOAD_CREATE_FOLDER_OFF = 0
    UPLOAD_CREATE_FOLDER_HOURLY = 60
    UPLOAD_CREATE_FOLDER_DAILY = 1440

    EMAIL_TLS_NONE = 0
    EMAIL_TLS_SSLTLS = 1
    EMAIL_TLS_STARTTLS = 2

    EMAIL_MODE_ALWAYS = 0
    EMAIL_MODE_SCHEDULE = 1
    EMAIL_MODE_MOTION = 2

    EMAIL_MOTION_MODE_IMMIDIATE = 0
    EMAIL_MOTION_MODE_MULTIFRAME = 1

    EMAIL_MOTION_MULTIFRAME_SECONDS_HALF = 0
    EMAIL_MOTION_MULTIFRAME_SECONDS_ONE = 1

    def __init__(self, host, user, password, port=80):
        """Initialize with the IP camera connection settings."""
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def send_command(self, cmd, params={}):
        """Send a control command to the IP camera."""
        _url = 'http://%s:%d/%s' % (self.host, self.port, cmd)
        r = requests.get(_url, auth=(self.user, self.password), params=params)
        log = logging.getLogger("DlinkDCSCamera.send_command")
        log.debug(r.request.url)
        return self.unmarshal_response(r.content.decode('utf-8'))

    def unmarshal_response(self, response):
        """Unmarshal the multiline key value pair response."""
        _obj = {}
        for line in response.splitlines():
            # ignore blank lines and xml <result> block
            if line != '' and not line.startswith('<'):
                _keyvalue = line.strip().split("=")
                _obj[_keyvalue[0]] = _keyvalue[1]
        return _obj

    def time_to_string(self, time):
        """Conert a datetime into the HH:MM:SS string format."""
        return datetime.strftime(time, '%H:%M:%S')

    # GETTERS

    def get_cgi_version(self):
        """Get IP Camera CGI version."""
        return self.send_command('cgiversion.cgi')

    def get_common_info(self):
        """Get IP Camera Information."""
        return self.send_command('common/info.cgi')

    def get_date_time(self):
        """Get IP Camera Data Time settings."""
        return self.send_command('datetime.cgi')

    def get_day_night(self):
        """Get the IP Camera Day Night Mode settings."""
        return self.send_command('daynight.cgi')

    def get_email(self):
        """Get the IP Camera Email notification settings."""
        return self.send_command('email.cgi')

    def get_iimage(self):
        """Get the IP Camera Image information."""
        return self.send_command('iimage.cgi')

    def get_image(self):
        """Get the IP Camera Image information."""
        return self.send_command('image.cgi')

    def get_inetwork(self):
        """Get the IP Camera Network information."""
        return self.send_command('inetwork.cgi')

    def get_isystem(self):
        """Get the IP Camera System information."""
        return self.send_command('isystem.cgi')

    def get_iwireless(self):
        """Get the IP Camera Wireless information."""
        return self.send_command('iwireless.cgi')

    def get_motion_detection(self):
        """Get the IP Camera Motion Detection settings."""
        return self.send_command('motion.cgi')

    def get_network(self):
        """Get the IP Camera Network settings."""
        return self.send_command('network.cgi')

    def get_ptz(self):
        """Get the IP Camera Network Pan Tilt Zoom."""
        return self.send_command('config/ptz_move.cgi')

    def get_ptz_presets(self):
        """Get the IP Camera Network Pan Tilt Zoom Preset List"""
        return self.send_command('config/ptz_preset_list.cgi')

    def get_sound_detection(self):
        """Get the IP Camera Sound Detection settings."""
        return self.send_command('sdbdetection.cgi')

    def get_stream_info(self):
        """Get the IP Camera Video stream info."""
        return self.send_command('config/stream_info.cgi')

    def get_upload(self):
        """Get the IP Camera FTP Upload settings."""
        return self.send_command('upload.cgi')

    def get_user(self):
        """Get the IP Camera user setttings."""
        return self.send_command('user.cgi')

    def get_user_list(self):
        """Get the list of IP Camera users."""
        return self.send_command('userlist.cgi')

    # SETTERS

    def set_day_night(self, mode):
        """
        Set the IP Camera Day Night Mode.

        mode -- one of DAY_NIGHT_AUTO, DAY_NIGHT_MANUAL, DAY_NIGHT_ALWAYS_DAY,
                DAY_NIGHT_ALWAYS_NIGHT, or DAY_NIGHT_SCHEDULE.
        """
        _params = {
            'DayNightMode': int(mode),
            'ConfigReboot': 'no',
        }
        return self.send_command('daynight.cgi', _params)

    def set_day_night_sensor(self, light_sensor_control):
        """
        Set the IP Camera Day Night light lensor control.

        light_sensor_control -- one of DAY_NIGHT_LIGHT_SENSOR_LOW,
                                DAY_NIGHT_LIGHT_SENSOR_MEDIUM
                                DAY_NIGHT_LIGHT_SENSOR_HIGH
        """
        _params = {
            'LightSensorControl': light_sensor_control,
            'ConfigReboot': 'no',
        }
        return self.send_command('daynight.cgi', _params)

    def set_day_night_schedule(self,
                               sun_start, sun_end, mon_start, mon_end,
                               tue_start, tue_end, wed_start, wed_end,
                               thu_start, thu_end, fri_start, fri_end,
                               sat_start, sat_end):
        """
        Set the IP Camera Day Night Schedule.

        Scheduled times are used when the Day Night Mode is set to
        DAY_NIGHT_SCHEDULE. Daily Start and End times must be in a 'HH:MM'
        format.
        """
        _params = {
            'IRLedScheduleSunStart': sun_start,
            'IRLedScheduleSunEnd': sun_end,
            'IRLedScheduleMonStart': mon_start,
            'IRLedScheduleMonEnd': mon_end,
            'IRLedScheduleTueStart': tue_start,
            'IRLedScheduleTueEnd': tue_end,
            'IRLedScheduleWedStart': wed_start,
            'IRLedScheduleWedEnd': wed_end,
            'IRLedScheduleThuStart': thu_start,
            'IRLedScheduleThuEnd': thu_end,
            'IRLedScheduleFriStart': fri_start,
            'IRLedScheduleFriEnd': fri_end,
            'IRLedScheduleSatStart': sat_start,
            'IRLedScheduleSatEnd': sat_end,
            'ConfigReboot': 'no',
        }
        return self.send_command('daynight.cgi', _params)

    def set_email_account(self, host, user, password, sender, receiver, tls, port=25):
        """
        Set the IP Camera Email Notification Account.

        host -- email server host address
        user -- email account user
        password -- email account password
        sender -- from email address of sender
        receiver -- to email address of receiver
        tls -- one of EMAIL_TLS_NONE, EMAIL_TLS_SSLTLS, EMAIL_TLS_STARTTLS
        port -- email server port (default = 25)
        """
        _params = {
            'EmailSMTPServerAddress': host,
            'EmailSMTPPortNumber': int(port),
            'EmailTLSAuthentication': int(tls),
            'EmailUserName': user,
            'EmailPassword': password,
            'EmailReceiverAddress': receiver,
            'EmailSenderAddress': sender,
            'ConfigReboot': 'no',
        }
        return self.send_command('email.cgi', _params)

    def set_email_image(self, enable):
        """Enable or Disable IP Camera Email Images."""
        _params = {
            'EmailScheduleEnable': ('1' if enable else '0'),
            'ConfigReboot': 'no',
        }
        return self.send_command('email.cgi', _params)

    def set_email_image_mode(self, mode,
                             motion_mode=0,
                             motion_frame_interval=1):
        """
        Set the IP Camera Email Image Mode.

        mode -- one of EMAIL_MODE_ALWAYS, EMAIL_MODE_SCHEDULE, EMAIL_MODE_MOTION
        motion_mode -- EMAIL_MOTION_MODE_IMMIDIATE or EMAIL_MOTION_MODE_MULTIFRAME
        motion_frame_interval -- set image interval if motion_mode is multi-frame.
                                 One of EMAIL_MOTION_MULTIFRAME_SECONDS_HALF or
                                 EMAIL_MOTION_MULTIFRAME_SECONDS_ONE
        """
        _params = {
            'EmailScheduleMode': int(mode),
            'EmailMotionMode': int(motion_mode),
            'EmailMotionFrameInterval': int(motion_frame_interval),
            'ConfigReboot': 'no',
        }
        return self.send_command('email.cgi', _params)

    def set_email_image_schedule(self, schedule_days,
                                 schedule_start, schedule_stop,
                                 interval=300):
        """
        Set the IP Camera Email Schedule for Images.

        Effective when Email Image mode is EMAIL_MODE_SCHEDULE

        schedule_days -- value representing scheduled days (1..127)
                         e.g. schedule_days = MONDAY + WEDNESDAY + FRIDAY
        schedule_start -- daily start time in the format 'HH:MM:SS'
        schedule_stop -- daily stop time in the format 'HH:MM:SS'
        interval -- number of seconds between emails (default 300 seconds)
        """
        _params = {
            'EmailScheduleDay': int(schedule_days),
            'EmailScheduleTimeStart': schedule_start,
            'EmailScheduleTimeStop': schedule_stop,
            'EmailScheduleInterval': int(interval),
            'ConfigReboot': 'no',
        }
        return self.send_command('email.cgi', _params)

    def set_email_video(self, enable):
        """Enable or Disable IP Camera Email Videos."""
        _params = {
            'EmailScheduleEnableVideo': ('1' if enable else '0'),
            'ConfigReboot': 'no',
        }
        return self.send_command('email.cgi', _params)

    def set_email_video_mode(self, mode):
        """
        Set the IP Camera Email Videos Mode.

        mode -- one of EMAIL_MODE_ALWAYS, EMAIL_MODE_SCHEDULE, EMAIL_MODE_MOTION
        """
        _params = {
            'EmailScheduleModeVideo': int(mode),
            'ConfigReboot': 'no',
        }
        return self.send_command('email.cgi', _params)

    def set_email_video_schedule(self, schedule_days,
                                 schedule_start, schedule_stop,
                                 interval=300):
        """
        Set the IP Camera Email Schedule for Videos.

        Effective when Email Image mode is EMAIL_MODE_SCHEDULE

        schedule_days -- value representing scheduled days (1..127)
                         e.g. schedule_days = MONDAY + WEDNESDAY + FRIDAY
        schedule_start -- daily start time in the format 'HH:MM:SS'
        schedule_stop -- daily stop time in the format 'HH:MM:SS'
        interval -- number of seconds between emails (default 300 seconds)
        """
        _params = {
            'EmailScheduleDayVideo': int(schedule_days),
            'EmailScheduleTimeStartVideo': schedule_start,
            'EmailScheduleTimeStopVideo': schedule_stop,
            'EmailScheduleIntervalVideo': int(interval),
            'ConfigReboot': 'no',
        }
        return self.send_command('email.cgi', _params)

    def set_motion_detection(self, enable):
        """Enable or Disable IP Camera Motion Detection."""
        _params = {
            'MotionDetectionEnable': ('1' if enable else '0'),
            'ConfigReboot': 'no',
        }
        return self.send_command('motion.cgi', _params)

    def set_motion_detection_sensitivity(self, sensitivity):
        """Set the IP Camera Motion Detection Sensitivity."""
        _params = {
            'MotionDetectionSensitivity': str(sensitivity),
            'ConfigReboot': 'no',
        }
        return self.send_command('motion.cgi', _params)

    def set_motion_detection_blockset(self, blockset):
        """
        Set the IP Camera Motion Detection Blockset mask.

        blockset -- a 5x5 bitmask of enabled motion capture cells e.g.
                    1111100000111110000011111
        """
        _params = {
            'MotionDetectionBlockSet': blockset,
            'ConfigReboot': 'no',
        }
        return self.send_command('motion.cgi', _params)

    def set_motion_detection_mode(self, mode):
        """
        Set the IP Camera Motion Detection mode.

        mode -- one of MOTION_DETECTION_ALWAYS or MOTION_DETECTION_SCHEDULE
        """
        _params = {
            'MotionDetectionScheduleMode': int(mode),
            'ConfigReboot': 'no',
        }
        return self.send_command('motion.cgi', _params)

    def set_motion_detection_schedule(self, schedule_days,
                                      schedule_start, schedule_stop):
        """
        Set the IP Camera Motion Detection Schedule.

        Effective when Motion Detection mode is MOTION_DETECTION_SCHEDULE

        schedule_days -- value representing scheduled days (1..127)
                         e.g. schedule_days = MONDAY + WEDNESDAY + FRIDAY
        schedule_start -- daily start time in the format 'HH:MM:SS'
        schedule_stop -- daily stop time in the format 'HH:MM:SS'
        """
        _params = {
            'MotionDetectionScheduleDay': int(schedule_days),
            'MotionDetectionScheduleTimeStart': schedule_start,
            'MotionDetectionScheduleTimeStop': schedule_stop,
            'ConfigReboot': 'no',
        }
        return self.send_command('motion.cgi', _params)


    def set_ptz(self, pan=167, tilt=25, zoom=0):
        """
        Set the IP Camera Pan Tilt Zoom location.

        pan -- 0 to 336 (default: 167)
        tile -- 0 to 106 (default: 25)
        zoom --
        """
        _params = {
            'p': int(pan),
            't': int(tilt),
            'z': int(zoom),
        }
        return self.send_command('config/ptz_move.cgi', _params)

    def set_ptz_move(self, x, y):
        """Move the IP Camera Pan Tilt Zoom location."""
        _params = {
            'command': 'set_relative_pos',
            'posX': int(x),
            'posY': int(y),
        }
        return self.send_command('cgi/ptdc.cgi', _params)

    def set_ptz_move_preset(self, preset):
        """Move the IP Camera to a Preset Pan Tilt Zoom location."""
        _params = {
            'PanTiltPresetPositionMove': preset,
        }
        return self.send_command('pantiltcontrol.cgi', _params)

    def set_sound_detection(self, enable):
        """Enable or Disable the IP Camera Sound Detection."""
        _params = {
            'SoundDetectionEnable': ('1' if enable else '0'),
            'ConfigReboot': 'no',
        }
        return self.send_command('sdbdetection.cgi', _params)

    def set_sound_detection_sensitivity(self, decibels):
        """
        Set the IP Camera Sound Detection sensitivity.

        decibels - the number of decibels required to trigger sound detection,
                   in the range 50..90
        """
        _params = {
            'SoundDetectionDB': str(decibels),
            'ConfigReboot': 'no',
        }
        return self.send_command('sdbdetection.cgi', _params)

    def set_sound_detection_mode(self, mode):
        """
        Set the IP Camera Sound Detection mode.

        mode -- one of SOUND_DETECTION_ALWAYS or SOUND_DETECTION_SCHEDULE
        """
        _params = {
            'SoundDetectionScheduleMode': int(mode),
            'ConfigReboot': 'no',
        }
        return self.send_command('sdbdetection.cgi', _params)

    def set_sound_detection_schedule(self, schedule_days,
                                     schedule_start, schedule_stop):
        """
        Set the IP Camera Sound Detection Schedule.

        Effective when Sound Detection mode is SOUND_DETECTION_SCHEDULE

        schedule_days -- value representing scheduled days (1..127)
                         e.g. schedule_days = MONDAY + WEDNESDAY + FRIDAY
        schedule_start -- daily start time in the format 'HH:MM:SS'
        schedule_stop -- daily stop time in the format 'HH:MM:SS'
        """
        _params = {
            'SoundDetectionScheduleDay': int(schedule_days),
            'SoundDetectionScheduleTimeStart': schedule_start,
            'SoundDetectionScheduleTimeStop': schedule_stop,
            'ConfigReboot': 'no',
        }
        return self.send_command('sdbdetection.cgi', _params)

    def set_upload_server(self, host, user, password, path='/',
                          passive=True, port=21):
        """
        Set the IP Camera FTP upload server settings.

        host -- FTP server hostname
        user -- FTP server user
        psasword -- FTP server password
        path -- FTP server upload path (default '/')
        passive -- Passive mode (deafault True)
        port -- FTP server port (default 21)
        """
        _params = {
            'FTPHostAddress': host,
            'FTPUserName': user,
            'FTPPassword': password,
            'FTPDirectoryPath': path,
            'FTPPortNumber': int(port),
            'FTPPassiveMode': ('1' if passive else '0'),
            'ConfigReboot': 'no',
        }
        return self.send_command('upload.cgi', _params)

    def set_upload_image(self, enable):
        """Enable or Disable Image upload."""
        _params = {
            'FTPScheduleEnable': ('1' if enable else '0'),
            'ConfigReboot': 'no',
        }
        return self.send_command('upload.cgi', _params)

    def set_upload_image_mode(self, mode):
        """
        Set the IP Camera image upload mode.

        mode -- one of FTP_MODE_ALWAYS, FTP_MODE_SCHEDULE, FTP_MODE_DETECTION
        """
        _params = {
            'FTPScheduleMode': int(mode),
            'ConfigReboot': 'no',
        }
        return self.send_command('upload.cgi', _params)

    def set_upload_image_settings(self,
                                  filename='image',
                                  filename_mode=1,
                                  max_file_sequence_number=1024,
                                  create_subfolder_minutes=0,
                                  frequency_mode=0,
                                  frames_per_second=-1,
                                  seconds_per_frame=1):
        """
        Set the IP Camera upload image settings.

        filename -- base file name
        filename_mode -- UPLOAD_FILE_MODE_OVERWRITE, UPLOAD_FILE_MODE_DATETIME
                         or UPLOAD_FILE_MODE_SEQUENCE
        max_file_sequence_number -- maxamum sequence number if mode is
                                    UPLOAD_FILE_MODE_SEQUENCE
        create_subfolder_minutes -- create date/time subfolders
        frequency_mode -- FRAMES_PER_SECONDS or SECONDS_PER_FRAME
        frames_per_second -- frames (images) per second (1..3), use -1 for Auto
        seconds_per_frame -- seconds between frames
        """
        _params = {
            'FTPScheduleVideoFrequencyMode': int(frequency_mode),
            'FTPScheduleFramePerSecond': int(frames_per_second),
            'FTPScheduleSecondPerFrame': int(seconds_per_frame),
            'FTPScheduleBaseFileName': filename,
            'FTPScheduleFileMode': int(filename_mode),
            'FTPScheduleMaxFileSequenceNumber': int(max_file_sequence_number),
            'FTPCreateFolderInterval': int(create_subfolder_minutes),
            'ConfigReboot': 'no',
        }
        return self.send_command('upload.cgi', _params)

    def set_upload_image_schedule(self,
                                  schedule_days=0,
                                  schedule_start='00:00:00',
                                  schedule_stop='00:00:00'):
        """
        Set the IP Camera upload image schedule.

        These settings are used if mode is FTP_MODE_SCHEDULE

        schedule_days -- value representing scheduled days (1..127)
                         e.g. schedule_days = MONDAY + WEDNESDAY + FRIDAY
        schedule_start -- daily start time in the format 'HH:MM:SS'
        schedule_stop -- daily end time in the format 'HH:MM:SS'
        """
        _params = {
            'FTPScheduleDay': schedule_days,
            'FTPScheduleTimeStart': schedule_start,
            'FTPScheduleTimeStop': schedule_stop,
            'ConfigReboot': 'no',
        }
        return self.send_command('upload.cgi', _params)

    def set_upload_video(self, enable):
        """Enable or Disable Video upload."""
        _params = {
            'FTPScheduleEnableVideo': ('1' if enable else '0'),
            'ConfigReboot': 'no',
        }
        return self.send_command('upload.cgi', _params)

    def set_upload_video_settings(self, filename='video',
                                  file_limit_size=2048,
                                  file_limit_time=10):
        """
        Set the IP Camera upload video file settings.

        filename -- base file name
        file_limit_size -- video file size KBytes
                           (default is 2048, max is 3072 KBytes)
        file_limit_time -- video file lenght in seconds
                           (default is 10, max is 15 seconds)
        """
        _params = {
            'FTPScheduleBaseFileNameVideo': filename,
            'FTPScheduleVideoLimitSize': int(file_limit_size),
            'FTPScheduleVideoLimitTime': int(file_limit_time),
            'ConfigReboot': 'no',
        }
        return self.send_command('upload.cgi', _params)

    def set_upload_video_mode(self, mode):
        """
        Set the IP Camera upload video mode.

        mode -- one of FTP_MODE_ALWAYS, FTP_MODE_SCHEDULE, FTP_MODE_DETECTION
        """
        _params = {
            'FTPScheduleModeVideo': mode,
            'ConfigReboot': 'no',
        }
        return self.send_command('upload.cgi', _params)

    def set_upload_video_schedule(self, schedule_days=0,
                                  schedule_start='00:00:00',
                                  schedule_stop='00:00:00'):
        """
        Set the IP Camera upload video schedule.

        These settings are used if mode is FTP_MODE_SCHEDULE

        schedule_days -- value representing scheduled days (1..127)
                         e.g. schedule_days = MONDAY + WEDNESDAY + FRIDAY
        schedule_start -- daily start time in the format 'HH:MM:SS'
        schedule_stop -- daily end time in the format 'HH:MM:SS'
        """
        _params = {
            'FTPScheduleDayVideo': schedule_days,
            'FTPScheduleTimeStartVideo': schedule_start,
            'FTPScheduleTimeStopVideo': schedule_stop,
            'ConfigReboot': 'no',
        }
        return self.send_command('upload.cgi', _params)

    # HELPERS

    def disable_email_image(self):
        """Disable image emails."""
        return self.set_email_image(False)

    def disable_email_video(self):
        """Disable video emails."""
        return self.set_email_video(False)

    def disable_motion_detection(self):
        """Disable motion detection."""
        return self.set_motion_detection(False)

    def disable_sound_detection(self):
        """Disable sound detection."""
        return self.set_sound_detection(False)

    def disable_upload_image(self):
        """Disable image upload."""
        return self.set_upload_image(False)

    def disable_upload_video(self):
        """Disable video upload."""
        return self.set_upload_video(False)

    def enable_email_image(self):
        """Enable image emails."""
        return self.set_email_image(True)

    def enable_email_video(self):
        """Enable video emails."""
        return self.set_email_video(True)

    def enable_motion_detection(self):
        """Enable motion detection."""
        return self.set_motion_detection(True)

    def enable_sound_detection(self):
        """Enable sound detection."""
        return self.set_sound_detection(True)

    def enable_upload_image(self):
        """Enable image upload."""
        return self.set_upload_image(True)

    def enable_upload_video(self):
        """Enable video upload."""
        return self.set_upload_video(True)
