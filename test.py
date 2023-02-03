import collections
import datetime
import functools
import random
import time

import matplotlib.pyplot as plt
import matplotlib.animation as animation

# stolen from https://towardsdatascience.com/plotting-live-data-with-matplotlib-d871fac7500b
if __name__ == "__main__":
    # function to update the data
    def my_function(i, should_slide=True, slide_window=20):
        r = random.randint(0, 5)

        for i in range(r):
            # get data
            if should_slide and len(cpu) >= slide_window:
                x.popleft()
                cpu.popleft()

            time.sleep(random.random())

            x.append(datetime.datetime.now())
            cpu.append(random.randrange(20*scale, 100*scale)/scale)

        # clear axis
        ax.cla()

        # plot cpu
        ax.plot(x, cpu, 'bo', linestyle="--")

        ax.scatter(x[-1], cpu[-1])
        ax.text(x[-1], cpu[-1] + 2, "{}%".format(cpu[-1]))
        ax.set_ylim(0, 100)


    resolution = 0.01
    scale = int(1/resolution)

    time_range = 20

    x = collections.deque()
    cpu = collections.deque()

    time.sleep(random.random())

    # define and adjust figure
    fig, ax = plt.subplots(constrained_layout=True)
    f = functools.partial(my_function, should_slide=False)

    for i in range(100):
        # animate
        ani = animation.FuncAnimation(fig, f, interval=1000)

        plt.show()
