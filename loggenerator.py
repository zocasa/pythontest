import datetime
import random
import time

import filehandler


resolution = 0.01
scale = int(1/resolution)

# 50%
common_line_1 = "fun isn't something one considers when balancing the universe\n"
common_line_2 = "but this does put a smile on my face\n"
common_line_3 = "Dread it... Run from it... Destiny still arrives\n"
common_lines = [common_line_1, common_line_2, common_line_3]

# 25%
occasional_line_1 = "Mr. Anderson\n"
occasional_line_2 = "Not impossible, Inevitable\n"
occasional_lines = [occasional_line_1, occasional_line_2]

# 15%
sporadic_line_1 = "I never freeze\n"
sporadic_line_2 = "Inception\n"
sporadic_lines = [sporadic_line_1, sporadic_line_2]

# 10%
target_line_1 = "x is: " + str(int(time.time())) + ", y is : " + str(random.randrange(20*scale, 100*scale)/scale) + ".\n"
target_lines = [target_line_1]


if __name__ == "__main__":
    filename = filehandler.get_filename()

    while True:
        lines_to_write = []
        lines = []

        rarity = random.random()

        should_repeat = False

        if rarity < 0.5:
            lines = common_lines
            should_repeat = True
        elif rarity < 0.75:
            lines = occasional_lines
            should_repeat = True
        elif rarity < 0.9:
            lines = sporadic_lines
            should_repeat = True
        else:
            lines = target_lines

        i = random.randrange(0, len(lines))
        lines_to_write.append(lines[i])

        times_to_repeat = random.randint(1, 3)

        if should_repeat:
            for c in range(times_to_repeat):
                i = random.randrange(0, len(lines))
                lines_to_write.append(lines[i])

        sleep_timer = random.random()
        if sleep_timer < 0.25:
            time.sleep(sleep_timer)

        filehandler.write_to_file(filename, lines_to_write)
