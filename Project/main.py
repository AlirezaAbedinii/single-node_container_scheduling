import sys
from tabulate import tabulate
import os

def min(inp):
    mini = inp[0]
    for element in inp:
        if element < mini:
            mini = element
    return [mini]

def max(inp):
    maxi = inp[0]
    for element in inp:
        if element > maxi:
            maxi = element
    return [maxi]

def avg(inp):
    sum = 0.
    count = 0
    for element in inp:
        sum += element
        count += 1
    return [sum/count]
    

def sort(inp):
    return sorted(inp, reverse=True)

def wordcount(inp):
    dictionary = dict()
    for word in inp:
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary[word] = 1
            
    sorted_result = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))
    return sorted_result

def read_file(file_path, is_wordcount = False):
    file = open(file_path, "r")
    result = []
    if not is_wordcount:
        for num in file:
            result.append(int(num))
        file.close()
        return result
    else:
        for word in file:
            word = word.replace('\n', '')
            temp_result = word.split(' ')
            result += temp_result
        file.close()
        return result
            
def write_output(file_path, result):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    file = open(file_path, "w")
    if type(result) == type([]):
        for line in result:
            file.write(str(line)+'\n')
    elif type(result) == type({}):
        table = [[k, v] for k, v in result.items()]
        file.write(tabulate(table, tablefmt="plain"))
    
    file.close()

inputs = sys.argv[1:]
desired_func, file_path, output_path = inputs[0], inputs[1], inputs[2]

try:
    result = ''
    if desired_func == 'min':
        result = min(read_file(file_path))
        
    elif desired_func == 'max':
        result = max(read_file(file_path))
        
    elif desired_func == "average":
        result = avg(read_file(file_path))
        
    elif desired_func == "sort":
        result = sort(read_file(file_path))
        
    elif desired_func == "wordcount":
        result = wordcount(read_file(file_path, is_wordcount=True))

    write_output(f'./{output_path}/{desired_func}.txt', result)
    
    
except Exception as ex:
    print(ex)
    print("bad input")
