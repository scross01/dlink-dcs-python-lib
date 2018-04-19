"""
DLINK DCS IP Camera Phyton SDK.

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

    def get_sound_detection(self):
        """Get the IP Camera Sound Detection settings."""
        return self.send_command('sdbdetection.cgi')

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

    # HELPERS

    def disable_motion_detection(self):
        """Disable motion detection."""
        return self.set_motion_detection(False)

    def disable_sound_detection(self):
        """Disable sound detection."""
        return self.set_sound_detection(False)

    def enable_motion_detection(self):
        """Enable motion detection."""
        return self.set_motion_detection(True)

    def enable_sound_detection(self):
        """Enable sound detection."""
        return self.set_sound_detection(True)
