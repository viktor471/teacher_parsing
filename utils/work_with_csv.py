import os
import pandas as pd


class CsvWriter:
    def __init__(self, csv_file_name: str, headers: list | tuple = None):
        self._file = open(csv_file_name, "w+")
        self._first_recording = True

        if headers:
            self._append_iterable_to_csv(headers)

    def _append_iterable_to_csv(self, iterable: list | tuple ):
        joined = ",".join(str(el) for el in iterable)
        self._file.write(f"{joined}\n")


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
                self._append_iterable_to_csv(some_dict.values())
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
