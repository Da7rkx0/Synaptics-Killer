#!/usr/bin/env python3
# Synaptics Killer Pro v5.0 - Next-Gen Enterprise Defense System
# Developed By Da7rkx0 | GitHub: https://github.com/Da7rkx0

import os
import sys
import time
from colorama import Fore, Back, Style, init
init(autoreset=True)
import psutil
import winreg
import ctypes
import subprocess
import fnmatch
import stat
import threading
from datetime import datetime

# Configuration
VIRUS_NAME = "Synaptics.exe"  
EXCLUSIONS = ["SynapticsKiller.exe"]  
SCAN_INTERVAL = 3  # seconds
LOG_FILE = "C:\\Windows\\Temp\\virus_hunter.log"

# Kill File Patterns (Case-insensitive)
KILL_FILE_PATHS = [
    r"C:\Windows\System32",
    r"C:\Windows\Temp",
    r"C:\ProgramData",
    os.environ['TEMP'],
    os.environ['USERPROFILE'],
    r"C:\Program Files",
    r"C:\Program Files (x86)",
    os.path.join(os.environ['USERPROFILE'], 'Downloads'),
    os.path.join(os.environ['USERPROFILE'], 'Desktop'),
    r"C:\Users\Public",
    r"C:\Windows\Prefetch"
]

# Target Locations
VIRUS_PATHS = [
    r"C:\ProgramData\Synaptics",
    r"C:\Users\All Users\Synaptics",
    os.path.join(os.environ['TEMP'], 'Synaptics')
]

