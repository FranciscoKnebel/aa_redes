import socket
import getopt
import sys
import time

def main():
    host = ''
    port = ''

    try:
      opts, args = getopt.getopt(sys.argv[1:], 'hpn:v', ['help', 'port=', 'host='])
    except getopt.GetoptError as err:
      print('client.py <host> -p <port>')
      print(err)
      sys.exit(2)

    for opt, arg in opts:
      if opt in ['-h', '--help']:
        print('client.py -n <host> -p <port>')
        sys.exit(4)
      elif opt in ('-p', '--port'):
        port = arg
      elif opt in ('-n', '--host'):
        host = arg

    if (port == ''):
      port = 8080

    if (host == ''):
      host = '127.0.0.1'

    connect_to_server(host, port)


def connect_to_server(HOST, PORT):
  print('Host: ', HOST)
  print('Port: ', PORT)

  s = None
  for res in socket.getaddrinfo(HOST, PORT, 0, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
      print("Establishing socket...")
      s = socket.socket(af, socktype, proto)
    except OSError as msg:
      s = None
      continue
    try:
      print("Trying to connect to server...")
      s.connect(sa)
    except OSError as msg:
      s.close()
      s = None
      continue
    break

  if s is None:
    print('Could not open socket')
    sys.exit(1)

  print('Server connection successful.')
  print('Starting to send data...')

  data = bytearray(1455)

  with s:
    i = 0

    for i in range(0, 100000):
      i = i + 1
      s.sendall(data)
    
    s.close()

main()