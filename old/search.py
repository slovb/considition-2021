from solver.config import Config
from solver.config_op import *

def search_1_attr(runner, config: Config, attr: str, value, step, fail_max=4):
    history = []
    memory = {}
    def display(value: tuple):
        if len(history) > 0:
            print('{}\t\tBest: {}'.format(value, max(history)))
        else:
            print(value)
        print('----------------------------------------------------------------')
    
    def f(v):
        if v in memory:
            return memory[v]
        op = set_op(attr, v)
        co = op.action(config)
        score = runner(co)
        entry = (score, op.name)
        display(entry)
        history.append(entry)
        memory[v] = score
        return score
    
    control = (runner(config), 'control')
    display(control)
    history.append(control)
    
    fail_count = 0
    while True:
        results = []
        control = f(value)
        
        for v in [value - step, value + step]:
            results.append( (f(v), v) )
        best_score, best_coord = max(results, key=lambda r: r[0])
        
        if control >= best_score:
            step /= 2
            if control == best_score:
                fail_count += 1
                if fail_count > fail_max:
                    break
        else:
            value = best_coord
            
    for h in sorted(history):
        print(h)
