import pandas as pd
import os

def create_data(df):
    niftydf = pd.read_csv('Data/niftydata.csv', index_col='date')
    uv = []

    for i in range(len(df)):
        try:
            d = str(df.iloc[i]['datetime'])[:-2] + '00+05:30'
            uv.append(niftydf.loc[d]['close'])
        except:
            uv.append(uv[-1])

    return uv

def get_data(filename):
    df = pd.read_csv('Data/niftymodopts/' + filename)
    df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    df['Underlying Value'] = create_data(df)

    df.set_index('datetime', inplace=True)

    return df

if __name__ == '__main__':
    files = os.listdir('Data/niftymodopts/')
    files.remove('.DS_Store')


    for i in files:
        print(i)
        df = get_data(i)
        df.to_csv('Data/df_csv/' + i)