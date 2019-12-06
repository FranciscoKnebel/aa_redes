import socket
import getopt
import sys
import datetime

BUFSIZE = 1455

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
  print('Sending data...')

  data = bytearray(BUFSIZE)
  starttime = datetime.datetime.now()
  with s:
    i = 0

    for i in range(0, 100000):
      i = i + 1
      s.sendall(data)

      delta = datetime.datetime.now() - starttime
      delta = delta.seconds + delta.microseconds / 1000000.0
      print('Throughput (K/s):', round((BUFSIZE*i*0.001) / (delta), 3))
    
    s.close()
    exit_procedure(i, starttime, endtime=datetime.datetime.now())

def exit_procedure(count, starttime, endtime):
  print('Closed connection.')

  print('Bytes transferred: %d' % count)
  delta = endtime - starttime
  delta = delta.seconds + delta.microseconds / 1000000.0
  print('Time used (seconds): %f' % delta)
  print('Averaged speed (MB/s): %f\n\r' % (count / 1024 / 1024 / delta))

main()
