import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse
import sys
import getopt

def main():
  inputfile = ''

  try:
    opts, args = getopt.getopt(sys.argv[1:], 'hi:v', ['help', 'input='])
  except getopt.GetoptError as err:
    print('generate_graph.py -i <input>')
    print(err)
    sys.exit(2)

  for opt, arg in opts:
    if opt in ['-h', '--help']:
      print('generate_graph.py -i <input>')
      sys.exit(4)
    elif opt in ('-i', '--input'):
      inputfile = arg

  generate_graph(inputfile)

def generate_graph(inputfile):
  print('Input', inputfile)





main()