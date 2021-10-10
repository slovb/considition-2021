import itertools
import random

from solver.config import Config
from solver.config_op import *

def additive_options(state):
    '''all the options for setting each parameters, additive steps'''
    return [[
        (name, value - step, step),
        (name, value, step),
        (name, value + step, step)] for name, value, step in state]


def scaling_options(state):
    '''all the options for setting each parameters, scaling steps'''
    return [[
        (name, value * (1.0 - step), step),
        (name, value, step),
        (name, value * (1.0 + step), step)] for name, value, step in state]


class Searcher:
    
    def __init__(self, runner: Callable[[Config], int]):
        self.runner = runner
        self.history = []
        self.memory = {}


    def search(self, config: Config, settings, depth: int = 4, greedy: bool = True, options_builder = additive_options) -> None:
        self.__displayAndStore((self.runner(config), 'nop'))
        state = tuple([(name, value, step) for name, value, step in settings]) # describe the datacube as name, value, radius tripplets
        results: list[int, tuple] = []
        while depth > 0:
            score = self.__run(config, state) # baseline
            
            options = options_builder(state) # all the options for setting each parameter
            states = list(itertools.product(*options)) # as a set of states
            
            for option in random.sample(states, len(states)): # random iteration because greed
                s = self.__run(config, option)
                results.append( (s, option) )
                if greedy and s > score:
                    break

            best_score, best_state = max(results, key=lambda r: r[0])            
            if best_score > score:
                state = best_state
            else:
                depth -= 1
                state = tuple([(name, value, step / 2) for name, value, step in state])
        
        for h in sorted(self.history):
            print(h)


    def __displayAndStore(self, value: tuple) -> None:
        self.history.append(value)
        if len(self.history) > 0:
            print('{}\nBest: {}'.format(value, max(self.history)))
        else:
            print(value)
        print('----------------------------------------------------------------')


    def __run(self, config: Config, values: tuple) -> int:
        op = set_ops(values)
        if op.name in self.memory:
            return self.memory[op.name]
        score = self.runner(op.action(config))
        self.memory[op.name] = score
        
        entry = (score, op.name)
        self.__displayAndStore(entry)
        return score
