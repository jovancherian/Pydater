# Pydater

A Python updater for projects distributed through **GitHub Releases**. Pydater downloads new releases, replaces outdated project files, and provides backup and rollback mechanisms to help protect users during updates.

## 1. What is Pydater?

Pydater lets users update their local copy of your Python project whenever a new release is available on GitHub. It downloads the release, installs the updated files, and handles cleanup after a successful update.

## 2. Is it for you?

Pydater is ideal if you:

- Build applications using Python.
- Distribute your software through GitHub Releases.
- Want a straightforward updater with backup and rollback support.

Integrate it from day one to make shipping updates easier as your project grows.

## 3. Main Features

- **Automatic backups:** Backs up existing project files before updating and verifies the backup before proceeding.
- **Safe downloads:** Downloads release assets and verifies their integrity using SHA-512.
- **Automatic rollback:** Restores the previous version if an update fails.
- **Automatic cleanup:** Removes temporary update files and backups after a successful update.
- **Force updates:** Reinstalls the current release when needed.

## 4. How to Use

1. **Clone the repository** using HTTPS, SSH, or GitHub CLI.
2. **Copy the `updater` folder** into your Python project's root directory.
3. **Configure `updater.py`:** Fill in the project name, current version, GitHub release API URL, repository URL, and restart command in the `info()` function. Keep the configuration consistent across the relevant Pydater files.
4. **Configure `initial_checker.py`:** Add the same project information. This file checks whether an update succeeded after restarting and handles post-update cleanup.
5. **Connect the functions** to your application's CLI or UI so users can trigger updates.
6. **Prepare your release asset:**
   - Copy the `installer` folder outside your project directory.
   - Download your project's source code for the release and extract it.
   - Move the actual project files from GitHub's nested source directory into the extracted root.
   - Remove the bundled `rollback.py` to avoid overwriting your configured rollback module.
   - Copy the installer files into the extracted project root.
   - Zip the prepared files and name the archive `{project_name}-Update.zip`. Replace {project_name} with your real project name given in the info fuction.
   - Upload the ZIP as an asset to your GitHub Release.

**Important:** Follow the file structure expected by the installer and ensure the configuration matches your project before publishing a release.

## 5. Functions

### `info()`

Defines the configuration required by Pydater.

```python
def info():
    Current_version = "0.0.0"
    Project_name = ""

    # Example: EnDek
    Github_Release_API = ""
    # https://api.github.com/repos/OWNER/REPO/releases/latest

    Github_Https = ""
    # https://github.com/OWNER/REPO/

    Reset_command = ""
    # Example: python Encrypter.py
```

Replace the example values with your project's details.

### `update()`

Checks for a newer release and updates the project if one is available. Takes no arguments when the configuration is provided.

### `force_update()`

Reinstalls the current release regardless of whether a newer version is available. Useful for recovering from persistent bugs or replacing corrupted project files.

### `startup_check()`

Checks the result of an update when the application starts. Reports whether the update succeeded and cleans up update-related files after success. This is optional.

Import the functions into your application and connect them to your CLI or UI:

```python
from updater import update, force_update
from initial_checker import startup_check
```

Call `startup_check()` during application startup if you want post-update verification and cleanup.

---

This README is AI or SI generated.

**Pydater — Simplifying Python application updates through GitHub Releases.**
