#!/usr/bin/env python3
"""
helper.py -- Offline CLI study helper tool for Full Stack Java Programming (FSJP).

Usage:
  python helper.py fsjp <exp_num> [file|all]
  python helper.py <exp_num> [file|all]
  python helper.py list
  python helper.py show  [subject] <topic_num> [file|all]
  python helper.py write [subject] <topic_num> [filename|folder]
  python helper.py copy  [subject] <topic_num> [file|all]

For FSJP experiments (Q1 to Q16), you can specify '1', 'exp1', or 'exp 1'.
"""

import sys
import os
import re
import json
import subprocess
import socket
import glob

# -----------------------------------------------------------------------------
#  DATA -- Loaded dynamically from data.json with embedded fallback
# -----------------------------------------------------------------------------

_EMBEDDED_SUBJECTS = json.loads("{\"fsjp\": {\"1\": {\"title\": \"Exp 01: Student class with inputDetails() and displayDetails()\", \"notes\": \"\", \"filename\": \"Student.java\", \"language\": \"java\", \"code\": \"import java.util.Scanner;\\n\\nclass Student {\\n    String name;\\n    int rollNumber;\\n    float marks;\\n\\n    void inputDetails() {\\n        Scanner sc = new Scanner(System.in);\\n        System.out.print(\\\"Enter name: \\\");\\n        name = sc.nextLine();\\n        System.out.print(\\\"Enter roll number: \\\");\\n        rollNumber = sc.nextInt();\\n        System.out.print(\\\"Enter marks: \\\");\\n        marks = sc.nextFloat();\\n    }\\n\\n    void displayDetails() {\\n        System.out.println(\\\"Name: \\\" + name + \\\", Roll: \\\" + rollNumber + \\\", Marks: \\\" + marks);\\n    }\\n\\n    public static void main(String[] args) {\\n        Student s = new Student();\\n        s.inputDetails();\\n        s.displayDetails();\\n    }\\n}\", \"files\": [{\"name\": \"Student.java\", \"language\": \"java\", \"code\": \"import java.util.Scanner;\\n\\nclass Student {\\n    String name;\\n    int rollNumber;\\n    float marks;\\n\\n    void inputDetails() {\\n        Scanner sc = new Scanner(System.in);\\n        System.out.print(\\\"Enter name: \\\");\\n        name = sc.nextLine();\\n        System.out.print(\\\"Enter roll number: \\\");\\n        rollNumber = sc.nextInt();\\n        System.out.print(\\\"Enter marks: \\\");\\n        marks = sc.nextFloat();\\n    }\\n\\n    void displayDetails() {\\n        System.out.println(\\\"Name: \\\" + name + \\\", Roll: \\\" + rollNumber + \\\", Marks: \\\" + marks);\\n    }\\n\\n    public static void main(String[] args) {\\n        Student s = new Student();\\n        s.inputDetails();\\n        s.displayDetails();\\n    }\\n}\"}]}, \"2\": {\"title\": \"Exp 02: Constructor Overloading\", \"notes\": \"\", \"filename\": \"Calculator.java\", \"language\": \"java\", \"code\": \"class Calculator {\\n    Calculator() {\\n        System.out.println(\\\"Welcome to Calculator!\\\");\\n    }\\n\\n    Calculator(int a, int b) {\\n        System.out.println(\\\"Sum = \\\" + (a + b));\\n    }\\n\\n    public static void main(String[] args) {\\n        new Calculator();\\n        new Calculator(10, 20);\\n    }\\n}\", \"files\": [{\"name\": \"Calculator.java\", \"language\": \"java\", \"code\": \"class Calculator {\\n    Calculator() {\\n        System.out.println(\\\"Welcome to Calculator!\\\");\\n    }\\n\\n    Calculator(int a, int b) {\\n        System.out.println(\\\"Sum = \\\" + (a + b));\\n    }\\n\\n    public static void main(String[] args) {\\n        new Calculator();\\n        new Calculator(10, 20);\\n    }\\n}\"}]}, \"3\": {\"title\": \"Exp 03: Method Overloading\", \"notes\": \"\", \"filename\": \"Calculator.java\", \"language\": \"java\", \"code\": \"class Calculator {\\n    int add() { return 5 + 10; }\\n    int add(int a, int b) { return a + b; }\\n    float add(float a, float b, float c) { return a + b + c; }\\n\\n    public static void main(String[] args) {\\n        Calculator c = new Calculator();\\n        System.out.println(\\\"No parameters: \\\" + c.add());\\n        System.out.println(\\\"Two integers: \\\" + c.add(20, 30));\\n        System.out.println(\\\"Three floats: \\\" + c.add(1.5f, 2.5f, 3.5f));\\n    }\\n}\", \"files\": [{\"name\": \"Calculator.java\", \"language\": \"java\", \"code\": \"class Calculator {\\n    int add() { return 5 + 10; }\\n    int add(int a, int b) { return a + b; }\\n    float add(float a, float b, float c) { return a + b + c; }\\n\\n    public static void main(String[] args) {\\n        Calculator c = new Calculator();\\n        System.out.println(\\\"No parameters: \\\" + c.add());\\n        System.out.println(\\\"Two integers: \\\" + c.add(20, 30));\\n        System.out.println(\\\"Three floats: \\\" + c.add(1.5f, 2.5f, 3.5f));\\n    }\\n}\"}]}, \"4\": {\"title\": \"Exp 04: Single Inheritance\", \"notes\": \"\", \"filename\": \"SingleInheritance.java\", \"language\": \"java\", \"code\": \"class Person {\\n    String name = \\\"Varun\\\";\\n    int age = 20;\\n}\\n\\nclass Student extends Person {\\n    String course = \\\"B.Tech\\\";\\n    int roll = 101;\\n\\n    public static void main(String[] args) {\\n        Student s = new Student();\\n        System.out.println(\\\"Name: \\\" + s.name + \\\", Age: \\\" + s.age);\\n        System.out.println(\\\"Course: \\\" + s.course + \\\", Roll: \\\" + s.roll);\\n    }\\n}\", \"files\": [{\"name\": \"SingleInheritance.java\", \"language\": \"java\", \"code\": \"class Person {\\n    String name = \\\"Varun\\\";\\n    int age = 20;\\n}\\n\\nclass Student extends Person {\\n    String course = \\\"B.Tech\\\";\\n    int roll = 101;\\n\\n    public static void main(String[] args) {\\n        Student s = new Student();\\n        System.out.println(\\\"Name: \\\" + s.name + \\\", Age: \\\" + s.age);\\n        System.out.println(\\\"Course: \\\" + s.course + \\\", Roll: \\\" + s.roll);\\n    }\\n}\"}]}, \"5\": {\"title\": \"Exp 05: Multilevel Inheritance\", \"notes\": \"\", \"filename\": \"MultilevelInheritance.java\", \"language\": \"java\", \"code\": \"class Person {\\n    String name = \\\"Varun\\\";\\n}\\n\\nclass Student extends Person {\\n    String course = \\\"B.Tech\\\";\\n}\\n\\nclass GraduateStudent extends Student {\\n    int year = 2026;\\n\\n    public static void main(String[] args) {\\n        GraduateStudent g = new GraduateStudent();\\n        System.out.println(\\\"Name: \\\" + g.name);\\n        System.out.println(\\\"Course: \\\" + g.course);\\n        System.out.println(\\\"Graduation Year: \\\" + g.year);\\n    }\\n}\", \"files\": [{\"name\": \"MultilevelInheritance.java\", \"language\": \"java\", \"code\": \"class Person {\\n    String name = \\\"Varun\\\";\\n}\\n\\nclass Student extends Person {\\n    String course = \\\"B.Tech\\\";\\n}\\n\\nclass GraduateStudent extends Student {\\n    int year = 2026;\\n\\n    public static void main(String[] args) {\\n        GraduateStudent g = new GraduateStudent();\\n        System.out.println(\\\"Name: \\\" + g.name);\\n        System.out.println(\\\"Course: \\\" + g.course);\\n        System.out.println(\\\"Graduation Year: \\\" + g.year);\\n    }\\n}\"}]}, \"6\": {\"title\": \"Exp 06: Hierarchical Inheritance\", \"notes\": \"\", \"filename\": \"HierarchicalInheritance.java\", \"language\": \"java\", \"code\": \"class Person {\\n    String college = \\\"ABC College\\\";\\n}\\n\\nclass Student extends Person {\\n    String course = \\\"B.Tech\\\";\\n}\\n\\nclass Teacher extends Person {\\n    String subject = \\\"Java\\\";\\n}\\n\\nclass Administrator extends Person {\\n    String dept = \\\"Admissions\\\";\\n}\\n\\npublic class HierarchicalInheritance {\\n    public static void main(String[] args) {\\n        Student s = new Student();\\n        Teacher t = new Teacher();\\n        Administrator a = new Administrator();\\n        System.out.println(\\\"Student: \\\" + s.course + \\\" (\\\" + s.college + \\\")\\\");\\n        System.out.println(\\\"Teacher: \\\" + t.subject + \\\" (\\\" + t.college + \\\")\\\");\\n        System.out.println(\\\"Administrator: \\\" + a.dept + \\\" (\\\" + a.college + \\\")\\\");\\n    }\\n}\", \"files\": [{\"name\": \"HierarchicalInheritance.java\", \"language\": \"java\", \"code\": \"class Person {\\n    String college = \\\"ABC College\\\";\\n}\\n\\nclass Student extends Person {\\n    String course = \\\"B.Tech\\\";\\n}\\n\\nclass Teacher extends Person {\\n    String subject = \\\"Java\\\";\\n}\\n\\nclass Administrator extends Person {\\n    String dept = \\\"Admissions\\\";\\n}\\n\\npublic class HierarchicalInheritance {\\n    public static void main(String[] args) {\\n        Student s = new Student();\\n        Teacher t = new Teacher();\\n        Administrator a = new Administrator();\\n        System.out.println(\\\"Student: \\\" + s.course + \\\" (\\\" + s.college + \\\")\\\");\\n        System.out.println(\\\"Teacher: \\\" + t.subject + \\\" (\\\" + t.college + \\\")\\\");\\n        System.out.println(\\\"Administrator: \\\" + a.dept + \\\" (\\\" + a.college + \\\")\\\");\\n    }\\n}\"}]}, \"7\": {\"title\": \"Exp 07: Servlet to display a welcome message (no web.xml)\", \"notes\": \"Run at: http://localhost:8080/YourProject/welcome (For Tomcat 10+, use jakarta.servlet instead of javax.servlet)\", \"filename\": \"WelcomeServlet.java\", \"language\": \"java\", \"code\": \"import java.io.*;\\nimport javax.servlet.annotation.WebServlet;\\nimport javax.servlet.http.*;\\n\\n@WebServlet(\\\"/welcome\\\")\\npublic class WelcomeServlet extends HttpServlet {\\n    protected void doGet(HttpServletRequest req, HttpServletResponse res) throws IOException {\\n        res.setContentType(\\\"text/html\\\");\\n        res.getWriter().println(\\\"<h1>Welcome to Servlet Programming!</h1>\\\");\\n    }\\n}\", \"files\": [{\"name\": \"WelcomeServlet.java\", \"language\": \"java\", \"code\": \"import java.io.*;\\nimport javax.servlet.annotation.WebServlet;\\nimport javax.servlet.http.*;\\n\\n@WebServlet(\\\"/welcome\\\")\\npublic class WelcomeServlet extends HttpServlet {\\n    protected void doGet(HttpServletRequest req, HttpServletResponse res) throws IOException {\\n        res.setContentType(\\\"text/html\\\");\\n        res.getWriter().println(\\\"<h1>Welcome to Servlet Programming!</h1>\\\");\\n    }\\n}\"}]}, \"8\": {\"title\": \"Exp 08: Servlet to accept a name from an HTML form (no web.xml)\", \"notes\": \"\", \"files\": [{\"name\": \"index.html\", \"language\": \"html\", \"code\": \"<form action=\\\"hello\\\" method=\\\"post\\\">\\n    Enter your name: <input type=\\\"text\\\" name=\\\"username\\\">\\n    <input type=\\\"submit\\\" value=\\\"Submit\\\">\\n</form>\"}, {\"name\": \"HelloServlet.java\", \"language\": \"java\", \"code\": \"import java.io.*;\\nimport javax.servlet.annotation.WebServlet;\\nimport javax.servlet.http.*;\\n\\n@WebServlet(\\\"/hello\\\")\\npublic class HelloServlet extends HttpServlet {\\n    protected void doPost(HttpServletRequest req, HttpServletResponse res) throws IOException {\\n        res.setContentType(\\\"text/html\\\");\\n        res.getWriter().println(\\\"<h2>Hello, \\\" + req.getParameter(\\\"username\\\") + \\\"!</h2>\\\");\\n    }\\n}\"}]}, \"9\": {\"title\": \"Exp 09: JSP welcome message\", \"notes\": \"\", \"filename\": \"welcome.jsp\", \"language\": \"jsp\", \"code\": \"<html>\\n<body>\\n    <h1>Welcome to JSP Programming!</h1>\\n</body>\\n</html>\", \"files\": [{\"name\": \"welcome.jsp\", \"language\": \"jsp\", \"code\": \"<html>\\n<body>\\n    <h1>Welcome to JSP Programming!</h1>\\n</body>\\n</html>\"}]}, \"10\": {\"title\": \"Exp 10: JSP to display name, register number and department\", \"notes\": \"\", \"filename\": \"details.jsp\", \"language\": \"jsp\", \"code\": \"<html>\\n<body>\\n    <%\\n        String name = \\\"Varun\\\", regNo = \\\"2021001\\\", dept = \\\"Computer Science\\\";\\n    %>\\n    <h2>Student Details</h2>\\n    <p>Name: <%= name %></p>\\n    <p>Register Number: <%= regNo %></p>\\n    <p>Department: <%= dept %></p>\\n</body>\\n</html>\", \"files\": [{\"name\": \"details.jsp\", \"language\": \"jsp\", \"code\": \"<html>\\n<body>\\n    <%\\n        String name = \\\"Varun\\\", regNo = \\\"2021001\\\", dept = \\\"Computer Science\\\";\\n    %>\\n    <h2>Student Details</h2>\\n    <p>Name: <%= name %></p>\\n    <p>Register Number: <%= regNo %></p>\\n    <p>Department: <%= dept %></p>\\n</body>\\n</html>\"}]}, \"11\": {\"title\": \"Exp 11: JDBC application (insert, update, delete, display)\", \"notes\": \"Run SQL in MySQL first: CREATE DATABASE college; USE college; CREATE TABLE student (roll INT PRIMARY KEY, name VARCHAR(50), marks FLOAT);\", \"files\": [{\"name\": \"student.sql\", \"language\": \"sql\", \"code\": \"CREATE DATABASE college;\\nUSE college;\\nCREATE TABLE student (roll INT PRIMARY KEY, name VARCHAR(50), marks FLOAT);\"}, {\"name\": \"StudentJDBC.java\", \"language\": \"java\", \"code\": \"import java.sql.*;\\nimport java.util.Scanner;\\n\\npublic class StudentJDBC {\\n    public static void main(String[] args) throws Exception {\\n        Connection con = DriverManager.getConnection(\\n                \\\"jdbc:mysql://localhost:3306/college\\\", \\\"root\\\", \\\"password\\\");\\n        Scanner sc = new Scanner(System.in);\\n        int ch;\\n\\n        do {\\n            System.out.print(\\\"\\\\n1.Insert 2.Update 3.Delete 4.Display 5.Exit: \\\");\\n            ch = sc.nextInt();\\n\\n            if (ch == 1) {\\n                System.out.print(\\\"Enter roll, name, marks: \\\");\\n                PreparedStatement ps = con.prepareStatement(\\\"INSERT INTO student VALUES (?,?,?)\\\");\\n                ps.setInt(1, sc.nextInt());\\n                ps.setString(2, sc.next());\\n                ps.setFloat(3, sc.nextFloat());\\n                ps.executeUpdate();\\n                System.out.println(\\\"Record inserted.\\\");\\n            } else if (ch == 2) {\\n                System.out.print(\\\"Enter roll and new marks: \\\");\\n                PreparedStatement ps = con.prepareStatement(\\\"UPDATE student SET marks=? WHERE roll=?\\\");\\n                int roll = sc.nextInt();\\n                ps.setFloat(1, sc.nextFloat());\\n                ps.setInt(2, roll);\\n                ps.executeUpdate();\\n                System.out.println(\\\"Record updated.\\\");\\n            } else if (ch == 3) {\\n                System.out.print(\\\"Enter roll to delete: \\\");\\n                PreparedStatement ps = con.prepareStatement(\\\"DELETE FROM student WHERE roll=?\\\");\\n                ps.setInt(1, sc.nextInt());\\n                ps.executeUpdate();\\n                System.out.println(\\\"Record deleted.\\\");\\n            } else if (ch == 4) {\\n                ResultSet rs = con.createStatement().executeQuery(\\\"SELECT * FROM student\\\");\\n                while (rs.next())\\n                    System.out.println(rs.getInt(1) + \\\" \\\" + rs.getString(2) + \\\" \\\" + rs.getFloat(3));\\n            }\\n        } while (ch != 5);\\n\\n        con.close();\\n    }\\n}\"}]}, \"12\": {\"title\": \"Exp 12: Student registration form with CSS\", \"notes\": \"\", \"files\": [{\"name\": \"index.html\", \"language\": \"html\", \"code\": \"<!DOCTYPE html>\\n<html>\\n<head>\\n    <title>Student Registration</title>\\n    <link rel=\\\"stylesheet\\\" href=\\\"style.css\\\">\\n</head>\\n<body>\\n    <form>\\n        <h3>Student Registration</h3>\\n        <input type=\\\"text\\\" placeholder=\\\"Enter Name\\\">\\n        <input type=\\\"email\\\" placeholder=\\\"Enter Email\\\">\\n        <input type=\\\"password\\\" placeholder=\\\"Enter Password\\\">\\n        <select>\\n            <option>B.Tech</option>\\n            <option>BCA</option>\\n            <option>MCA</option>\\n        </select>\\n        <button type=\\\"submit\\\">Register</button>\\n    </form>\\n</body>\\n</html>\"}, {\"name\": \"style.css\", \"language\": \"css\", \"code\": \"body {\\n    font-family: Arial, sans-serif;\\n    background-color: #f0f4f8;\\n}\\n\\nform {\\n    width: 300px;\\n    margin: 50px auto;\\n    padding: 20px;\\n    background-color: white;\\n    border: 1px solid #ccc;\\n    border-radius: 5px;\\n}\\n\\ninput, select, button {\\n    width: 100%;\\n    padding: 8px;\\n    margin: 8px 0;\\n    box-sizing: border-box;\\n    border: 1px solid #aaa;\\n    border-radius: 4px;\\n}\\n\\nbutton {\\n    background-color: #007bff;\\n    color: white;\\n    cursor: pointer;\\n}\"}]}, \"13\": {\"title\": \"Exp 13: College department webpage\", \"notes\": \"\", \"files\": [{\"name\": \"index.html\", \"language\": \"html\", \"code\": \"<!DOCTYPE html>\\n<html>\\n<head>\\n    <title>CSE Department</title>\\n    <link rel=\\\"stylesheet\\\" href=\\\"style.css\\\">\\n</head>\\n<body>\\n\\n    <header>\\n        <h2>Department of Computer Science</h2>\\n    </header>\\n\\n    <nav>\\n        <a href=\\\"#faculty\\\">Faculty</a> | \\n        <a href=\\\"#courses\\\">Courses</a> | \\n        <a href=\\\"#contact\\\">Contact</a>\\n    </nav>\\n\\n    <section id=\\\"faculty\\\">\\n        <h3>Faculty</h3>\\n        <table>\\n            <tr>\\n                <th>Name</th>\\n                <th>Designation</th>\\n            </tr>\\n            <tr>\\n                <td>Dr. Ravi Kumar</td>\\n                <td>Professor &amp; HOD</td>\\n            </tr>\\n            <tr>\\n                <td>Ms. Anita Sharma</td>\\n                <td>Assistant Professor</td>\\n            </tr>\\n        </table>\\n    </section>\\n\\n    <section id=\\\"courses\\\">\\n        <h3>Courses</h3>\\n        <table>\\n            <tr>\\n                <th>Course</th>\\n                <th>Duration</th>\\n            </tr>\\n            <tr>\\n                <td>B.Tech CSE</td>\\n                <td>4 Years</td>\\n            </tr>\\n            <tr>\\n                <td>MCA</td>\\n                <td>2 Years</td>\\n            </tr>\\n        </table>\\n    </section>\\n\\n    <section id=\\\"contact\\\">\\n        <h3>Contact</h3>\\n        <p>Email: cse@abccollege.edu | Phone: 044-12345678</p>\\n    </section>\\n\\n    <footer>\\n        &copy; 2026 CSE Department\\n    </footer>\\n\\n</body>\\n</html>\"}, {\"name\": \"style.css\", \"language\": \"css\", \"code\": \"body {\\n    font-family: Arial;\\n    margin: 0;\\n}\\n\\nheader, footer {\\n    background-color: navy;\\n    color: white;\\n    text-align: center;\\n    padding: 10px;\\n}\\n\\nnav {\\n    background-color: lightgray;\\n    text-align: center;\\n    padding: 5px;\\n}\\n\\nsection {\\n    padding: 10px 20px;\\n}\\n\\ntable, th, td {\\n    border: 1px solid black;\\n    border-collapse: collapse;\\n    padding: 6px;\\n}\"}]}, \"14\": {\"title\": \"Exp 14: JavaScript email validation\", \"notes\": \"\", \"filename\": \"index.html\", \"language\": \"html\", \"code\": \"<!DOCTYPE html>\\n<html>\\n<head>\\n    <title>Email Validation</title>\\n</head>\\n<body>\\n\\n    <input type=\\\"text\\\" id=\\\"email\\\" placeholder=\\\"Enter email\\\">\\n    <button onclick=\\\"validate()\\\">Validate</button>\\n    <p id=\\\"res\\\"></p>\\n\\n    <script>\\n    function validate() {\\n        let e = document.getElementById(\\\"email\\\").value;\\n        let valid = /^[^\\\\s@]+@[^\\\\s@]+\\\\.[^\\\\s@]+$/.test(e);\\n        document.getElementById(\\\"res\\\").innerText = valid ? \\\"Valid Email ID\\\" : \\\"Invalid Email ID\\\";\\n    }\\n    </script>\\n\\n</body>\\n</html>\", \"files\": [{\"name\": \"index.html\", \"language\": \"html\", \"code\": \"<!DOCTYPE html>\\n<html>\\n<head>\\n    <title>Email Validation</title>\\n</head>\\n<body>\\n\\n    <input type=\\\"text\\\" id=\\\"email\\\" placeholder=\\\"Enter email\\\">\\n    <button onclick=\\\"validate()\\\">Validate</button>\\n    <p id=\\\"res\\\"></p>\\n\\n    <script>\\n    function validate() {\\n        let e = document.getElementById(\\\"email\\\").value;\\n        let valid = /^[^\\\\s@]+@[^\\\\s@]+\\\\.[^\\\\s@]+$/.test(e);\\n        document.getElementById(\\\"res\\\").innerText = valid ? \\\"Valid Email ID\\\" : \\\"Invalid Email ID\\\";\\n    }\\n    </script>\\n\\n</body>\\n</html>\"}]}, \"15\": {\"title\": \"Exp 15: Student registration form validation\", \"notes\": \"\", \"filename\": \"index.html\", \"language\": \"html\", \"code\": \"<!DOCTYPE html>\\n<html>\\n<head>\\n    <title>Registration Validation</title>\\n</head>\\n<body>\\n\\n    <form onsubmit=\\\"return validate()\\\">\\n        Name: <input id=\\\"n\\\"><br><br>\\n        Email: <input id=\\\"e\\\"><br><br>\\n        Password: <input type=\\\"password\\\" id=\\\"p\\\"><br><br>\\n        <input type=\\\"submit\\\" value=\\\"Register\\\">\\n    </form>\\n\\n    <script>\\n    function validate() {\\n        let name = document.getElementById(\\\"n\\\").value.trim();\\n        let email = document.getElementById(\\\"e\\\").value.trim();\\n        let pass = document.getElementById(\\\"p\\\").value;\\n\\n        if (name === \\\"\\\") { \\n            alert(\\\"Name is required\\\"); \\n            return false; \\n        }\\n        if (!/^[^\\\\s@]+@[^\\\\s@]+\\\\.[^\\\\s@]+$/.test(email)) { \\n            alert(\\\"Enter a valid email\\\"); \\n            return false; \\n        }\\n        if (pass.length < 6) { \\n            alert(\\\"Password must be at least 6 characters\\\"); \\n            return false; \\n        }\\n\\n        alert(\\\"Registration successful!\\\");\\n        return true;\\n    }\\n    </script>\\n\\n</body>\\n</html>\", \"files\": [{\"name\": \"index.html\", \"language\": \"html\", \"code\": \"<!DOCTYPE html>\\n<html>\\n<head>\\n    <title>Registration Validation</title>\\n</head>\\n<body>\\n\\n    <form onsubmit=\\\"return validate()\\\">\\n        Name: <input id=\\\"n\\\"><br><br>\\n        Email: <input id=\\\"e\\\"><br><br>\\n        Password: <input type=\\\"password\\\" id=\\\"p\\\"><br><br>\\n        <input type=\\\"submit\\\" value=\\\"Register\\\">\\n    </form>\\n\\n    <script>\\n    function validate() {\\n        let name = document.getElementById(\\\"n\\\").value.trim();\\n        let email = document.getElementById(\\\"e\\\").value.trim();\\n        let pass = document.getElementById(\\\"p\\\").value;\\n\\n        if (name === \\\"\\\") { \\n            alert(\\\"Name is required\\\"); \\n            return false; \\n        }\\n        if (!/^[^\\\\s@]+@[^\\\\s@]+\\\\.[^\\\\s@]+$/.test(email)) { \\n            alert(\\\"Enter a valid email\\\"); \\n            return false; \\n        }\\n        if (pass.length < 6) { \\n            alert(\\\"Password must be at least 6 characters\\\"); \\n            return false; \\n        }\\n\\n        alert(\\\"Registration successful!\\\");\\n        return true;\\n    }\\n    </script>\\n\\n</body>\\n</html>\"}]}, \"16\": {\"title\": \"Exp 16: DOM: change background color every 5 seconds\", \"notes\": \"\", \"filename\": \"index.html\", \"language\": \"html\", \"code\": \"<!DOCTYPE html>\\n<html>\\n<body>\\n    <h2>Background changes every 5 seconds</h2>\\n\\n    <script>\\n        let colors = [\\\"lightblue\\\", \\\"lightgreen\\\", \\\"lightpink\\\", \\\"lightyellow\\\", \\\"lavender\\\"];\\n        let i = 0;\\n\\n        function changeColor() {\\n            document.body.style.backgroundColor = colors[i];\\n            i = (i + 1) % colors.length;\\n        }\\n\\n        changeColor();\\n        setInterval(changeColor, 5000);\\n    </script>\\n</body>\\n</html>\", \"files\": [{\"name\": \"index.html\", \"language\": \"html\", \"code\": \"<!DOCTYPE html>\\n<html>\\n<body>\\n    <h2>Background changes every 5 seconds</h2>\\n\\n    <script>\\n        let colors = [\\\"lightblue\\\", \\\"lightgreen\\\", \\\"lightpink\\\", \\\"lightyellow\\\", \\\"lavender\\\"];\\n        let i = 0;\\n\\n        function changeColor() {\\n            document.body.style.backgroundColor = colors[i];\\n            i = (i + 1) % colors.length;\\n        }\\n\\n        changeColor();\\n        setInterval(changeColor, 5000);\\n    </script>\\n</body>\\n</html>\"}]}}}")

