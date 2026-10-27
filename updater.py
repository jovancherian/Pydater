import json
import urllib.request
import urllib.error
import shutil
from pathlib import Path
import os
import zipfile
import hashlib
import subprocess
import sys




def update_checker(user_version):
    integer_user_version = user_version.split('.')
    GitHub_API = "https://api.github.com/repos/jovancherian-source/EnDek/releases/latest"
    try:
        request = urllib.request.Request(GitHub_API, headers={"User-Agent": "EnDek"})
        with urllib.request.urlopen(request, timeout=5) as whole_data_json:
            whole_data = json.loads(whole_data_json.read().decode())
        latest_verison = whole_data['tag_name'].strip('v').split('.')
        if latest_verison[0] > integer_user_version[0]:
            return "There is a major new release!!!"
        elif latest_verison[1] > integer_user_version[1]:
            return "you have a minor new release!!"
        elif latest_verison[2] > integer_user_version[2]:
            return "update available!"
        else:
            return("you are up to date!")
    except urllib.error.URLError:
        return("No internet connection. Unable to Check for Updates...")
    except Exception as e:
        print(e)
def intial_update_checker(user_version):
    integer_user_version = user_version.split('.')
    GitHub_API = "https://api.github.com/repos/jovancherian-source/EnDek/releases/latest"
    try:
        request = urllib.request.Request(GitHub_API, headers={"User-Agent": "EnDek"})
        with urllib.request.urlopen(request, timeout=5) as json_whole_data:
            whole_data = json.loads(json_whole_data.read().decode())
        latest_verison = whole_data["tag_name"].strip("v").split(".")
        
        if latest_verison[0] > integer_user_version[0]:
            return "There is a major new release!!!"
        elif latest_verison[1] > integer_user_version[1]:
            return "you have a minor new release!!"
        elif latest_verison[2] > integer_user_version[2]:
            return "update available!"
    except Exception as e:
        pass
def back_up_verifier(EnDek_path, EnDek_backup_path):
    toal_files = 0
    toal_size = 0
    toal_files_1 = 0
    toal_size_1 = 0
    ignored_file = (".git", ".cache", "__pycache__", ".pyc" ,".venv")
    for root, dirs, files in os.walk(EnDek_path):
        dirs[:] = [d for d in dirs if d not in ignored_file]
        for file in files:
            if file not in ignored_file:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                toal_files+= 1
                toal_size+= file_size
    for root, dirs, files in os.walk(EnDek_backup_path):
        dirs[:] = [d for d in dirs if d not in ignored_file]
        for file in files:
            if file not in ignored_file:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                toal_files_1+= 1
                toal_size_1+= file_size
    if toal_files_1 == toal_files and toal_size == toal_size_1:
        return True, toal_files
    else:
        return False
def backup():
    try:
        updater_path =  Path(__file__).resolve()
        Fuctionalities_folder = updater_path.parent
        EnDek_main = Fuctionalities_folder.parent
    except PermissionError:
        print("Insufficient permissions in main folder to install updates")
        return False
    except Exception as e:
        print(f"failed to index file path due to: {e}")
        return False
    if not os.access(EnDek_main, os.W_OK):
        print("Insufficient permissions in main folder to install updates")
        return False
    if Path.exists(EnDek_main.parent/".EnDek_backup_for_update" ):
        shutil.rmtree(EnDek_main.parent/ ".EnDek_backup_for_update")
        print("cleared cache") 
    try:
        above_EnDek_temporary = EnDek_main.parent/ ".EnDek_backup_for_update"
        shutil.copytree(EnDek_main, above_EnDek_temporary, symlinks=True, ignore=shutil.ignore_patterns(".git") )
    except PermissionError:
        print("Insufficient permissions to backup EnDek folder for update")
        return False
    except Exception as e:
        print(f"Error occured while backing up files: {e}")
        return False
    backup_path = EnDek_main.parent/ ".EnDek_backup_for_update"
    verify_status = back_up_verifier(EnDek_path=EnDek_main, EnDek_backup_path=backup_path)
    if verify_status[0]:
        return True
    else:
        backup()
    
