#############################################################
# Description: plota a distribuicao da proporcao entre caras
#              e coroas para K jogadas em N simulacoes
# Dependencies: math
# Usage: dist_estocastica(K, N)
# 
# Pre-Condition: K, N:integer
# Post-Condition: retorna um dicionario relacionando a
#                 proporcao entre caras e coroas e
#                 o numero de simulacoes em que ocorreu
#
# Author: Rafael Badain @ University of Sao Paulo
#############################################################

### Dependencies
import argparse
import random # designed for modelling and simulation, not security or cryptography
from collections import Counter
import matplotlib.pyplot as plt

### Argument Parsing
parser = argparse.ArgumentParser(description='Plots a graphical representation of a stochastic distribution.')
parser.add_argument('k', type=int, metavar='K', help='number of coin tosses')
parser.add_argument('n', type=int, metavar='N', help='number of simulations')
parser.add_argument('--s', '--silent', default=False, action='store_true', help='does not prints graphics',)
args = parser.parse_args()

### Coin Toss
coin_seq = [0,1] # possible coin toss results
distribution = Counter()

for j in range(args.n): 
    random.seed() # initializes random number generator: uses sys time
    results = Counter()

    for i in range(args.k):
        coin_toss = random.choice(coin_seq) # coin toss result
        results[coin_toss] += 1

    proportion = results[0] / args.k
    distribution[proportion] += 1

# Ploting
if(not args.s):
    plt.xlim(0, 1)
    plt.scatter(distribution.keys(), distribution.values())
    plt.savefig('stocastic_'+str(args.k)+'_'+str(args.n)+'.png')
    print(distribution)