import subprocess
import time

APP_NAMES = ["Slack", "Google Chrome", "PyCharm", "OrbStack"]


def get_pids(process_name):
    pids = []
    try:
        process = subprocess.Popen(["ps", "aux"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result, error = process.communicate()

        if error:
            print("Error:", error.decode())
            return []

        for line in result.splitlines():
            if process_name in line.decode():
                pid = int(line.split()[1])
                pids.append(pid)
        return pids
    except Exception as e:
        print(f"Execution error: {e}")
        return []
    
    
def start_process(process_name):
    try:
        subprocess.run(["open", '-a', process_name])
        print(f"Process init: {process_name}.")
        time.sleep(0.5)
        if process_name in ['OrbStack', 'Docker Desktop']:
            time.sleep(2.5)
            containers = subprocess.run(["docker", "ps", "-q"], stdout=subprocess.PIPE, text=True)
            containers_ids = containers.stdout.strip()
            if containers_ids:
                subprocess.run(["docker", "stop"] + containers_ids.split())
            print(f"Containers ended.")
    except Exception as e:
        print(f"Execution error: {e}")


def end_process(pids, process_name):
    for pid in pids:
        try:
            subprocess.run(["kill", str(pid)])
            print(f"PID process killed: {pid}({process_name})")
        except Exception as e:
            print(f"Execution error {pid}({process_name}): {e}")


for app_name in APP_NAMES:
    pids_process = get_pids(app_name)
    if not pids_process:
        start_process(app_name)
    else:
        end_process(pids_process, app_name)
