from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import WebDriverException
from typing import Callable

class Waiter:
    def __init__(self, logger, driver):
        self._logger = logger
        self._driver = driver

    def wait_until(self, condition, waiting_sec: int, msg: str):
        try:
            WebDriverWait(self._driver, waiting_sec).until(condition)
            return True
        except WebDriverException as ex:
            if not ex.msg.isspace():
                self._logger.warning(ex.msg)
            if msg:
                self._logger.warning(msg)
            return False

    def wait_element_visibility(self, by, value, waiting_sec: int = 30):
        msg = f"Element wasn't loaded {value} by {by} in page: \n {self._driver.title}"
        condition = ec.visibility_of_element_located((by, value))
        return self.wait_until(condition, waiting_sec, msg)

    def wait_elements_visibility(self, by, value, waiting_sec: int = 30):
        msg = f"Elements wasn't loaded {value} by {by} in page: \n {self._driver.title}"
        condition = ec.visibility_of_all_elements_located((by, value))
        return self.wait_until(condition, waiting_sec, msg)



