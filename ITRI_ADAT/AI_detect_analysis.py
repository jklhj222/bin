#!/usr/bin/env python3
import subprocess
import re
from datetime import datetime

def follow_docker_logs(container_id, detect_frames):
    command = ["sudo", "docker", "logs", "-f", container_id]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)

    try:
        idx = 0
        parsing = False
        results_dict = {}
        results_dict_last = {}
        for line in process.stdout:
#            print(parsing, idx)
            if parsing == True and idx <= detect_frames:
                line = re.sub(r'(\w+): ([\w\d_]+)', r'"\1": "\2"', line)
                results = eval(line)
                for result in results:
#                    print('result: ', result)
                    if result['tag'] not in results_dict:
                        results_dict[result['tag']] = [int(result['confidence'])]

                    else:
                        results_dict[result['tag']].append(int(result['confidence']))

                    if idx == detect_frames:
                        if result['tag'] not in results_dict_last:
                            results_dict_last[result['tag']] = [int(result['confidence'])]

                        else:
                            results_dict_last[result['tag']].append(int(result['confidence']))


                parsing = False
                if idx == detect_frames:
                    print(datetime.now())
                    print('Total Results: ')
                    for tag in results_dict:
                        print(tag, ':', results_dict[tag], 'number:', len(results_dict[tag]))
 
                    print('Last Results: ')
                    for tag in results_dict_last:
                        print(tag, ':', results_dict_last[tag], 'number:', len(results_dict_last[tag]))

                    idx = 0
                    results_dict = {}
                    results_dict_last = {}

                    print()

            if '==res==' in line:
                parsing = True
                idx += 1
#                print('idx: ', idx, line, end='')

    except KeyboardInterrupt:
        pass

    finally:
        process.terminate()

if __name__ == "__main__":
    import os

    detect_frames = int(input('Number of detect frames (defualt: 5): ').strip() or '5')

    cmd = "sudo docker container ls -a | grep lim | awk '{print $1}'"
    lim_id = os.popen(cmd).read().rstrip('\n')

    follow_docker_logs(lim_id, detect_frames)