def _load_subjects():
    candidates = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "helper", "data.json"),
        os.path.join(os.getcwd(), "data.json"),
        os.path.join(os.getcwd(), "helper", "data.json"),
        os.path.join(os.path.expanduser("~"), "helper", "data.json"),
    ]
    for p in candidates:
        if os.path.isfile(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    d = json.load(f)
                    if d and "fsjp" in d and d["fsjp"]:
                        return d
            except Exception:
                pass
    return _EMBEDDED_SUBJECTS

SUBJECTS = _load_subjects()
EXPERIMENT_SUBJECTS = ("fsjp",)
DEFAULT_SUBJECT = "fsjp"

DIVIDER = "=" * 60


def _valid_subjects():
    return sorted(SUBJECTS.keys()) if SUBJECTS else ["fsjp"]


def _valid_topics(subject=DEFAULT_SUBJECT):
    s = _resolve_subject(subject)
    if not s or s not in SUBJECTS:
        return []
    keys = [k for k in SUBJECTS[s].keys() if k.isdigit()]
    return sorted(keys, key=int)


def _resolve_subject(raw):
    """Return the canonical subject key or None."""
    if not raw:
        return DEFAULT_SUBJECT
    raw_str = str(raw).strip().lower()
    for s in SUBJECTS:
        if s.lower() == raw_str:
            return s
    if raw_str in ("fsjp", "java", "fullstack", "fullstackjava", "subject3", "sub3", "s3"):
        return "fsjp"
    return None


def _resolve_topic(subject, raw):
    """Return the canonical topic key or None."""
    s = _resolve_subject(subject) or DEFAULT_SUBJECT
    if not s or s not in SUBJECTS:
        return None
    topics = SUBJECTS[s]
    raw_str = str(raw).strip().lower()

    if raw_str in topics:
        return raw_str

    cleaned = re.sub(r"^(exp|experiment|topic|q)[\s_\-]*", "", raw_str)
    if cleaned in topics:
        return cleaned

    cleaned_num = cleaned.lstrip("0") or "0"
    if cleaned_num in topics:
        return cleaned_num

    return None


def _normalize_args(args):
    """
    Handle split arguments such as:
      ['fsjp', 'exp', '1'] -> ['fsjp', 'exp1']
      ['exp', '1'] -> ['fsjp', 'exp1']
    """
    if len(args) >= 3 and args[1].lower() in ("exp", "experiment", "topic", "q"):
        return [args[0], f"exp{args[2]}"] + args[3:]
    if len(args) >= 2 and args[0].lower() in ("exp", "experiment", "topic", "q"):
        return [f"exp{args[1]}"] + args[2:]
    return args


def _get_topic(subject, topic_num):
    """Validated lookup; prints error and exits on bad input."""
    s = _resolve_subject(subject) or DEFAULT_SUBJECT
    if s not in SUBJECTS:
        print(f"[error] Unknown subject: '{subject}'")
        print(f"        Valid subjects: {', '.join(_valid_subjects())}")
        sys.exit(1)
    t = _resolve_topic(s, topic_num)
    if t is None:
        label = "experiment" if s in EXPERIMENT_SUBJECTS else "topic"
        print(f"[error] Unknown {label} identifier: '{topic_num}' for subject '{s}'")
        valid_items = [f"exp{k}" for k in _valid_topics(s)]
        print(f"        Valid {label}s: {', '.join(valid_items)} (or 1..{len(valid_items)})")
        sys.exit(1)
    return SUBJECTS[s][t]


def _copy_to_clipboard(text):
    """Try multiple clipboard strategies; degrade gracefully."""
    platform = sys.platform
    try:
        if platform == "win32":
            proc = subprocess.Popen(["clip"], stdin=subprocess.PIPE, shell=True)
            proc.communicate(input=text.encode("utf-16"))
            if proc.returncode == 0:
                return True
        elif platform == "darwin":
            proc = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
            proc.communicate(input=text.encode("utf-8"))
            if proc.returncode == 0:
                return True
        else:
            for cmd in (["xclip", "-selection", "clipboard"], ["xsel", "--clipboard", "--input"]):
                try:
                    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
                    proc.communicate(input=text.encode("utf-8"))
                    if proc.returncode == 0:
                        return True
                except FileNotFoundError:
                    continue
    except Exception:
        pass

    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()
        root.after(300, root.destroy)
        root.mainloop()
        return True
    except Exception:
        pass

    return False


_LANGUAGE_LABELS = {
    "java": "JAVA",
    "html": "HTML",
    "css": "CSS",
    "js": "JAVASCRIPT",
    "javascript": "JAVASCRIPT",
    "jsp": "JSP",
    "sql": "SQL",
    "xml": "XML",
}


def _language_label(language):
    text = str(language or "").strip()
    return _LANGUAGE_LABELS.get(text.lower(), text.upper() or "TEXT")


def _topic_files(topic):
    """Return a topic's files as [{name, language, code}, ...]."""
    files = topic.get("files")
    if isinstance(files, list) and files:
        return files
    return [{
        "name": topic.get("filename", ""),
        "language": topic.get("language", "java"),
        "code": topic.get("code", ""),
    }]


def _line_count(code):
    return len(code.strip("\n").splitlines())


def _resolve_file(files, raw):
    """Resolve a 1-based number or file name. Returns index, -1 for all, or None."""
    if raw is None:
        return None
    text = str(raw).strip()
    if text.lower() == "all":
        return -1
    if text.isdigit():
        number = int(text)
        if 1 <= number <= len(files):
            return number - 1
        return None
    lower = text.lower()
    for index, item in enumerate(files):
        name = str(item.get("name", ""))
        if name.lower() == lower or os.path.basename(name).lower() == lower:
            return index
    return None


def _print_file_index(subject, topic_key, topic, files):
    display_id = f"Exp {int(topic_key):02d}" if (topic_key and str(topic_key).isdigit()) else topic_key
    print(f"[{display_id}] {topic.get('title', '')}")
    print(f"{len(files)} files:\n")
    for index, item in enumerate(files, 1):
        name = item.get("name") or f"file{index}"
        language = _language_label(item.get("language", ""))
        lines = _line_count(item.get("code", ""))
        print(f"  {index}. {name:<32} {language:<12} {lines:>3} lines")


def _print_files(files):
    for index, item in enumerate(files, 1):
        if index > 1:
            print()
        print(f"===== {index}. {item.get('name') or f'file{index}'} =====")
        print(item.get("code", "").strip("\n"))


# -----------------------------------------------------------------------------
#  TOMCAT DETECTION & RUNTIME INSTRUCTIONS
# -----------------------------------------------------------------------------

def _is_port_in_use(port=8080, host="127.0.0.1"):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)
        res = s.connect_ex((host, port))
        s.close()
        return res == 0
    except Exception:
        return False


