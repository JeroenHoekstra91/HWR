import argparse
import shutil
from transcript import *
import matlab.engine


def main():
    wordNumber = 1
    lineNumber = 1

    parser = argparse.ArgumentParser(description='Transcribes hebrew scripts.')
 
    parser.add_argument('input_dir', type=str, metavar='input',
                    help='path to directory containing the images to be transcribed')

    args = parser.parse_args()

    if os.path.isdir(output_pipeline1):
        shutil.rmtree(output_pipeline1)

    print('Starting Matlab...')
    eng = matlab.engine.start_matlab()
    eng.addpath(eng.genpath('./preprocessing'))
    print('Done.')
    eng.pipeline1(args.input_dir, output_pipeline1, nargout=0)

    if os.path.isdir(output_pipeline2):
        shutil.rmtree(output_pipeline2)
    os.mkdir(output_pipeline2)

    for root, dirs, files in os.walk(output_pipeline1):
        for file in files:
            dir = root.replace("pipeline1-output-wordsegments/","").split('/')[0]

            newWord = False
            newLine = False

            startWord = file.find('Word')
            word = file[startWord+5:].split(".")[0]
            if int(word) > wordNumber:
                newWord = True
                wordNumber = int(word)

            startLine = file.find('Line')
            line = file[startLine+5:].split("_")[0]
            if int(line) > lineNumber:
                newLine = True
                lineNumber = int(line)

            pipeline2(str(root+"/"+file), str(output_pipeline2+dir+".txt"), newWord, newLine)

if __name__ == '__main__':
    main()