from individual import *

class NatutalSelection():
    def __init__(self, sz):
        self.populationSize = sz
        self.gen = 1
        # scores
        self.globalBest = 0.0
        self.currentBest = 0.0
        self.keep = 10
        self.dna = np.random.randint(0, 7, size=1000)
        self.elite = 3
        self.mutationRate = 0.1
        self.pop = []

        #------------Individuo mejor adaptado------------#
        for _ in range(sz):
            self.pop.append(Individual())
        self.globalBestIndividual = self.pop[0].clone()

    def save(self):
        stadistics = self.gen + " " + str(self.globalBest)
        np.savez(stadistics, iWeights=self.globalBestIndividual.brain.iWeights, hWeights=self.globalBestIndividual.brain.hWeights,
                 oWeights=self.globalBestIndividual.brain.oWeights)

    def set_best(self):
        #
        self.pop.sort(key=operator.attrgetter('fitness'), reverse=True)
        self.totalFitness = 0

        for i in range(self.populationSize):
            self.totalFitness += self.pop[i].fitness

        self.currentBest = self.pop[0].fitness
        print("current best", self.currentBest, "global best", self.globalBest)
        if self.currentBest > self.globalBest:
            self.globalBestIndividual = self.pop[0].clone()
            self.globalBest = self.pop[0].fitness
            self.globalBestIndividual.dna = copy.deepcopy(self.dna)
            self.save()

    def evolve(self):
        print("EVOLVE")
        self.set_best()
        print("BEST", self.globalBest)
        self.gen += 1

        # crear un nuevo individuo
        new = []

        for i in range(0, self.populationSize):
            print(i)
            # descendencia sin mutación
            if i < self.elite:
                print("keep, don´t mutate")
                new.append(self.pop[i])
                continue
            # descendencia con mutación
            elif i < self.keep:
                print("keep")
                new.append(self.pop[i])
            elif random.uniform(0, 1) > 0.50:
                print("keep")
                new.append(self.pop[i])
            # se seleccionan los padres de manera aleatoria
            else:
                current = 0
                limA = random.randrange(self.totalFitness)
                limB = random.randrange(self.totalFitness)
                a, b = -1

                for k in range(self.populationSize):
                    current += self.pop[k].fitness
                    if limA < current and a == -1:
                        a = k
                    if limB < current and b == -1:
                        b = k

                print("procreate", a, "with", b)
                new.append(self.pop[a].half_blood(self.pop[b]))
            # o.0
            print("mutating time")
            new[i].brain.mutate_all(self.mutationRate)

        time.sleep(1)
        return new