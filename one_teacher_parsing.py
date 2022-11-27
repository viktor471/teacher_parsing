from logging import WARNING, ERROR

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver

from utils.wait_visibilty import Waiter
from utils.logger import get_logger, Output, catch_errors_to_log
from utils.driver import get_driver
from utils.work_with_csv import CsvWriter

warnings = get_logger("warnings", WARNING, Output.ConsoleAndFileOutput, "logs/warnings.log")
errors   = get_logger("errors",   ERROR,   Output.ConsoleAndFileOutput, "logs/errors.log")
unloaded_values = get_logger("unloaded_values", WARNING, Output.ConsoleAndFileOutput,
                             "logs/unloaded_values.log")

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


def teacher_parsing(teacher_link: str, driver: WebDriver) -> dict:
    driver.get(teacher_link)
    teacher = {}
    for key in english_keys.values():
        teacher[key] = ""

    teacher["name"] = driver.find_element(By.TAG_NAME, 'h1').text

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

    waiter = Waiter(logger=unloaded_values, driver=driver)
    
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
    
    return teacher


if __name__ == "__main__":
    driver = get_driver("drivers/chromedriver")

    link = ("https://wiki.mipt.tech/index.php/%D0%90%D0%B3%D0%B0%D1%85%D0%B0%D0%BD%D0%BE%D0%B2_%D0%9D%D0%B0"
            "%D0%B7%D0%B0%D1%80_%D0%A5%D0%B0%D0%BD%D0%B3%D0%B5%D0%BB%D1%8C%D0%B4%D1%8B%D0%B5%D0%B2%D0%B8%D1%87")

    teacher = teacher_parsing(link, driver)

    csv_file = CsvWriter("csv/test.csv")

    csv_file.append_to_csv(teacher)

    print(teacher)

