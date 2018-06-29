import argparse
import matlab.engine
from transcript import *

def main():
    parser = argparse.ArgumentParser(description='Transcribes hebrew scripts.')
 
    parser.add_argument('input_dir', type=str, metavar='input',
                    help='path to directory containing the images to be transcribed')

    args = parser.parse_args()

    print('Starting Matlab...')
    eng = matlab.engine.start_matlab()
    eng.addpath(eng.genpath('./preprocessing'))
    print('Done.')
    eng.pipeline1(args.input_dir, output_pipeline1, nargout=0)

    for root, dirs, files in os.walk(output_pipeline1):
        for dir in dirs:
            print dir
            # pipeline2(str(root+"/"+dir+"/"), str(dir+".txt"))

if __name__ == '__main__':
    main()