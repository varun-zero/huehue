# Helper CLI

Offline CLI study helper tool for AOA lab C programs and study subjects.

## Installation via npm

Install globally from inside the repository directory:
```bash
npm install -g .
```
*(Or for live development linking: `npm link`)*

---

## How to Get Only Code in the Terminal

To print **purely and strictly the C code** (with no headers, notes, or dividers):

```bash
# By experiment number:
helper aoa 1

# Or with 'exp' prefix:
helper aoa exp2
helper aoa exp10
```

### Save directly into a `.c` file:
```bash
helper aoa 1 > solution.c
```

### Copy directly to clipboard:
```bash
# Built-in command:
helper copy aoa 1

# Or via Windows clip pipe:
helper aoa 1 | clip
```

---

## Other Useful Commands

```bash
# List all experiments in AOA:
helper list aoa

# List all subjects:
helper list

# Write directly to default file name:
helper write aoa 1
```

## Running Without npm

If `npm` or `node` is **not installed** on the computer, you have 3 ready options:

### Option 1: Direct Python (Recommended if Python is installed)
```bash
python helper.py aoa 1
# or: py helper.py aoa 1
```

### Option 2: Windows Batch File (`helper.bat`)
Run directly in CMD or PowerShell:
```cmd
.\helper aoa 1
```

### Option 3: Built-in Windows PowerShell (`helper.ps1` - Zero Installs Required)
Even on a lab PC with no Node and no Python:
```powershell
.\helper.ps1 aoa 1
```

---

## ⚡ Direct 1-Liners on Any Other PC (No npm needed)

If you are on a different computer, run any of these in **PowerShell**:

### Download `helper.py` and run:
```powershell
irm https://raw.githubusercontent.com/varun-zero/huehue/main/helper.py -OutFile helper.py; python helper.py aoa 1
```

### Run `helper.py` straight from memory (no files saved):
```powershell
irm https://raw.githubusercontent.com/varun-zero/huehue/main/helper.py | python - aoa 1
```

### Pure Zero-Install One-Liner (No Node, No Python needed):
```powershell
(irm https://raw.githubusercontent.com/varun-zero/huehue/main/data.json).aoa."1".code
```
*(Copy directly to clipboard:)*
```powershell
(irm https://raw.githubusercontent.com/varun-zero/huehue/main/data.json).aoa."1".code | Set-Clipboard
```


