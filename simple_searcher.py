import itertools
import random

from solver.config import Config
from solver.config_op import *
from log import log

same = lambda value, _: value
madd = lambda value, step: value * (1.0 + step)
mrem = lambda value, step: value * (1.0 - step)

anotherStep = lambda state: tuple([(name, stepper(value, step), step, stepper) for name, value, step, stepper in state])


class SimpleSearcher:
    
    def __init__(self, runner: Callable[[Config], int]):
        self.runner = runner
        self.memory = {}
        self.options_builder = SimpleSearcher.scaling_options
        self.step_max = 5
        self.best_score = 0
        self.best_name = ''


    @staticmethod
    def scaling_options(state):
        '''all the options for setting each parameters, scaling steps'''
        return [[
            (name, mrem(value, step), step, mrem),
            (name, value,             step, same),
            (name, madd(value, step), step, madd)] for name, value, step, _ in state]


    def search(self, config: Config, settings) -> tuple[ConfigOp, int]:
        state = tuple([(name, value, step, same) for name, value, step in settings]) # describe the datacube as name, value, radius tripplets
        
        results: list[int, tuple] = []
        def run(state):
            s = self.__run(config, state)
            results.append( (s, state) )
            return s
        max_score = lambda: max([s for s, _ in results])
        least_state = lambda score: min([x for s, x in results if s == score], key=self.__state_value_sum)
        
        while True:
            score = run(state) # baseline
            options = self.options_builder(state) # all the options for setting each parameter
            states = list(itertools.product(*options)) # as a set of states
            
            done = False
            for option_state in random.sample(states, len(states)): # random iteration because greed
                if all([stepper == same for _, _, _, stepper in option_state]): # don't do the non-step
                    continue
                option_score = run(option_state)
                for _ in range(self.step_max):
                    if option_score > score: # if improved, we'll be done, but keep looking in this direction, just in case
                        done = True
                    elif option_score < score: # if not an improvement, drop it
                        break
                    option_state = anotherStep(option_state)
                    option_score = run(option_state)
                if done or option_score > score:
                    break

            candidate_score = max_score()
            candidate_state = least_state(candidate_score)  # prefer lowest value
            if candidate_score > score:
                self.__log(config, candidate_score, candidate_state)
                state, score = candidate_state, candidate_score
            else: # no improvement
                self.__log(config, candidate_score, candidate_state)
                break
        
        score = max_score()
        state = least_state(score) # prefer lowest value
        return set_ops(state), score


    def __state_value_sum(self, state: tuple):
        return sum([value for _, value, _, _ in state])


    def __log(self, config: Config, score: int, state: tuple):
        op = set_ops(state)
        log('log/config.txt', '{}, {}, {}'.format(score, op.name, op.action(config)))


    def __display(self, score: int, name: str) -> None:
        print('Sum:  {}, {}\nBest: {}, {}'.format(score, name, self.best_score, self.best_name))
        print('----------------------------------------------------------------')


    def __run(self, config: Config, state: tuple) -> int:
        op = set_ops(state)
        if op.name not in self.memory:
            self.memory[op.name] = self.runner(op.action(config))
        score = self.memory[op.name]
        if score > self.best_score:
            self.best_score = score
            self.best_name = op.name
        self.__display(score, op.name)
        return score
        