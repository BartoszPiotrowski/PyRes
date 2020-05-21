

def compute_returns(rewards, gamma):
    returns = []
    sum_of_rewards = 0
    list(rewards).reverse()
    for r in rewards:
        sum_of_rewards = gamma * sum_of_rewards + r
        returns.append(sum_of_rewards)
    returns.reverse()
    return returns
