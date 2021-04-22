import matplotlib.animation as animation
from particle import *
import pandas as pd


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
        u = [{'security_measures': 1, 'mortality': 0.15}]
    else:
        n_iter = len(u)-1
    population = [[Particle('healthy') for i in range(n_particles[0])] for j in range(n_particles[0])]
    if infected_indexes:
        for (ix, iy) in infected_indexes:
            population[ix][iy].get_infected()
    else:
        for (ix, iy) in zip(range(4), range(4)):
            population[ix][iy].get_infected()

    fig,ax = plt.subplots(2,1, figsize = (10,10))
    ax[1].set_title('Infected')

    ims = []
    infected = []
    dead = []
    recovered = []
    for i in range(n_iter):

        im1 = ax[0].imshow(particles_to_image(population))
        im2, = ax[1].plot(np.array(infected))
        im3, = ax[1].plot(np.array(recovered))
        im4, = ax[1].plot(np.array(dead))
        ax[1].legend([im2, im3, im4], ['Infected', 'Recovered', 'Dead'])
        ims.append([im1,im2, im3,im4])
        if len(u)>1:
            update_particles(population, u[i])
            print(u[i])
        else:
            update_particles(population, u[0])
            print(i)
        infected.append(get_state_number(population,['infected', 'sick', 'infected_and_sick']))
        dead.append(get_state_number(population,['dead']))
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

    data = pd.read_csv('data/UKdata.csv')
    security_measures = data['GovernmentResponseIndex'].fillna(0).apply(lambda x: 1-x/data['GovernmentResponseIndex'].max()).head(200).to_numpy()
    control = [{'security_measures': sm, 'mortality': m} for sm, m in zip(list(security_measures),
                                                                          list(np.full(security_measures.shape,0.15)))]

    animate_pandemic(100,(500,500), u = control)