def _detect_tomcat():
    candidates = []
    for var in ("CATALINA_HOME", "CATALINA_BASE"):
        val = os.environ.get(var)
        if val and os.path.isdir(val):
            candidates.append((val, f"%{var}%" if sys.platform == "win32" else f"${var}"))
    search_patterns = [
        r"C:\apache-tomcat*",
        r"C:\Program Files\Apache Software Foundation\Tomcat*",
        r"C:\Program Files (x86)\Apache Software Foundation\Tomcat*",
        r"D:\apache-tomcat*",
        os.path.expanduser(r"~\apache-tomcat*"),
        "/opt/tomcat*",
        "/usr/local/tomcat*",
        "/opt/homebrew/opt/tomcat*",
    ]
    for pattern in search_patterns:
        for p in glob.glob(pattern):
            if os.path.isdir(p) and not any(os.path.abspath(p) == os.path.abspath(c[0]) for c in candidates):
                candidates.append((p, "filesystem"))
    for path, source in candidates:
        bin_dir = os.path.join(path, "bin")
        lib_dir = os.path.join(path, "lib")
        if os.path.isdir(bin_dir) and os.path.isdir(lib_dir):
            ver = "Unknown"
            rel_notes = os.path.join(path, "RELEASE-NOTES")
            if os.path.isfile(rel_notes):
                try:
                    with open(rel_notes, "r", encoding="latin1") as f:
                        m = re.search(r"Apache Tomcat Version ([\d\.]+)", f.read(2048))
                        if m:
                            ver = m.group(1)
                except Exception:
                    pass
            if ver == "Unknown":
                m = re.search(r"tomcat-?(\d+[\.\d]*)", os.path.basename(path), re.IGNORECASE)
                if m:
                    ver = m.group(1)
            has_jakarta = os.path.isfile(os.path.join(lib_dir, "jakarta.servlet-api.jar"))
            major_ver = 10 if has_jakarta else 9
            if ver != "Unknown":
                try:
                    major_ver = int(ver.split(".")[0])
                except Exception:
                    pass
            return {
                "found": True,
                "path": os.path.abspath(path),
                "source": source,
                "version": ver,
                "major_version": major_ver,
                "servlet_jar": "jakarta.servlet-api.jar" if has_jakarta else "servlet-api.jar",
                "use_jakarta": major_ver >= 10,
            }
    return {
        "found": False,
        "path": "%CATALINA_HOME%" if sys.platform == "win32" else "$CATALINA_HOME",
        "source": "none",
        "version": "Unknown",
        "major_version": 9,
        "servlet_jar": "servlet-api.jar",
        "use_jakarta": False,
    }


