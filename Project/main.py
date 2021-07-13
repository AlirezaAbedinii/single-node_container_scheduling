import sys
from tabulate import tabulate
import os
import subprocess

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
    
def compile_python_file(inp):
    try:
        # proc = subprocess.run(inp[:-1], shell=True, capture_output=True, text=True, timeout=5)
        # if proc.returncode != 0:
        #     return
        # return [proc.stdout]

        os.makedirs(os.path.dirname(f'./{inp[-1]}/{inp[0][:-3]}.txt'), exist_ok=True)
        # file = open(inp[0][:-3], "w")
        sys.stdout = open(f'./{inp[-1]}/{inp[0][:-3]}.txt', "w")
        
        
        exec(open(f'{inp[0]}').read())
        sys.stdout.close()
    except Exception as e: #subprocess.TimeoutExpired:
        print(e)
        return ['time out expired']

def compile_cpp_file(inp):
    program_name = inp[0][:-4]
    program_name = program_name.replace('\\', '')
    program_name = program_name.replace('.', '')
    proc = subprocess.run(['gcc', '-o', program_name, inp[0], '-lstdc++', ';', f'./{program_name}'] + inp[1:-1], shell=True, capture_output=True, text=True)
    print(['gcc', '-o', program_name, inp[0], '-lstdc++', ';', f'./{program_name}'] + inp[1:-1])
    if proc.returncode != 0:
        return
    return [proc.stdout]
            
def write_output(file_path, result):
    print(file_path)
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
try:
    desired_func, file_path, output_path = inputs[0], inputs[1], inputs[2]
except:
    desired_func, output_path = inputs[0], inputs[1]

try:
    result = ''
    if desired_func == 'min':
        print('umad')
        result = min(read_file(file_path))
        write_output(f'./{output_path}/{desired_func}.txt', result)
        
    elif desired_func == 'max':
        result = max(read_file(file_path))
        write_output(f'./{output_path}/{desired_func}.txt', result)
        
    elif desired_func == "average":
        result = avg(read_file(file_path))
        write_output(f'./{output_path}/{desired_func}.txt', result)
        
    elif desired_func == "sort":
        result = sort(read_file(file_path))
        write_output(f'./{output_path}/{desired_func}.txt', result)
        
    elif desired_func == "wordcount":
        result = wordcount(read_file(file_path, is_wordcount=True))
        write_output(f'./{output_path}/{desired_func}.txt', result)
    
    elif desired_func.endswith(".py"):
        result = compile_python_file(inputs)
        desired_func = desired_func[:-3]
        output_path = inputs[-1]
    elif desired_func.endswith('.cpp'):
        result = compile_cpp_file(inputs)
        desired_func = desired_func[:-4]
        output_path = inputs[-1]

    # if desired_func in ('min', 'max', 'sort', 'wordcount', 'average'):
        # write_output(f'./{output_path}/{desired_func}.txt', result)
    
    
except Exception as ex:
    print(ex)
    print("bad input")
