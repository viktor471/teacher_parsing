from selenium.webdriver.common.by import By
from selenium import webdriver
from utils.logger import catch_errors_to_log, get_logger, Output
from utils.wait_visibilty import Waiter
from logging import ERROR, WARNING
import logging

unloaded_values = get_logger("unloaded_values", WARNING, Output.ConsoleAndFileOutput,
                             "logs/unloaded_values.log")

errors   = get_logger("errors",   ERROR,   Output.ConsoleAndFileOutput, "logs/errors.log")
warnings = get_logger("warnings", WARNING, Output.ConsoleAndFileOutput, "logs/warnings.log")

def parse_teachers():
    teacher_links = []

    teachers = {}

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
            warnings.info(f"field {field} not in english keys")
            key_ = field

        return key_

    driver = webdriver.Firefox()
    waiter = Waiter(logger=unloaded_values, driver=driver)
    driver.get("https://wiki.mipt.tech")

    xpath = "//a[contains(@title, 'Кафедра') or " \
            "    contains(@title, 'Высшая школа системного') or " \
            "    contains(@title, 'Военная')] "

    department_elements = driver.find_elements(By.XPATH, xpath)

    departments = [el.get_attribute("href") for el in department_elements
                   if "биофизики и экологии" not in el.get_attribute("title")]

    for department in departments:
        driver.get(department)
        current_teachers_div_xpath = "//span[text()='Преподаватели кафедры']/parent::h2/following-sibling::div"
        current_teachers_div = driver.find_element(By.XPATH, current_teachers_div_xpath)

        for teacher_element in current_teachers_div.find_elements(By.XPATH, "//div[contains(@class, 'gallerytext')]"
                                                                            "/p/a"):
            teacher_links.append(teacher_element.get_attribute("href"))


    for teacher_link in teacher_links:
        driver.get(teacher_link)

        teacher = {"name": driver.find_element(By.TAG_NAME, 'h1').text}

        wiki_table = driver.find_element(By.XPATH, "//table[contains(@class, 'wikitable')]")

        ths = wiki_table.find_elements(By.XPATH, "//th[not(contains(@colspan, '2'))]")

        for th in ths:
            with catch_errors_to_log(errors, driver.title):
                td = th.find_element(By.XPATH, "./following-sibling::td")
                name = th.text
                value = td.text

                if "\n" in value:
                    value = td.text.split("\n")

                key = get_eng_key(name)
                teacher[key] = value

        template = ('//div[contains(@title, "Отлично")]'
                    '/following-sibling::div[contains(@class, "ratingsinfo-avg")]')

        if not waiter.wait_elements_visibility(By.XPATH, template):
            wrong_elements = wiki_table.find_elements(By.XPATH, template)
            for wrong_element in wrong_elements:
                if not wrong_element.text:
                    name_of_wrong_field_xpath = "../../../preceding-sibling::td"
                    description = wrong_element.find_element(By.XPATH, name_of_wrong_field_xpath).text
                    unloaded_values.warning(f"Пустое поле '{description}' у преподавателя '{teacher['name']}'")


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
        teachers[name] = teacher

    print(teachers)

    input()
    driver.quit()


if __name__ == "__main__":
    parse_teachers()
