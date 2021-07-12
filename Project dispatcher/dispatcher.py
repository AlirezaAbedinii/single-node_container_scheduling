import time
import threading
import re


def run_command(container_index, container_job):
    global free
    free[container_index] = False
    time.sleep(1)
    print(f'job assigned to container {container_index}')
    free[container_index] = True


def dispatcher():
    while not finished:
        if len(jobs) > 0:
            for i in range(3):
                if free[i] and len(jobs) > 0:
                    threading.Thread(target=run_command, args=(i, jobs.pop(0))).start()
        time.sleep(0.5)


def run_cli():
    global finished
    try:
        threading.Thread(target=dispatcher).start()
    except Exception as e:
        print(e)
        print("Unable to start the dispatcher")
        return

    print('[+] Dispatcher is running')
    print('[+] Please enter your command or enter exit to finish')
    user_input = input()
    while user_input != 'e':
        if re.search("{(<.*>)+}", user_input) is None:
            print("Bad Request")
            return
        mod_input = re.findall("<.*?>", user_input)
        output_part = mod_input[-1][1:-1]
        for i in mod_input[:-1]:
            i = i[1:-1].split(",")

            jobs.append(i.copy() + [output_part])

        user_input = input()
    finished = True
    print(jobs)


# global variables
container_ids = ['a2d636520ea4', 'c0c0b0ac1bd2', 'db3c7b983dc1']
free = [True, True, True]
job_counter = 0
jobs = []
finished = False
run_cli()
