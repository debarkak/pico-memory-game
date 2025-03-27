from machine import Pin
import time
import urandom

start_btn = Pin(14, Pin.IN, Pin.PULL_UP)
reset_btn = Pin(22, Pin.IN, Pin.PULL_UP)
down_btn = Pin(18, Pin.IN, Pin.PULL_UP)
mid_btn = Pin(19, Pin.IN, Pin.PULL_UP)
up_btn = Pin(20, Pin.IN, Pin.PULL_UP)

fail_led = Pin(15, Pin.OUT)
led1 = Pin(13, Pin.OUT)
led2 = Pin(12, Pin.OUT)
led3 = Pin(11, Pin.OUT)
win_led = Pin(10, Pin.OUT)
pwr_led = Pin(0, Pin.OUT)
pwr_led.value(1)

step_leds = [fail_led, led1, led2, led3, win_led]
game_leds = [led1, led2, led3]
game_btns = [down_btn, mid_btn, up_btn]

MIN_STEPS = 4
MAX_EXTRA = 5

def startup_seq():
    print("Starting up...")
    for led in step_leds:
        led.value(1)
        time.sleep(0.25)
        led.value(0)
    print("Startup complete.")

def clear_leds():
    for led in step_leds:
        led.value(0)

def choose_steps():
    extra = 0
    print("Select steps: Down/Up to adjust, Start to confirm.")
    while True:
        for i, led in enumerate(step_leds):
            led.value(1 if i < extra else 0)
        if reset_btn.value() == 0:
            print("Reset during step selection.")
            time.sleep(0.2)
            return -1
        if down_btn.value() == 0 and extra > 0:
            extra -= 1
            print("Steps:", MIN_STEPS + extra)
            time.sleep(0.2)
        if up_btn.value() == 0 and extra < MAX_EXTRA:
            extra += 1
            print("Steps:", MIN_STEPS + extra)
            time.sleep(0.2)
        if start_btn.value() == 0:
            print("Game starting with", MIN_STEPS + extra, "steps.")
            time.sleep(0.5)
            return MIN_STEPS + extra

def gen_pattern(n):
    p = [urandom.randint(0, 2) for _ in range(n)]
    print("Pattern:", p)
    return p

def show_pattern(p):
    print("Showing pattern...")
    for index in p:
        print("LED", index + 1, "on")
        game_leds[index].value(1)
        time.sleep(1)
        game_leds[index].value(0)
        time.sleep(0.5)
    print("Pattern done.")

def player_input(p):
    print("Your turn...")
    step = 0
    while step < len(p):
        if reset_btn.value() == 0:
            print("Reset during input.")
            return -1
        for i, btn in enumerate(game_btns):
            if btn.value() == 0:
                print("Step", step + 1, "expected:", p[step], "got:", i)
                game_leds[i].value(1)
                time.sleep(0.2)
                game_leds[i].value(0)
                while btn.value() == 0:
                    time.sleep(0.05)
                if i == p[step]:
                    step += 1
                else:
                    print("Wrong input.")
                    return False
    return True

while True:
    startup_seq()
    steps = choose_steps()
    if steps == -1:
        continue
    clear_leds()
    pattern = gen_pattern(steps)
    show_pattern(pattern)
    res = player_input(pattern)
    if res == -1:
        continue
    if res:
        print("Win!")
        for _ in range(5):
            win_led.value(1)
            time.sleep(0.5)
            win_led.value(0)
            time.sleep(0.5)
    else:
        print("Lose!")
        for _ in range(5):
            fail_led.value(1)
            time.sleep(0.5)
            fail_led.value(0)
            time.sleep(0.5)

