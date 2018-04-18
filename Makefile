test:
	python3 -m unittest discover

testone:
	python3 -m unittest tests.test.TestDlinkDCSCam.test_get_date_time -v


.PHONY: test
