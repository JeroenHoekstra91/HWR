import argparse
import matlab.engine
from transcript import *

word_segment_images_directory = ""

def main():
    parser = argparse.ArgumentParser(description='Transcribes hebrew scripts.')
 
    parser.add_argument('input_dir', type=str, metavar='input',
                    help='path to directory containing the images to be transcribed')
    parser.add_argument('output_dir', type=str, metavar='output',
                    help='path to directory where the intermediate and final results will be saved')
    
    args = parser.parse_args()

    print('Starting Matlab...')
    eng = matlab.engine.start_matlab()
    eng.addpath(eng.genpath('./preprocessing'))
    print('Done.')
    eng.pipeline1(args.input_dir, args.output_dir, nargout=0)

    pipeline2(args.ouput_dir)

if __name__ == '__main__':
    main()