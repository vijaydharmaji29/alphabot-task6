import yfinance as yf
import matplotlib.pyplot as plt

def limit_backtest(symbol, principal=100000, days=252):
   
    stock = yf.Ticker(symbol)
    data = stock.history(period=f"{days}d")
    close = data['Close']

    print(close)

    
    high = data['High']
    low = data['Low']
    limit = (high + low) / 2
    upper_limit = limit + 0.05 * limit
    lower_limit = limit - 0.05 * limit


   
    positions = []
    cash = principal
    total_trades = 0
    win_trades = 0
    loss_trades = 0
    total_gain = 0
    max_drawdown = 0
    start_principal = principal

    
    for i in range(1, len(close)):
        if close[i] > upper_limit[i-1] and cash > 0: #buy signal
            print('buy')
            positions.append(cash / close[i]) #storing the quantity bough
            cash = 0
            total_trades += 1
        elif close[i] < lower_limit[i-1] and positions: #sell signal
            print('sell')
            sell_price = positions.pop() * close[i] #sell value
            cash = sell_price
            total_trades += 1
            gain = (sell_price - principal) / principal
            total_gain += gain
            if gain > 0:
                win_trades += 1
            else:
                loss_trades += 1
            max_drawdown = min(max_drawdown, (sell_price - start_principal) / start_principal)
            
    end_principal = cash + sum(positions) * close[-1]
    total_return = (end_principal - principal) / principal * 100
    win_pct = win_trades / total_trades * 100 if total_trades > 0 else 0
    loss_pct = loss_trades / total_trades * 100 if total_trades > 0 else 0
    avg_win = total_gain / win_trades * 100 if win_trades > 0 else 0
    avg_loss = abs(total_gain) / loss_trades * 100 if loss_trades > 0 else 0
    ann_return = (end_principal / principal) ** (365/days) - 1
    calmar = ann_return / max_drawdown 
    
    print(f'Total Trades: {total_trades}')
    print(f'Win Trades: {win_trades} ({win_pct:.2f}%)')
    print(f'Loss Trades: {loss_trades} ({loss_pct:.2f}%)')
    print(f'Average Win: {avg_win:.2f}%')
    print(f'Average Loss: {avg_loss:.2f}%')
    print(f'Total Return: {total_return:.2f}%')
    print(f'End Principal: {end_principal:.2f}')
    print(f'Total Gain: {total_gain:.2f}')
    print(f'Avg Annual Return: {ann_return * 100:.2f}%')
    print(f'Max Drawdown: {max_drawdown * 100:.2f}%')
    print(f'Calmar: {calmar:.2f}')
    
    plt.plot(close)
    plt.plot(upper_limit, linestyle='-')
    plt.plot(lower_limit, linestyle='--')
    plt.title
    plt.show()

if __name__ == '__main__':
    limit_backtest("MSFT")