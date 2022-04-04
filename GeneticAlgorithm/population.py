import math
from copy import deepcopy
from individual import Individual
from random import randint, random, sample
import numpy as np


class Population:
    def __init__(self, flows, costs, amount):
        self.__flows = flows
        self.__costs = costs
        self.__amount = amount
        self.__individuals = []

    def generate_random(self, n, m):
        for i in range(0, self.__amount):
            ind = Individual()
            ind.random_arrangement(n, m)
            self.__individuals.append(ind)

    def add_individual(self, individual):
        self.__individuals.append(individual)

    def tournament_selection(self, n, next_population):
        for j in range(0, self.__amount):
            ids = sample(range(self.__amount), n)

            best = self.__individuals[ids[0]]
            best_adaptation_value = best.adaptation_function(self.__flows, self.__costs)
            for i in ids[1:]:
                c_adaptation_value = self.__individuals[i].adaptation_function(self.__flows, self.__costs)
                if c_adaptation_value < best_adaptation_value:
                    best_adaptation_value = c_adaptation_value
                    best = self.__individuals[i]
            next_population.add_individual(best)

    def roulette_selection(self, next_population):
        exponential_values = [1 / (ind.adaptation_function(self.__flows, self.__costs) ** 3) for ind in self.__individuals]
        population_sum = sum(exponential_values)
        individual_probabilities = [ind / population_sum for ind in exponential_values]

        for i in range(0, self.__amount):
            next_population.add_individual(
                self.__individuals[np.random.choice(self.__amount, p=individual_probabilities)])

    def crossover(self, probability):
        new_population = []
        for i in range(0, len(self.__individuals)):
            if random() < probability:
                parent2_index = i
                while parent2_index == i:
                    parent2_index = randint(0, self.__amount - 1)
                parent2 = self.__individuals[parent2_index]
                child = self.__individuals[i].cross(parent2)
                new_population.append(child)
            else:
                new_population.append(deepcopy(self.__individuals[i]))
        self.__individuals = new_population

    def mutation(self, probability):
        for entity in self.__individuals:
            if random() < probability:
                entity.mutate()

    def print(self):
        for entity in self.__individuals:
            print(entity.to_array(), entity.adaptation_function(self.__flows, self.__costs))

    def best(self):
        best = math.inf
        for ind in self.__individuals:
            temp = ind.adaptation_function(self.__flows, self.__costs)
            if temp < best:
                best = temp
        return best
