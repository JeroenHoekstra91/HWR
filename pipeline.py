import argparse
import matlab.engine

def main():
    f = '/home/mario/Desktop/data'
    t = '/home/mario/Desktop/data/saved'
    print('Starting Matlab...')
    eng = matlab.engine.start_matlab()
    print('Done.')
    eng.pipeline(f, t)


if __name__ == '__main__':
    main()