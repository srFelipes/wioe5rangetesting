import argparse
import json
import pickle as pkl

def raw_msg_to_int(input : str):
    return_int = 0
    for i in range(int(len(input)/2)):
        sub_data = input[i*2:i*2+2]
        try:
            return_int += int(sub_data,base=16)<<i*8
        except:
            return -1
    return return_int


def get_last_data(file):
    """
    return a list of the last data in the file
    """
    output = []
    while True:
        line = file.readline()
        if 'entering continuous RX test mode' in line:
            
            output  = []
        elif 'received the following packet' in line:
            time_of_data = line[:line.find(' [')]
            data_raw = line[line.find('{'):-1]
            data_raw = data_raw.replace('\'','\"')
            data = json.loads(data_raw)
            process_dict = {'time':time_of_data,
                            'id':data['MSG'][:2],
                            'num':raw_msg_to_int(data['MSG'][2:])}
            data.update(process_dict)
            output.append(data)

        elif '' == line:
            return output
        
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