
def get_neighbors(particles, x, y):
    """
    Zwraca sąsiadów wg sąsiedztwa Moora
    :param particles: zestaw osobników
    :param x: indeks x
    :param y: index y
    :return: lista sąsiedztwa
    """
    neighbors = []
    w, k = len(particles), len(particles[0])
    if x > 0: # w przeciwnym razie nie ma co zliczac, bo nie ma nikogo u gory
        neighbors.append(particles[x - 1][y])

    if y > 0: # w przeciwnym razie nie ma co zliczac, bo nie ma nikogo po lewej

        neighbors.append(particles[x] [y - 1])

    if x < w-1: # w przeciwnym razie nie ma co zliczac, bo nie ma nikogo na dole

        neighbors.append(particles[x + 1][y])

    if y < k-1: # w przeciwnym razie nie ma co zliczac, bo nie ma nikogo po prawej
        neighbors.append(particles[x][y + 1])

    if x > 0 and y > 0: # w przeciwnym razie nie ma co zliczac, bo nie ma nikogo u gory po lewej

        neighbors.append(particles[x - 1][y - 1])

    if x > 0 and y < k-1: # w przeciwnym razie nie ma co zliczac, bo nie ma nikogo u gory po prawej

        neighbors.append(particles[x - 1][y + 1])

    if x < w-1 and y > 0: # w przeciwnym razie nie ma co zliczac, bo nie ma nikogo na dole po lewej

        neighbors.append(particles[x + 1] [y - 1])

    if x < w-1 and y < k-1: # w przeciwnym razie nie ma co zliczac, bo nie ma nikogo na dole po prawej

        neighbors.append(particles[x + 1][y + 1])
    return neighbors
if __name__ == "__main__":
    x = [[f'{i},{j}' for i in range(10)] for j in range(10)]
    print(x)
    print(get_neighbors(x,0,1))