REGISTRY_PATHS = [
    (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
    (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
    (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services")
]

def is_admin():
    """Check for administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def log_message(message):
    """Log activities with timestamp"""
    timestamp = datetime.now().strftime(Fore.CYAN + "%Y-%m-%d %H:%M:%S" + Style.RESET_ALL)
    status = Fore.GREEN + "[+]"  # Default info status
    
    # Determine message type and color coding
    if any(keyword in message for keyword in ["Terminated", "Purged", "Destroyed", "Annihilated"]):
        status = Fore.GREEN + Style.BRIGHT + "[✓]"  # Success
    elif "Failed" in message or "Error" in message:
        status = Fore.RED + Style.BRIGHT + "[✗]"   # Failure
    elif "Skipped" in message:
        status = Fore.YELLOW + Style.BRIGHT + "[!]"  # Warning
    
    # Format output with aligned columns
    formatted_msg = f"{Style.DIM}{timestamp}{Style.RESET_ALL}  {status}  {Fore.WHITE}{message}"
    log_entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n"
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)
    
    # Print only important messages
    if "Protected file bypassed" not in message:
        print(f"{formatted_msg}")

def nuclear_kill(process_name):
    """Terminate process with multiple methods"""
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'].lower() == process_name.lower():
                exe_path = proc.exe()
                try:
                    # Method 1: Standard kill
                    proc.kill()
                except:
                    # Method 2: Taskkill force
                    subprocess.run(f"taskkill /f /im {process_name}", shell=True, check=True)
                finally:
                    # Method 3: Secure file deletion with ownership takeover
                    if os.path.exists(exe_path):
                        try:
                            # Take ownership and set full permissions
                            if os.path.isfile(exe_path):
                                subprocess.run(f'takeown /f "{exe_path}" /A', shell=True, check=True)
                                subprocess.run(f'icacls "{exe_path}" /grant:r *S-1-5-32-544:(F) /Q', shell=True, check=True)
                            elif os.path.isdir(exe_path):
                                subprocess.run(f'takeown /f "{exe_path}" /R /A /D Y', shell=True, check=True)
                                subprocess.run(f'icacls "{exe_path}" /grant:r *S-1-5-32-544:(F) /T /Q', shell=True, check=True)
                            # Nuclear deletion with PowerShell
                            # Ultimate deletion protocol v3
                            try:
                                # Phase 1: Terminate ALL related processes
                                for proc in psutil.process_iter():
                                    try:
                                        if any(exe_path in f.path for f in proc.open_files()):
                                            proc.kill()
                                            time.sleep(0.5)
                                            if proc.is_running():
                                                subprocess.run(f"taskkill /f /pid {proc.pid}", shell=True)
                                    except Exception:
                                        pass
                                
                                # Phase 2: Multiple deletion methods
                                deletion_attempts = [
                                    lambda: os.remove(exe_path),
                                    lambda: subprocess.run(f'del /f /q "{exe_path}"', shell=True),
                                    lambda: subprocess.run(f'rd /s /q "{exe_path}"', shell=True),
                                    lambda: ctypes.windll.kernel32.DeleteFileW(exe_path),
                                    lambda: subprocess.run(
                                        f'powershell "Remove-Item \'{exe_path}\' -Recurse -Force"', 
                                        shell=True
                                    )
                                ]
                                
                                # Phase 3: Attempt all deletion methods
                                max_retries = 10
                                for attempt in range(max_retries):
                                    try:
                                        # Remove attributes and take ownership
                                        subprocess.run(f'attrib -r -h -s "{exe_path}"', shell=True)
                                        subprocess.run(f'takeown /f "{exe_path}" /R /A', shell=True)
                                        subprocess.run(f'icacls "{exe_path}" /grant *S-1-5-32-544:F /T', shell=True)
                                        
                                        # Try all deletion methods
                                        for method in deletion_attempts:
                                            try:
                                                method()
                                                if not os.path.exists(exe_path):
                                                    break
                                            except Exception:
                                                pass
                                        
                                        # Final verification
                                        if os.path.exists(exe_path):
                                            raise RuntimeError("All deletion methods failed")
                                        else:
                                            break
                                            
                                    except Exception as e:
                                        if attempt == max_retries - 1:
                                            # Phase 4: Nuclear options
                                            ctypes.windll.kernel32.MoveFileExW(exe_path, None, 0x4)  # Schedule on reboot
                                            subprocess.run(f'schtasks /Create /TN "Delete_{os.getpid()}" /TR "cmd /c del /f /q \"{exe_path}\"" /SC ONCE /ST 23:59', shell=True)
                                            subprocess.run(f'shutdown /r /t 10 /c "SynapticsKiller强制删除"', shell=True)
                                            log_message("SYSTEM REBOOT INITIATED FOR FINAL DELETION")
                                            sys.exit(0)
                                        time.sleep(3)
                                
                                # Final verification
                                if os.path.exists(exe_path):
                                    log_message(f"ULTIMATE DELETION FAILURE: {exe_path}")
                                    sys.exit(1)
                                    
                            except Exception as e:
                                log_message(f"DELETION APOCALYPSE: {str(e)}")
                                sys.exit(1)
                        except Exception as e:
                            log_message(f"File Deletion Error: {str(e)}")
                log_message(f"Process Terminated: {process_name} (PID: {proc.pid})")
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

def delete_resurrection_paths():
    """Destroy all possible resurrection paths"""
    for path in VIRUS_PATHS:
        try:
            if os.path.exists(path):
                # Take ownership and set full permissions
                # PowerShell directory removal
                ps_script = f"""
                $path = '{path}'
                if (Test-Path $path) {{
                    try {{
                        # Take ownership recursively
                        Take-Ownership -Path $path -Recurse -Force
                        
                        # Remove with retries
                        Remove-Item -LiteralPath $path -Force -Recurse -ErrorAction Stop -Retry 5 -RetryWait 1
                        
                        # Verify deletion
                        if (Test-Path $path) {{
                            throw "Failed to delete directory: $path"
                        }}
                    }} catch {{
                        # Force delete using low-level API
                        Add-Type -TypeDefinition @"
                        using System;
                        using System.IO;
                        using System.Runtime.InteropServices;
                        public static class FileUtils {{
                            [DllImport("kernel32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
                            public static extern bool DeleteFile(string path);
                            
                            [DllImport("kernel32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
                            public static extern bool RemoveDirectory(string path);
                        }}
"@
                        if ([FileUtils]::DeleteFile($path) -or [FileUtils]::RemoveDirectory($path)) {{
                            Write-Host "Deleted using native API: $path"
                        }} else {{
                            throw "Final deletion failed: $path"
                        }}
                    }}
                }}
                """
                subprocess.run(
                    ["powershell", "-Command", ps_script],
                    shell=True,
                    check=True,
                    timeout=30
                )
                log_message(f"Folder Annihilated: {path}")
        except Exception as e:
            log_message(f"Deletion Failed: {str(e)}")

def is_system_file(path):
    """Check if file has system attribute or is in Windows dir"""
    try:
        if os.path.getattr(path).st_file_attributes & stat.FILE_ATTRIBUTE_SYSTEM:
            return True
        if path.lower().startswith(("c:\\windows\\", "c:\\program files\\")):
            return True
        return False
    except:
        return False

def hunt_kill_files():
    """Eradicate kill-related files from system"""
    kill_patterns = []
    protected_paths = [
        r"C:\Windows\System32", 
        r"C:\Program Files",
        r"C:\Program Files (x86)"
    ]
    excluded_files = [
        "taskkill.exe", "tskill.exe", "kill.exe.mui",
        "taskkill.exe.mui", "tskill.exe.mui", "shutdown.exe"
    ]
    
    for root_dir in KILL_FILE_PATHS:
        try:
            for root, _, files in os.walk(root_dir):
                for file in files:
                    file_lower = file.lower()
                    full_path = os.path.join(root, file)
                    
                    # Enhanced safety checks with proper syntax
                    is_protected_path = any(
                        full_path.lower().startswith(p.lower()) 
                        for p in protected_paths
                    )
                    
                    if (is_system_file(full_path) or
                        file_lower in excluded_files or
                        is_protected_path):
                        log_message(f"Protected file bypassed: {full_path}")
                        continue
                        
                    if any(fnmatch.fnmatch(file_lower, p.lower()) for p in kill_patterns):
                        try:
                            # Check if file is in use
                            if not os.access(full_path, os.W_OK):
                                # Force take ownership and set permissions
                                if os.path.exists(full_path):
                                    if os.path.isdir(full_path):
                                        subprocess.run(f'takeown /f "{full_path}" /R /A /D Y', shell=True, check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                                    else:
                                        subprocess.run(f'takeown /f "{full_path}" /A /D Y', shell=True, check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                                else:
                                    log_message(f"Path not found: {full_path}")
                                subprocess.run(f'icacls "{full_path}" /grant:r "%username%":(F) /T /C /Q', shell=True, check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                                subprocess.run(f'attrib -r -h -s "{full_path}"', shell=True, check=True)
                                os.chmod(full_path, stat.S_IWRITE)  # Force writable flag at OS level
                            
                            try:
                                # Force delete with expanded permissions
                                subprocess.run(f'takeown /f "{full_path}" /R /A', shell=True, check=True)
                                subprocess.run(f'icacls "{full_path}" /grant:r "%username%":(F) /T /C /Q', shell=True, check=True)
                                subprocess.run(f'attrib -r -h -s "{full_path}"', shell=True, check=True)
                                
                                # PowerShell nuclear deletion
                                # Hybrid deletion approach
                                deletion_script = f"""
                                $path = '{full_path}'
                                $maxRetries = 5
                                $retryDelay = 1

                                for ($i=0; $i -lt $maxRetries; $i++) {{
                                    try {{
                                        if (Test-Path $path) {{
                                            Remove-Item -LiteralPath $path -Force -Recurse -ErrorAction Stop
                                            Start-Sleep -Seconds $retryDelay
                                            if (Test-Path $path) {{
                                                throw "File still exists after deletion"
                                            }}
                                            break
                                        }}
                                    }} catch {{
                                        if ($i -eq ($maxRetries-1)) {{
                                            [System.IO.File]::Delete($path)
                                            [System.IO.Directory]::Delete($path, $true)
                                            throw
                                        }}
                                        Start-Sleep -Seconds $retryDelay
                                    }}
                                }}
                                """
                                subprocess.run(
                                    ["powershell", "-Command", deletion_script],
                                    shell=True,
                                    check=True,
                                    timeout=20
                                )
                                
                                # Verify deletion
                                if os.path.exists(full_path):
                                    log_message(f"CRITICAL FAILURE: Unable to delete {full_path}")
                            except Exception as e:
                                log_message(f"Advanced Deletion Failed: {str(e)}")
                            log_message(f"Kill File Terminated: {full_path}")
                        except Exception as e:
                            log_message(f"Kill File Termination Failed: {str(e)}")
        except Exception as e:
            log_message(f"Directory Scan Failed: {str(e)}")

def clean_registry():
    """Continuous registry sterilization"""
    for hive, subkey in REGISTRY_PATHS:
        try:
            with winreg.OpenKey(hive, subkey, 0, winreg.KEY_ALL_ACCESS) as key:
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        if "Synaptics" in name or "Synaptics" in value:
                            winreg.DeleteValue(key, name)
                            log_message(f"Registry Purged: {name}")
                        i += 1
                    except OSError:
                        break
        except Exception as e:
            log_message(f"Registry Error: {str(e)}")

def monitor_scheduled_tasks():
    """Hunt scheduled tasks continuously"""
    try:
        tasks = subprocess.check_output(
            ["schtasks", "/query", "/fo", "CSV", "/nh"],
            stderr=subprocess.DEVNULL,
            shell=True
        ).decode('utf-8', errors='ignore')
        
        for task in tasks.split('\r\n'):
            if VIRUS_NAME.lower() in task.lower():
                task_name = task.split(',')[0].strip('"')
                subprocess.run(
                    ["schtasks", "/delete", "/tn", task_name, "/f"],
                    check=True,
                    shell=True
                )
                log_message(f"Task Destroyed: {task_name}")
    except Exception as e:
        log_message(f"Task Error: {str(e)}")

class ProcessWatcher:
    """Real-time process monitoring core"""
    def __init__(self):
        self.active = True
        self.last_scan = time.time()
        
    def start(self):
        """Initialize monitoring systems"""
        threading.Thread(target=self._scan_processes, daemon=True).start()
        threading.Thread(target=self._registry_guard, daemon=True).start()
        
    def _scan_processes(self):
        """Continuous process surveillance"""
        while self.active:
            try:
                current_processes = {p.pid: p.name() for p in psutil.process_iter()}
                if VIRUS_NAME in current_processes.values():
                    nuclear_kill(VIRUS_NAME)
                time.sleep(0.5)
            except Exception as e:
                log_message(f"Process Scan Error: {str(e)}")
                
    def _registry_guard(self):
        """Registry change detection"""
        last_state = {}
        while self.active:
            try:
                current_state = {}
                for hive, subkey in REGISTRY_PATHS:
                    with winreg.OpenKey(hive, subkey) as key:
                        current_state[(hive, subkey)] = winreg.QueryInfoKey(key)[1]
                
                if last_state and current_state != last_state:
                    clean_registry()
                
                last_state = current_state.copy()
                time.sleep(2)
            except Exception as e:
                log_message(f"Registry Guard Error: {str(e)}")

def eternal_hunter():
    """Main hunting loop with enhanced monitoring"""
    # Initialize real-time watchers
    process_watcher = ProcessWatcher()
    process_watcher.start()
    
    log_message("=== Synaptics Killer v6.0 - AI-Powered Defense ===")
    log_message("=== Advanced Threat Elimination Activated ===")
    while True:
        try:
            # Process Termination Protocol
            if nuclear_kill(VIRUS_NAME):
                delete_resurrection_paths()
            
            # File System Cleansing
            hunt_kill_files()
            
            # System Cleansing
            clean_registry()
            monitor_scheduled_tasks()
            
            # Anti-Sleep Mechanism
            time.sleep(SCAN_INTERVAL)
            
        except KeyboardInterrupt:
            log_message("=== Hunter Protocol Disabled ===")
            sys.exit(0)
        except Exception as e:
            log_message(f"Critical Error: {str(e)}")
            time.sleep(10)

if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()
    
    # Display enhanced color banner
    print(Fore.MAGENTA + Style.BRIGHT + r"""
    
  ██████▓██   ██▓ ███▄    █  ▄▄▄       ██▓███  ▄▄▄█████▓ ██▓ ▄████▄    ██████  ██ ▄█▀ ██▓ ██▓     ██▓    ▓█████  ██▀███  
▒██    ▒ ▒██  ██▒ ██ ▀█   █ ▒████▄    ▓██░  ██▒▓  ██▒ ▓▒▓██▒▒██▀ ▀█  ▒██    ▒  ██▄█▒ ▓██▒▓██▒    ▓██▒    ▓█   ▀ ▓██ ▒ ██▒
░ ▓██▄    ▒██ ██░▓██  ▀█ ██▒▒██  ▀█▄  ▓██░ ██▓▒▒ ▓██░ ▒░▒██▒▒▓█    ▄ ░ ▓██▄   ▓███▄░ ▒██▒▒██░    ▒██░    ▒███   ▓██ ░▄█ ▒
  ▒   ██▒ ░ ▐██▓░▓██▒  ▐▌██▒░██▄▄▄▄██ ▒██▄█▓▒ ▒░ ▓██▓ ░ ░██░▒▓▓▄ ▄██▒  ▒   ██▒▓██ █▄ ░██░▒██░    ▒██░    ▒▓█  ▄ ▒██▀▀█▄  
▒██████▒▒ ░ ██▒▓░▒██░   ▓██░ ▓█   ▓██▒▒██▒ ░  ░  ▒██▒ ░ ░██░▒ ▓███▀ ░▒██████▒▒▒██▒ █▄░██░░██████▒░██████▒░▒████▒░██▓ ▒██▒
▒ ▒▓▒ ▒ ░  ██▒▒▒ ░ ▒░   ▒ ▒  ▒▒   ▓▒█░▒▓▒░ ░  ░  ▒ ░░   ░▓  ░ ░▒ ▒  ░▒ ▒▓▒ ▒ ░▒ ▒▒ ▓▒░▓  ░ ▒░▓  ░░ ▒░▓  ░░░ ▒░ ░░ ▒▓ ░▒▓░
░ ░▒  ░ ░▓██ ░▒░ ░ ░░   ░ ▒░  ▒   ▒▒ ░░▒ ░         ░     ▒ ░  ░  ▒   ░ ░▒  ░ ░░ ░▒ ▒░ ▒ ░░ ░ ▒  ░░ ░ ▒  ░ ░ ░  ░  ░▒ ░ ▒░
░  ░  ░  ▒ ▒ ░░     ░   ░ ░   ░   ▒   ░░         ░       ▒ ░░        ░  ░  ░  ░ ░░ ░  ▒ ░  ░ ░     ░ ░      ░     ░░   ░ 
      ░  ░ ░              ░       ░  ░                   ░  ░ ░            ░  ░  ░    ░      ░  ░    ░  ░   ░  ░   ░     
         ░ ░                                                ░                                                            
""" + Fore.CYAN + "ADVANCED EDITION" + Style.RESET_ALL)
    
    print(Fore.BLUE + Style.BRIGHT + """
    ═══════════════════════════════════════════════════
    """ + Style.RESET_ALL)
    
    print(Fore.YELLOW + f"""
    {Fore.GREEN}➤ Version:    {Fore.WHITE}v6.0{Fore.CYAN}  ║  {Fore.GREEN}Developer: {Fore.MAGENTA}Da7rkx0
    {Fore.GREEN}➤ Protection: {Fore.RED}ACTIVE{Fore.CYAN}  ║  {Fore.GREEN}GitHub:    {Fore.BLUE}github.com/Da7rkx0
    {Fore.BLUE}═══════════════════════════════════════════════════
    """ + Style.RESET_ALL)
    
    # Start eternal monitoring
    eternal_hunter()
