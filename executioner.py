class position(object):
    def __init__(self, ticker, strike, option_type, expiry, qty, value, trade_type, entry_time):
        self.ticker = ticker
        self.strike = strike
        self.option_type = option_type
        self.expiry = expiry
        self.value = value
        self.qty = qty
        self.trade_type = trade_type #shorting (false) or longing (true)
        self.entry_time = entry_time

def trade(execute, capital, positions):
    positions = positions
    executed = []
    capital = capital
    transaction_cost = 0
    ctr = 0
    for e in execute:
        print("EXECUTING: - ", ctr)
        capital -= transaction_cost

        if e.sell and e.trade_type == False: #short selling
            capital += e.sell_val
            new_position = position(e.ticker, e.strike, e.option_type, e.expiry, e.qty, e.sell_val, False, e.date)
            executed.append(e)
            positions.append(new_position)
        
        elif e.buy and e.trade_type == False: #short buying
            capital -= e.buy_val
            for i in range(len(positions)):
                if positions[i].option_type == e.option_type and positions[i].strike == e.strike and positions[i].expiry == e.expiry:
                    positions.pop(i)
                    # print('POPPING')
                    executed.append(e)
                    break

        ctr += 1

    return executed, capital, positions
