import requests
import logging

from datetime import datetime


class DlinkDCSCamera(object):

    DAY_NIGHT_AUTO = '0'
    DAY_NIGHT_MANUAL = '1'
    DAY_NIGHT_ALWAYS_DAY = '2'
    DAY_NIGHT_ALWAYS_NIGHT = '3'
    DAY_NIGHT_SCHEDULE = '4'

    DAY_NIGHT_LIGHT_SENSOR_LOW = '1'
    DAY_NIGHT_LIGHT_SENSOR_MEDIUM = '3'
    DAY_NIGHT_LIGHT_SENSOR_HIGH = '5'

    SUNDAY = 1
    MONDAY = 2
    TUESDAY = 4
    WEDNESDAY = 8
    THURDAY = 16
    FRIDAY = 32
    SATURDAY = 64

    def __init__(self, host, user, password, port=80):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def send_command(self, cmd, params={}):
        _url = 'http://%s:%d/%s' % (self.host, self.port, cmd)
        r = requests.get(_url, auth=(self.user, self.password), params=params)
        log = logging.getLogger("DlinkDCSCamera.send_command")
        log.debug(r.request.url)
        return self.unmarshal_response(r.content.decode('utf-8'))

    def unmarshal_response(self, response):
        _obj = {}
        for line in response.splitlines():
            _keyvalue = line.strip().split("=")
            _obj[_keyvalue[0]] = _keyvalue[1]
        return _obj

    def time_to_string(self, time):
        return datetime.strftime(time, '%H:%M:%S')

    # GETTERS

    def get_cgi_version(self):
        return self.send_command('cgiversion.cgi')

    def get_date_time(self):
        return self.send_command('datetime.cgi')

    def get_day_night(self):
        return self.send_command('daynight.cgi')

    def get_email(self):
        return self.send_command('email.cgi')

    def get_iimage(self):
        return self.send_command('iimage.cgi')

    def get_inetwork(self):
        return self.send_command('inetwork.cgi')

    def get_isystem(self):
        return self.send_command('isystem.cgi')

    def get_iwireless(self):
        return self.send_command('iwireless.cgi')

    def get_motion_detection(self):
        return self.send_command('motion.cgi')

    def get_network(self):
        return self.send_command('network.cgi')

    def get_sound_detection(self):
        return self.send_command('sdbdetection.cgi')

    def get_upload(self):
        return self.send_command('upload.cgi')

    def get_user(self):
        return self.send_command('user.cgi')

    def get_user_list(self):
        return self.send_command('userlist.cgi')

    # SETTERS

    def set_day_night(self, mode):
        _params = {
            'DayNightMode': int(mode),
            'ConfigReboot': 'no',
        }
        return self.send_command('daynight.cgi', _params)

    def set_day_night_sensor(self, light_sensor_control):
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
        _params = {
            'MotionDetectionEnable': ('1' if enable else '0'),
            'ConfigReboot': 'no',
        }
        return self.send_command('motion.cgi', _params)

    def set_motion_detection_sensitivity(self, sensitivity):
        _params = {
            'MotionDetectionSensitivity': str(sensitivity),
            'ConfigReboot': 'no',
        }
        return self.send_command('motion.cgi', _params)

    # blockset is a 5x5 bitmask of enabled motion capture cells
    def set_motion_detection_blockset(self, blockset):
        _params = {
            'MotionDetectionBlockSet': blockset,
            'ConfigReboot': 'no',
        }
        return self.send_command('motion.cgi', _params)

    def set_motion_detection_schedule(self,
                                      schedule_mode, schedule_day,
                                      schedule_start, schedule_stop):
        _params = {
            'MotionDetectionScheduleMode': int(schedule_mode),  # TODO
            'MotionDetectionScheduleDay': int(schedule_day),   # TODO
            'MotionDetectionScheduleTimeStart': self.time_to_string(schedule_start),
            'MotionDetectionScheduleTimeStop': self.time_to_string(schedule_stop),
            'ConfigReboot': 'no',
        }
        return self.send_command('motion.cgi', _params)

    def set_sound_detection(self, enable):
        _params = {
            'SoundDetectionEnable': ('1' if enable else '0'),
            'ConfigReboot': 'no',
        }
        return self.send_command('sdbdetection.cgi', _params)

    def set_sound_detection_sensitivity(self, decibels):
        _params = {
            'SoundDetectionDB': str(decibels),
            'ConfigReboot': 'no',
        }
        return self.send_command('sdbdetection.cgi', _params)

    def set_sound_detection_schedule(self,
                                     schedule_mode, schedule_day,
                                     schedule_start, schedule_stop):
        _params = {
            'SoundDetectionScheduleMode': int(schedule_mode),  # TODO
            'SoundDetectionScheduleDay': int(schedule_day),  # TODO
            'SoundDetectionScheduleTimeStart': self.time_to_string(schedule_start),
            'SoundDetectionScheduleTimeStop': self.time_to_string(schedule_stop),
            'ConfigReboot': 'no',
        }
        return self.send_command('sdbdetection.cgi', _params)

    # HELPERS

    def disable_motion_detection(self):
        return set_motion_detection(False)

    def disable_sound_detection(self):
        return set_sound_detection(False)

    def enable_motion_detection(self):
        return set_motion_detection(True)

    def enable_sound_detection(self):
        return set_sound_detection(True)
