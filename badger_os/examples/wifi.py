import badger2040
from badger2040 import WIDTH
import network
import socket
import time
import qrcode
import random


def generate_psk():
    ascii_letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digits = "0123456789"
    return "".join([random.choice(ascii_letters + digits) for _ in range(8)])


def get_wifi_setup_html():
    try:
        with open("/pages/wifi-setup.html", "r") as file:
            html_content = file.read()
        return html_content
    except Exception as e:
        print("Error reading template file:", e)
        return "<html><body><h1>Error loading template</h1></body></html>"


def get_wifi_setup_successful_html():
    try:
        with open("/pages/wifi-setup-successful.html", "r") as file:
            html_content = file.read()
        return html_content
    except Exception as e:
        print("Error reading template file:", e)
        return "<html><body><h1>Error loading template</h1></body></html>"


def generate_qr_credentials(ssid, psk):
    code = qrcode.QRCode()
    code.set_text(f"WIFI:T:WPA;S:{ssid};P:{psk};;")
    return code


def generate_qr_ip(ip):
    code = qrcode.QRCode()
    code.set_text(f"http://{ip}?timestamp={time.time()}")
    return code


def measure_qr_code(size, code):
    w, h = code.get_size()
    module_size = int(size / w)
    return module_size * w, module_size


def draw_qr_code(ox, oy, size, code):
    size, module_size = measure_qr_code(size, code)
    badger.set_pen(15)
    badger.rectangle(ox, oy, size, size)
    badger.set_pen(0)
    for x in range(size):
        for y in range(size):
            if code.get_module(x, y):
                badger.rectangle(
                    ox + x * module_size, oy + y * module_size, module_size, module_size
                )


def draw_view(name, lines, qr=None):
    # Clear to white
    badger.set_pen(15)
    badger.clear()

    badger.set_font("bitmap8")
    badger.set_pen(0)
    badger.rectangle(0, 0, WIDTH, 16)
    badger.set_pen(15)
    badger.text("WiFi", 3, 4, WIDTH, 1)
    badger.text(name, WIDTH - badger.measure_text(name, 0.4) - 4, 4, WIDTH, 1)

    badger.set_pen(0)
    qr_width = 0
    if qr:
        qr_width = 100
        draw_qr_code(10, 30, qr_width, qr)
    for i, line in enumerate(lines):
        badger.text(line, qr_width + 10, 30 + i * 16)
    badger.update()


# WiFi Configuration
SSID = "Badger2040"
PSK = generate_psk()

# Socket Configuration
BUFFER_SIZE = 2048
HTTP_OK_HEADER = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
wifi_setup_html = get_wifi_setup_html()
wifi_setup_successful_html = get_wifi_setup_successful_html()

# States
STATE_INIT = "Init"
STATE_AP = "Access Point"
STATE_AP_OK = "Access Point OK"
STATE_AP_ERROR = "Access Point Error"
STATE_SOCKET_OK = "Socket OK"
STATE_SOCKET_ERROR = "Socket Error"
STATE_CONFIGURED = "Configured"


print("Initialized")
CURRENT_STATE = STATE_INIT

badger2040.system_speed(3)
print("Setting up Badger2040")
badger = badger2040.Badger2040()
badger.led(128)
badger.set_update_speed(2)
draw_view("Initializing", ["Setting up Badger2040..."])

print("Setting up Access Point")
CURRENT_STATE = STATE_AP
draw_view("Access Point", ["Creating Access Point..."])

ap = network.WLAN(network.AP_IF)
# https://docs.micropython.org/en/latest/library/network.WLAN.html
ap.config(essid=SSID, password=PSK, security=2)
ap.active(True)

time.sleep(1)

if ap.active():
    print("Access Point is active")
    print("SSID: ", SSID)
    print("PASS: ", PSK)
    ip = ap.ifconfig()[0]
    print("IP Address: ", ip)
    CURRENT_STATE = STATE_AP_OK
    draw_view(
        "Access Point",
        [f"SSID: {SSID}", f"PASS: {PSK}"],
        generate_qr_credentials(SSID, PSK),
    )
else:
    print("Access Point failed to activate")
    CURRENT_STATE = STATE_AP_ERROR
    draw_view(
        "Access Point", ["Error creating Access Point.", "Close the app and try again."]
    )


if CURRENT_STATE == STATE_AP_OK:
    while len(ap.status("stations")) == 0:
        time.sleep(1)

    print("Device connected")
    draw_view("Connection", ["Establishing connection..."])
    print("Setting up socket")
    try:
        address = (ip, 80)
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        connection.bind(address)
        connection.listen(1)
        print("Socket is set up successfully")
        CURRENT_STATE = STATE_SOCKET_OK
        draw_view("Connection", ["IP: " + ip], generate_qr_ip(ip))

    except Exception as e:
        print("Socket setup failed: ", e)
        CURRENT_STATE = STATE_SOCKET_ERROR
        draw_view(
            "Connection", ["Error setting up socket.", "Close the app and try again."]
        )


while True:
    if CURRENT_STATE == STATE_SOCKET_OK:
        print("Waiting for a connection...")
        clientConnection, clientAddress = connection.accept()
        print(f"Connection from {clientAddress}")

        request_data = b""
        content_length = None

        while True:
            chunk = clientConnection.recv(BUFFER_SIZE)
            if not chunk:
                break
            request_data += chunk
            if b"\r\n\r\n" in request_data:
                headers_part = request_data.split(b"\r\n\r\n")[0]
                if b"Content-Length: " in headers_part:
                    content_length = int(
                        headers_part.split(b"Content-Length: ")[1].split(b"\r\n")[0]
                    )
                    headers_end = headers_part + b"\r\n\r\n"
                    if len(request_data) >= len(headers_end) + content_length:
                        break
                else:
                    # Handle case where Content-Length header is missing
                    break

        # If the request has a body, receive it
        if content_length is not None:
            while len(request_data) < content_length + len(headers_part) + 4:
                chunk = clientConnection.recv(BUFFER_SIZE)
                if not chunk:
                    break
                request_data += chunk

        request = request_data.decode()
        print("Request: ", request)

        if "GET /" in request:
            print("Sending WiFi setup page")
            clientConnection.sendall(HTTP_OK_HEADER.encode() + wifi_setup_html.encode())

        elif "POST /update" in request:
            print("Updating WiFi configuration")
            ssid = request.split("ssid=")[1].split("&")[0]
            print("SSID: ", ssid)
            psk = request.split("psk=")[1].split(" ")[0]
            print("PSK: ", psk)

            print("Sending WiFi setup successful page")
            clientConnection.sendall(
                HTTP_OK_HEADER.encode() + wifi_setup_successful_html.encode()
            )

            with open("WIFI_CONFIG.py", "w") as f:
                f.write(f'SSID = "{ssid}"\n')
                f.write(f'PSK = "{psk}"\n')
                f.write('COUNTRY = "pl"\n')

            CURRENT_STATE = STATE_CONFIGURED

        clientConnection.close()

    elif CURRENT_STATE == STATE_CONFIGURED:
        print("Configuration completed.")
        draw_view("Configured", ["Configuration completed."])
        print("Waiting for 5 seconds before closing the connection")
        time.sleep(5)
        print("Closing connection")
        clientConnection.close()
        print("Closing socket")
        ap.active(False)
        badger.led(0)
        draw_view("Configured", ["You can close the app."])
        break

# Call halt in a loop, on battery this switches off power.
# On USB, the app will exit when A+C is pressed because the launcher picks that up.
while True:
    badger.keepalive()
    badger.halt()
