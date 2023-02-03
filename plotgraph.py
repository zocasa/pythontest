import argparse
import collections
import functools

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import re


def get_graph_title():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('-gt', '-graph_title', type=str, help='Title for graph')

    args = arg_parser.parse_args()
    return args.graph_title


# stolen from https://towardsdatascience.com/plotting-live-data-with-matplotlib-d871fac7500b
def parse_graph_coordinates(source_lines):
    x = collections.deque()
    y = collections.deque()

    for line in source_lines:
        pattern = re.compile(r'x is: \d+, y is : \d+')
        match = pattern.search(line)
        if match:
            sub_pattern = re.compile(r'\d+')
            datapoint = sub_pattern.findall(match.group())
            x.append(datapoint[0])
            y.append(datapoint[1])

    return x, y


def create_graph(poller, stream, should_slide=True, slide_window=20):
    x = collections.deque()
    y = collections.deque()

    fig, subplot = plt.subplots(constrained_layout=True)

    f = functools.partial(update_graph, plot=subplot, poller=poller, stream=stream,
                          should_slide=should_slide, slide_window=slide_window, x=x, y=y)
    animation.FuncAnimation(fig, f, interval=1)

    plt.show()

    return fig, subplot


def update_graph(frame, plot, poller, stream, should_slide, slide_window, x, y):
    plot.cla()

    _x = collections.deque()
    _y = collections.deque()

    if poller.poll(999):
        _x, _y = parse_graph_coordinates(stream.stdout.readline())

    if should_slide and len(x) >= slide_window:
        for i in range(len(_x)):
            x.popleft()
            y.popleft()

    plot.plot(x, y, 'bo', linestyle="--")
    plot.scatter(x[-1], y[-1])
    plot.text(x[-1], y[-1] + 2, "{}".format(y[-1]))
