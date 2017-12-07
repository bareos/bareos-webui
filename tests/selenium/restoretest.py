# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, TimeoutException, WebDriverException, ElementNotInteractableException, InvalidSelectorException
import unittest, time, re, sys, os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys





class WebuiSeleniumTest(unittest.TestCase):
    def setUp(self):
        d = DesiredCapabilities.FIREFOX
        d['loggingPrefs'] = { 'browser':'ALL' }
        fp = webdriver.FirefoxProfile()
        fp.set_preference('webdriver.log.file', os.getcwd() + '/firefox_console')
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(4)
        self.base_url = "http://%s" % targethost
        self.verificationErrors = []
        self.accept_next_alert = True
        
    def test_restore(self):        
        
        
        driver = self.driver
        actions = ActionChains(self.driver)
        # LOGGING IN:
        driver.get(self.base_url + "/bareos-webui/auth/login")
        driver.find_element_by_xpath("//button[@type='button']").click()
        driver.find_element_by_xpath("//form[@id='login']/div/div/div/div/div[2]/div/ul/li[2]/a/span").click()
        driver.find_element_by_name("consolename").clear()
        driver.find_element_by_name("consolename").send_keys(username)
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys(password)
        driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        driver.find_element_by_link_text("English").click()
        driver.find_element_by_xpath("//input[@id='submit']").click()
        
        # CHANGING TO RESTORE TAB:
        self.click_and_wait("/bareos-webui/restore/")
        
        
        
        # SELECTING CLIENT:
        # Selects the correct client
        self.click_element_and_wait("(//button[@type='button'])[3]")
        driver.find_element_by_css_selector("span.text").click()
        # self.click_element_and_wait("/html/body/div[2]/div/div/form/div[1]/div[1]/p[1]/div/div/ul/li[1]/a/span[1]")
        
        # driver.find_element_by_link_text(client).click()
        
        
        # CLICK ON FILE VIA XPATH-POSITION:
        # to be replaced by click_element_and_wait
        # self.click_element_and_wait("//a[contains(text(),'/')]")
        # driver.find_element_by_xpath("//a[contains(text(),'/')]").click()
        # driver.find_element_by_xpath("//a[contains(text(),'/')]").click()
        # time.sleep(t)
        element = self.wait_for_element(By.XPATH, "//a[contains(text(),'/')]")
        # element = driver.find_element_by_xpath("//a[contains(text(),'/')]")
        print "element %s - %s" % (element, dir(element))
        
        # actions.double_click(element)
        # actions.perform()
        element.send_keys(Keys.ARROW_RIGHT)
        time.sleep(t)
        
        
        self.click_element_and_wait("//a[contains(text(),'etc/')]")
        self.click_element_and_wait("//a[contains(text(),'bareos/')]")
        self.click_element_and_wait("//a[contains(text(),'bconsole.conf')]")
        
        
        # CONFIRMATION:
        # Clicks on 'submit'
        self.click_element_and_wait("//input[@id='submit']")
        # Confirms alert that has text "Are you sure ?"
        self.assertRegexpMatches(self.close_alert_and_get_its_text(), r"^Are you sure[\s\S]$")
        
        
        # LOGOUT:
        # Opens the dropdown menue and chooses logout        
        driver.find_element_by_link_text(username).click()
        time.sleep(2)
        driver.find_element_by_link_text("Logout").click()
                
    # This Method clicks and URL and waits
    # until the URL matches the desired URL.
    def click_and_wait(self, what):
        start_time = time.time()
        i=0
        # the url to compare the current url against
        url=self.base_url + what
        print url
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
                print "error %s" % i
            else:
                time.sleep(1)
                print "Try %s succeeded" % what
                self.driver.find_element_by_xpath(xpath).click()
                return True
            time.sleep(1)
            i=i+1
            if(i==10):
                print "Generated timeout."
                return True
        timer = time.time() - start_time
        print url + " loaded after %s seconds." % timer
        
    # Works like click_and_wait but also
    # works with non-url's: the xpath
    # must be given as argument when calling.
    def click_element_and_wait(self, xpath):
        i=0
        t=0
        found=False
        # while i<6 and found=False:
        while i<6 and t==0:
            time.sleep(2)
            try:
                self.driver.find_element_by_xpath(xpath)
            except ElementNotInteractableException:
                print "Waiting since %s sec" % i
            # except NoSuchElementException:
           #      print "Waiting ince %s sec" % i
           #      i=i+1
            else:
                 print "Try %s succeeded" % xpath
                 self.driver.find_element_by_xpath(xpath).click()
                 time.sleep(2)
                 t=1
                 # found=True
            i=i+1
            if(i==6):
                print "Timeout while loading %s ." % xpath
                
        if(i==6):
            return False
        else:    
            print "Element loaded after %s seconds." %i

    def wait_for_element(self, by, value):
        i=10
        element=None
        # while i<6 and found=False:
        while i>0 and element is None:
            try:
                element = self.driver.find_element(by, value)
            except ElementNotInteractableException:
                print "Waiting since %s sec" % i
                time.sleep(1)
            except NoSuchElementException:
                print "NSE Waiting ince %s sec" % i                
                time.sleep(1)
            i=i-1
                
        if(i==0):
            print "Timeout while loading %s ." % xpath
            return None
        else:    
            print "Element loaded after %s seconds." %i
            return element

        
    # def wait_for_element(self, what):
    #     element = WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((By.XPATH, what))
    #     )

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

    # get username from environment if set
    # otherwise use defaults
    client = "bareos-fd"
    username = os.environ.get('USERNAME')
    password = os.environ.get('PASSWORD')
    if not username:
        username = "admin"
    if not password:
        password = "secret"
    t = 3
    targethost = os.environ.get('VM_IP')
    if not targethost:
        targethost = "10.20.240.49"
    unittest.main()