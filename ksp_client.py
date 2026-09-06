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
eccentricity_stream = None
sem_major_axis_stream = None
body_stream = None

altitude_stream = None

def setup_streams():
    global vessel, control, apoapsis_stream, periapsis_stream, eccentricity_stream, sem_major_axis_stream, body_stream
    global altitude_stream

    apoapsis_stream = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
    apoapsis_stream.rate = 5
    periapsis_stream = conn.add_stream(getattr, vessel.orbit, 'periapsis_altitude')
    periapsis_stream.rate = 5
    eccentricity_stream = conn.add_stream(getattr, vessel.orbit, 'eccentricity')
    eccentricity_stream.rate = 5
    sem_major_axis_stream = conn.add_stream(getattr, vessel.orbit, 'semi_major_axis')
    sem_major_axis_stream.rate = 5
    body_stream = conn.add_stream(getattr, vessel.orbit, 'body')
    body_stream.rate = 0.2
    
    altitude_stream = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
    altitude_stream.rate = 5


def connect():
    global conn
    
    try:
        conn = krpc.connect(name='RPI2', address=ADDRESS, rpc_port=RPC_PORT, stream_port=STREAM_PORT)
        setup_vessel()
        return True
    except Exception as e:
        print("Could not connect to kRPC — is KSP running with the server started?")
        print(e)
        return False
