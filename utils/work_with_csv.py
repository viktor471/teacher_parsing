import itertools
import os
import pandas as pd


class CsvWriter:
    def __init__(self, csv_file_name: str, headers: list | tuple = None):
        self._file = open(csv_file_name, "w+")
        self._first_recording = True

        if headers:
            self._append_iterable_to_csv(headers)

    def _append_iterable_to_csv(self, iterable: list | tuple ):
        joined = ";".join(str(el) for el in iterable)
        self._file.write(f"{joined}\n")

    def _append_complex_dict_to_csv(self, target_dict: dict):
        complex_fields_keys = []
        for key, value in target_dict.items():
            if isinstance(value, list):
                complex_fields_keys.append(key)

        if complex_fields_keys:
            itertools_args = [target_dict[key] for key in complex_fields_keys]

            for fields in itertools.product(*itertools_args):
                field_dict = dict(zip(complex_fields_keys, fields))

                dict_for_record = target_dict.copy()

                for key, value in field_dict.items():
                    dict_for_record[key] = value

                self._append_iterable_to_csv(dict_for_record.values())
        else:
            self._append_iterable_to_csv(target_dict.values())

    @property
    def first_recording(self) -> bool:
        if self._first_recording:
            self._first_recording = False
            return True
        else:
            return False

    def append_to_csv(self, smth_to_write: dict):
        match smth_to_write:
            case dict(some_dict):
                if self.first_recording:
                    self._append_iterable_to_csv(some_dict.keys())
                self._append_complex_dict_to_csv(some_dict)
            case list(some_iterable) | tuple(some_iterable):
                self._append_iterable_to_csv(some_iterable)
            case _:
                raise RuntimeError(f"unknown type of smth_to_write: {smth_to_write}, type: {type(smth_to_write)}")

    def flush(self):
        self._file.flush()

    def __del__(self):
        self._file.close()


def get_dataframe_from_csv(filename: str) -> pd.DataFrame:
    if not os.path.isfile(filename):
        raise RuntimeError(f"csv file with dataframe {filename} not found")
    return pd.read_csv(filename)
