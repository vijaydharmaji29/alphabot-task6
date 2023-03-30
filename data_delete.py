import os
import csv
from datetime import datetime

def deleted(curr_rows):
    mindate = datetime(2022, 11, 9, 9, 15, 59)
    maxdate = datetime(2022, 11, 17, 15, 29, 59)
    new_rows = []
    ctr = 0
    
    for i in curr_rows:
        do = datetime.strptime(i[4] + ' ' + i[5], '%Y-%m-%d %H:%M:%S')
        if do >= mindate and do <= maxdate:
            if do.hour == 15 and do.minute == 30:
                i[5] = '15:29:59'
            new_rows.append(i)

    return new_rows

def delete_data(filename):

    curr_rows = []
    with open('Data/niftyoptions/' + filename) as file:
         csvfile = csv.reader(file)
         for row in file:
              curr_rows.append(row.split(','))

    header = curr_rows.pop(0)
    header[-1] = 'OI'

    new = deleted(curr_rows)

    # print(curr_rows)

    with open('Data/niftymodopts/' + filename, 'w') as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(header)
        for i in new:
            i[-1] = int(i[-1])
            csvwriter.writerow(i)


    print('DONE -', filename)

if __name__ == '__main__':
    files = os.listdir('Data/niftyoptions/')
    files.remove('.DS_Store')

    for f in files:
        # try:
        #     delete_data(f)
        # except:
        #     print('ERROR: ', f)

        delete_data(f)
