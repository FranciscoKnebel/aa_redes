import socket
import getopt
import sys
import datetime
import select

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
  CONNECTION_LOCATION = HOSTNAME + ':' + str(PORT)

  print('Starting server on port', PORT)
  print('Host', HOSTNAME)
  print('')

  HOST = ''   # Symbolic name meaning all available interfaces
  s = None    # socket
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, int(PORT)))
    s.listen(1)
  except OSError as msg:
    s.close()
    s = None

  if s is None:
    print('Could not open socket.')
    sys.exit(1)

  print('Server ready for connections on', CONNECTION_LOCATION)

  conn, addr = s.accept()
  starttime = datetime.datetime.now()

  with conn:
    print('Connected by', addr)

    connection_flag = 0
    count = 0
    connection_open = True
    while (connection_open):
      data = conn.recv(4096)

      if len(data) == 0:
        connection_flag = connection_flag + 1

        if connection_flag > 5:
          conn.shutdown(2)
          conn.close()
          connection_open = False
      else:
        connection_flag = 0
        count += len(data)
        print(count)
        del data

    endtime = datetime.datetime.now()
    exit_procedure(count, starttime, endtime)

def exit_procedure(count, starttime, endtime):
  print('Closed connection.')

  print('bytes transferred: %d' % count)
  delta = endtime - starttime
  delta = delta.seconds + delta.microseconds / 1000000.0
  print('time used (seconds): %f' % delta)
  print('averaged speed (MB/s): %f\n\r' % (count / 1024 / 1024 / delta))

  sys.exit(0)

main()