import random
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

def simulation(board_size, balls):
    count = [0 for _ in range(board_size+1)]
    end_positions = []

    for b in range(balls):
        i = 0
        for _ in range(board_size):
            if bool(random.getrandbits(1)):
                i += 1
        count[i] += 1
        end_positions += [i]
    return count, end_positions

def experiment_with_plot(board_size, balls):
    ball_count, ball_end_position = simulation(board_size, balls)
    positions = [i for i in range(board_size+1)]

    # Plot normal distribution
    mean, std = norm.fit(ball_end_position)
    mean_expected = board_size/2
    std_expected = (board_size**0.5)/2

    plt.hist(positions, weights=ball_count, bins=board_size, density=True, alpha=0.6, color='g')

    x = np.linspace(0, board_size, board_size+1)
    p_expected = norm.pdf(x, mean_expected, std_expected)
    plt.plot(x, p_expected, linewidth=2, color='blue')

    title = """Board size = %.0f, ball count = %.0f
    Results: mean = %.2f,  standard deviation = %.2f,
    Expected: mean = %.2f,  standard deviation = %.2f""" % (board_size, balls, mean, std, mean_expected, std_expected)
    plt.title(title, fontsize=10)
    plt.show()

def experiment_mse(board_size, balls):
    ball_count, ball_end_position = simulation(board_size, balls)

    mean_expected = board_size/2
    std_expected = (board_size**0.5)/2

    x = np.linspace(0, board_size, board_size+1)
    p_expected = norm.pdf(x, mean_expected, std_expected)

    mse = 0
    for i in range(board_size+1):
        mse += (ball_count[i]/balls - p_expected[i])**2

    mse /= (board_size+1)

    return mse


def average_mse(board_size, balls, count):
    mses = [experiment_mse(board_size, balls) for _ in range(count)]
    return sum(mses)/count

def multiple_mse_constant_board_size():

    board_size = 500
    upper_bound = 1000
    lower_bound = 10
    step = 10

    y = [average_mse(board_size, i, 10) for i in range(lower_bound, upper_bound, step)]
    x = [i for i in range(lower_bound, upper_bound, step)]

    plt.plot(x, y)
    plt.title("Mean square error for board size = %.0f""" % (board_size))
    plt.xlabel("Number of balls")
    plt.show()


def multiple_mse_constant_balls_count():
    balls = 1000
    upper_bound = 1000
    lower_bound = 10
    step = 10

    y = [average_mse(i, balls, 10) for i in range(lower_bound, upper_bound, step)]
    x = [i for i in range(lower_bound, upper_bound, step)]

    plt.plot(x, y)
    plt.title("Mean square error for ball count = %.0f""" % (balls))
    plt.xlabel("Board size")
    plt.show()


for i in [(10, 100), (10, 1000), (100, 100), (100, 1000), (100, 1000000)]:
    experiment_with_plot(i[0], i[1])

multiple_mse_constant_board_size()

multiple_mse_constant_balls_count()
