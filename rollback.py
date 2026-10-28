from pathlib import Path
import os
import shutil
restart_commannd = ""
Project_name = ""
Project_verison = "0.0.0"

current_path = Path(__file__).resolve()
Project_path = current_path.parent
Project_parent_path = Project_path.parent
Back_up_path = Project_parent_path / f".{Project_name}_backup_for_update"

user_agrement = input(f"""Are you sure you want to role back to version {Project_verison}.
This version can be later updated to the latest(y/n): """)
if user_agrement.lower() == "y":
    try:
        shutil.copytree(str(Back_up_path), Project_path, dirs_exist_ok=True, ignore=shutil.ignore_patterns("rollback.py"))
        print(f"""completed the rollback. Safe to use and to upgrade to newer versions again.
Restart using: {restart_commannd}""")
    except Exception as e:
        print(f"""Could not roll back due to {e}. Please manually copy the 
old {Project_name} files from {Back_up_path}""")