from random import randrange
import random
import numpy as np
import matplotlib.pyplot as plt
def one_plus_beta_choice(n, m, beta):
    bins = [0 for _ in range(m)]

    for _ in range(n):
        if random.random() < beta:
            bins[randrange(m)] += 1
        else:
            b1 = randrange(m)
            b2 = randrange(m)
            if bins[b1] > bins[b2]:
                bins[b2] += 1
            elif bins[b2] > bins[b1]:
                bins[b1] += 1
            else:
                bins[random.choice([b1, b2])] += 1
    return max(bins) - n / m

def standard(n, m):
    return one_plus_beta_choice(n, m, 1)

def two_choice(n,m):
    return one_plus_beta_choice(n, m, 0)

def batch_two_choice(n, m, b):
    batch_beta_choice(n, m, b,0)

def batch_beta_choice(n, m, b, beta):
    bins = [0 for _ in range(m)]

    for _ in range(n // b):
        outdated_bins = [b for b in bins]
        for _ in range(b):
            if random.random() < beta:
                bins[randrange(m)] += 1
            else:
                b1 = randrange(m)
                b2 = randrange(m)
                if outdated_bins[b1] > outdated_bins[b2]:
                    bins[b2] += 1
                elif outdated_bins[b2] > outdated_bins[b1]:
                    bins[b1] += 1
                else:
                    bins[random.choice([b1, b2])] += 1

    outdated_bins = [b for b in bins]
    for _ in range(n%b):
        if random.random() < beta:
            bins[randrange(m)] += 1
        else:
            b1 = randrange(m)
            b2 = randrange(m)
            if outdated_bins[b1] > outdated_bins[b2]:
                bins[b2] += 1
            elif outdated_bins[b2] > outdated_bins[b1]:
                bins[b1] += 1
            else:
                bins[random.choice([b1, b2])] += 1

    return max(bins) - n / m

def question_k_2(n, m, beta):
    bins = [0 for _ in range(m)]

    for _ in range(n):
        if random.random() < beta:
            bins[randrange(m)] += 1
        else:
            b1 = randrange(m)
            b2 = randrange(m)
            percentile25, percentile50, percentile75 = np.percentile(bins, [25, 50, 75])

            if (bins[b1] > percentile50) and (bins[b2] > percentile50): #both higher then median
                if ((bins[b1] >= percentile75) and (bins[b2] >= percentile75)) or ((bins[b1] < percentile75) and (bins[b2] < percentile75)):
                    bins[random.choice([b1, b2])] += 1
                else:
                    if bins[b1] > bins[b2]: bins[b2] += 1
                    else: bins[b1] += 1
            elif (bins[b1] <= percentile50) and (bins[b2] <= percentile50): #both lower then median
                if ((bins[b1] > percentile25) and (bins[b2] > percentile25)) or ((bins[b1] <= percentile25) and (bins[b2] <= percentile25)):
                    bins[random.choice([b1, b2])] += 1
                else:
                    if bins[b1] > bins[b2]: bins[b2] += 1
                    else: bins[b1] += 1
            else:
                if bins[b1] > bins[b2]: bins[b2] += 1
                else: bins[b1] += 1



    return max(bins) - n / m

def question_k_1_with_beta(n, m, beta):
    bins = [0 for _ in range(m)]
    print(n)

    for x in range(n):
        if random.random() < beta:
            bins[randrange(m)] += 1
        else:
            b1 = randrange(m)
            b2 = randrange(m)
            median = np.median(bins)

            if bins[b1] > median and bins[b2] > median: #both are above median
                bins[random.choice([b1, b2])] += 1
            elif bins[b1] <= median and bins[b2] <= median: #both are below or equal to median
                bins[random.choice([b1, b2])] += 1
            else:
                if bins[b1] > bins[b2]:
                    bins[b2] += 1
                else:
                    bins[b1] += 1

    return max(bins) - n / m

def no_parametrized_experiment():
    m = 50
    n = [i for i in range(5, m**2+1, 5)]
    T = 10

    g = []
    for i in n:
        print(i)
        g.append(sum(question_k_2(i, m, 0) for _ in range(T))/T)

    plt.scatter(n, g, s=10)
    plt.title("Question k=2 strategy, m = 50")
    plt.scatter(m, [g[n.index(m)]], color="red", label="n = m")
    plt.legend()
    plt.show()

    g = []
    for i in n:
        g.append(sum(question_k_1_with_beta(i, m, 0) for _ in range(T))/T)

    plt.scatter(n, g, s=10)
    plt.title("Question k=1 strategy, m = 50")
    plt.scatter(m, [g[n.index(m)]], color="red", label="n = m")
    plt.legend()
    plt.show()

    g = []
    for i in n:
        g.append(sum(standard(i, m) for _ in range(T))/T)

    plt.scatter(n, g, s=10)
    plt.title("Standard strategy, m = 50")
    plt.scatter(m, [g[n.index(m)]], color="red", label="n = m")
    plt.legend()
    plt.show()

    g = []
    for i in n:
        g.append(sum(two_choice(i, m) for _ in range(T))/T)

    plt.scatter(n, g, s=10)
    plt.title("Two-choice strategy, m = 50")
    plt.scatter(m, [g[n.index(m)]], color="red", label="n = m")
    plt.legend()
    plt.show()


def beta_experiment():
    m = 30
    n = [i for i in range(5, m**2+1, 5)]
    T = 20
    beta = [0, 0.25, 0.5, 0.75, 1]


    for b in beta:
        g = []
        for i in n:
            g.append(sum(one_plus_beta_choice(i, m, b) for _ in range(T)) / T)
        print((b, g[n.index(m)]))
        plt.scatter(n, g, s=10, label="beta: " + str(b))

    plt.title(" 1 + beta, m = 30")
    plt.legend()
    plt.show()


def batch_experiment():
    m = 40
    b_vals = [m//2, m, 2*m, 3*m, 4*m, 5*m]
    T = 20


    for b in b_vals:
        print(b)
        g = []
        n = [i for i in range(b, m ** 2+1, b)]
        for i in n:
            g.append(sum(batch_beta_choice(i, m, b, 0) for _ in range(T)) / T)
        plt.plot(n, g, label="Batch size: " + str(b))

    plt.title("Batch strategy m=40")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    no_parametrized_experiment()
    beta_experiment()
    batch_experiment()