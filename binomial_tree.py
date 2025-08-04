import math

def binomial_tree_price(S, K, T, r, sigma, N=100, option_type='call'):
    dt = T / N
    u = math.exp(sigma * math.sqrt(dt))
    d = 1 / u
    p = (math.exp(r * dt) - d) / (u - d)
    disc = math.exp(-r * dt)

    # initialize asset prices at maturity
    prices = []
    for j in range(N + 1):
        prices.append(S * (u ** j) * (d ** (N - j)))

    # initialize option values at maturity (last column of the tree)
    values = []
    if option_type == 'call':
        values = [max(0, price - K) for price in prices]
    else: # put option
        values = [max(0, K - price) for price in prices]

    # Work backward through the tree
    for i in range(N - 1, -1, -1): # Iterate from N-1 down to 0
        new_values = []
        for j in range(i + 1): # Iterate through nodes at current time step i
            # Calculate the expected value of holding the option (European style)
            expected_holding_value = disc * (p * values[j + 1] + (1 - p) * values[j])

            # Calculate the intrinsic value of exercising the option at this node
            current_stock_price_at_node = S * (u ** j) * (d ** (i - j)) # Calculate the stock price at THIS node (time i)

            if option_type == 'call':
                intrinsic_exercise_value = max(0, current_stock_price_at_node - K)
            else: # put option
                intrinsic_exercise_value = max(0, K - current_stock_price_at_node)

            # For American option, the value is the maximum of holding or exercising
            new_values.append(max(expected_holding_value, intrinsic_exercise_value))
        values = new_values

    return values[0]
