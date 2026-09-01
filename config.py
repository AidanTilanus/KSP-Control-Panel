import configparser

_config = configparser.ConfigParser()
_config.read('config.ini')

NAME = _config['krpc']['name']

ADDRESS = _config['krpc']['address']
RPC_PORT = _config['krpc'].getint('rpc_port')
STREAM_PORT = _config['krpc'].getint('stream_port')
