from flask import Flask
import shlex
from subprocess import Popen, PIPE
#from concurrent.futures import ThreadPoolExecutor
import threading, time
import sched
# import things
from flask_table import Table, Col
app = Flask(__name__)


file_1 = "/home/user/gpu_status_server/status/gpu_status.txt"
file_2 = "/home/user/gpu_status_server/status/gpu_free_status.txt"

def add_tags(tag, word):
    return "<%s>%s</%s>"%(tag, word, tag)

class ItemTable(Table):
    status = Col('Status')

class Item(object):
    def __init__(self, status):
        self.status = status

def cache_status():
    # generate all gpus info
    start_time = time.time()
    while True:
        print("start to scan gpu status")
        cmd1 = "/home/user/gpu-monitor/gpu_monitor.py -f --server-file /home/user/gpu-monitor/servers.txt"
        #file_1 = "/home/user/gpu_status_server/status/gpu_status.txt"
        get_gpu_status(cmd1, file_1)
    
        cmd2 = "/home/user/gpu-monitor/gpu_monitor.py --server-file /home/user/gpu-monitor/servers.txt"
        #file_2 = "/home/user/gpu_status_server/status/gpu_free_status.txt"
        get_gpu_status(cmd2, file_2)
        time.sleep(60) # every 1 minutes
     
    
def get_gpu_status(cmd, file_name):
    proc = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    
    out, err = proc.communicate()
    #print(out)
    #print(err)
    output = err.decode("utf-8")
    
    output_list = output.split("\n")
    with open(file_name,'w+') as of:
        for item in output_list:
            of.write("%s\n"%item)
    
    #print(output_list)
    #items = []
    #for line in output_list:
    #    items.append(dict(status=line))
    #table = ItemTable(items) 
    
    #print(table.__html__())
    # save result into a file
    #return table.__html__()

    

@app.route("/", methods=['GET'])
def gpu_status():
    print("start to scan gpu status ...")
    #cmd = "/home/user/gpu-monitor/gpu_monitor.py -l --server-file /home/user/gpu-monitor/servers.txt"
    #args = shlex.split(cmd)
    #proc = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    
    #out, err = proc.communicate()
    #print(out)
    #print(err)
    #output = err.decode("utf-8")
    #print(output)
    #message_header = "<html><head>12 Sigma GPU Server Status</head>"
    #message_footer = "</html>"
    #message_body = ""
    #output_list = output.split("\n")
    output_list = []
    with open(file_1, 'r+') as rf:
        for line in rf:
           line = line.strip()
           output_list.append(line)
    print(output_list)
    items = []
    for line in output_list:
        items.append(dict(status=line))
    table = ItemTable(items) 
    
    #print(table.__html__())
    return table.__html__()

@app.route("/Free", methods=['GET'])
def gpu_free_status():
    print("start to scan gpu status ...")
    #cmd = "/home/user/gpu-monitor/gpu_monitor.py --server-file /home/user/gpu-monitor/servers.txt"
    #args = shlex.split(cmd)
    #proc = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    
    #out, err = proc.communicate()
    #print(out)
    #print(err)
    #output = err.decode("utf-8")
    #print(output)
    #message_header = "<html><head>12 Sigma GPU Server Status</head>"
    #message_footer = "</html>"
    #message_body = ""
    #output_list = output.split("\n")
    output_list = []
    with open(file_2, 'r+') as rf:
        for line in rf:
            line = line.strip()
            output_list.append(line)
    print(output_list)
    items = []
    for line in output_list:
        items.append(dict(status=line))
    table = ItemTable(items) 
    
    #print(table.__html__())
    return table.__html__()



if __name__ == '__main__':
    #executor = ThreadPoolExecutor(max_workers=1)
    print("run cache")
    thread = threading.Thread(target=cache_status)
    thread.daemon = True
    thread.start()
    #executor.submit(cache_status, file_list=[file_1, file_2])
    app.run(host="192.168.0.34",threaded=True, debug=False, port=5000)
