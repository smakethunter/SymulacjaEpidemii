import matplotlib.pyplot as plt
import numpy as np
from typing import List
from neighborhood import get_neighbors
from copy import deepcopy
main_states = {k: i for i, k in enumerate(['healthy','quarantine', 'infected', 'sick', 'infected_and_sick', 'in_hospital','recovered', 'dead'])}
conj_states = {k: i for i, k in enumerate(['protecting_others', 'self_protecting', 'no_security_measures', 'infecting', 'organizing_protection'])}
colours = dict(zip(['healthy','quarantine', 'infected', 'sick', 'infected_and_sick', 'in_hospital','recovered', 'dead'],
               [0,0,1,1,1,0,2,3]))
colours2rgb = dict(zip([0,1,2,3],[np.array([90, 252, 3])/255.,np.array([252, 28, 3])/255.,np.array([3, 173, 252])/255.,np.array([2, 1, 8])/255.]))
state_proba = np.array([[0.000001, 0.000015, 0.00003, 0, 0.00003],
                                 [0.00025, 0, 0, 0, 0],
                                 [0, 0, 0.04, 0.07, 0],
                                 [0, 0, 0.05, 0, 0],
                                 [0, 0, 0.07, 0.095, 0],
                                 [0, 0, 0, 0, 0.00004],
                                 [0.0001, 0, 0, 0, 0.0002],
                                 [0, 0, 0, 0, 0]])
class Particle:
    def __init__(self, state):
        self.state = state
        self.state_conj = np.random.choice(['protecting_others', 'self_protecting', 'no_security_measures'])
        self.time_waiting = 0
        self.mortality = 0.15

    def update_mortality(self,mortality):
        """
        Update śmiertelności
        :param mortality:
        :return:
        """
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
        """
        umrzyj

        """
        self.state = 'dead'
        self.state_conj = 'no_security_measures'

    def quarantine(self):
        """
        wyślij na kwarantannę

        """
        self.state = 'quarantine'
        self.state_conj = 'protecting_others'
        pass

    def is_dead(self):
        """
        sprawdza czy osobnik umrze
        :return: bool
        """
        number = np.random.rand()
        probability = self.mortality
        return number < probability
    def wait(self):
        """
        Zmienia stan jednostki zakażonej lub na kwarantannie w zależności od czasu symulacji

        """
        if self.state != 'healthy' and self.state != 'dead':
            self.time_waiting += 1
            if self.state == 'infected' and self.time_waiting == 5:
                self.state = 'infected_and_sick'
            elif self.state == 'infected_and_sick' and self.time_waiting == 9:
                self.state = 'sick'
            elif self.state == 'sick' and self.time_waiting == 14:
                if self.is_dead():
                    self.die()
                    self.time_waiting = 0
                else:
                    self.recover()
                    self.time_waiting = 0
            elif self.state == 'quarantine':

                if self.time_waiting == 14:
                    self.time_waiting = 0
                    self.state = 'healthy'


def probability_of_getting_infected(neighbors: List[Particle], proba_from_state=state_proba):
    """
    Zwraca prawdopodobieństwo zakażenia na podstawie stanu sąsiadów
    :param proba_from_state:
    :param neighbors: lista sąsiadów
    :return: prawdopodobieństwo
    """
    # TODO: edytować tabelę prawopodobieństw
    proba = 0
    for neighbor in neighbors:
        proba += proba_from_state[main_states[neighbor.state], conj_states[neighbor.state_conj]]
    return proba


def update_particles(particles, u):
    """
    Dla każdego osobnika z planszy wykonujemy update stanu
    :param particles: osobniki z planszy
    :param u: sterowanie w postaci słownika
    :return: None
    """
    previous_state = deepcopy(particles)

    for i, particles_row in enumerate(particles):
        for j, particle in enumerate(particles_row):
            if particle.state == 'healthy':
                # próba zakażenia
                number = np.random.rand()
                neighbors = get_neighbors(previous_state, i, j)
                probability = u['security_measures']*probability_of_getting_infected(neighbors)
                if number <= probability :
                    particle.get_infected()
                else:
                    # skierowanie na kwarantannę
                    number = np.random.rand()
                    probability = u['security_measures']/100
                    if number <= probability:
                        particle.quarantine()

            else:
                # zmiana stanu dla zakażonego
                particle.update_mortality(u['mortality'])
                particle.wait()


def particles_to_image(particles)-> np.ndarray:
    """
    Rysowanie planszy
    :param particles: List(List(Particle)) - osobniki
    :return: np.ndarray pokolorowany obrazek
    """
    image = np.zeros((len(particles), len(particles[0]),3))
    for i, particles_row in enumerate(particles):
        for j, particle in enumerate(particles_row):
            image[i, j, :] = colours2rgb[colours[particle.state]]
    return image

def get_state_number(particles, states: List[str]):
    """
    Podaje liczebność danych klas
    :param particles: osobniki
    :param states: stany które chcemy podliczyć
    :return: podliczone stany
    """
    sum = 0
    for i, particles_row in enumerate(particles):
        for j, particle in enumerate(particles_row):
            if particle.state in states:
                sum += 1
    return sum


if __name__ == "__main__":
    particles = [[Particle('healthy') for i in range(100)] for j in range(100)]
    particles[3][4].get_infected()
    particles[3][3].get_infected()
    particles[2][3].get_infected()
    print(main_states)
    u = {'security_measures': 0.01, 'mortality': 0.15}
    for i in range(100):
        update_particles(particles, u)
    print([[particle.state for particle in particle_row] for particle_row in particles])
    plt.imshow(particles_to_image(particles))
    plt.show()
