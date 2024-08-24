import psutil

def process_status(process_name):
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == process_name:
            return True
    return False
 
# Example
process_name = "sshd"
if process_status(process_name):
    print(f"The process {process_name} is running.")
else:
    print(f"The process {process_name} is not running.")