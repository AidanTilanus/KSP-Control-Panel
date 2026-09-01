import krpc

from time import sleep

def watch_vessel(conn, refresh_vessel, get_vessel):
    last_name = None
    while True:
        try:
            current = conn.space_center.active_vessel
            if current.name != last_name:
                refresh_vessel()
                last_name = current.name
                print('Vessel switched, refreshed')
        except krpc.error.RPCError:
            pass
        sleep(1)
        