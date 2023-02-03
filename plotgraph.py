import argparse
import collections
import datetime
import functools

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import re

import filehandler


def get_graph_title():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('-gt', '-graph_title', type=str, help='Title for graph')

    args = arg_parser.parse_args()
    return args.graph_title


# stolen from https://towardsdatascience.com/plotting-live-data-with-matplotlib-d871fac7500b
def parse_timestamp_and_digit_graph_coordinates(source_lines):
    x = collections.deque()
    y = collections.deque()

    for line in source_lines:
        pattern = re.compile(r'x is: \d+\.\d+, y is: \d+\.\d+')
        match = pattern.search(line)
        if match:
            sub_pattern = re.compile(r'\d+\.\d+')
            datapoint = sub_pattern.findall(match.group())
            x.append(datetime.datetime.fromtimestamp(float(datapoint[0])))
            y.append(float(datapoint[1]))

    return x, y


def create_graph(file, should_slide=True, slide_window=20):
    x = collections.deque()
    y = collections.deque()

    fig, subplot = plt.subplots(constrained_layout=True)

    f = functools.partial(update_graph, plot=subplot, file=file,
                          should_slide=should_slide, slide_window=slide_window, x=x, y=y)
    # Die but do not delete the variable assignment
    ani = animation.FuncAnimation(fig, f, interval=1)

    plt.show()

    return fig, subplot


def update_graph(frame, plot, file, should_slide, slide_window, x, y):
    plot.cla()

    _x = collections.deque()
    _y = collections.deque()

    _x, _y = parse_timestamp_and_digit_graph_coordinates(filehandler.read_till_eof(file))

    if should_slide and len(x) >= slide_window:
        for i in range(len(_x)):
            x.popleft()
            y.popleft()

    x.extend(_x)
    y.extend(_y)

    plot.plot(x, y, 'bo', linestyle="--")

    if len(x) > 0:
        plot.scatter(x[-1], y[-1])
        plot.text(x[-1], y[-1] + 2, "{}".format(y[-1]))
