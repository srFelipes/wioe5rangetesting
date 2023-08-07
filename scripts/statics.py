import argparse
import json
import pickle as pkl
from src.utils.utils import *
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script to calculate statics in the data that is in logs",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-p','--path', help='path to file to be processed', metavar='')
    parser.add_argument('-o','--output', help='output name', metavar='')
    args = parser.parse_args()
    if args.path:
        file = open(args.p)
    else:
        file = open('src/logs/info.log','r')
    
    data = get_last_data(file)
    
    if args.output:
        output_file = open(args.o,'wb')
    else:
        output_file = open('output.pkl','wb')
    pkl.dump(data,output_file)

    ids = []
    nums = {}

    for d in data:
        if not d['id'] in ids:
            ids.append(d['id'])
    
    for id in ids:
        nums.update({id:[]}) 

    for d in data:
        nums[d['id']].append(d['num'])

    pkl.dump(nums,output_file)
    file.close()
    output_file.close()