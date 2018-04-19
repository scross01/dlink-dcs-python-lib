TEST=

test-all:
	python3 -m unittest discover

# run `make test TEST=test_name`
test:
	python3 -m unittest tests.test_dlinkdcs.TestDlinkDCSCam.$(TEST) -v

list-tests:
	grep test_ tests/*.py | awk '{ gsub("\\(self\\):","",$$3); print $$3}'

.PHONY: test-all test list-tests
