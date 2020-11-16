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

### Argument Parsing
parser = argparse.ArgumentParser(description='Plots a graphical representation of a stochastic distribution.')
parser.add_argument('n', type=int, metavar='N', help='number of individuals')
parser.add_argument('g', type=int, metavar='G', help='number of aditional generations')
parser.add_argument('p', type=int, metavar='P', help='number of generated populations')
parser.add_argument('s', type=int, metavar='S', help='number of simulations')
parser.add_argument('--v', '--verbose', default=False, action='store_true', help='prints every generation',)
args = parser.parse_args()

### Population Generation
double_n = 2*args.n
similar = {"true": 0, "false": 0}

for simulation in range(args.s):
    popularity = [None] * args.p

    for population in range(args.p):
        ## Generates initial population
        generation_parent = array.array('I') # unsigned int
        for i in range(double_n):
            generation_parent.append(i) # gera array com 2n distintos alelos

        if(args.v):print("Population: "+str(population+1)+" N: "+str(args.n)+"\n"+str(generation_parent))

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
            
            if(args.v):print(generation_parent, popular_aleles)
            if(len(popular_aleles) == 1): break
        
        popularity[population] = popular_aleles

    ### Similarity Evaluation
    # Medida de similaridade: top 2% eh igual
    podium = math.ceil(0.02 * double_n)
    if(args.v):print("Medida de Similaridade: "+str(podium))

    # Extraindo os alelos mais populares
    top_aleles = [None] * podium # alelos mais populares de uma populacao
    population_top_aleles = [None] * args.p # lista com lista de alelos mais populares das populacoes
    for i in range(args.p):
        top_aleles = [None] * podium
        for j in range(podium):
            top_aleles[j] = popularity[i].most_common(podium)[j][0] # extrai os alelos x% mais populares
        population_top_aleles[i] = top_aleles
        if(args.v):print("Pop "+str(i)+": "+str(top_aleles))

    # Comparando os alelos mais populares
    if args.p > 1:
        if collections.Counter(population_top_aleles[0]) == collections.Counter(population_top_aleles[1]):
            similar["true"] += 1
            if(args.v):print("True")
        else: 
            similar["false"] += 1
            if(args.v):print("False")

if args.p > 1:
        print(similar)
        print(similar["true"] / similar["false"])

# TO-DO: traçar um grafico de como o a % de similares diminui com o aumento do numero de alelos
