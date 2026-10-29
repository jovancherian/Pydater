from pathlib import Path
import os
import shutil
def info():
    Project_verison = "0.0.0"
    Project_name = ""
    # Example: EnDek
    return Project_name, Project_verison
def after_update_cleanup(Project_name):
    try:
        updater_path =  Path(__file__).resolve()
        updater_folder = updater_path.parent
        Project_main = updater_folder.parent
    except PermissionError:
        print("Insufficient permissions in main folder to install updates")
        return False
    except Exception as e:
        print(f"failed to index file path due to: {e}")
        return False
    try:
        shutil_zip_path = Path(os.path.join(Project_main.parent, f"{Project_name}_update_file.zip"))
        shutil_backup_path = Path(os.path.join(Project_main.parent,f".{Project_name}_backup_for_update"))
        shutil_zip_path.unlink(missing_ok=True)
        if Path(Project_main.parent/ f"{Project_name}_update").exists():
            shutil.rmtree(Path(Project_main.parent/ f"{Project_name}_update"))
        if shutil_backup_path.exists():
            shutil.rmtree(shutil_backup_path)
        return "cleaned up"
    except Exception as e:
        return f"could not clean up due to {e}."
def startup_check():
    data = info()
    try:
        updater_path =  Path(__file__).resolve()
        updater_folder = updater_path.parent
        Project_main = updater_folder.parent
    except PermissionError:
        print("Insufficient permissions in main folder to install updates")
        return False
    if os.path.exists(Project_main.parent/f"{data[0]}_update"):
        after_update_cleanup(data[0])
        print(f"""You {data[0]} has been updated to the latest version {data[1]}.
And backups have been cleared.""")
    elif os.path.exists(Path(os.path.join(Project_main.parent, f"{data[0]}_update_file.zip"))):
        after_update_cleanup(data[0])
        print(f"""You {data[0]} has been updated to the latest version {data[1]}.
And backups have been cleared.""")
    elif os.path.exists(Path(os.path.join(Project_main.parent,f".{data[0]}_backup_for_update"))):
        after_update_cleanup(data[0])
        print(f"""You {data[0]} has been updated to the latest version {data[1]}.
And backups have been cleared.""")
        return  True
    else:
        return  False