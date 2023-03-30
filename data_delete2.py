import os
import csv

if __name__ == '__main__':
    files = os.listdir('Data/niftymodopts/')
    files.remove('.DS_Store')

    todel = []

    for f in files:
        with open('Data/niftymodopts/' + f) as file:
            csvfile = csv.reader(file)
            ctr = 0
            try:
                for row in csvfile:
                    ctr += 1
            except:
                print('ERROR: ', f)

        if ctr <= 1:
            todel.append(f)

        # curr_rows = []
        # with open('Data/niftymodopts/' + f) as file:
        #  csvfile = csv.reader(file)
        #  for row in csvfile:
        #     pr
    print(todel)

    for f in todel:
        os.remove('Data/niftymodopts/' + f)
        os.remove('Data/df_csv/' + f)