def _detect_java():
    jh = os.environ.get("JAVA_HOME", "")
    if jh and os.path.isdir(jh) and os.path.isfile(os.path.join(jh, "bin", "javac.exe" if sys.platform == "win32" else "javac")):
        return {"found": True, "path": jh, "source": "JAVA_HOME"}
    patterns = [
        r"C:\Program Files\Eclipse Adoptium\jdk*",
        r"C:\Program Files\Java\jdk*",
        r"C:\Program Files\Amazon Corretto\jdk*",
        r"C:\Program Files\Microsoft\jdk*",
        r"C:\Program Files\Zulu\zulu*",
    ]
    for pattern in patterns:
        for p in glob.glob(pattern):
            if os.path.isfile(os.path.join(p, "bin", "javac.exe" if sys.platform == "win32" else "javac")):
                return {"found": True, "path": p, "source": "detected"}
    return {"found": False, "path": jh or "Not Set", "source": "none"}


def _requires_tomcat(topic_key, topic=None):
    key = str(topic_key).strip().lower()
    if key in ("7", "8", "9", "10", "exp7", "exp8", "exp9", "exp10", "q7", "q8", "q9", "q10"):
        return True
    if topic:
        files = topic.get("files") or []
        for f in files:
            name = (f.get("name") or "").lower()
            lang = (f.get("language") or "").lower()
            code = f.get("code") or ""
            if name.endswith(".jsp") or lang == "jsp":
                return True
            if any(m in code for m in ("@WebServlet", "HttpServlet", "javax.servlet", "jakarta.servlet")):
                return True
    return False


