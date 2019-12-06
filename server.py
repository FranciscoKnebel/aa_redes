import socket
import getopt
import sys

def main():
    port = ''
    try:
      opts, args = getopt.getopt(sys.argv[1:],'hp:v',['help', 'port='])
    except getopt.GetoptError as err:
      print('server.py -p <port>')
      print(err)
      sys.exit(2)
        
    for opt, arg in opts:
      if opt in ('-h', '--help'):
        print('server.py -p <port>')
        sys.exit()
      elif opt in ('-p', '--port'):
        port = arg

    if (port == ''):
      port = 8080

    print('Defined Port:', port)
  
    start_server(port)


def get_host():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  try:
    # doesn't even have to be reachable
    s.connect(('10.255.255.255', 1))
    IP = s.getsockname()[0]
  except:
    IP = '127.0.0.1'
  finally:
    s.close()
  return IP

def start_server(PORT):
  HOSTNAME = get_host()
  CONNECTION_LOCATION = HOSTNAME + ':' + PORT

  print('Starting server on port', PORT)
  print('Host', HOSTNAME)
  print('')

  HOST = None # Symbolic name meaning all available interfaces
  s = None    # socket
  
  for res in socket.getaddrinfo(
    HOST, PORT, socket.AF_UNSPEC,
    socket.SOCK_STREAM, 0, socket.AI_PASSIVE
  ):
    af, socktype, proto, canonname, sa = res
    try:
      s = socket.socket(af, socktype, proto)
    except OSError as msg:
      s = None
      continue
    try:
      s.bind(sa)
      s.listen(1)
    except OSError as msg:
      s.close()
      s = None
      continue
    break

  if s is None:
    print('Could not open socket.')
    sys.exit(1)

  print('Server ready for connections on', CONNECTION_LOCATION)

  conn, addr = s.accept()
  with conn:
    print('Connected by', addr)

    while True:
      data = conn.recv(1024)
    
      if not data:
        break
      conn.send(data)

main()