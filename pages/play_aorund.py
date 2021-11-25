import pandas as pd
data_list = [[1, 2, 2], [4, 1, 4]]
new_list = []
max_value = 4
num_of_columns = len(data_list[0]) - 1
for i in range(0, max_value + 1):
    empty_row = [0] * num_of_columns
    row = [i] + empty_row
    new_list.append(row)
# for i in range(0, max_value + 1):
for row in data_list:
    index = row[0]
    new_list[index] = row

print(new_list)




print(new_list)