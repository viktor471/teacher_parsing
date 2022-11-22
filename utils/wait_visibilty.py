from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import WebDriverException
from typing import Callable

class Waiter:
    def __init__(self, logger, driver):
        self._logger = logger
        self._driver = driver

    def _try_wait_for(self, wait_function, by, value) -> Callable:
        try:
            wait_function(self, by, value)
        except WebDriverException as ex:
            if not ex.msg.isspace():
                self._logger.info(ex.msg)
            self._logger.info(f"Element(s) wasn't loaded {value} by {by} in page: \n {self._driver.title}")
        return False

    def wait_element_visibility(self, by, value, waiting_sec: int = 60):
        WebDriverWait(self._driver, waiting_sec).until(ec.visibility_of_element_located((by, value)))

    def wait_elements_visibility(self, by, value, waiting_sec: int = 60):
        WebDriverWait(self._driver, waiting_sec).until(ec.visibility_of_all_elements_located((by, value)))



