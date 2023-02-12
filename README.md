# pythontest
Python testing package and some utilities?

## Dependencies
In `requirements.txt`

## Run
1. `python3 loggenerator.py -f .custom_log.txt`
2. `python3 main.py -f .custom_log.txt`

### Things to tinker
* in `main.py`, change `open_read_file`'s `beginning` to `false` 
to read from current position of log instead of beginning
* in `loggenerator.py` when opening file, change `w+` to `a+` to not overwrite file
* in `loggenerator.py`, some not very useful constants to tinker
* in `main.py`, while calling the `plotgraph`'s `create_graph`,
pass optionals `should_slide` which will plot a sliding graph (new updates will push older ones out of frame)
and use `slide_window` with it to control the width of the sliding window

## TODO (In no particular order)
* Separate out argParser
* Graph is Jell-O TT
* Clean and some comment?
* PRETTIFY GRAPH
* Better `loggenerator` (one with map kind of thing for better interlacing)
* logging (and testing in the `FuncAnimation`'s function)
* Regex pattern does not account for integers (need to test)

## Things used (not in detail)
* File opening
* Reading till somewhere
* matplotlib FuncAnimation and plotting
* partial functions (very cool feature)
* sleeping a thread
* random number generation
* measuring time
* getting time in date format
* collections.deque
* argParse
* regex
  * and the plague