def download_update():
    try:
        updater_path =  Path(__file__).resolve()
        Fuctionalities_folder = updater_path.parent
        EnDek_main = Fuctionalities_folder.parent
    except PermissionError:
        print("Insufficient permissions in main folder to install updates")
        return False
    except Exception as e:
        print(f"failed to index file path due to: {e}")
        return False
    try:
        output_file = EnDek_main.parent/ "EnDek_update_file.zip"
        if Path.exists(output_file):
            shutil.rmtree(output_file)
        GitHub_release_API = "https://api.github.com/repos/jovancherian-source/EnDek/releases/latest"
        release_data = urllib.request.Request(GitHub_release_API, headers={"User-Agent": "EnDek"})
        with urllib.request.urlopen(release_data, timeout=5) as json_data:
            data = json.loads(json_data.read().decode())
        latest_verison = data["tag_name"]
        GitHub_API = f"https://github.com/jovancherian-source/EnDek/releases/download/{latest_verison}/{latest_verison.strip("v")}-Update.zip"
        url_data = urllib.request.Request(GitHub_API, headers={"User-Agent" : "EnDek"})
        with urllib.request.urlopen(url_data) as request, open(output_file, "wb") as output:
            output.write(request.read())
        return True
    except urllib.error.URLError:
        return("No internet connection. Unable to Check for Updates...")
    except Exception as e:
        return f"could not download update due to: {e}"

def sha_checker():
    sha = None
    try:
        updater_path =  Path(__file__).resolve()
        Fuctionalities_folder = updater_path.parent
        EnDek_main = Fuctionalities_folder.parent
    except PermissionError:
        print("Insufficient permissions in main folder to install updates")
        return False
    except Exception as e:
        print(f"failed to index file path due to: {e}")
        return False
    GitHub_release_API = "https://api.github.com/repos/jovancherian-source/EnDek/releases/latest"
    try:
        release_data = urllib.request.Request(GitHub_release_API, headers={"User-Agent": "EnDek"})
        with urllib.request.urlopen(release_data, timeout=5) as json_data:
            data = json.loads(json_data.read().decode())
        for asset in data["assets"]:
            if asset["name"].endswith("Update.zip"):
                sha = asset["digest"]
    except Exception as e:
        return f"could not get GitHub SHA-256 due to: {e}"
    try:
        sha_hasher = hashlib.sha256()
        with open(Path(EnDek_main.parent/ "EnDek_update_file.zip"), "rb") as fl:
            for chuck in iter(lambda: fl.read(65536), b""):
                sha_hasher.update(chuck)
            sha_made = sha_hasher.hexdigest()
    except Exception as e:
        return f"could not generate automonous SHA-256 string for verification due to {e}"
    sha_made_gen = f"sha256:{sha_made}"
    if sha == sha_made_gen:
        return True
    elif sha != sha_made_gen:
        return False
