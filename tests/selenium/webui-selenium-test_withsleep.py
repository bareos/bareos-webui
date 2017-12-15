# -*- coding: utf-8 -*-
import logging, os, re, sys, time, unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait

class WebuiSeleniumTest(unittest.TestCase):

    def setUp(self):
        if browser.matches("chrome"):
            d = DesiredCapabilities.CHROME
            d['loggingPrefs'] = { 'browser':'ALL' }
            self.driver = webdriver.Chrome('/usr/local/sbin/chromedriver')
        if browser == "firefox":
            d = DesiredCapabilities.FIREFOX
            d['loggingPrefs'] = { 'browser':'ALL' }
            fp = webdriver.FirefoxProfile()
            fp.set_preference('webdriver.log.file', os.getcwd() + '/firefox_console')
            self.driver = webdriver.Firefox()
        # d = DesiredCapabilities.FIREFOX
        # d['loggingPrefs'] = { 'browser':'ALL' }
        # fp = webdriver.FirefoxProfile()
        # fp.set_preference('webdriver.log.file', os.getcwd() + '/firefox_console')
        # self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(4)
        self.base_url = "http://%s" % targethost
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_login(self):
        self.login()
        time.sleep(3)
        self.logout()

    def test_menue(self):
        driver = self.driver
        # on windows we have a different baseurl
        if os.getenv('DIST') == "windows":
            driver.get(self.base_url + "/")
        else:
            driver.get(self.base_url + "/bareos-webui/")
        self.login()
        self.wait_for_url("/bareos-webui/director/")
        self.wait_for_url("/bareos-webui/schedule//")
        self.wait_for_url("/bareos-webui/schedule/status/")
        self.wait_for_url("/bareos-webui/storage/")
        self.wait_for_url("/bareos-webui/client/")
        self.wait_for_url("/bareos-webui/restore/")
        self.logout()

    def deactivated_test_restore(self):

        pathlist = restorefile.split('/')
        driver = self.driver
        # LOGGING IN:
        self.login()

        # CHANGING TO RESTORE TAB:
        self.wait_for_url("/bareos-webui/restore/")
        time.sleep(2)

        # SELECTING CLIENT:
        # Selects the correct client
        self.wait_for_element(By.XPATH, "//p/div/button").click()
        self.wait_for_element(By.CSS_SELECTOR, "span.text").click()
        time.sleep(2)

        # FILE-SELECTION:
        # Clicks on file and navigates through the tree
        # by using the arrow-keys.
        for i in pathlist[:-1]:
            self.wait_for_element(By.XPATH, "//a[contains(text(),'%s/')]" % i).send_keys(Keys.ARROW_RIGHT)
        else:
            self.wait_for_element(By.XPATH, "//a[contains(text(),'%s')]" % pathlist[-1]).click()

        # CONFIRMATION:
        # Clicks on 'submit'
        self.wait_for_element(By.XPATH, "//input[@id='submit']").click()
        # Confirms alert that has text "Are you sure ?"
        self.assertRegexpMatches(self.close_alert_and_get_its_text(), r"^Are you sure[\s\S]$")

        # LOGOUT:
        self.logout()

    def login(self):
        driver = self.driver
        driver.get(self.base_url + "/bareos-webui/auth/login")
        Select(driver.find_element_by_name("director")).select_by_visible_text("localhost-dir")
        driver.find_element_by_name("consolename").clear()
        driver.find_element_by_name("consolename").send_keys(username)
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys(password)
        driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        driver.find_element_by_link_text("English").click()
        driver.find_element_by_xpath("//input[@id='submit']").click()

    def logout(self):
        self.wait_for_element(By.LINK_TEXT, username).click()
        self.wait_for_element(By.LINK_TEXT, "Logout").click()

    def wait_for_url(self, what):
        # This Method clicks an URL and waits
        # until the URL matches the desired URL.
        start_time = time.time()
        i=0
        # the url to compare the current url against
        url=self.base_url + what
        # xpath-reference is generated
        xpath="//a[contains(@href, '%s')]" % what
        # while the url is not the desired url
        # try to click on the xpath element
        # until the time is more than 10 seconds
        # and displays the time the test took.
        while (url not in self.driver.current_url) and i<10:
            try:
                self.driver.find_element_by_xpath(xpath)
            except (NoSuchElementException, ElementNotInteractableException) as e:
                logging.debug("error %s", i)
            else:
                time.sleep(1)
                self.driver.find_element_by_xpath(xpath).click()
                timer = time.time() - start_time
                logging.debug(url + " loaded after %s seconds." % timer)
                return True
            time.sleep(1)
            i=i+1
            if(i==10):
                logging.debug("Generated timeout while loading %s", what)
                return False

    def neu_wait_for_url(self, value):
        i=10
        element="//a[contains(@href, '%s')]" % value
        while i>0 and element is None:
            try:
                tmp_element = self.driver.find_element(By.XPATH, element)
                if tmp_element.is_displayed():
                    element = tmp_element
            except ElementNotInteractableException:
                print "Waiting since %s sec" % (11-i)
                time.sleep(1)
            except NoSuchElementException:
                print "NSE Waiting since %s sec" % (11-i)
                time.sleep(1)
            except ElementNotVisibleException:
                print "NSE Waiting since %s sec" % (11-i)
                time.sleep(1)
            i=i-1
        
        if(i==0):
            print "Timeout while loading %s ." % value
        else:
            print "Element loaded after %s seconds." % (11-i)
            print element
        return element

    def wait_for_element(self, by, value):
        i=10
        element=None
        while i>0 and element is None:
            try:
                tmp_element = self.driver.find_element(by, value)
                if tmp_element.is_displayed():
                    element = tmp_element
            except ElementNotInteractableException:
                logging.debug(element, "Waiting since %s sec" % (11-i))
                time.sleep(1)
            except NoSuchElementException:
                logging.debug(element, "NSE Waiting since %s sec" % (11-i))
                time.sleep(1)
            except ElementNotVisibleException:
                logging.debug(element, "NSE Waiting since %s sec" % (11-i))
                time.sleep(1)
            i=i-1

        if(i==0):
            logging.debug(element, "Timeout while loading %s ." % value)
        else:
            logging.debug(element, "Element loaded after %s seconds." % (11-i))
        return element

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)
        


if __name__ == "__main__":
    # Configure the logger
    logging.basicConfig(format='%(levelname)s %(module)s.%(funcName)s: %(message)s', level=logging.INFO)
    logger = logging.getLogger()

    # Get attributes as environment variables,
    # if not available or set use defaults.
    browser = os.environ.get('BROWSER')
    if not browser:
        browser = 'firefox'
    restorefile = os.environ.get('RESTOREFILE')
    if not restorefile:
        restorefile = '/usr/sbin/bconsole'
    username = os.environ.get('USERNAME')
    if not username:
        username = "admin"
    password = os.environ.get('PASSWORD')
    if not password:
        password = "secret"
    t = 3
    targethost = os.environ.get('VM_IP')
    if not targethost:
        targethost = "10.20.240.49"
    unittest.main()
