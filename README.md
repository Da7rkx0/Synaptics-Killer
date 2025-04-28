# Synaptics Killer Pro - Advanced Malware Defense System

![Synaptics Killer Banner](https://placehold.co/800x200/000000/FFFFFF/png?text=Synaptics+Killer+Pro%0ANext-Gen+Enterprise+Defense+System&font=roboto)

#  Video
[video](https://github.com/user-attachments/assets/eee59b97-3e0b-4f7b-8ad5-1477e8799a89)
An enterprise-grade solution for detecting and eradicating Synaptics malware with advanced resurrection prevention mechanisms

## Key Features
- ✅ Real-time process monitoring  
- ☢️ Comprehensive file eradication  
- 🔒 Registry protection  
- 📊 Scheduled tasks analysis  
- 🛡️ Advanced file deletion techniques  
- 📈 Detailed logging system

## How It Works
```mermaid
graph TD
    A[Start] --> B{Admin Rights?}
    B -- Yes --> C[Activate Monitoring]
    B -- No --> D[Request UAC Elevation]
    D --> C
    C --> E[Scan Running Processes]
    E --> F{Found Synaptics.exe?}
    F -- Yes --> G[Terminate Process]
    F -- No --> H[Periodic Scanning]
    G --> I[Delete Associated Files]
    I --> J[Clean Registry Entries]
    J --> K[Check Scheduled Tasks]
    K --> L{Found Suspicious Tasks?}
    L -- Yes --> M[Delete Tasks Immediately]
    L -- No --> H
    H --> E
```

## Installation
```bash
# Install required libraries
pip install -r requirements.txt
```

## Required Libraries
- `psutil` - Process monitoring  
- `colorama` - Console coloring  
- `winreg` - Windows registry access  
- `ctypes` - System-level operations

## Usage
```bash
# Run directly from source
python SynapticsKiller.py

# Compile to EXE (requires pyinstaller)
pip install pyinstaller
pyinstaller --onefile  SynapticsKiller.py

# The compiled EXE will be in dist/ folder
# Note: Run compiled EXE as Administrator
dist\SynapticsKiller.exe
```

## Technical Specifications
- Multi-phase deletion protocols
- File ownership takeover
- PowerShell-enhanced removal
- Registry sterilization
- Real-time process watcher
- Automatic UAC elevation

## License
MIT License - [Da7rkx0](https://github.com/Da7rkx0)
