from blinkstick import blinkstick
from time import sleep
from colour import Color
from signal import signal, SIGINT
from sys import exit

####
# breathing.py by Different55 <burritosaur@protonmail.com>
# This script smoothly fades between two colors in a kind of breathing pattern.
# The color is set equally to all available LEDs on the first blinkstick found.
####

# To allow user to turn off color with CTRL-C
def turn_off():
    sticks = blinkstick.find_all()
    for stick in sticks:
        stick.set_led_data(0, [0, 0, 0] * stick.get_led_count())


def handler(signal_received, frame):
    print("\nLater Skater")
    turn_off()
    exit(0)


########## -------- MAIN FUNCTION ------- #########
def main():
    fps = 50.0  # How many frames per second. 50 is about the upper limit.
    colorin = Color("#b71500")
    colorout = Color("black")

    ### END OPTIONS ###

    stk = blinkstick.find_first()
    cnt = stk.get_led_count()

    while True:
        mult = 0
        last = colorout
        while (
            last.hex != colorin.hex
        ):  # For some reason if I use anything but .hex, they'll never equal the same color.
            last = Color(
                rgb=(
                    (last.red * 5 + colorin.red) / 6,
                    (last.green * 5 + colorin.green) / 6,
                    (last.blue * 5 + colorin.blue) / 6,
                )
            )
            data = [
                int(last.green * 255),
                int(last.red * 255),
                int(last.blue * 255),
            ] * cnt
            stk.set_led_data(0, data)
            sleep(1 / fps)
            print("breathe in", last)
        print("pause", last)
        sleep(1 / fps * 7)
        while (
            last.hex != colorout.hex and last.luminance > 0.004
        ):  # For fading to black, this helps a bit since the blinkstick completely blanks out at low brightness levels.
            last = Color(
                rgb=(
                    (last.red * 6 + colorout.red) / 7,
                    (last.green * 6 + colorout.green) / 7,
                    (last.blue * 6 + colorout.blue) / 7,
                )
            )
            data = [
                int(last.green * 255),
                int(last.red * 255),
                int(last.blue * 255),
            ] * cnt
            stk.set_led_data(0, data)
            sleep(1 / fps)
            print("breathe out", last)


if __name__ == "__main__":
    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)

    print("It's lit bruv. Press CTRL-C to turn down.")
    while True:
        main()
