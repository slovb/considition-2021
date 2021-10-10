import itertools

from solver.config import Config
from solver.config_op import *

class Searcher:
    
    def __init__(self, runner: Callable[[Config], int]):
        self.runner = runner
        self.history = []
        self.memory = {}
        
    
    def displayAndStore(self, value: tuple):
        self.history.append(value)
        if len(self.history) > 0:
            print('{}\t\tBest: {}'.format(value, max(self.history)))
        else:
            print(value)
        print('----------------------------------------------------------------')


    def run(self, config: Config, values: tuple):
        if values in self.memory:
            return self.memory[values]
        op = set_ops(values)
        co = op.action(config)
        score = self.runner(co)
        self.memory[values] = score
        
        entry = (score, op.name)
        self.displayAndStore(entry)
        return score
    
    
    def search(self, config: Config, settings, depth: int = 4):
        self.displayAndStore((self.runner(config), 'nop'))
        state = tuple([(name, value, step) for name, value, step in settings])
        results = []
        while depth > 0:
            score = self.run(config, state)
            options = [
                [
                    (name, value - step),
                    (name, value),
                    (name, value + step)
                ] for name, value, step in settings
            ]
            for option in itertools.product(*options):
                results.append( (self.run(config, option), option) )

            best_score, best_coord = max(results, key=lambda r: r[0])            
            if score >= best_score:
                depth -= 1
                state = tuple([(name, value, step / 2) for name, value, step in settings])
            else:
                state = best_coord
        
        for h in sorted(self.history):
            print(h)
