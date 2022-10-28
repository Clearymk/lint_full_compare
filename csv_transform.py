import pandas as pd
import os


def csv_to_xlsx_pd(file_dir):
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            filename, file_extension = os.path.splitext(file)
            if file_extension.endswith(".csv"):
                csv = pd.read_csv(os.path.join(root, file), encoding='utf-8')
                csv.to_excel(os.path.join(root, filename + ".xlsx"), sheet_name='data', index=False)


if __name__ == '__main__':
    csv_to_xlsx_pd("data")
