from django.http.response import HttpResponse
import psutil
import subprocess
import re
from django.http import JsonResponse
import json

# TUPLES AND NAMED TUPLES ARE DIFFERENT IDIOT. STOP USING THIS AND MOVE TO NAMEDTUPLE 
def tupleToDict(k , v):
    l = len(k)
    d = {}
    temp = ""
    try:
        for i in range(0 , l):
            d[k[i]] = v[i]
    except:
        print("==" * 50)
        print ("K {0} V {1}" , len(k) , len(v))
        print("Out of range") 
        print(k)
        print(v)
        print("==" * 50)

    return d



class CPU:
    @staticmethod
    def usage():
        return {
            "error" : False,
            "data" : {
                "CPUCount" : psutil.cpu_count(),
                "CPUUtilization" : psutil.cpu_percent(interval=1, percpu=True),
            }
        }

    @staticmethod
    def speed():
        l = []
        speed = psutil.cpu_freq(percpu=True)
        CPUCount = 0
        for item in speed:
            l.append((item[0]))
            #l.append(tupleToDict(["current" , "min" , "max"] , item))
            CPUCount += 1

        return {
            "error" : False,
            "data" : {
                "CPUCount" : CPUCount,
                "speed" : l
            }
        }

    @staticmethod
    def stats():
        return {
            "error" : False,
            "data" : {
                "stats" : list(psutil.cpu_stats()) , #tupleToDict(["ctx_switches" , "interrupts" , "soft_interrupts"] , psutil.cpu_stats()),
                "labels" : ["ctx_switches" , "interrupts" , "soft_interrupts" , "syscalls"]
            }
        }
        

class Memory:
    @staticmethod
    def virtualMemory():
        data = psutil.virtual_memory()
        d = {}
        k = ["total" , "used" , "available"]
        l = list(data)
        return {
            "error" : False,
            "data" : {
                "virtual" : [100 , 100 - ((l[1] / l[0]) * 100) , (l[1] / l[0]) * 100 ],
                "labels" : k
            }
        }
        
    
    @staticmethod
    def swapMemory():
        l = list(psutil.swap_memory())
        return {
            "error" : False,
            "data" : {
                "info" : [100 , 100 - ((l[1] / l[0]) * 100) , (l[1] / l[0]) * 100  , l[3] , l[4] , l[5]],
                "labels" : ["total" , "used" , "free" , "percent" , "sin" , "sout"]
            }
        }



class Disk:
    @staticmethod
    def diskStats():
        data = psutil.disk_io_counters(perdisk=True)
        d = {}
        k = ["read_count" , "write_count" , "read_bytes" , "write_bytes" , "read_time" , "write_time"]
        for key in data:
            l = list(data[key])
            d[key] = {
                "read_write_count" : l[0:2],
                "read_write_bytes" : [l[2]/1000000 , l[3]/1000000]
            }
        
        return {
            "error" : False,
            "data" : d,
            "labels" : k,
        }
        
# memory % , data , name , cpu %
class Process:
    @staticmethod
    def memoryInfo():
        l = ["rss" , "vms" , "shared" , "text" , "lib" , "data" , "dirty" , "uss" , "pss" , "swap"]
        output = []
        item = {}
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            #data = proc.memory_full_info()
            # print("=" * 50)
            # print(data)
            # print("=" * 50)
            item["name"] = proc.name()
            item["CPUPercent"] = proc.cpu_percent(interval=1)
            item["CPUNum"] = proc.cpu_num()
            item["memoryInfo"] = tupleToDict(l , proc.memory_full_info())

            output.append(item)
            
        return {
            "error" : False,
            "data" : output
        }

    
class Application:
    @staticmethod
    def processInfo():
#        labels = ["user",  "pr" , "ni" , "virt" , "res" , "shr" , "s" , "cpu" , "mem" , "time" , "command"]
        labels = ["cpu" , "mem" , "time" , "command"]
        childLabels = []
        data = subprocess.check_output("top n1" , shell=True)
        data = data.decode('utf8', errors='strict').strip()

        paragraph = data.split("\n")
        output = []

        for i, line in enumerate(paragraph):
            i += 1
            if i < 8:
                continue
            
            lineArr = line.split(" ")
            lineHolder = []
            l = len(lineArr)

            for j , word in enumerate(lineArr):
                if(word != "" and j != 0 and j != l - 1):
                    lineHolder.append(word) 
            
            l = len(lineHolder)
            if(l != 0):
                childLabels.append(lineHolder[-1])
                if(l == 12):
                    #output.append(lineHolder[1:])
                    output.append(lineHolder[8:])
                else:
                    #output.append(lineHolder)
                    output.append(lineHolder[8:])
        
     
        i = 0
        cpu = []
        mem = []
        
        for i in range(0 , len(output)):
            cpu.append(output[i][0])
            mem.append(output[i][1])

        return {
            "error" : False,
            "data" : {
                "info" : output,
                "cpu" : cpu,
                "memory" : mem
            },
            "labels" : childLabels
        }



# returns list of list 
#user , PR , NI , VIRT , RES , SHR , S , CPU , MEM , TIME , COMMAND

#print(Application.processInfo())


#print(Disk.diskStats())

def mainFunction(request):
    data = {
        "CPU" : {
            "usage" : CPU.usage(),
            "speed" : "",#CPU.speed(),
            "stats" : CPU.stats()
        },
        "disk" : {
            "stats" : Disk.diskStats()
        },

        "memory" : {
            "swap" : Memory.swapMemory(),
            "virtual" : Memory.virtualMemory()

        },
        "application" : {
            "info" : Application.processInfo()
        }
    }

    return JsonResponse(data)

