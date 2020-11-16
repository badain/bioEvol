#############################################################
# Description: simula o modelo estocastico de Wright-Fischer
#              para a transmissão de cópias gênicas
# Usage: dist_estocastica(K, N)
# 
# Pre-Condition: K, N:integer
# Post-Condition: retorna um dicionario relacionando a
#                 o número de cópias para cada característica
#
# Author: Rafael Badain @ University of Sao Paulo
#############################################################

### Dependencies
import argparse
import random # designed for modelling and simulation, not security or cryptography
import array # takes less space since supports only one datatype
import math # ceil()
import collections
from collections import Counter
import matplotlib.pyplot as plt

### Argument Parsing
parser = argparse.ArgumentParser(description='Plots a graphical representation of a stochastic distribution.')
parser.add_argument('n', type=int, metavar='N', help='max number of individuals')
parser.add_argument('g', type=int, metavar='G', help='number of aditional generations')
parser.add_argument('s', type=int, metavar='S', help='number of simulations')
args = parser.parse_args()

pop_num = 2
similar_per_n = {}
for n in range(2, args.n):
    ### Population Generation
    double_n = 2*n
    similar = {"true": 0, "false": 0}

    for simulation in range(args.s):
        popularity = [None] * pop_num

        for population in range(pop_num):
            ## Generates initial population
            generation_parent = array.array('I') # unsigned int
            for i in range(double_n):
                generation_parent.append(i) # gera array com 2n distintos alelos

            for i in range(args.g):
                ## Generates Next Generation
                generation_child = array.array('I') # unsigned int
                popular_aleles = Counter()

                # Sorteio dos Alelos
                for i in range(double_n):
                    viable_alele = random.choice(range(double_n)) # seleciona um dos indicies aleatoriamente
                    generation_child.append(generation_parent[viable_alele]) # adiciona o alelo viavel na proxima geracao
                    popular_aleles[generation_parent[viable_alele]] += 1 # conta a ocorrencia dos alelos

                generation_parent = generation_child # as geracoes sao discretas
                if(len(popular_aleles) == 1): break
                
            popularity[population] = popular_aleles

        ### Similarity Evaluation
        # Medida de similaridade: top 2% eh igual
        podium = math.ceil(0.02 * double_n)

        # Extraindo os alelos mais populares
        top_aleles = [None] * podium # alelos mais populares de uma populacao
        population_top_aleles = [None] * pop_num # lista com lista de alelos mais populares das populacoes
        for i in range(pop_num):
            top_aleles = [None] * podium
            for j in range(podium):
                top_aleles[j] = popularity[i].most_common(podium)[j][0] # extrai os alelos x% mais populares
            population_top_aleles[i] = top_aleles

        # Comparando os alelos mais populares
        if collections.Counter(population_top_aleles[0]) == collections.Counter(population_top_aleles[1]):
            similar["true"] += 1
        else: 
            similar["false"] += 1
    
    similar_per_n[n] = similar["true"] / similar["false"]

#print(similar_per_n)
plt.scatter(similar_per_n.keys(), similar_per_n.values())
plt.xlabel("População (N)")
plt.title("% de similaridades após "+str(args.g)+" gerações em "+str(args.s)+" simulações")
plt.savefig('wright_'+str(args.n)+'_'+str(args.g)+'_'+str(args.s)+'.png')