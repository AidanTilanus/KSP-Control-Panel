import krpc

from config import NAME, ADDRESS, RPC_PORT, STREAM_PORT

conn = None

vessel = None
control = None

def setup_vessel():
    global vessel, control
    
    vessel = conn.space_center.active_vessel
    control = vessel.control

apoapsis_stream = None
periapsis_stream = None
altitude_stream = None

def setup_streams():
    global vessel, control, apoapsis_stream, periapsis_stream, altitude_stream

    apoapsis_stream = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
    periapsis_stream = conn.add_stream(getattr, vessel.orbit, 'periapsis_altitude')
    altitude_stream = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')


def connect():
    global conn
    
    try:
        conn = krpc.connect(name='RPI2', address=ADDRESS, rpc_port=RPC_PORT, stream_port=STREAM_PORT)
        setup_vessel()
        return True
    except ConnectionRefusedError:
        print("Could not connect to kRPC — is KSP running with the server started?")
        return False
