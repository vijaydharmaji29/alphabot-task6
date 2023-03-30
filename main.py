import data_giver as dg
import csv
import brain
import executioner

def run():
    all_actions = []
    #getting all possible datetimes
    all_datetimes = []
    capital = 0
    positions = []
    last_call_price, last_put_price = None, None

    #for calculating all possible datetimes
    with open('Data/df_csv/NIFTY22N1714900PE.csv', mode ='r')as file:
        csvFile = csv.reader(file)  
        for lines in csvFile:
            if lines[0] != 'datetime':
                dateformated = lines[0]
                all_datetimes.append(dateformated)

    print('CALCULATING...')

    flag = True

    for i in range(len(all_datetimes)):
        # print(all_datetimes[i][14:16])
        if int(all_datetimes[i][14:16]) % 15 != 0 and all_datetimes[i][11:16] != '15:19' and all_datetimes[i][11:16] != '09:15':
            continue
        
        if all_datetimes[i][11:13] == '18' or all_datetimes[i][11:13] == '19':
            continue

        call_df, put_df = dg.next(all_datetimes[i])

        if len(call_df) == 0 or len(put_df) == 0:
            continue

        try:
        
            execute, last_call_price, last_put_price = brain.calculate(call_df, put_df, positions, last_call_price, last_put_price)
        
        except:
            print('ERROR: ', all_datetimes[i], flag, all_datetimes[i][11:16])
            break    

        if len(execute) > 0:
            print(execute)

            executed, capital, positions = executioner.trade(execute, capital, positions)
            for e in executed:
                all_actions.append((e.date, e.option_type, e.strike, e.qty, e.sell, e.sell_val))
                print(e.option_type, e.strike, e.qty, e.buy, e.sell_val)

        fields = ['Datetime', 'Option Type', 'Strike', 'Qty', 'Sell', 'Sell Value']

        #writing to csv file
        with open('Data/actions.csv', 'w') as csvfile: 
            # creating a csv writer object 
            csvwriter = csv.writer(csvfile) 
                
            # writing the fields 
            csvwriter.writerow(fields) 
                
            # writing the data rows 
            csvwriter.writerows(all_actions)


        
if __name__ == '__main__':
    run()
