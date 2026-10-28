# Helper CLI

Offline CLI study helper tool for AOA, COA and FSJP lab programs and study subjects.

## Installation via npm

Install globally from inside the repository directory:
```bash
npm install -g .
```
*(Or for live development linking: `npm link`)*

---

## How to Get Only Code in the Terminal

To print **purely and strictly the code** (with no headers, notes, or dividers):

```bash
# By experiment number:
helper aoa 1
helper coa 1
helper coa 3
helper fsjp 1

# Or with 'exp' prefix:
helper aoa exp2
helper coa exp3
helper fsjp exp3
helper aoa exp10
```

COA experiments **3, 4, 8, and 9** print their 8086 assembly directly.
FSJP experiments are Java programs; experiments 1-3 are single-file.

### Get only the 8086 assembly code:
```bash
helper asm coa 3
# or:
python helper.py asm coa 3
```

### Save directly into a source file:
```bash
helper aoa 1 > solution.c
helper coa 1 > coa_exp1.c
helper coa 3 > coa_exp3.asm
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
# List all experiments in AOA, COA or FSJP:
helper list aoa
helper list coa
helper list fsjp

# List all subjects:
helper list

# Write directly to default file name:
helper write aoa 1
helper write coa 3
helper write fsjp 1
```

## COA Assembly Programs

COA experiments **3, 4, 8, and 9** are **assembly-only**. The other COA experiments use C.

```bash
# Print the assembly program directly:
python helper.py coa 3

# The asm command also works:
python helper.py asm coa 3

# Save the assembly program (write picks .asm automatically):
python helper.py write coa 3
python helper.py asm coa 3 > coa_exp3.asm

# Copy the assembly program to clipboard:
python helper.py copy coa 3 asm
```

## FSJP (Full Stack Java Programming)

FSJP experiments are stored under the `fsjp` subject. Experiments 1-3 are
single-file Core Java programs. Experiment 4 is a 3-file servlet app
(`index.html`, `GenericServletDemo.java`, `HttpServletDemo.java`), experiment 5
is a 5-file JSP + JDBC app (`userdb.sql`, `login.jsp`, `LoginServlet.java`,
`welcome.jsp`, `error.jsp`), experiment 7 is a 2-file HTML + JavaScript email
validator, and later experiments can contain HTML, CSS, JavaScript, JSP,
servlet, React and Spring Boot files.

```bash
# List FSJP experiments:
python helper.py list fsjp

# Print a single-file experiment:
python helper.py fsjp 1
python helper.py fsjp exp2

# Write it using its correct Java file name:
python helper.py write fsjp 1
# -> Exp1_43.java
```

### Experiments with multiple files

For a multi-file experiment, `show` prints a compact file list instead of
dumping every file into the terminal:

```bash
python helper.py fsjp 4
```

```
Exp 04: Implementing Generic Servlet and HTTP Servlet
3 files

  1. index.html                    HTML            7 lines
  2. GenericServletDemo.java       JAVA           16 lines
  3. HttpServletDemo.java          JAVA           16 lines

Show one file:
  python helper.py show fsjp 4 1
  python helper.py show fsjp 4 index.html

Show all files:
  python helper.py show fsjp 4 all

Write all files to a folder:
  python helper.py write fsjp 4
```

```bash
# Print one file only (pure code, no headers):
python helper.py show fsjp 4 1
python helper.py show fsjp 4 index.html

# Print every file with separators (explicitly):
python helper.py show fsjp 4 all

# Write all files into fsjp_exp_4/:
python helper.py write fsjp 4

# Write them into a folder you choose:
python helper.py write fsjp 4 my_servlet_app

# Copy one file to the clipboard:
python helper.py copy fsjp 4 2
```

`write` preserves subdirectories in file names, so a file named
`WEB-INF/web.xml` is written to `fsjp_exp_4/WEB-INF/web.xml`.

### Servlet compatibility

Experiment 4 uses `@WebServlet` annotations, so it does not need a `web.xml`.
It targets Tomcat 11 (`jakarta.servlet`, Servlet 6.1, Java 17+). Tomcat 10.1
uses the same imports (Servlet 6.0). On Tomcat 9 or older, change the imports
to `javax.servlet` and the annotation import to
`javax.servlet.annotation.WebServlet`.

### Experiment 5 (JSP + JDBC)

Experiment 5 is five files:

```bash
python helper.py fsjp 5
```

```
  1. userdb.sql                       SQL           10 lines
  2. login.jsp                        JSP           10 lines
  3. LoginServlet.java                JAVA          42 lines
  4. welcome.jsp                      JSP            7 lines
  5. error.jsp                        JSP            7 lines
```

`LoginServlet` uses `@WebServlet("/LoginServlet")`, so no `web.xml` is needed.
Deployment layout:

```
webapps\loginapp\login.jsp
webapps\loginapp\welcome.jsp
webapps\loginapp\error.jsp
webapps\loginapp\WEB-INF\classes\com\example\LoginServlet.class
webapps\loginapp\WEB-INF\lib\mysql-connector-j-9.7.0.jar
```

```bash
# 1. create the database
mysql -u root -p < fsjp_exp_5/userdb.sql

# 2. compile the servlet
javac -cp "C:\apache-tomcat-11.0.27\lib\servlet-api.jar" -d WEB-INF\classes LoginServlet.java

# 3. drop the MySQL driver in WEB-INF\lib
```

Replace `your_password` in `LoginServlet.java` with your real MySQL password
before compiling.

### Experiment 7 (email validation)

Experiment 7 is two files and needs no server:

```bash
python helper.py write fsjp 7
# fsjp_exp_7/index.html
# fsjp_exp_7/script.js
```

Open `index.html` in a browser. The script blocks submission, alerts on an
empty field or a missing `@`/`.`, then uses a RegEx to write "Valid Email
Address." (green) or "Invalid Email Address." (red) into `<p id="msg">`.

## Running Without npm

If `npm` or `node` is **not installed** on the computer, you have 3 ready options:

### Option 1: Direct Python (Recommended if Python is installed)
```bash
python helper.py aoa 1
python helper.py coa 1
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
irm https://raw.githubusercontent.com/varun-zero/huehue/main/helper.py -OutFile helper.py; python helper.py coa 1
```

### Run `helper.py` straight from memory (no files saved):
```powershell
irm https://raw.githubusercontent.com/varun-zero/huehue/main/helper.py | python - coa 1
```

### Pure Zero-Install One-Liner (No Node, No Python needed):
```powershell
(irm https://raw.githubusercontent.com/varun-zero/huehue/main/data.json).coa."1".code
```
*(Copy directly to clipboard:)*
```powershell
(irm https://raw.githubusercontent.com/varun-zero/huehue/main/data.json).coa."1".code | Set-Clipboard
```