def _format_tomcat_instructions(topic_key, topic=None):
    tc = _detect_tomcat()
    tc_path = tc["path"] if tc["found"] else "%CATALINA_HOME%"
    tc_jar = tc.get("servlet_jar", "servlet-api.jar")
    port_active = _is_port_in_use(8080)

    key = str(topic_key).lstrip("0") or "0"
    if "exp" in key.lower():
        key = re.sub(r"[^\d]", "", key)

    lines = [
        "=" * 60,
        f"  APACHE TOMCAT EXECUTION GUIDE -- Exp {int(key):02d}",
        "=" * 60,
    ]

    if tc["found"]:
        status_str = "ACTIVE (Port 8080 is listening)" if port_active else "STOPPED (Ready to start)"
        lines.append(f"Tomcat Status : {tc['version']} at {tc['path']}")
        lines.append(f"Server State  : {status_str}")
    else:
        lines.append("Tomcat Status : Not detected in standard paths (set %CATALINA_HOME%)")
        lines.append(f"Server State  : {'Port 8080 active' if port_active else 'Port 8080 free'}")
    lines.append("-" * 60)

    if key == "7":
        lines.extend([
            "Experiment Type : Servlet (Welcome Message)",
            "Webapp Target   : webapps/myapp/WEB-INF/classes/WelcomeServlet.class",
            "Browser URL     : http://localhost:8080/myapp/welcome",
            "",
            "[1] Universal Commands (Works on ANY PC with %CATALINA_HOME%):",
            "    # 1. Create classes folder:",
            '    mkdir "%CATALINA_HOME%\\webapps\\myapp\\WEB-INF\\classes" 2>nul',
            "",
            "    # 2. Compile Servlet directly into Tomcat classes folder:",
            f'    javac -cp "%CATALINA_HOME%\\lib\\{tc_jar}" -d "%CATALINA_HOME%\\webapps\\myapp\\WEB-INF\\classes" WelcomeServlet.java',
            "",
            "    # 3. Start Tomcat:",
            '    "%CATALINA_HOME%\\bin\\startup.bat"',
            '    (PowerShell: & "$env:CATALINA_HOME\\bin\\startup.bat")',
            "    (Linux/Mac:  $CATALINA_HOME/bin/startup.sh)",
            "",
            "    # 4. Open in Browser:",
            "    http://localhost:8080/myapp/welcome",
            "",
            "    # 5. Stop Tomcat when done:",
            '    "%CATALINA_HOME%\\bin\\shutdown.bat"',
        ])
        if tc["found"]:
            lines.extend([
                "",
                f"[2] Ready-to-Run for THIS PC (Detected: {tc['path']}):",
                f'    javac -cp "{tc_path}\\lib\\{tc_jar}" -d "{tc_path}\\webapps\\myapp\\WEB-INF\\classes" WelcomeServlet.java',
                f'    "{tc_path}\\bin\\startup.bat"',
                "    http://localhost:8080/myapp/welcome",
            ])
    elif key == "8":
        lines.extend([
            "Experiment Type : HTML Form + Servlet (Greeting)",
            "Webapp Target   : webapps/myapp/index.html",
            "                  webapps/myapp/WEB-INF/classes/HelloServlet.class",
            "Browser URL     : http://localhost:8080/myapp/index.html",
            "",
            "[1] Universal Commands (Works on ANY PC with %CATALINA_HOME%):",
            "    # 1. Create classes folder:",
            '    mkdir "%CATALINA_HOME%\\webapps\\myapp\\WEB-INF\\classes" 2>nul',
            "",
            "    # 2. Copy index.html into webapp root:",
            '    copy index.html "%CATALINA_HOME%\\webapps\\myapp"',
            "",
            "    # 3. Compile HelloServlet.java into Tomcat classes folder:",
            f'    javac -cp "%CATALINA_HOME%\\lib\\{tc_jar}" -d "%CATALINA_HOME%\\webapps\\myapp\\WEB-INF\\classes" HelloServlet.java',
            "",
            "    # 4. Start Tomcat:",
            '    "%CATALINA_HOME%\\bin\\startup.bat"',
            '    (PowerShell: & "$env:CATALINA_HOME\\bin\\startup.bat")',
            "    (Linux/Mac:  $CATALINA_HOME/bin/startup.sh)",
            "",
            "    # 5. Open HTML form in Browser (submits POST to /myapp/hello):",
            "    http://localhost:8080/myapp/index.html",
            "",
            "    # 6. Stop Tomcat when done:",
            '    "%CATALINA_HOME%\\bin\\shutdown.bat"',
        ])
        if tc["found"]:
            lines.extend([
                "",
                f"[2] Ready-to-Run for THIS PC (Detected: {tc['path']}):",
                f'    copy index.html "{tc_path}\\webapps\\myapp"',
                f'    javac -cp "{tc_path}\\lib\\{tc_jar}" -d "{tc_path}\\webapps\\myapp\\WEB-INF\\classes" HelloServlet.java',
                f'    "{tc_path}\\bin\\startup.bat"',
                "    http://localhost:8080/myapp/index.html",
            ])
    elif key == "9":
        lines.extend([
            "Experiment Type : JSP (Welcome Message)",
            "Webapp Target   : webapps/myapp/welcome.jsp",
            "Browser URL     : http://localhost:8080/myapp/welcome.jsp",
            "",
            "[Note]: JSP files DO NOT need javac compilation!",
            "        Tomcat compiles JSP files into servlets automatically on request.",
            "",
            "[1] Universal Commands (Works on ANY PC with %CATALINA_HOME%):",
            "    # 1. Create webapp folder:",
            '    mkdir "%CATALINA_HOME%\\webapps\\myapp" 2>nul',
            "",
            "    # 2. Copy welcome.jsp directly into webapps/myapp/:",
            '    copy welcome.jsp "%CATALINA_HOME%\\webapps\\myapp"',
            "",
            "    # 3. Start Tomcat:",
            '    "%CATALINA_HOME%\\bin\\startup.bat"',
            '    (PowerShell: & "$env:CATALINA_HOME\\bin\\startup.bat")',
            "    (Linux/Mac:  $CATALINA_HOME/bin/startup.sh)",
            "",
            "    # 4. Open in Browser:",
            "    http://localhost:8080/myapp/welcome.jsp",
            "",
            "    # 5. Stop Tomcat when done:",
            '    "%CATALINA_HOME%\\bin\\shutdown.bat"',
        ])
        if tc["found"]:
            lines.extend([
                "",
                f"[2] Ready-to-Run for THIS PC (Detected: {tc['path']}):",
                f'    copy welcome.jsp "{tc_path}\\webapps\\myapp"',
                f'    "{tc_path}\\bin\\startup.bat"',
                "    http://localhost:8080/myapp/welcome.jsp",
            ])
    elif key == "10":
        lines.extend([
            "Experiment Type : JSP (Student Details)",
            "Webapp Target   : webapps/myapp/details.jsp",
            "Browser URL     : http://localhost:8080/myapp/details.jsp",
            "",
            "[Note]: JSP files DO NOT need javac compilation!",
            "        Tomcat compiles JSP files into servlets automatically on request.",
            "",
            "[1] Universal Commands (Works on ANY PC with %CATALINA_HOME%):",
            "    # 1. Create webapp folder:",
            '    mkdir "%CATALINA_HOME%\\webapps\\myapp" 2>nul',
            "",
            "    # 2. Copy details.jsp directly into webapps/myapp/:",
            '    copy details.jsp "%CATALINA_HOME%\\webapps\\myapp"',
            "",
            "    # 3. Start Tomcat:",
            '    "%CATALINA_HOME%\\bin\\startup.bat"',
            '    (PowerShell: & "$env:CATALINA_HOME\\bin\\startup.bat")',
            "    (Linux/Mac:  $CATALINA_HOME/bin/startup.sh)",
            "",
            "    # 4. Open in Browser:",
            "    http://localhost:8080/myapp/details.jsp",
            "",
            "    # 5. Stop Tomcat when done:",
            '    "%CATALINA_HOME%\\bin\\shutdown.bat"',
        ])
        if tc["found"]:
            lines.extend([
                "",
                f"[2] Ready-to-Run for THIS PC (Detected: {tc['path']}):",
                f'    copy details.jsp "{tc_path}\\webapps\\myapp"',
                f'    "{tc_path}\\bin\\startup.bat"',
                "    http://localhost:8080/myapp/details.jsp",
            ])
    else:
        lines.extend([
            "Experiment Type : Generic Servlet / JSP Web Application",
            "Webapp Target   : %CATALINA_HOME%\\webapps\\myapp",
            "",
            "[1] General Deployment Rules:",
            "    * Java Servlets (.class) -> %CATALINA_HOME%\\webapps\\myapp\\WEB-INF\\classes",
            "    * HTML / JSP files       -> %CATALINA_HOME%\\webapps\\myapp",
            "    * Start Tomcat           -> %CATALINA_HOME%\\bin\\startup.bat",
            "    * Access in browser      -> http://localhost:8080/myapp/<endpoint>",
        ])

    lines.extend([
        "-" * 60,
        "Universality Notes:",
        "  * %CATALINA_HOME% is universal: Set it once in System Environment Variables,",
        "    and the exact same commands run on ANY Windows machine.",
        "  * Tomcat 9 vs 10+: Tomcat 9 uses 'javax.servlet.*' (used in this lab).",
        "    Tomcat 10+ uses 'jakarta.servlet.*'. If using Tomcat 10+, replace 'javax'",
        "    with 'jakarta' in the import statements.",
        "=" * 60,
    ])
    return "\n".join(lines)


