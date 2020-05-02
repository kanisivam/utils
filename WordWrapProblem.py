import os

index_to_start = 0
output_data = []

def get_input_data(input_file):
    """
    1) get file and do validation
    2) read file and store the words in ds
    """
    all_words = [] # list to allow duplicates so tat can store repeated words also from file.
    if not (os.path.exists(input_file) and os.path.isfile(input_file)):
        print("seems not valid file..process further")
    with open(input_file,'r') as input_data:
        for line in input_data.readlines():
            all_words.extend(line.split())
    return all_words

def write_output(input_file):
    try:
        output_file = input_file.split('.')[0] + '_out'+'.txt'
        with open(output_file, 'w') as out:
            for o in output_data:
                out.write(o+'\n')
    except Exception as e:
        print("Error in writing output file..",e)

def word_wrap(input_data, wrap_count,cur_str):
    global index_to_start
    if len(input_data) <= index_to_start:
        return cur_str
    nxt_str = '-'+input_data[index_to_start+1] if len(input_data) > index_to_start+1 else ''
    index_to_start += 1
    if len(cur_str) + len(nxt_str) <= wrap_count:
        cur_str += nxt_str
        return word_wrap(input_data, wrap_count, cur_str)
    else:
        return cur_str

wrap_count=16
input_file = os.path.join(os.getcwd(), 'wordwrap.txt')
input_data = get_input_data(input_file)
while len(input_data) > index_to_start:
    output_data.append(word_wrap(input_data, wrap_count, input_data[index_to_start]))
if output_data:
    write_output(input_file)
del input_data, output_data