from selenium.webdriver.common.by import By

from utils.work_with_csv import CsvWriter
from utils.driver import get_driver

from one_teacher_parsing import teacher_parsing


def parse_all_teachers(filename: str):
    """
    :param filename: название файла csv с результатом парсинга
    :return: None
    """
    csv_file = CsvWriter(filename)
    teacher_links = []

    driver = get_driver("drivers/chromedriver")

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

        class_attribute = current_teachers_div.get_attribute("class")

        if class_attribute:
            teacher_elements = current_teachers_div.find_elements(By.XPATH, "//div[contains(@class, 'gallerytext')]/p/a")
        else:
            teacher_elements = current_teachers_div.find_elements(By.TAG_NAME, "a")

        for teacher_element in teacher_elements:
            teacher_links.append(teacher_element.get_attribute("href"))

    for teacher_link in teacher_links:

        teacher = teacher_parsing(teacher_link, driver)

        csv_file.append_to_csv(teacher)
        csv_file.flush()

    driver.quit()


if __name__ == "__main__":
    # TODO генерировать имя по дате
    parse_all_teachers("csv/parsed.csv")