def _print_tomcat_if_needed(topic_key, topic=None):
    if _requires_tomcat(topic_key, topic):
        print()
        print(_format_tomcat_instructions(topic_key, topic))


# -----------------------------------------------------------------------------
#  COMMANDS
# -----------------------------------------------------------------------------

def cmd_list(args):
    """
    list           -> list all experiments in fsjp
    list <subject> -> list experiments in that subject
    """
    subject = args[0] if len(args) > 0 else DEFAULT_SUBJECT
    s = _resolve_subject(subject)
    if s is None or s not in SUBJECTS:
        print(f"[error] Unknown subject: '{subject}'")
        print(f"        Valid subjects: {', '.join(_valid_subjects())}")
        sys.exit(1)

    topics = SUBJECTS[s]
    label = "Experiments"

    print(DIVIDER)
    print(f"  {label} in '{s}' (Full Stack Java Programming)")
    print(DIVIDER)
    for num in _valid_topics(s):
        title = topics[num].get("title", "")
        prefix = f"Exp {int(num):02d}"
        files = _topic_files(topics[num])
        suffix = f" ({len(files)} files)" if len(files) > 1 else ""
        print(f"  [{prefix}]  {title}{suffix}")
    print(DIVIDER)


def cmd_show(args):
    """show [subject] <topic_num> [file|all] -- Outputs code."""
    args = _normalize_args(args)
    if not args:
        print("[error] Usage: python helper.py [show] <exp_num> [file|all]")
        print("               python helper.py [show] fsjp <exp_num> [file|all]")
        sys.exit(1)

    if len(args) == 1:
        raw_subject = DEFAULT_SUBJECT
        raw_topic = args[0]
        file_arg = None
    elif _resolve_subject(args[0]):
        raw_subject = args[0]
        raw_topic = args[1]
        file_arg = args[2] if len(args) >= 3 else None
    else:
        raw_subject = DEFAULT_SUBJECT
        raw_topic = args[0]
        file_arg = args[1] if len(args) >= 2 else None

    s = _resolve_subject(raw_subject) or DEFAULT_SUBJECT
    t = _resolve_topic(s, raw_topic)
    topic = _get_topic(s, raw_topic)

    files = _topic_files(topic)

    if len(files) > 1:
        selector = file_arg
        if selector is None:
            if sys.stdin.isatty():
                _print_file_index(s, t, topic, files)
                print()
                try:
                    raw_file = input(f"Select file (1-{len(files)}, all) [1]: ").strip()
                    selector = raw_file or "1"
                except (EOFError, KeyboardInterrupt):
                    print()
                    return
            else:
                _print_file_index(s, t, topic, files)
                print(f"\nPass '1'..'{len(files)}' or 'all' to print contents.")
                return

        chosen = _resolve_file(files, selector)
        if chosen is None:
            print(f"[error] Unknown file '{selector}' for {s} experiment {int(t):02d}.")
            _print_file_index(s, t, topic, files)
            sys.exit(1)

        if chosen == -1:
            _print_files(files)
        else:
            print(files[chosen].get("code", "").strip("\n"))
        _print_tomcat_if_needed(t, topic)
        return

    code = files[0].get("code", "").strip()
    if code:
        print(code)
    else:
        print("// (no code yet)")
    _print_tomcat_if_needed(t, topic)


