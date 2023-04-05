import csv
from datetime import datetime
import os

#getting all datetimes possible
all_datetimes = []
with open('data/BANKNIFTY.csv', mode ='r')as file:
        # reading the CSV file
        csvFile = csv.reader(file)
        # displaying the contents of the CSV file
        for lines in csvFile:
            dateformated = lines[1][6:10] + '-' + lines[1][3:5] + '-' + lines[1][0:2] + ' ' + lines[1][-5:] + ':59'
            all_datetimes.append(dateformated)
all_datetimes.pop(0)

all_datetime_modified = []
datetime_max = datetime.strptime('2022-11-17 15:29:59', '%Y-%m-%d %H:%M:%S')
datetime_min = datetime.strptime('2022-10-17 09:15:59', '%Y-%m-%d %H:%M:%S')

for i in all_datetimes:
    datetime_obj = datetime.strptime(i, '%Y-%m-%d %H:%M:%S')
    if datetime_obj >= datetime_min and datetime_obj <= datetime_max:
        all_datetime_modified.append(i)



def add_before(curr_rows):
    new_rows = []
    ctr = 0
    for i in all_datetime_modified:
        # print(i, ' = ', curr_rows[0][4] + ' ' + curr_rows[0][5])
        if i != (curr_rows[0][4] + ' ' + curr_rows[0][5]):
            new_rows.append((curr_rows[ctr][0], curr_rows[ctr][1], curr_rows[ctr][2], curr_rows[ctr][3], i[:10], i[11:], curr_rows[ctr][6], curr_rows[ctr][7], curr_rows[ctr][8], curr_rows[ctr][9], 0, 0))
        else:
            print("breakkk")
            print(i, ' = ', curr_rows[0][4] + ' ' + curr_rows[0][5])
            break

    return new_rows

def add_middle(curr_rows, start):
    new_rows = []

    ctr = 0
    flag = True

    for i in all_datetime_modified[start: ]:
        new_rows.append((curr_rows[ctr][0], curr_rows[ctr][1], curr_rows[ctr][2], curr_rows[ctr][3], i[:10], i[11:], curr_rows[ctr][6], curr_rows[ctr][7], curr_rows[ctr][8], curr_rows[ctr][9], 0, 0))
        # print(i,' = ',  curr_rows[ctr][4] + ' ' + curr_rows[ctr][5])
        if i == (curr_rows[ctr][4] + ' ' + curr_rows[ctr][5]):
            print(i,' = ',  curr_rows[ctr][4] + ' ' + curr_rows[ctr][5], ctr)
            ctr += 1
            if ctr == len(curr_rows):
                ctr -= 1

    # print(curr_rows[ctr][4] + ' ' + curr_rows[ctr][5], ctr)

    return new_rows
    
def add_data(filename):
    #adding before
    curr_rows = []
    with open('Data/niftymodopts/' + filename) as file:
         csvfile = csv.reader(file)
         for row in file:
              curr_rows.append(row.split(','))

    header = curr_rows.pop(0)
    header[-1] = 'OI'
    

    # print(header)
    # print(type(header))

    # print(curr_rows[371])

    new = add_before(curr_rows)

    new += add_middle(curr_rows, len(new))

    with open('Data/niftymodopts/' + filename, 'w') as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(header)
        for i in new:
            csvwriter.writerow(i)


    print('DONE -', filename)


if __name__ == '__main__':
    files = os.listdir('Data/niftyoptions/')
    files.remove('.DS_Store')

    for f in files:
        try:
            add_data(f)
        except:
            print(f)

    # add_data('NIFTY22N1718400PE.csv')