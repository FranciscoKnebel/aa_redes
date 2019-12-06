import socket
import getopt
import sys
import datetime

BUFSIZE = 1455

def main():
    host = ''
    port = ''
    logfile = ''

    try:
      opts, args = getopt.getopt(sys.argv[1:], 'hpno:v', ['help', 'port=', 'host=', 'output='])
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
      elif opt in ('-o', '--output'):
        logfile = arg

    if (port == ''):
      port = 8080

    if (host == ''):
      host = '127.0.0.1'

    if (logfile == ''):
      logfile = 'output.txt'

    connect_to_server(host, port, logfile)


def connect_to_server(HOST, PORT, LOG_NAME):
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

  # Open logfile for writing throughput.
  logfile = open(LOG_NAME, 'w')

  print('Server connection successful.')
  print('Sending data...')
  data = bytearray(BUFSIZE)
  starttime = datetime.datetime.now()
  with s:
    
    i = 0

    for i in range(0, 10000):
      i = i + 1
      s.sendall(data)

      delta = datetime.datetime.now() - starttime
      delta = delta.seconds + delta.microseconds / 1000000.0

      throughput = round((BUFSIZE*i*0.001) / (delta), 3)
      print('Throughput (KB/s):', throughput)

      # Saving throughput to logfile, in bit/s
      logfile.write(i + ': ', throughput * 8, '\n')
    
    s.close()
    exit_procedure(i, starttime, datetime.datetime.now(), logfile)

def exit_procedure(count, starttime, endtime, logfile):
  print('Closed connection.')

  print('Bytes transferred:', count * BUFSIZE)
  delta = endtime - starttime
  delta = delta.seconds + delta.microseconds / 1000000.0
  print('Time used (seconds): %f' % delta)
  print('Averaged speed (MB/s): %f\n\r' % (count * BUFSIZE / 1024 / 1024 / delta))

  logfile.write('\n\nTime used:', delta)
  logfile.write('\nAverage speed:', (count * BUFSIZE * 8)/delta, '\n')
  logfile.close()

main()
