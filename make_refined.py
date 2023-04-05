import pandas as pd
import csv

if __name__ == '__main__':
    df = pd.read_csv('Data/actions.csv')
    trades = []
    fields = ['Ticker', 'Time of Entry', 'Qty', 'Entry Price', 'Time of Exit', 'Exit Price', 'PnL', 'Cummulative PnL']
    positions_dict = {}
    c_pnl = 0
    for i in range(len(df)):
        if df.iloc[i]['Sell'] == True:
            ticker = str(df.iloc[i]['Strike']) + str(df.iloc[i]['Option Type']) + str(df.iloc[i]['Datetime'])
            positions_dict[ticker] = df.iloc[i]
        else:
            ticker = str(df.iloc[i]['Strike']) + str(df.iloc[i]['Option Type'] + str(df.iloc[i]['ID']))
            entry_series = positions_dict[ticker]
            time_of_entry = entry_series['Datetime']
            qty = entry_series['Qty']
            entry_price = float(entry_series['Sell Value'])

            time_of_exit = df.iloc[i]['Datetime']
            exit_price = float(df.iloc[i]['Buy Value'])

            pnl = (entry_price - exit_price)*int(qty)
            c_pnl += pnl

            trades.append((ticker, time_of_entry, qty, entry_price, time_of_exit, exit_price, pnl, c_pnl))


        #writing to csv file
        with open('Data/refined_actions.csv', 'w') as csvfile: 
            # creating a csv writer object 
            csvwriter = csv.writer(csvfile) 
                
            # writing the fields 
            csvwriter.writerow(fields) 
                
            # writing the data rows 
            csvwriter.writerows(trades)

