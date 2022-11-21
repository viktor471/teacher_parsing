from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from functools import wraps
from typing import Callable
from bs4 import BeautifulSoup as Bs
import logging



driver = webdriver.Firefox()

def get_html_source(tag_element):
    soup_html = Bs(tag_element.get_attribute("outerHTML"), features="lxml").prettify()
    return soup_html.removeprefix("<html>\n <body>\n").removesuffix("\n </body>\n</html>")


def print_html(tag_element):
    print(get_html_source(tag_element))


def try_wait_for(wait_function) -> Callable:
    @wraps(wait_function)
    def new_wait_function(by, value):
        try:
            wait_function(by, value)
        except WebDriverException as ex:
            if not ex.msg.isspace():
                log.info(ex.msg)
            log.info(f"Element(s) wasn't loaded {value} by {by} in page: \n {driver.title}")
            return False

    return new_wait_function


@try_wait_for
def wait_element_visibility(by, value, waiting_sec: int = 60):
    WebDriverWait(driver, waiting_sec).until(ec.visibility_of_element_located((by, value)))


@try_wait_for
def wait_elements_visibility(by, value, waiting_sec: int = 60):
    WebDriverWait(driver, waiting_sec).until(ec.visibility_of_all_elements_located((by, value)))


driver.get("https://wiki.mipt.tech")

xpath = "//a[contains(@title, 'Кафедра') or contains(@title, 'Высшая школа системного') or contains(@title, 'Военная')]"
department_elements = driver.find_elements(By.XPATH, xpath)

departments = [el.get_attribute("href") for el in department_elements
               if "биофизики и экологии" not in el.get_attribute("title")]

teacher_links = []

teachers = []

english_keys = {"Имя":                "name",
                "Альма-матер":        "alma_mater",
                "Дата рождения":      "birthday",
                "Учёная степень":     "academic_degree",
                "Работает":           "department",
                "Работал":            "preceding_work",
                "Ведёт":              "subject",
                "Вёл":                "preceding subject",
                "Знания":             "knowledge",
                "Умение преподавать": "teaching_skill",
                "В общении":          "soft_skill",
                "«Халявность»":       "freebie",
                "Халявность":         "freebie",
                "Общая оценка":       "total_score"}


def get_eng_key(field: str) -> str:
    key_ = english_keys.get(field, None)

    if not key_:
        log.info(f"field {field} not in english keys")
        key_ = field

    return key_


for department in departments:
    driver.get(department)
    current_teachers_div_xpath = "//span[text()='Преподаватели кафедры']/parent::h2/following-sibling::div"
    current_teachers_div = driver.find_element(By.XPATH, current_teachers_div_xpath)

    for teacher_element in current_teachers_div.find_elements(By.TAG_NAME, "a"):
        teacher_links.append(teacher_element.get_attribute("href"))


for teacher_link in teacher_links:
    driver.get(teacher_link)

    teacher = {}

    teacher["name"] = driver.find_element(By.TAG_NAME, 'h1').text
    
    wiki_table = driver.find_element(By.XPATH, "//table[contains(@class, 'wikitable')]")

    ths = wiki_table.find_elements(By.XPATH, "//th[not(contains(@colspan, '2'))]")

    for th in ths:
        try:
            td = th.find_element(By.XPATH, "./following-sibling::td")
            name = th.text
            value = td.text

            if "\n" in value:
                value = td.text.split("\n")

            key = get_eng_key(name)
            teacher[key] = value
        except WebDriverException as ex:
            log.info(f"Exception: {ex} in page {driver.title}")

    template = ('//div[contains(@title, "Отлично")]'
                '/following-sibling::div[contains(@class, "ratingsinfo-avg")]')

    if not wait_elements_visibility(By.XPATH, template):
        wrong_elements = wiki_table.find_elements(By.XPATH, template)
        for wrong_element in wrong_elements:
            if not wrong_element.text:
                name_of_wrong_field_xpath = "../../../preceding-sibling::td"
                description = wrong_element.find_element(By.XPATH, xpath).text
                log.info(f"Пустое поле '{description}' у преподавателя '{teacher['name']}'")


    stars = wiki_table.find_elements(By.XPATH, template)

    for star in stars:
        xpath = "../../../preceding-sibling::td"
        description = star.find_element(By.XPATH, xpath).text
        if star.text:
            score, _ = star.text.split(" ")
        else:
            score = ""

        key = get_eng_key(description)
        teacher[key] = score

    print(teacher)
    teachers.append(teacher)

print(teachers)

input()
driver.quit()
