import time
import threading
import re
import subprocess
import docker


def run_command(container_index, request, job_index):
    global free
    free[container_index] = False
    print(f'[+] job {request} assigned to container {container_index}')
    command = ['docker', 'exec', '-it', container_ids[container_index]]
    command += ['python', 'main.py', request[0].strip(), request[1].strip(), request[2].strip()]
    proc = subprocess.run(command, shell=True,
                          capture_output=True, text=True)
    if proc.stderr:
        print(f'[+] Error: {proc.stderr}')
    request_jobs[job_index] -= 1
    if request_jobs[job_index] == 0:
        print(f'[+] request number {job_index} finished')

    free[container_index] = True
    if request[0].strip().endswith('.py'):
        proc2 = subprocess.run(['echo', 'y', '|', 'docker', 'volume', 'prune'], shell=True, capture_output=True, text=True)
        print(f'[+] container cleaned')


def dispatcher():
    time.sleep(4)
    global job_counter
    while not finished:
        if len(jobs) > 0:
            if not jobs[0][0]:
                jobs.pop(0)

            if len(jobs) > 0:
                requests = jobs[0][0]
                for i in range(3):
                    if free[i] and len(requests) > 0:
                        threading.Thread(target=run_command, args=(i, requests.pop(0), jobs[0][1])).start()
        time.sleep(1)


def run_cli():
    global finished, job_counter
    try:
        threading.Thread(target=dispatcher).start()
    except Exception as e:
        print(e)
        print("Unable to start the dispatcher")
        return

    print('[+] Dispatcher is running')
    print('[+] Please enter your command or enter exit to finish')
    user_input = input()
    user_input = user_input.strip()
    while user_input != 'e':
        request = []
        if re.search("{(<.*>)+}", user_input) is None:
            print("Bad Request")
            return
        mod_input = re.findall("<.*?>", user_input)
        output_part = mod_input[-1][1:-1]
        for i in mod_input[:-1]:
            i = i[1:-1].split(",")

            request.append(i.copy() + [output_part])
        jobs.append([request, job_counter])
        request_jobs[job_counter] = len(request)
        job_counter += 1

        user_input = input()
    print(job_counter)
    finished = True
    print(jobs)


# global variables
container_ids = ['compute-server3', 'compute-server2', 'compute-server1']
free = [True, True, True]
request_jobs = {}
job_counter = 0
jobs = []
finished = False
client = docker.from_env()
run_cli()
