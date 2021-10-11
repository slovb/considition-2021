import itertools
import random

from solver.config import Config
from solver.config_op import *

same = lambda value, _: value
add = lambda value, step: value + step
rem = lambda value, step: value - step
madd = lambda value, step: value * (1.0 + step)
mrem = lambda value, step: value * (1.0 - step)


def additive_options(state):
    '''all the options for setting each parameters, additive steps'''
    return [[
        (name, rem(value, step), step, rem),
        (name, value,            step, same),
        (name, add(value, step), step, add)] for name, value, step, _ in state]


def scaling_options(state):
    '''all the options for setting each parameters, scaling steps'''
    return [[
        (name, mrem(value, step), step, mrem),
        (name, value,             step, same),
        (name, madd(value, step), step, madd)] for name, value, step, _ in state]

from log import log


class Searcher:
    
    def __init__(self, runner: Callable[[Config], int]):
        self.runner = runner
        self.history = []
        self.memory = {}


    def search(self, config: Config, settings, depth: int = 4, greedy: bool = True, options_builder = additive_options) -> ConfigOp:
        anotherStep = lambda state: tuple([(name, stepper(value, step), step, stepper) for name, value, step, stepper in state])
        self.__displayAndStore((self.runner(config), 'nop'))
        state = tuple([(name, value, step, same) for name, value, step in settings]) # describe the datacube as name, value, radius tripplets
        results: list[int, tuple] = []
        while depth > 0:
            score = self.__run(config, state) # baseline
            
            options = options_builder(state) # all the options for setting each parameter
            states = list(itertools.product(*options)) # as a set of states
            
            for option in random.sample(states, len(states)): # random iteration because greed
                if all([stepper == same for _, _, _, stepper in option]):
                    continue
                optionScore = self.__run(config, option)
                results.append( (optionScore, option) )
                while optionScore == score:
                    option = anotherStep(option)
                    optionScore = self.__run(config, option)
                    results.append( (optionScore, option) )
                if greedy and optionScore > score:
                    break

            best_score, best_state = max(results, key=lambda r: r[0])            
            if best_score > score:
                self.__log(config, best_score, best_state)
                state = best_state
                score = best_score
                while True: # try to go in that direction
                    another_state = anotherStep(state)
                    another_score = self.__run(config, another_state)
                    results.append( (another_score, another_state) )
                    if another_score > score:
                        self.__log(config, another_score, another_state)
                        state = another_state
                        score = another_score
                    else:
                        break
            else:
                self.__log(config, score, state)
                depth -= 1
                state = tuple([(name, value, step / 2, stepper) for name, value, step, stepper in state])
        
        for h in sorted(self.history):
            print(h)
        return set_ops(state)


    def __log(self, config: Config, score: int, state: tuple):
        op = set_ops(state)
        log('log/config.txt', '{}, {}, {}'.format(score, op.name, op.action(config)))


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
            entry = (self.memory[op.name], op.name)
            self.__displayAndStore(entry)
            return self.memory[op.name]
        score = self.runner(op.action(config))
        self.memory[op.name] = score
        
        entry = (score, op.name)
        self.__displayAndStore(entry)
        return score
