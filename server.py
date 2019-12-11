#!/usr/bin/python

import socket
import getopt
import sys
import datetime

BUFSIZE = 1455

def main():
  port = ''
  logfile = ''
  try:
    opts, args = getopt.getopt(sys.argv[1:],'hp:v',['help', 'port=', 'output='])
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
    elif opt in ('-o', '--output'):
      logfile = arg

  if (port == ''):
    port = 8080

  if (logfile == ''):
    logfile = 'output.txt'

  print('Defined Port:', port)
  start_server(port, logfile)


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

def start_server(PORT, LOG_NAME):
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

  # Open logfile for writing throughput.
  log = open(LOG_NAME, 'w')
  log.write('date,bit/s\n')

  starttime = datetime.datetime.now()

  with conn:
    print('Connected by', addr)

    t1 = datetime.datetime.now()

    # Set starting time of connection
    save_throughput(log, t1, 0)

    connection_flag = 0
    bytes_received = 0
    count = 0
    connection_open = True

    t1 = datetime.datetime.now()
    while (connection_open):
      data = conn.recv(BUFSIZE)

      if len(data) == 0:
        connection_flag = connection_flag + 1

        if connection_flag > 5:
          conn.shutdown(2)
          conn.close()
          connection_open = False
      else:
        connection_flag = 0
        count = count + 1
        bytes_received += len(data)
        del data
        
        t2 = datetime.datetime.now()
        delta = t2 - t1
        delta = delta.seconds + delta.microseconds / 1000000.0
	      
        if (delta >= 0.5):
          throughput = bytes_received * 8 / delta;
          t1 = datetime.datetime.now()

          save_throughput(log, t1, throughput)

          bytes_received = 0
	        

    exit_procedure(count, starttime, datetime.datetime.now(), log)

def save_throughput(log, time, throughput):
  print(str(time) + ':' + str(throughput))
  log.write(str(time) + ',' + str(throughput) + '\n')

def exit_procedure(count, starttime, endtime, logfile):
  print('Closed connection.')

  print('Bytes transferred:', count * BUFSIZE)
  delta = endtime - starttime
  delta = delta.seconds + delta.microseconds / 1000000.0
  print('Time used (seconds): %f' % delta)
  print('Averaged speed (MB/s): %f\n\r' % (count * BUFSIZE / 1024 / 1024 / delta))

  logfile.write('\n\nTime used: ' + str(delta))
  logfile.write('\nAverage speed: ' + str((count * BUFSIZE * 8)/delta) + '\n')
  logfile.close()

  sys.exit(0)

main()
