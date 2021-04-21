import numpy as np
from typing import List
from neighborhood import get_neigbors
main_states = {k: i for i, k in enumerate(['healthy','quarantine', 'infected', 'sick', 'infected_and_sick', 'in_hospital','recovered', 'dead'])}
conj_states = {k: i for i, k in enumerate(['protecting_others', 'self_protecting', 'no_security_measures', 'infecting', 'organizing_protection'])}
class Particle:
    def __init__(self, state, state_conj):
        self.state = state
        self.state_conj = state_conj
        self.time_waiting = 0
        self.mortality = 0.15
    def update_mortality(self,mortality):
        self.mortality = mortality
    def get_infected(self):
        self.state = 'infected'
        self.state_conj = np.random.choice(['no_security_measures', 'infecting'])
        pass

    def recover(self):
        self.state = 'recovered'
        self.state_conj = 'protecting_others'
        pass

    def get_sick(self):
        self.state = 'infected_and_sick'
        self.state_conj = np.random.choice(['no_security_measures', 'infecting'])
        pass

    def stop_infecting(self):
        self.state = 'sick'
        self.state_conj = 'no_security_measures'

    def die(self):
        self.state = 'dead'
        self.state_conj = 'no_security_measures'

    def quarantine(self):
        self.state = 'quarantine'
        self.state_conj = 'protecting_others'
        pass
    def is_dead(self):
        number = np.random.rand()
        probability = self.mortality
        return number <= probability
    def wait(self):
        if self.state == 'infected':
            self.time_waiting+=1
            if self.time_waiting == 5:
                self.state = 'infected_and_sick'
            elif self.time_waiting == 9:
                self.state = 'sick'
            elif self.time_waiting == 14:
                if self.is_dead():
                    self.die()
                else:
                    self.recover()
                    self.time_waiting = 0
        elif self.state == 'quarantine':
            self.time_waiting += 1
            if self.time_waiting == 14:
                self.time_waiting = 0
                self.state = 'healthy'


def infecting_probability(neighbors: List[Particle]):
    proba_from_state = np.ones((8,5))
    proba = 0
    for neighbor in neighbors:
        proba += proba_from_state[main_states[neighbor.state], conj_states[neighbor.state_conj]]
    return proba


def update_particles(particles, u):
    for i, part_row in enumerate(particles):
        for j, particle in enumerate(particles):
            if particle.state == 'healthy':
                number = np.random.rand()
                probability = infecting_probability(get_neigbors(particles, i, j))
                if number <= probability :
                    particle.get_infected()
                else:
                    number = np.random.rand()
                    probability = u['security_measures']
                    if number <= probability :
                        particle.quarantine()

            else:
                particle.update_mortality(u['mortality'])
                particle.wait()




