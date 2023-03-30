import os
import pandas as pd

all_files = os.listdir('Data/df_csv/') #getting all possible options
all_files.remove('.DS_Store')
all_options_df = {} #dictionary for storing all data of each option
calldf = pd.DataFrame()

for file in all_files:
    # print('GETTING DATA FOR -', file[:-4], end='')
    new_df = pd.read_csv('Data/df_csv/' + file)
    new_df['datetime'] = pd.to_datetime(new_df['Date'] + ' ' + new_df['Time'])
    new_df.set_index('datetime', inplace=True)
    all_options_df[file[:-4]] = new_df

def next(datetime):
    call_df = pd.DataFrame()
    put_df = pd.DataFrame()

    call_df_data = {'Symbol': [], 'Expiry': [], 'Strike': [], 'OptionType': [], 'datetime': [], 'Close': [], 'Underlying Value': []}
    put_df_data = {'Symbol': [], 'Expiry': [], 'Strike': [], 'OptionType': [], 'datetime': [], 'Close': [], 'Underlying Value': []}

    for i in all_options_df:

        # if datetime in all_options_df[i].index.values:
        # try:
        #     # row = all_options_df[i].loc[datetime]
        #     if i[-2:] == 'CE':
        #         call_df_data['Symbol'].append(all_options_df[i].loc[datetime]['Symbol'])
        #         call_df_data['Expiry'].append(all_options_df[i].loc[datetime]['Expiry'])
        #         call_df_data['Strike'].append(all_options_df[i].loc[datetime]['Strike'])
        #         call_df_data['OptionType'].append(all_options_df[i].loc[datetime]['OptionType'])
        #         call_df_data['datetime'].append(all_options_df[i].loc[datetime]['Date'] + ' ' + all_options_df[i].loc[datetime]['Time'])
        #         call_df_data['Close'].append(all_options_df[i].loc[datetime]['Close'])
        #         call_df_data['Underlying Value'].append(all_options_df[i].loc[datetime]['Underlying Value'])

        #     elif i[-2:] == 'PE':
        #         put_df_data['Symbol'].append(all_options_df[i].loc[datetime]['Symbol'])
        #         put_df_data['Expiry'].append(all_options_df[i].loc[datetime]['Expiry'])
        #         put_df_data['Strike'].append(all_options_df[i].loc[datetime]['Strike'])
        #         put_df_data['OptionType'].append(all_options_df[i].loc[datetime]['OptionType'])
        #         put_df_data['datetime'].append(all_options_df[i].loc[datetime]['Date'] + ' ' + all_options_df[i].loc[datetime]['Time'])
        #         put_df_data['Close'].append(all_options_df[i].loc[datetime]['Close'])
        #         put_df_data['Underlying Value'].append(all_options_df[i].loc[datetime]['Underlying Value'])
        # except:
        #     print('ERROR', i)

        # print(i)

        if i[-2:] == 'CE':
            call_df_data['Symbol'].append(all_options_df[i].loc[datetime]['Symbol'])
            call_df_data['Expiry'].append(all_options_df[i].loc[datetime]['Expiry'])
            call_df_data['Strike'].append(all_options_df[i].loc[datetime]['Strike'])
            call_df_data['OptionType'].append(all_options_df[i].loc[datetime]['OptionType'])
            call_df_data['datetime'].append(all_options_df[i].loc[datetime]['Date'] + ' ' + all_options_df[i].loc[datetime]['Time'])
            call_df_data['Close'].append(all_options_df[i].loc[datetime]['Close'])
            call_df_data['Underlying Value'].append(all_options_df[i].loc[datetime]['Underlying Value'])

        elif i[-2:] == 'PE':
            put_df_data['Symbol'].append(all_options_df[i].loc[datetime]['Symbol'])
            put_df_data['Expiry'].append(all_options_df[i].loc[datetime]['Expiry'])
            put_df_data['Strike'].append(all_options_df[i].loc[datetime]['Strike'])
            put_df_data['OptionType'].append(all_options_df[i].loc[datetime]['OptionType'])
            put_df_data['datetime'].append(all_options_df[i].loc[datetime]['Date'] + ' ' + all_options_df[i].loc[datetime]['Time'])
            put_df_data['Close'].append(all_options_df[i].loc[datetime]['Close'])
            put_df_data['Underlying Value'].append(all_options_df[i].loc[datetime]['Underlying Value'])

    call_df['Symbol'] = call_df_data['Symbol']
    call_df['Expiry'] = call_df_data['Expiry']
    call_df['Strike'] = call_df_data['Strike']
    call_df['OptionType'] = call_df_data['OptionType']
    call_df['datetime'] = call_df_data['datetime']
    call_df['Close'] = call_df_data['Close']
    call_df['Underlying Value'] = call_df_data['Underlying Value']
    call_df['Index'] = call_df['Strike']


    put_df['Symbol'] = put_df_data['Symbol']
    put_df['Expiry'] = put_df_data['Expiry']
    put_df['Strike'] = put_df_data['Strike']
    put_df['OptionType'] = put_df_data['OptionType']
    put_df['datetime'] = put_df_data['datetime']
    put_df['Close'] = put_df_data['Close']
    put_df['Underlying Value'] = put_df_data['Underlying Value']
    put_df['Index'] = put_df['Strike']


    call_df.set_index('Index', inplace=True)
    put_df.set_index('Index', inplace=True)

    return call_df, put_df

if __name__ == '__main__':
    call_df, put_df = next('2020-12-07 10:00:59')
    print(call_df.head())
    print(put_df.head())
    print('DONE')
