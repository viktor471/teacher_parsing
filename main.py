from teacher_parsing import parse_teachers
from utils.work_with_csv import get_dataframe_from_csv

def main():
    # TODO брать аргументы для выбора действий
    parse_teachers(filename)
    df = get_dataframe_from_csv(filename)

    # model = Model()

    # p
    # model.fit(x, y)
