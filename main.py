import psutil
import pymongo as mongo
import socket
client = mongo.MongoClient("mongodb://localhost:27017/")
db = client['System_Resource']
collection = db['data']

def convert_to_GB(n):
    value = float(n) / 1073741824
    return round(value,2)

def get_system_info():
    _document = {}
    _document['Hostname'] = socket.gethostname()
    # CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)
    _document['CPU Usage(%)'] = cpu_usage #adding to db

    # Memory Usage
    memory = psutil.virtual_memory()
    ram_usage = memory.percent
    _document['RAM Usage(%)'] = ram_usage #adding to db

    # Disk Space Usage
    disk_usage = psutil.disk_usage('/')
    _document['Disk Space Usage(%)'] = disk_usage.percent
    _document['Total Disk Space(GB)'] = convert_to_GB(disk_usage.total)
    _document['Used Disk Space(GB)'] = convert_to_GB(disk_usage.used)
    _document['Free Disk Space(GB)'] = convert_to_GB(disk_usage.free)

    # Disk I/O
    # disk_io = psutil.disk_io_counters()
    # print(f"Disk Read Count: {disk_io.read_count}, Disk Write Count: {disk_io.write_count}")
    # print(f"Disk Read Bytes: {convert_to_GB(disk_io.read_bytes)}, Disk Write Bytes: {convert_to_GB(disk_io.write_bytes)}")

    # Number of Threads
    total_threads = sum(p.num_threads() for p in psutil.process_iter())
    _document['Total Threads'] = total_threads

    # Number of Processes
    processes = len(psutil.pids())
    _document['Number of Processes'] = processes

    # Open connections
    connections = psutil.net_connections()
    _document['Number of Open Connections'] = len(connections)

    collection.insert_one(_document)

get_system_info()
