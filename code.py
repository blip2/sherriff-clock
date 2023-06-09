import time
import microcontroller
from screen import Screen

network = None
try:
    from network import Network
    network = Network()
except:
    print("No network available")

screen = Screen()
screen.draw_time()

while True:
    try:
        if network:
            network.server.poll()
        screen.update()
        screen.display.refresh(minimum_frames_per_second=0)

    except Exception as e:
        print("Error:\n", str(e))
        print("Resetting microcontroller in 10 seconds")
        time.sleep(10)
        #microcontroller.reset()
        