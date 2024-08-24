import psutil
import time
import os

def setup(data_dir):
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    global focus_dir
    focus_dir = os.path.join(data_dir, "focus")

    if not os.path.exists(focus_dir):
        os.mkdir(focus_dir)

    print("Setup Check Complete.")

def focus_loop(profile, focus_time):
    start_time = time.time()

    with open(profile, 'r') as file: 
        prevented_process_list = file.readlines()
        prevented_process_list = [line.strip() for line in prevented_process_list]

    while time.time() - start_time < focus_time:
        for prevented_process in prevented_process_list:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] == prevented_process:
                    try:
                        proc.terminate()
                        proc.wait()
                        print(f"{proc.info['name']} has been terminated. FOCUS ON WHAT YOU ARE DOING")
                    except psutil.AccessDenied:
                        print(f"Access denied for {proc.info['name']}, but process was still terminated.")
                    except (psutil.NoSuchProcess, psutil.ZombieProcess):
                        pass

        print(f"Remaining Minutes of Focus: {(focus_time - (time.time() - start_time))/60}")

def start_focus_loop():
    focus_time = 60*10*int(input("How long do you want to Focus? (Multiple of 10 Minutes): "))
    profile = input("What profile do you want to use? (Exact name of txt file, including extension): ")
    profile = os.path.join(focus_dir, profile)
    if not os.path.exists(profile):
        print(f'"{profile}" Profile does not exist, please restart the program enter a proper profile.')
        exit()
    next_thing = input("You can stop Focusing at any time by closing the window.\n Press Enter to continue")

    focus_loop(profile, focus_time)

def run_focus(data_dir):
    setup(data_dir)
    start_focus_loop()

run_focus("app_data")