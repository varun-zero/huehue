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

Experiments with multiple files (Exp 8 and Exp 11):

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
- **Exp 01**: Student class with `inputDetails()` and `displayDetails()`
- **Exp 02**: Constructor Overloading
- **Exp 03**: Method Overloading
- **Exp 04**: Single Inheritance
- **Exp 05**: Multilevel Inheritance
- **Exp 06**: Hierarchical Inheritance
- **Exp 07**: Servlet to display a welcome message (`@WebServlet`, no `web.xml`)
- **Exp 08**: Servlet to accept a name from an HTML form (`index.html`, `HelloServlet.java`)
- **Exp 09**: JSP welcome message (`welcome.jsp`)
- **Exp 10**: JSP to display name, register number and department (`details.jsp`)
- **Exp 11**: JDBC application: insert, update, delete, display (`student.sql`, `StudentJDBC.java`)
- **Exp 12**: Student registration form with CSS
- **Exp 13**: College department webpage
- **Exp 14**: JavaScript email validation
- **Exp 15**: Student registration form validation
- **Exp 16**: DOM: change background color every 5 seconds

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
├── exp-01/
├── exp-02/
└── ...
└── exp-16/
```

Multi-file experiments keep their original filenames inside the corresponding experiment folder.
