import badger2040
from badger2040 import WIDTH
import time

NAVIGATION = [
    "WiFi:    (A) Home | (B) Work",
    "         (C) HotSpot",
    "GitHub: (UP) Home | (DOWN) Work",
]


def copy_file(src, dest):
    with open(src, "rb") as src_file:
        with open(dest, "wb") as dest_file:
            dest_file.write(src_file.read())


def draw_view(lines):
    badger.set_pen(15)
    badger.clear()

    badger.set_font("bitmap8")
    badger.set_pen(0)
    badger.rectangle(0, 0, WIDTH, 16)
    badger.set_pen(15)
    badger.text("Restore Defaults", 3, 4, WIDTH, 1)

    badger.set_pen(0)
    for i, line in enumerate(lines):
        badger.text(line, 10, 30 + i * 16)
    badger.update()


def restoreWifi(fileName):
    badger.led(128)
    draw_view(["Restoring config..."] + [""] * 2 + NAVIGATION)
    copy_file("/defaults/" + fileName, "/WIFI_CONFIG.py")
    time.sleep(2)
    draw_view(["Config restored!"] + [""] * 2 + NAVIGATION)
    badger.led(0)


def restoreGithubConfig(fileName):
    badger.led(128)
    draw_view(["Restoring config..."] + [""] * 2 + NAVIGATION)
    copy_file("/defaults/" + fileName, "/GITHUB_CONFIG.py")
    time.sleep(2)
    draw_view(["Config restored!"] + [""] * 2 + NAVIGATION)
    badger.led(0)


badger = badger2040.Badger2040()
badger.set_update_speed(2)
badger.led(128)

draw_view([""] * 3 + NAVIGATION)


while True:
    # Sometimes a button press or hold will keep the system
    # powered *through* HALT, so latch the power back on.
    badger.keepalive()

    if badger.pressed(badger2040.BUTTON_A):
        restoreWifi("WIFI_HOME.py")
    if badger.pressed(badger2040.BUTTON_B):
        restoreWifi("WIFI_WORK.py")
    if badger.pressed(badger2040.BUTTON_C):
        restoreWifi("WIFI_HOTSPOT.py")
    if badger.pressed(badger2040.BUTTON_UP):
        restoreGithubConfig("GITHUB_HOME.py")
    if badger.pressed(badger2040.BUTTON_DOWN):
        restoreGithubConfig("GITHUB_WORK.py")

    badger.halt()
