#!/usr/bin/python

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib.dates as mdates
import numpy as np
import argparse
import sys
import getopt


def main():
    inputs = []

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'h', ['help'])
    except getopt.GetoptError as err:
        print('generate_graph.py <input_1> (input_2) ... (input_N)')
        print(err)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ['-h', '--help']:
            print('generate_graph.py <input_1> (input_2) ... (input_N)')
            sys.exit(1)

    for arg in args:
        if arg.endswith('.csv'):
            inputs.append(arg)

    generate_graph(inputs)


def generate_graph(inputs):
    n = len(inputs)
    print('Received ' + str(n) + ' input files:')

    if n >= 1:
        print(inputs)
    else:
        print('Terminating...')
        sys.exit(2)

    plt.style.use('seaborn-darkgrid')
    mpl.rcParams['lines.linewidth'] = 2

    fig, ax = plt.subplots()

    for filename in inputs:
      x, y = np.loadtxt(
        open(filename, 'rt').readlines()[:-4],
        delimiter=',',
        dtype={'names': ('date', 'value'),
                'formats': ('datetime64[us]', 'f')},
        converters={0: date2datetime},
        skiprows=1,
        unpack=True
      )
      ax.plot(x, y, label=filename)

    fig.autofmt_xdate()

    plt.xlabel('Time')
    start, end = ax.get_xlim()
    print(start, end)
    # ax.xaxis.set_ticks(np.arange(start, end))

    plt.ylabel('Throughput (bits/s)')

    plt.fmt_xdata = mdates.DateFormatter('%Y-%m-%d %H-%M-%S:%f')
    plt.title('Teste de Equidade de trafego na rede\n Francisco Knebel')
    plt.legend()
    plt.show()


def date2datetime(date):
    return np.datetime64(date, 'us')


main()
