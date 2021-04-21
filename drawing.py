
import matplotlib.animation as animation


from particle import *
u={'security_measures': 0.01, 'mortality': 0.15}
def animate_pandemic(n_iter=20, n_particles=(100,100), u=None, infected_indexes=None, save = True):
    # Animate
    if u is None:
        u = {'security_measures': 0.01, 'mortality': 0.15}
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
        update_particles(population, u)
        infected.append(get_state_number(population,['infected', 'sick', 'infected_and_sick']))
        dead.append(get_state_number(population,['dead']))
        recovered.append(get_state_number(population, ['recovered']))
    im_ani = animation.ArtistAnimation(
        fig, ims, interval=10, repeat_delay=3000, blit=True
    )
    # Optional: save the animation, with a name based on the seed.
    if save:
        im_ani.save((str(n_iter) + str('_'.join([str(int(ui)) for ui in u.values()])) + ".gif"), writer="imagemagick")
        FFwriter = animation.FFMpegWriter(fps=10)
        im_ani.save(str(n_iter) + str('_'.join([str(int(ui)) for ui in u.values()])) +'animation.mp4', writer=FFwriter)
if __name__ == "__main__":
    animate_pandemic()