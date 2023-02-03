import random
import time

import filehandler


resolution = 0.01
scale = int(1/resolution)

common_line_1 = "fun isn't something one considers when balancing the universe\n"
common_line_2 = "but this does put a smile on my face\n"
common_line_3 = "Dread it... Run from it... Destiny still arrives\n"
common_lines = [common_line_1, common_line_2, common_line_3]

occasional_line_1 = "Mr. Anderson\n"
occasional_line_2 = "Not impossible, Inevitable\n"
occasional_lines = [occasional_line_1, occasional_line_2]

sporadic_line_1 = "I never freeze\n"
sporadic_line_2 = "Inception\n"
sporadic_lines = [sporadic_line_1, sporadic_line_2]


if __name__ == "__main__":
    filename = filehandler.get_filename()
    file = open(filename, 'w+')

    while True:
        lines_to_write = []
        lines = []

        rarity = random.random()

        should_repeat = False

        # 50%
        if rarity < 0.5:
            lines = common_lines
            should_repeat = True
        # 25%
        elif rarity < 0.75:
            lines = occasional_lines
            should_repeat = True
        # 15%
        elif rarity < 0.9:
            lines = sporadic_lines
            should_repeat = True
        # 10%
        else:
            lines = ["x is: " + str(time.time()) + ", y is: " + str(random.randrange(0*scale, 100*scale)/scale) + ".\n"]

        i = random.randrange(0, len(lines))
        lines_to_write.append(lines[i])

        # feels like should be a word
        repeatness = 3
        times_to_repeat = random.randint(1, repeatness)

        if should_repeat:
            for c in range(times_to_repeat):
                i = random.randrange(0, len(lines))
                lines_to_write.append(lines[i])

        # simulate some sort of TPS
        sleep_timer = random.random()
        if sleep_timer < 0.25:
            time.sleep(sleep_timer)

        file.writelines(lines_to_write)
