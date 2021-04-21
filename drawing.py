
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

    fig = plt.figure()

    ims = []
    for i in range(n_iter):
        print()
        ims.append((plt.imshow(particles_to_image(population)),))
        update_particles(population, u)
    im_ani = animation.ArtistAnimation(
        fig, ims, interval=1, repeat_delay=3000, blit=True
    )
    # Optional: save the animation, with a name based on the seed.
    if save:
        im_ani.save((str(n_iter) + str('_'.join([str(int(ui)) for ui in u.values()])) + ".gif"), writer="imagemagick")
        FFwriter = animation.FFMpegWriter(fps=10)
        im_ani.save(str(n_iter) + str('_'.join([str(int(ui)) for ui in u.values()])) +'animation.mp4', writer=FFwriter)
if __name__ == "__main__":
    animate_pandemic()