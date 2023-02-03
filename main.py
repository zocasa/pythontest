import filehandler
import plotgraph

if __name__ == "__main__":
    filename = filehandler.get_filename()
    poller, stream = filehandler.tail_file(filename)
    fig, subplot = plotgraph.create_graph(poller, stream)
    # while True:
    #     if poller.poll(1000):
    #         coordinates = parse_graph_coordinates(stream.stdout.readlines())
    #         update_graph(coordinates)
