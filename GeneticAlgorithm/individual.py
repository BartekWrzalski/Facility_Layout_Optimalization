from random import shuffle, randint, uniform, choice
from copy import deepcopy


class Individual:
    def __init__(self):
        self.__positions = []
        self.__sorted_positions = []

    def set_arrangement(self, positions):
        self.__positions = positions
        self.__sorted_positions = sorted(self.__positions, key=lambda k: k['machine'])

    def random_arrangement(self, n, m):
        machines = []
        for i in range(0, n * m):
            machines.append(i)
        shuffle(machines)

        for i in range(0, n):
            for j in range(0, m):
                self.__positions.append({'machine': machines[i * m + j], "x": j, "y": i})
        self.__sorted_positions = sorted(self.__positions, key=lambda k: k['machine'])

    def adaptation_function(self, flows, costs):
        adaptation_value = 0
        for i in range(0, len(flows)):
            xi, xj = flows[i]['source'], flows[i]['dest']
            yi, yj = flows[i]['source'], flows[i]['dest']

            flow = flows[i]['amount']
            cost = costs[i]['cost']
            dist = abs(self.__sorted_positions[xi]['x'] - self.__sorted_positions[xj]['x']) + \
                   abs(self.__sorted_positions[yi]['y'] - self.__sorted_positions[yj]['y'])

            adaptation_value += flow * cost * dist
        return adaptation_value

    def mutate(self):
        x = randint(0, len(self.__positions) - 2)
        ran = list(range(0, x - 1)) + list(range(x + 2, len(self.__positions) - 2))
        y = choice(ran)

        self.__sorted_positions[x]['machine'] = y
        self.__sorted_positions[x + 1]['machine'] = y + 1
        self.__sorted_positions[y]['machine'] = x
        self.__sorted_positions[y + 1]['machine'] = x + 1

        temp = self.__sorted_positions[x]
        self.__sorted_positions[x] = self.__sorted_positions[y]
        self.__sorted_positions[y] = temp

        temp = self.__sorted_positions[x + 1]
        self.__sorted_positions[x + 1] = self.__sorted_positions[y + 1]
        self.__sorted_positions[y + 1] = temp

        self.__positions = sorted(self.__sorted_positions, key=lambda k: k['y'] * 100 + k['x'])

    def cross(self, parent2):
        child = Individual()
        break_point = int(len(self.__positions) * uniform(0.15, 0.85))
        child_gen = deepcopy(self.__positions[0:break_point]) + deepcopy(parent2.__positions[break_point:])
        machines_left = [i for i in self.__positions if i['machine'] not in [m['machine'] for m in child_gen]]

        seen = []
        for i in range(0, len(child_gen)):
            if child_gen[i]['machine'] in seen:
                child_gen[i]['machine'] = machines_left[0]['machine']
                machines_left.pop(0)
            seen.append(child_gen[i]['machine'])
        child.set_arrangement(child_gen)
        return child

    def to_array(self):
        return [ma['machine'] for ma in self.__positions]
