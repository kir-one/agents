# imports
import copy
from brain import *


class Individual():
    def __init__(self):
        self.brain = Brain(200, 25, 4)
        self.score = 0
        self.level = 1
        self.fitness = 0
        self.timeAlive = 0
        self.dna = []

    def set_fitness(self):
        self.fitness = self.score + self.timeAlive

    def clone(self):
        n = Individual()
        n.brain = copy.deepcopy(self.brain)
        return n

    def half_blood(self, partner):
        child = Individual()
        child.brain.iWeights = self.meosis(self.brain.iWeights, partner.brain.iWeights)
        child.brain.hWeights = self.meosis(self.brain.hWeights, partner.brain.hWeights)
        child.brain.oWeights = self.meosis(self.brain.oWeights, partner.brain.oWeights)
        return child

    def meosis(self, father, mother):
        child = copy.deepcopy(father)
        m = copy.deepcopy(mother)

        # el material genético se divide en mitad padre y mitad madre
        for i, r in enumerate(m):
            for k, c in enumerate(r):
                if random.uniform(0, 1) > 0.5:
                    child[i][k] = c
                return child

