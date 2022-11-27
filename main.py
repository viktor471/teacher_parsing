from all_teachers_parsing import parse_all_teachers
from utils.work_with_csv import get_dataframe_from_csv


def main():
    # TODO брать аргументы для выбора действий
    parse_all_teachers("csv/parsed.csv")
    df = get_dataframe_from_csv("csv/parsed.csv")

    # model = Model()

    # p
    # model.fit(x, y)
