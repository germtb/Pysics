from algorithms import monte_carlo_min, RandomVariable


def function(x):
    return x * x - 9

x = RandomVariable(0, 5)
print(monte_carlo_min(function, x))