def cmd_write(args):
    """write [subject] <topic_num> [filename|folder]"""
    args = _normalize_args(args)
    if not args:
        print("[error] Usage: python helper.py write [subject] <exp_num> [filename|folder]")
        sys.exit(1)

    if len(args) == 1:
        raw_subject = DEFAULT_SUBJECT
        raw_topic = args[0]
        dest_arg = None
    elif _resolve_subject(args[0]):
        raw_subject = args[0]
        raw_topic = args[1]
        dest_arg = args[2] if len(args) >= 3 else None
    else:
        raw_subject = DEFAULT_SUBJECT
        raw_topic = args[0]
        dest_arg = args[1] if len(args) >= 2 else None

    s = _resolve_subject(raw_subject) or DEFAULT_SUBJECT
    t = _resolve_topic(s, raw_topic)
    topic = _get_topic(s, raw_topic)
    files = _topic_files(topic)

    if len(files) > 1:
        folder = dest_arg or f"{s}_exp_{t}"
        written = []
        try:
            for item in files:
                name = str(item.get("name") or "file.txt").replace("\\", "/")
                parts = [part for part in name.split("/") if part]
                if not parts or name.startswith("/") or ":" in parts[0] or ".." in parts:
                    raise ValueError(f"unsafe file name: {name}")
                target = os.path.join(folder, *parts)
                parent = os.path.dirname(target)
                if parent:
                    os.makedirs(parent, exist_ok=True)
                with open(target, "w", encoding="utf-8") as fh:
                    fh.write(item.get("code", "").strip("\n") + "\n")
                written.append(target)
        except (OSError, ValueError) as exc:
            print(f"[error] Could not write files: {exc}")
            sys.exit(1)
        print(f"[ok] Wrote {len(written)} files to '{folder}'")
        for path in written:
            print(f"     {path}")
        return

    filename = dest_arg or files[0].get("name") or f"{s}_exp_{t}.java"
    code = files[0].get("code", "")

    try:
        parent = os.path.dirname(filename)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(filename, "w", encoding="utf-8") as fh:
            fh.write(code.strip() + "\n")
        print(f"[ok] Code written to '{filename}'")
        if _requires_tomcat(t, topic):
            print(f"[tomcat] Exp {int(t):02d} requires Tomcat. Run 'python helper.py tomcat {int(t)}' for deploy & run commands.")
    except OSError as exc:
        print(f"[error] Could not write file: {exc}")
        sys.exit(1)


