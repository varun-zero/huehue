# Helper CLI -- Full Stack Java Programming (FSJP)

Offline CLI study helper tool for Full Stack Java Programming (FSJP) lab programs (Q1 to Q16).

Servlets use `@WebServlet` annotation (Servlet 3.0+), so no `web.xml` is needed.
All code blocks are clean with zero unnecessary comments.

---

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
# Using python:
python helper.py 6
python helper.py fsjp 6

# Using npm CLI:
helper 6
helper fsjp 6

# Using PowerShell:
.\helper.ps1 6
.\helper.ps1 fsjp 6
```

---

## Multi-File Experiments

Experiments with multiple files (Q8 and Q11):

```bash
# View list of files in experiment:
python helper.py fsjp 8

# View a specific file (1-based index or filename):
python helper.py fsjp 8 1
python helper.py fsjp 8 2
python helper.py fsjp 8 index.html
python helper.py fsjp 8 HelloServlet.java

# View all files together:
python helper.py fsjp 8 all
```

---

## List All Experiments

```bash
python helper.py list
helper list
.\helper.ps1 list
```

### Experiments Overview:
- **Q1**: Student Class (inputDetails / displayDetails)
- **Q2**: Constructor Overloading
- **Q3**: Method Overloading
- **Q4**: Single Inheritance
- **Q5**: Multilevel Inheritance
- **Q6**: Hierarchical Inheritance
- **Q7**: Servlet Welcome Message
- **Q8**: Servlet Form Input (Name Display)
- **Q9**: JSP Welcome Message
- **Q10**: JSP Student Details (Name, Reg No, Department)
- **Q11**: JDBC Student Records (Insert, Update, Delete, Display)
- **Q12**: Student Registration Form with CSS
- **Q13**: College Department Webpage
- **Q14**: JavaScript Email Validation
- **Q15**: Student Registration Form Validation (HTML + JavaScript)
- **Q16**: DOM Background Color Change Every 5 Seconds

---

## Save Directly into a Source File

```bash
# Using write command:
python helper.py write fsjp 6
python helper.py write fsjp 8

# Or redirecting standard output:
python helper.py 6 > HierarchicalInheritance.java
```

---

## Copy Directly to Clipboard

```bash
# Built-in copy command:
python helper.py copy fsjp 6
helper copy fsjp 6

# Or piping to Windows clip:
python helper.py 6 | clip
```

## Code Files

All FSJP source files are also available as separate files under [`fsjp-codes/`](fsjp-codes/), organized by experiment:

```text
fsjp-codes/
├── q01-student-class/
├── q02-constructor-overloading/
└── ...
└── q16-dom-background-color-change/
```

Multi-file experiments keep their original filenames inside the corresponding experiment folder.
