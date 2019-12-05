import socket
import getopt
import sys

def main():
    host = ''
    port = ''

    try:
      opts, args = getopt.getopt(sys.argv[1:], "hop:v", ["help", "output=", "port="])

      if len(args) >= 1:
        host = args[0]
      else:
        print('client.py <host>. Host is needed.')
        sys.exit(3)
    except getopt.GetoptError as err:
      print('client.py <host> -p <port>')
      print(err)
      sys.exit(2)

    print(args)
    for opt, arg in opts:
      print('opt ', opt)

      if opt in ['-h', '--help']:
        print('client.py <host> -p <port>')
        sys.exit(4)
      elif opt in ("-p", "--port"):
        port = arg

    if (port == ''):
      port = 8080

    # start_server(host, port)


def start_server(HOST, PORT):
  print('Host: ', HOST)
  print('Port: ', PORT)

main()

# import socket
# import sys

# HOST = 'daring.cwi.nl'    # The remote host
# PORT = 50007              # The same port as used by the server
# s = None
# for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
#     af, socktype, proto, canonname, sa = res
#     try:
#         s = socket.socket(af, socktype, proto)
#     except OSError as msg:
#         s = None
#         continue
#     try:
#         s.connect(sa)
#     except OSError as msg:
#         s.close()
#         s = None
#         continue
#     break
# if s is None:
#     print('could not open socket')
#     sys.exit(1)
# with s:
#     s.sendall(b'Hello, world')
#     data = s.recv(1024)
# print('Received', repr(data))