def cmd_copy(args):
    """copy [subject] <topic_num> [file|all]"""
    args = _normalize_args(args)
    if not args:
        print("[error] Usage: python helper.py copy [subject] <exp_num> [file|all]")
        sys.exit(1)

    if len(args) == 1:
        raw_subject = DEFAULT_SUBJECT
        raw_topic = args[0]
        file_arg = None
    elif _resolve_subject(args[0]):
        raw_subject = args[0]
        raw_topic = args[1]
        file_arg = args[2] if len(args) >= 3 else None
    else:
        raw_subject = DEFAULT_SUBJECT
        raw_topic = args[0]
        file_arg = args[1] if len(args) >= 2 else None

    s = _resolve_subject(raw_subject) or DEFAULT_SUBJECT
    t = _resolve_topic(s, raw_topic)
    topic = _get_topic(s, raw_topic)
    files = _topic_files(topic)

    if len(files) > 1:
        selector = file_arg
        if selector is None:
            if sys.stdin.isatty():
                _print_file_index(s, t, topic, files)
                print()
                try:
                    raw_file = input(f"Select file to copy (1-{len(files)}, all) [1]: ").strip()
                    selector = raw_file or "1"
                except (EOFError, KeyboardInterrupt):
                    print()
                    return
            else:
                selector = "1"

        chosen = _resolve_file(files, selector)
        if chosen is None:
            print(f"[error] Unknown file '{selector}' for {s} experiment {int(t):02d}.")
            sys.exit(1)

        if chosen == -1:
            text = "\n\n".join(
                f"===== {index}. {item.get('name') or f'file{index}'} =====\n"
                f"{item.get('code', '').strip(chr(10))}"
                for index, item in enumerate(files, 1)
            )
            label = f"{len(files)} files"
        else:
            text = files[chosen].get("code", "").strip("\n")
            label = files[chosen].get("name") or f"file {chosen + 1}"

        if not text.strip():
            print("[warn] The selected file is empty - nothing to copy.")
            return

        success = _copy_to_clipboard(text + "\n")
        if success:
            print(f"[ok] {label} from '{s}' experiment {int(t):02d} copied to clipboard.")
            if _requires_tomcat(t, topic):
                print(f"[tomcat] Exp {int(t):02d} requires Tomcat. Run 'python helper.py tomcat {int(t)}' for deploy & run commands.")
        else:
            print("[warn] Could not access clipboard.")
            print("       Here is the code snippet:\n")
            print(text)
        return

    code = files[0].get("code", "")
    if not code.strip():
        print(f"[warn] The code block for experiment {int(t):02d} is empty - nothing to copy.")
        return

    success = _copy_to_clipboard(code.strip() + "\n")
    display_id = f"Exp {int(t):02d}"

    if success:
        print(f"[ok] Code for '{s}' {display_id} copied to clipboard.")
        if _requires_tomcat(t, topic):
            print(f"[tomcat] Exp {int(t):02d} requires Tomcat. Run 'python helper.py tomcat {int(t)}' for deploy & run commands.")
    else:
        print("[warn] Could not access clipboard.")
        print("       Here is the code snippet:\n")
        print(code)


def cmd_tomcat(args):
    """tomcat [exp_num] -- Check Tomcat environment and show deploy instructions."""
    args = _normalize_args(args)
    if args:
        raw_topic = args[0]
        s = DEFAULT_SUBJECT
        t = _resolve_topic(s, raw_topic)
        topic = _get_topic(s, raw_topic) if t else None
        if not t or not _requires_tomcat(t, topic):
            print(f"[warn] Experiment '{raw_topic}' does not require Tomcat.")
            print("       Experiments requiring Tomcat are: 7, 8, 9, 10.\n")
        print(_format_tomcat_instructions(t or raw_topic, topic))
        return

    tc = _detect_tomcat()
    java = _detect_java()
    port_active = _is_port_in_use(8080)

    print(DIVIDER)
    print("  APACHE TOMCAT ENVIRONMENT & QUICK REFERENCE")
    print(DIVIDER)
    print(f"Tomcat Found    : {'YES (' + tc['version'] + ')' if tc['found'] else 'NO (Set %CATALINA_HOME%)'}")
    print(f"Tomcat Location : {tc['path']}")
    print(f"Servlet JAR     : {tc.get('servlet_jar', 'servlet-api.jar')}")
    print(f"Java JDK        : {java['path']}")
    print(f"Port 8080 Status: {'IN USE (Tomcat is listening)' if port_active else 'FREE (Tomcat stopped)'}")
    print(DIVIDER)
    print("Experiments requiring Tomcat in FSJP:")
    print("  * Exp 07 : WelcomeServlet.java (Servlet)           -> http://localhost:8080/myapp/welcome")
    print("  * Exp 08 : index.html + HelloServlet.java (Form)   -> http://localhost:8080/myapp/index.html")
    print("  * Exp 09 : welcome.jsp (JSP)                       -> http://localhost:8080/myapp/welcome.jsp")
    print("  * Exp 10 : details.jsp (JSP)                       -> http://localhost:8080/myapp/details.jsp")
    print("-" * 60)
    print("Universal Quick Commands (Works on ANY PC with %CATALINA_HOME%):")
    print('  Create classes folder: mkdir "%CATALINA_HOME%\\webapps\\myapp\\WEB-INF\\classes" 2>nul')
    print('  Start Tomcat:          "%CATALINA_HOME%\\bin\\startup.bat"')
    print('  Stop Tomcat:           "%CATALINA_HOME%\\bin\\shutdown.bat"')
    if tc["found"]:
        print(f'  Start on THIS PC:      "{tc["path"]}\\bin\\startup.bat"')
    print("-" * 60)
    print("Tip: Run 'python helper.py tomcat <7|8|9|10>' for detailed commands per experiment.")
    print(DIVIDER)


# -----------------------------------------------------------------------------
#  ENTRY POINT
# -----------------------------------------------------------------------------

USAGE = """\
helper.py -- Offline CLI study helper tool for Full Stack Java Programming (FSJP).

Usage:
  python helper.py fsjp <exp_num> [file|all]
  python helper.py <exp_num> [file|all]
  python helper.py list
  python helper.py show   [subject] <topic_or_exp> [file|all]
  python helper.py write  [subject] <topic_or_exp> [filename|folder]
  python helper.py copy   [subject] <topic_or_exp> [file|all]
  python helper.py tomcat [exp_num]

For FSJP experiments (Q1 to Q16), specify '1', 'exp1', 'exp 1', or 'q1'.
For multi-file experiments (Exp 8, Exp 11), pass a file number or 'all'.
For Tomcat experiments (Exp 7, 8, 9, 10), deploy commands are shown automatically.
"""

COMMANDS = {
    "list":   cmd_list,
    "show":   cmd_show,
    "write":  cmd_write,
    "copy":   cmd_copy,
    "tomcat": cmd_tomcat,
}


def main():
    argv = sys.argv[1:]

    if not argv or argv[0] in ("-h", "--help"):
        print(USAGE)
        sys.exit(0)

    cmd = argv[0].lower()
    rest = argv[1:]

    if cmd in ("show", "code", "get"):
        cmd_show(rest)
    elif cmd in ("tomcat", "tc"):
        cmd_tomcat(rest)
    elif cmd in COMMANDS:
        COMMANDS[cmd](rest)
    elif _resolve_subject(cmd):
        # Direct: python helper.py fsjp 6
        cmd_show([cmd] + rest)
    elif _resolve_topic(DEFAULT_SUBJECT, cmd):
        # Direct number shortcut: python helper.py 6
        cmd_show([DEFAULT_SUBJECT, cmd] + rest)
    else:
        print(f"[error] Unknown command or experiment: '{cmd}'")
        print(f"        Valid commands: {', '.join(COMMANDS)}")
        print()
        print(USAGE)
        sys.exit(1)


if __name__ == "__main__":
    main()
