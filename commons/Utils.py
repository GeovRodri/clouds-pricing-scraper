import os
import time
from time import sleep

from commons.Log import Log


class Utils(object):

    def __init__(self, driver):
        self.driver = driver

    def wait_for(self, condition_function):
        start_time = time.time()
        while time.time() < start_time + 3:
            if condition_function():
                return True
            else:
                time.sleep(0.1)
        raise Exception('Timeout waiting for {}'.format(condition_function.__name__))

    def page_has_loaded(self):
        page_state = self.driver.execute_script('return document.readyState;')
        return page_state == 'complete'

    @staticmethod
    def start_docker():
        Log.info('Killing firefox active containers...')
        os.system('docker kill firefox')

        Log.info('Removing old firefox containers...')
        os.system('docker rm firefox')

        Log.info('Running a new firefox container...')
        os.system('docker run -d -p 4444:4444 -p 5900:5900 --name firefox --network selenium'
                  ' -v /dev/shm:/dev/shm selenium/standalone-firefox-debug:3.14.0-dubnium')
        sleep(10)
