from pathlib import Path
import os
import shutil
EnDek_verison = "2.7.5"
current_path = Path(__file__).resolve()
EnDek_path = current_path.parent
EnDek_parent_path = EnDek_path.parent
Back_up_path = EnDek_parent_path / ".EnDek_backup_for_update"

user_agrement = input(f"""Are you sure you want to role back to version {EnDek_verison}.
This version can be later updated to the latest(y/n): """)
if user_agrement.lower() == "y":
    try:
        shutil.copytree(str(Back_up_path), EnDek_path, dirs_exist_ok=True, ignore=shutil.ignore_patterns("rollback.py"))
        print("""completed the rollback. Safe to use and to upgrade to newer versions again.
Restart using: python Encrypter.py""")
    except Exception as e:
        print(f"""Could not roll back due to {e}. Please manually copy the 
old EnDek files from {Back_up_path}""")