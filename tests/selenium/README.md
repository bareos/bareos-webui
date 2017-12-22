# Bareos-WebUI Selenium Test

This test checks the Bareos Web UI by using seleniums webdriver.


## Setting up the test

To run the test you must set certain environment variables:

 * **BROWSER**: The test takes either 'firefox' or 'chrome', where 'firefox' is the default.
 * **USERNAME** and **PASSWORD**: These should contain the login information for the Web UI.
 * **VM_IP**: This should be the IP adress of the system where the Bareos Web UI runs on.
 * **RESTOREFILE**: The third test is designed to restore a certain file. The path to this file is set here and should look like '/usr/sbin/testfile.txt" for example.

## Running the test

To run all tests included you need a system that runs the WebUI, a client for restore-testing, chromedriver or geckodriver as well as any Python 2.7.

If you meet all the requirements and set the environment variables you can run the test with `python webui-selenium-test.py`.

## Debugging

If the test should fail you will find additional informations in the webui-selenium-test.log file.