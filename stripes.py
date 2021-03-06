from blinkstick import blinkstick
import time, math, colorsys

from signal import signal, SIGINT
from sys import exit

####
# stripes.py by Different55 <burritosaur@protonmail.com>
# Rotates two stripes of hopefully similar colors around all available LEDs on
# the first channel of the first blinkstick. I use it with orange/yellow for
# indicating hot weather in the forecast.
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
    color1 = (0.05, 1, 0.98)  # These are in hsv format
    color2 = (0.08, 0.95, 1)
    speed = 10  # Speed of the animation
    width = 15  # Width of the stripes. Lower = wider.
    fps = 50.0  # FPS of the animation. 50 is about the upper limit.

    ### END OPTIONS ###

    stk = blinkstick.find_first()
    cnt = stk.get_led_count()

    while True:
        data = []
        for i in range(cnt):
            fac = math.sin((time.time()) * speed + i * width) / 2 + 0.5
            hue = color1[0] + (color2[0] - color1[0]) * fac
            sat = color1[1] + (color2[1] - color1[1]) * fac
            val = color1[2] + (color2[2] - color1[2]) * fac
            r, g, b = colorsys.hsv_to_rgb(hue, sat, val)
            data = data + [
                int(g * 255),
                int(r * 255),
                int(b * 255),
            ]  # Convert to GRB and add to the frame.
        stk.set_led_data(0, data)  # Send off to the blinkstick
        time.sleep(1 / fps)  # Nap for a bit so we don't overwhelm the blinkstick.


if __name__ == "__main__":
    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)

    print("It's lit bruv. Press CTRL-C to turn down.")
    while True:
        main()
