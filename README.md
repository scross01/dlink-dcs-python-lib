Python Library for DLINK DCS 5025L Wireless IP Camera
=====================================================

This library has been built for an tested with the DLINK DCS 5025L Wireless Pan Tile IP Webcam. The library may work fully or partially with other DLINK IP Cameras (untested).


Running Tests
-------------

Running the library tests will update and rest various IP Camera settings. If you need to retain you current configuration you should **manually save your IP Camera configuration** in the DLINK web console and restore the configuration running the tests.

Create a file  `tests/camtest.cfg` with the test camera connection details.

```
[DEFAULT]
host=192.168.1.101
port=80
user=admin
password=Pa55_Word
```

### Run all Tests

```
$ python3 -m unittest discover
```

### Run a single test

```
$ python3 -m unittest tests.test_dlinkdcs.TestDlinkDCSCam.TESTNAME -v
```

Where TESTNAME is the test function to run e.g. `test_get_common_info`
