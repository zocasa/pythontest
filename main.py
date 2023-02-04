import filehandler
import plotgraph

if __name__ == "__main__":
    filename = filehandler.get_filename()
    file = filehandler.open_read_file(filename, True)
    fig, subplot = plotgraph.create_graph(file, True)
