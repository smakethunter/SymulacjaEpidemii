import matplotlib.animation as animation
from particle import *
import pandas as pd
from tqdm import tqdm

def init(x):
    if x < 1:
        return 1
    elif x < 6:
        return x/4
    else:
        return x /12

def animate_pandemic(n_iter=100,
                     n_particles=(100,100),
                     u=None,
                     infected_indexes=None,
                     save=True):
    # Animate
    if u is None:
        u = [{'security_measures': 1, 'mortality': 0.15, 'hygene': 0.02}]
    else:
        n_iter = len(u)-1
    population = [[Particle('healthy') for i in range(n_particles[0])] for j in range(n_particles[0])]
    if infected_indexes:
        for (ix, iy) in infected_indexes:
            population[ix][iy].get_infected()


    fig,ax = plt.subplots(2,1, figsize = (10,10))
    ax[1].set_title('Infected')

    ims = []
    infected = []
    dead = []
    recovered = []

    for i in tqdm(range(n_iter)):
        infecting = False
        iter = 1
        im1 = ax[0].imshow(particles_to_image(population))
        im2, = ax[1].plot(np.array(infected))
        im3, = ax[1].plot(np.array(recovered))
        im4, = ax[1].plot(np.array(dead))
        ax[1].legend([im2, im3, im4], ['Infected', 'Recovered', 'Dead'])
        ims.append([im1, im2, im3, im4])

        if n_iter-25 > i > 50 and get_state_number(population, ['infected', 'sick', 'infected_and_sick'])/len(population)**2<0.06:
            new_samples = 100
            infecting = True
        else:
            new_samples = 2
        for pop in range(new_samples):
            ip = np.random.choice([x for x in range(len(population))])
            jp = np.random.choice([x for x in range(len(population))])

            population[ip][jp].get_infected()

        if infecting:
            iter = 10

        if len(u)>1:

            update_particles(population, u[i],iter)

        else:
            update_particles(population, u[0],iter)

        # print({k:get_state_number(population,[k]) for k in ['healthy','infected', 'sick', 'infected_and_sick','recovered','dead']})
        infected.append(get_state_number(population, ['infected', 'sick', 'infected_and_sick']))
        dead.append(get_state_number(population, ['dead']))
        recovered.append(get_state_number(population, ['recovered']))

    im_ani = animation.ArtistAnimation(
        fig, ims, interval=10, repeat_delay=3000, blit=True
    )
    # Optional: save the animation, with a name based on the seed.
    if save:
        im_ani.save((str(n_iter)+"_"+str(n_particles[0])+'control' + ".gif"), writer="imagemagick")
        print('gif saved')
        FFwriter = animation.FFMpegWriter(fps=10)
        im_ani.save(str(n_iter)+"_"+str(n_particles[0])+'control' + 'animation.mp4', writer=FFwriter)
        print('mp4 saved')
if __name__ == "__main__":
    import os

    cwd = os.getcwd()
    data = pd.read_csv(os.path.join(cwd, 'data/UKdata.csv'))
    security_measures = data['GovernmentResponseIndex'].fillna(0).apply(lambda x: 0.1+1-x/data['GovernmentResponseIndex'].max()).to_numpy()

    hygene = data['ContainmentHealthIndex'].fillna(0).apply(lambda x: x/data['GovernmentResponseIndex'].max()-0.2).to_numpy()

    mortality = data['ContainmentHealthIndex'].fillna(0).apply(lambda x: 0.45-0.1*data['H8_Protection of elderly people'].max()).to_numpy()

    control = [{'security_measures': sm, 'mortality': m, 'hygene':hygene} for sm, m, hygene in zip(list(security_measures),
                                                                          list(mortality), list(hygene))]

    animate_pandemic(100, (500, 500), u=control)