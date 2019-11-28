import socket

import getopt
import sys

def main():
    port = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:],"p:v",["port="])
    except getopt.GetoptError as err:
        print('server.py -p <port>')
        print(err)
        sys.exit(2)
        
    for opt, arg in opts:
        if opt == '-h':
            print('server.py -p <port>')
            sys.exit()
        elif opt in ("-p", "--port"):
            port = arg


    if (port == ''):
        port = 8080

    print('Port: ', port)

    start_server(port)


def start_server(PORT):
    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()


main()