def extracter():
    try:
        updater_path =  Path(__file__).resolve()
        Fuctionalities_folder = updater_path.parent
        EnDek_main = Fuctionalities_folder.parent
    except PermissionError:
        print("Insufficient permissions in main folder to install updates")
        return False
    except Exception as e:
        print(f"failed to index file path due to: {e}")
        return False
    try:
        output_file = Path(EnDek_main.parent/ "EnDek_update_file.zip")
        GitHub_release_API = "https://api.github.com/repos/jovancherian-source/EnDek/releases/latest"
        release_data = urllib.request.Request(GitHub_release_API, headers={"User-Agent": "EnDek"})
        with urllib.request.urlopen(release_data, timeout=5) as json_data:
            data = json.loads(json_data.read().decode())
        latest_verison = data["tag_name"]
    except urllib.error.URLError:
        return("No internet connection. Unable to Check for Updates...")
    except Exception as e:
        return f"could not download update due to: {e}"
    if os.path.exists(EnDek_main.parent / "EnDek_update_file.zip"):
        if os.path.exists(Path(EnDek_main.parent/ f"EnDek-{latest_verison}")):
            os.rmdir(Path(EnDek_main.parent/ f"EnDek-{latest_verison}"))
        try:
            with zipfile.ZipFile(EnDek_main.parent/ "EnDek_update_file.zip", "r") as rf:
                rf.extractall(EnDek_main.parent)
                return True
        except PermissionError:
            return("Insufficient permissions in system to install updates")
        except Exception as e:
            return f"could not extract the update zip due to: {e}"
    elif not os.path.exists(Path.joinpath(EnDek_main.parent, "EnDek_update_file.zip")):
        return("Update zip file not found. Please download the update first.")
def installer():
    GitHub_API = "https://api.github.com/repos/jovancherian-source/EnDek/releases/latest"
    try:
        request = urllib.request.Request(GitHub_API, headers={"User-Agent": "EnDek"})
        with urllib.request.urlopen(request, timeout=5) as whole_data_json:
            whole_data = json.loads(whole_data_json.read().decode())
        latest_verison = whole_data['tag_name'].strip('v')
    except Exception as e:
        print(f"could not install update due to{e}")
    try:
        updater_path =  Path(__file__).resolve()
        Fuctionalities_folder = updater_path.parent
        EnDek_main = Fuctionalities_folder.parent
        EnDek_parent = EnDek_main.parent
        installer_path = Path(EnDek_parent/ f"{latest_verison}-Update/installer.py")
    except PermissionError:
        print("Insufficient permissions in main folder to install updates")
        return False
    except Exception as e:
        print(f"failed to index file path due to: {e}")
        return False
    if os.path.exists(Path(EnDek_parent/f"{latest_verison}-Update")):
        subprocess.Popen(
            [sys.executable, str(installer_path), latest_verison ],
            cwd=EnDek_parent, creationflags= subprocess.CREATE_NEW_PROCESS_GROUP
        )
        sys.exit()
    else:
        print("Update file are not available. Please re-run the update.")

def update_now(user_current_version):
    if update_checker(user_version=user_current_version) != "you are up to date!":
        sys.stdout.write("\r[░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]   0.0%")
        sys.stdout.flush()
        if backup() == True :
            sys.stdout.write( "\r[████░░░░░░░░░░░░░░░░░░░░░░░░░░]  14.3%")
            sys.stdout.flush()
            if download_update() == True:
                sys.stdout.write("\r[██████████░░░░░░░░░░░░░░░░░░░░]  35.7%")
                sys.stdout.flush()
                if sha_checker() == True:
                    sys.stdout.write("\r[███████████████████░░░░░░░░░░░]  64.3%")
                    sys.stdout.flush()
                    if extracter() == True:
                        sys.stdout.write("\r[█████████████████████████░░░░░]  85.7%")
                        sys.stdout.flush()
                        installer()
def update_now_overide():
    sys.stdout.write("\r[░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]   0.0%")
    sys.stdout.flush()
    if backup() == True :
        sys.stdout.write( "\r[████░░░░░░░░░░░░░░░░░░░░░░░░░░]  14.3%")
        sys.stdout.flush()
        if download_update() == True:
            sys.stdout.write("\r[██████████░░░░░░░░░░░░░░░░░░░░]  35.7%")
            sys.stdout.flush()
            if sha_checker() == True:
                sys.stdout.write("\r[███████████████████░░░░░░░░░░░]  64.3%")
                sys.stdout.flush()
                if extracter() == True:
                    sys.stdout.write("\r[█████████████████████████░░░░░]  85.7%")
                    sys.stdout.flush()
                    installer()
