import threading

from signal import pause
from PIL import Image

import controls
import ksp_client
import vessel_watcher
import actions
import display

if __name__ == "__main__":
    #SECTION - start client and control
    
    controls.setup_controls()
    display.init()
    display.clear_screen()
    
    display.write_screen(Image.open('assets/logo_screen.png').convert('1')) #TODO - Do this in the correct place!
    
    connected = ksp_client.connect()
    if not connected:
        exit(1)
    
    print("Connected to kRPC")
    ksp_client.setup_streams()
    
    #SECTION - Setup Actions
    
    controls.setup_actions(lambda: actions.stage(ksp_client.control, controls.safety_switch))
    
    #SECTION - Start Watcher
    
    threading.Thread(
        target=vessel_watcher.watch_vessel,
        args=(ksp_client.conn, ksp_client.setup_vessel),
        daemon=True
    ).start()
    
    #SECTION - MAIN LOOP
    
    while True:
        print(ksp_client.apoapsis_stream(), ksp_client.periapsis_stream(), ksp_client.altitude_stream())
