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
def create_graph(file, should_slide=True, slide_window=20):
    x_labels = collections.deque()
    y_values = collections.deque()

    fig, subplot = plt.subplots(constrained_layout=True)

    f = functools.partial(update_graph, plot=subplot, file=file,
                          should_slide=should_slide, slide_window=slide_window,
                          x_labels=x_labels, y_values=y_values)

    # Die but do not delete the variable assignment
    ani = animation.FuncAnimation(fig, f, interval=1)

    plt.show()

    return fig, subplot


def update_graph(frame, plot, file, should_slide, slide_window, x_labels, y_values):
    plot.cla()

    _x_labels = collections.deque()
    _y_values = collections.deque()

    _x_labels, _y_values = parse_timestamp_and_digit_graph_coordinates(filehandler.read_till_eof(file))

    overflow = len(x_labels) + len(_x_labels) - slide_window
    if should_slide and overflow > 0:
        for i in range(len(_x_labels)):
            if i < overflow:
                x_labels.popleft()
                y_values.popleft()
            else:
                break

    x_labels.extend(_x_labels)
    y_values.extend(_y_values)

    _x_values = []
    if len(x_labels) > 0:
        _x_values = [*range(0, len(x_labels))]

    plot.plot(_x_values, y_values, 'bo', linestyle="--")

    if len(x_labels) > 0:
        for i, j in zip(_x_values, y_values):
            plot.annotate(str(j), xy=(i, j+2))

        plt.xticks(_x_values)
        plt.xlim([0, slide_window+1])
        plt.ylim([0, 110])
        plot.set_xticklabels(x_labels, rotation=45, ha='right')
        plot.scatter(_x_values[-1], y_values[-1])
        plot.text(_x_values[-1], y_values[-1] + 2, "{}".format(y_values[-1]))


def parse_timestamp_and_digit_graph_coordinates(source_lines):
    x = collections.deque()
    y = collections.deque()

    for line in source_lines:
        pattern = re.compile(r'x is: (\d+\.\d+|\d+), y is: (\d+\.\d+|\d+)')
        match = pattern.search(line)
        if match:
            sub_pattern = re.compile(r'(\d+\.\d+|\d+)')
            datapoint = sub_pattern.findall(match.group())
            x.append(str(datetime.datetime.fromtimestamp(float(datapoint[0]))))
            y.append(float(datapoint[1]))

    return x, y


if __name__ == "__main__":
    filename = filehandler.get_filename()
    file = filehandler.open_read_file(filename, True)
    create_graph(file)
