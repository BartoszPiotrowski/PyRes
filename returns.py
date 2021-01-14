

def compute_returns(rewards, gamma, simple=False):
    if simple:
        returns = []
        l = list(range(len(rewards)))
        l.reverse()
        l = [(x * (-1)) for x in l]
        print(l)
        return l
    returns = []
    sum_of_rewards = 0
    list(rewards).reverse()
    for r in rewards:
        sum_of_rewards = gamma * sum_of_rewards + r
        returns.append(sum_of_rewards)
    returns.reverse()
    return returns
