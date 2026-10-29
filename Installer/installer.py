from pathlib import Path 
import shutil
import json 
import sys
import shutil
project_name = sys.argv[2]
restart_command = sys.argv[3]

current_path = Path(__file__).resolve()
Project_new_main_path = current_path.parent
Project_new_parent = Project_new_main_path.parent
old_project_path = Path(Project_new_parent/ project_name)
json_path = Path(Project_new_main_path/ "status.json")
print("installing updates...")
def status_json_writer(status):
    status_json_file = {
        "status" : status
    }
    with open(json_path, "w") as status_data_json:
        json.dump(status_json_file, status_data_json)
def status_reader():
    try:
        with open(json_path, "r") as status_data_json:
            status = json.load(status_data_json)
            return status["status"]
    except FileNotFoundError:
        status_json_writer("under_installation")
        return "under_installation"
def transfer():
    shutil.copytree(Project_new_main_path, old_project_path, dirs_exist_ok=True, ignore=shutil.ignore_patterns("*.db", "*.json", "__pycache__", ".venv", "installer.py"))
    sys.stdout.write("\r[██████████████████████████████] 100.0%")
    sys.stdout.flush()
    status_json_writer("completed")
    Project_new_main_path.rename(Path(Project_new_parent/ f"{project_name}_update"))
    print(f"completed the update. Please restart to use this latest verison: {restart_command}")
    sys.exit()
transfer()
