import socket
import getopt
import sys
import time

def main():
    host = ''
    port = ''

    try:
      opts, args = getopt.getopt(sys.argv[1:], 'hp:v', ['help', 'port='])
    except getopt.GetoptError as err:
      print('client.py <host> -p <port>')
      print(err)
      sys.exit(2)

    for opt, arg in opts:
      if opt in ['-h', '--help']:
        print('client.py <host> -p <port>')
        sys.exit(4)
      elif opt in ("-p", "--port"):
        port = arg

    if len(args) >= 1:
      host = args[0]
    else:
      print('client.py <host>. Host is needed.')
      sys.exit(3)

    if (port == ''):
      port = 8080

    connect_to_server(host, port)


def connect_to_server(HOST, PORT):
  print('Host: ', HOST)
  print('Port: ', PORT)

  s = None
  for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
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

  data = bytearray(4096)

  with s:
    i = 0

    for i in range(1, 100000):
      i = i + 1
      s.send(data)
    
    s.close()

main()