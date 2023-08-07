"""
utilities
"""
import json

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
        