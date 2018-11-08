"""
Carwash example.

Covers:

- Waiting for other processes
- Resources: Resource

Scenario:
  A carwash has a limited number of washing machines and defines
  a washing processes that takes some (random) time.

  Car processes arrive at the carwash at a random time. If one washing
  machine is available, they start the washing process and wait for it
  to finish. If not, they wait until they an use one.

"""

import random
import numpy as np
import simpy

RANDOM_SEED = 42
RANDOM_SEED = 42
NUM_CHECKERS = 2
NUM_SCANNERS = 4
ARRIVALRATE = 5
CHECKERRATE = .75
MINIMUMSCAN = 0.5
MAXIMUMSCAN = 1
 
    
 
CHECKTIME = list(np.random.exponential(scale=CHECKERRATE, size=1000))      
SCANTIME = list(np.random.uniform(low=MINIMUMSCAN, high=MAXIMUMSCAN, size=1000))      
SIM_TIME = 20     # 

results = {
        'arrival':
            {'arrival_time':[], 'index':[]},
        'enter':
            {'enter_time':[], 'index':[]},
        'check':
            {'check_time':[], 'index':[]},
        'scan':
            {'scan_time':[], 'index':[]},
        }
        

class Checker(object):
    """

    """
    def __init__(self, env, num_checkers, checktime):
        self.env = env
        self.checkers = simpy.Resource(env, num_checkers)
        


    def check(self, person):
        """"""
        yield self.env.timeout(CHECKTIME.pop(0))


class Scanner(object):
    """

    """
    def __init__(self, env, num_scanners, scantime):
        self.env = env
        self.machine = simpy.Resource(env, num_scanners)

    def scan(self, person):
       
        yield self.env.timeout(SCANTIME.pop(0))

              

def person(env, name, checker, scanner):
    """

    """
    arrival_name = name
    arrival_time = env.now
    
    results["arrival"]['arrival_time'].append(arrival_time)
    results["arrival"]['index'].append(arrival_name)
    
    with checker.checkers.request() as request:
        yield request
        enter_time = env.now
        enter_name = name
        results["enter"]['enter_time'].append(enter_time)
        results["enter"]['index'].append(enter_name)
        
        
        check_time = env.now
        check_name = name
        results["check"]['check_time'].append(check_time)
        results["check"]['index'].append(check_name)
        yield env.process(checker.check(check_name))
        
        scan_time = env.now
        scan_name = name
        results["scan"]['scan_time'].append(scan_time)
        results["scan"]['index'].append(scan_name)
        yield env.process(scanner.scan(scan_name))
        
        

def setup(env, num_checkers, checktime, num_scanners, scantime):
    """"""
    # Create queue
    checker = Checker(env, num_checkers, checktime)
    scanner = Scanner(env, num_scanners, scantime)
    # Create 4 initial persons
    for person_id in range(4):
        env.process(person(env, person_id, checker, scanner))

    # Create more persons while the simulation is running
    while True:
        for i in np.random.poisson(lam=ARRIVALRATE, size=100):
            yield env.timeout(1)
            for c in range(i+1):
                env.process(person(env, person_id, checker, scanner))
                person_id += 1
        
    



random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create an environment and start the setup process
env = simpy.Environment()
s = setup(env, NUM_CHECKERS, CHECKTIME.pop(0), NUM_SCANNERS, SCANTIME.pop(0))
env.process(s)

# Execute!
env.run(until=SIM_TIME)