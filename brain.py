class action(object):
    def __init__(self, ticker, option_type, strike ,expiry,qty, buy, sell, buy_val, sell_val, date, trade_type, id='0'):
        self.ticker = ticker
        self.option_type = option_type
        self.strike = strike
        self.expiry = expiry
        self.qty = qty
        self.buy = buy
        self.sell = sell
        self.buy_val = buy_val
        self.sell_val = sell_val
        self.date = date
        self.trade_type = trade_type #True for longing, False for shorting
        self.id = id

def calculate(call_df, put_df, positions, last_call_price, last_put_price):
    execute = []

    if len(call_df) == 0 or len(put_df) == 0:
        return execute
    
    #morning trade
    if str(call_df.iloc[0]['datetime'])[11:] == '09:15:59':
        print('Last call price:', last_call_price, ' - Last put price:', last_put_price)

        #sell atm straddle
        #finding atm strike - min difference betwene strike and underlying value
        min = abs(call_df.iloc[0].Strike - call_df.iloc[0]['Underlying Value'])
        atm_strike = call_df.iloc[0].Strike
        
        for i in range(len(call_df)):
            if abs(call_df.iloc[i].Strike - call_df.iloc[i]['Underlying Value']) < min:
                min = abs(call_df.iloc[i].Strike - call_df.iloc[i]['Underlying Value'])
                atm_strike = call_df.iloc[i].Strike

        call_atm = call_df.loc[atm_strike]
        put_atm = put_df.loc[atm_strike]

        action_call = action(call_atm.Symbol, 'CE',call_atm.Strike, call_atm.Expiry, 1, False, True, 0, call_atm.Close, call_atm.datetime, False)
        action_put = action(put_atm.Symbol, 'PE', put_atm.Strike, put_atm.Expiry, 1, False, True, 0, put_atm.Close, put_atm.datetime, False)

        execute.append(action_call)
        execute.append(action_put)

        last_call_price = call_atm.Close
        last_put_price = put_atm.Close

        print('Call ATM:', last_call_price, ' - Put ATM:', last_put_price)
        return execute, last_call_price, last_put_price


    #otherwise checking if 30% move
    # print('checking for 30 call', call_df.loc[positions[0].strike].Close, last_call_price)
    # print('checking for 30 put', call_df.loc[positions[1].strike].Close, last_put_price)

    
    #eod sqaure off
    if str(call_df.iloc[0]['datetime'])[11:] == '15:19:59':
        #buy all positions
        for p in positions:
            if p.option_type == 'CE':
                new_action = action(p.ticker, p.option_type, p.strike, p.expiry, p.qty, True, False, call_df.loc[p.strike].Close, 0, call_df.iloc[0].datetime, False, p.entry_time)
            else:
                new_action = action(p.ticker, p.option_type, p.strike, p.expiry, p.qty, True, False, put_df.loc[p.strike].Close, 0, put_df.iloc[0].datetime, False, p.entry_time)
            execute.append(new_action)

        return execute, None, None
    
    if (int(call_df.loc[positions[0].strike].Close) - last_call_price)/last_call_price >= 0.3:
        #sell 4 lots of closest premium pe
        #finding closest premium pe:
        print('Last call MID - price:', last_call_price, ' - Last put MID price:', last_put_price)
        print('Call Price Now: ', call_df.loc[positions[0].strike].Close)
        print('Time: ', call_df.loc[positions[0].strike].datetime)

        closest_diff = abs(put_df.iloc[0].Close - call_df.loc[positions[0].strike].Close)
        closest_strike = put_df.iloc[0].Strike

        for i in range(len(put_df)):
            if abs(put_df.iloc[i].Close - call_df.loc[positions[0].strike].Close) < closest_diff:
                closest_diff = abs(put_df.iloc[i].Close - call_df.loc[positions[0].strike].Close)
                closest_strike = put_df.iloc[i].Strike

        put_rebalance = put_df.loc[closest_strike]
        
        action_put = action(put_rebalance.Symbol, 'PE',put_rebalance.Strike, put_rebalance.Expiry, 4, False, True, 0, put_rebalance.Close, put_rebalance.datetime, False)
        execute.append(action_put)

        last_call_price = call_df.loc[positions[0].strike].Close
        last_put_price = put_df.loc[positions[1].strike].Close
        return execute, last_call_price, last_put_price
    

    elif (int(put_df.loc[positions[1].strike].Close) - last_put_price)/last_put_price >= 0.3:
        #sell 4 lots of closest premium ce
        print('Last call MID - price:', last_call_price, ' - Last put MID price:', last_put_price)
        print('Put Price Now: ', put_df.loc[positions[1].strike].Close)
        print('Time: ', put_df.loc[positions[1].strike].datetime)

        #finding closest premium ce
        closest_diff = abs(call_df.iloc[0].Close - put_df.loc[positions[1].strike].Close)
        closest_strike = call_df.iloc[0].Strike

        for i in range(len(call_df)):
            if abs(call_df.iloc[i].Close - put_df.loc[positions[1].strike].Close) < closest_diff:
                closest_diff = abs(call_df.iloc[i].Close - put_df.loc[positions[1].strike].Close)
                closest_strike = call_df.iloc[i].Strike
        
        call_rebalance = call_df.loc[closest_strike]

        action_call = action(call_rebalance.Symbol, 'CE',call_rebalance.Strike, call_rebalance.Expiry, 4, False, True, 0, call_rebalance.Close, call_rebalance.datetime, False)
        execute.append(action_call)

        last_call_price = call_df.loc[positions[0].strike].Close
        last_put_price = put_df.loc[positions[1].strike].Close
        return execute, last_call_price, last_put_price
    
    # last_call_price = call_df.loc[positions[0].strike].Close
    # last_put_price = put_df.loc[positions[1].strike].Close
    
    return execute, last_call_price, last_put_price