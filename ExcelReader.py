import pandas as pd
import os

class ExcelReader:
    def __init__(self):
        pass

    def get_columns_from_excel(self, file_path, columns):
        df = pd.read_csv(file_path)
    
        column_data = {}
    
        for column in columns:
            if isinstance(column, int):
                if column < 0 or column >= df.shape[1]:
                    raise ValueError(f"Column index {column} is out of range for this Excel sheet.")
                column_name = df.columns[column]  
                column_data[column_name] = df.iloc[:, column].tolist()
            elif isinstance(column, str):
                if column not in df.columns:
                    raise ValueError(f"Column name '{column}' does not exist in this Excel sheet.")
                column_data[column] = df[column].tolist()
            else:
                raise TypeError("Each column must be an integer (column index) or a string (column name).")
    
        return column_data
    
    
    def get_columns_from_xlsx(self, file_path, columns):
        df = pd.read_excel(file_path)
    
        column_data = {}
    
        for column in columns:
            if isinstance(column, int):
                if column < 0 or column >= df.shape[1]:
                    raise ValueError(f"Column index {column} is out of range for this Excel sheet.")
                column_name = df.columns[column]
                column_data[column_name] = df.iloc[:, column].tolist()
            elif isinstance(column, str):
                if column not in df.columns:
                    raise ValueError(f"Column name '{column}' does not exist in this Excel sheet.")
                column_data[column] = df[column].tolist()
            else:
                raise TypeError("Each column must be an integer (column index) or a string (column name).")
    
        return column_data

'''''
file_path = r'D:\Courses.csv' 
columns = [0, 1, 2, 5, 7, 8]

reader = ExcelReader()
data_dict = reader.get_columns_from_excel(file_path, columns)
num_rows = len(next(iter(data_dict.values())))

for row_index in range(num_rows):
    row_data = {col_name: data_list[row_index] for col_name, data_list in data_dict.items()}
    print(f"Data for row {row_index}: {row_data}")

'''
