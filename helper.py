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

# -----------------------------------------------------------------------------
#  DATA -- Loaded dynamically from data.json with embedded fallback
# -----------------------------------------------------------------------------

_EMBEDDED_SUBJECTS = json.loads("{\n    \"fsjp\": {\n        \"1\": {\n            \"title\": \"Exp 01: Student class with inputDetails() and displayDetails()\",\n            \"notes\": \"\",\n            \"filename\": \"Student.java\",\n            \"language\": \"java\",\n            \"code\": \"import java.util.Scanner;\\n\\nclass Student {\\n    String name;\\n    int rollNumber;\\n    float marks;\\n\\n    void inputDetails() {\\n        Scanner sc = new Scanner(System.in);\\n        System.out.print(\\\"Enter name: \\\");\\n        name = sc.nextLine();\\n        System.out.print(\\\"Enter roll number: \\\");\\n        rollNumber = sc.nextInt();\\n        System.out.print(\\\"Enter marks: \\\");\\n        marks = sc.nextFloat();\\n    }\\n\\n    void displayDetails() {\\n        System.out.println(\\\"Name: \\\" + name + \\\", Roll: \\\" + rollNumber + \\\", Marks: \\\" + marks);\\n    }\\n\\n    public static void main(String[] args) {\\n        Student s = new Student();\\n        s.inputDetails();\\n        s.displayDetails();\\n    }\\n}\",\n            \"files\": [\n                {\n                    \"name\": \"Student.java\",\n                    \"language\": \"java\",\n                    \"code\": \"import java.util.Scanner;\\n\\nclass Student {\\n    String name;\\n    int rollNumber;\\n    float marks;\\n\\n    void inputDetails() {\\n        Scanner sc = new Scanner(System.in);\\n        System.out.print(\\\"Enter name: \\\");\\n        name = sc.nextLine();\\n        System.out.print(\\\"Enter roll number: \\\");\\n        rollNumber = sc.nextInt();\\n        System.out.print(\\\"Enter marks: \\\");\\n        marks = sc.nextFloat();\\n    }\\n\\n    void displayDetails() {\\n        System.out.println(\\\"Name: \\\" + name + \\\", Roll: \\\" + rollNumber + \\\", Marks: \\\" + marks);\\n    }\\n\\n    public static void main(String[] args) {\\n        Student s = new Student();\\n        s.inputDetails();\\n        s.displayDetails();\\n    }\\n}\"\n                }\n            ]\n        },\n        \"2\": {\n            \"title\": \"Exp 02: Constructor Overloading\",\n            \"notes\": \"\",\n            \"filename\": \"Calculator.java\",\n            \"language\": \"java\",\n            \"code\": \"class Calculator {\\n    Calculator() {\\n        System.out.println(\\\"Welcome to Calculator!\\\");\\n    }\\n\\n    Calculator(int a, int b) {\\n        System.out.println(\\\"Sum = \\\" + (a + b));\\n    }\\n\\n    public static void main(String[] args) {\\n        new Calculator();\\n        new Calculator(10, 20);\\n    }\\n}\",\n            \"files\": [\n                {\n                    \"name\": \"Calculator.java\",\n                    \"language\": \"java\",\n                    \"code\": \"class Calculator {\\n    Calculator() {\\n        System.out.println(\\\"Welcome to Calculator!\\\");\\n    }\\n\\n    Calculator(int a, int b) {\\n        System.out.println(\\\"Sum = \\\" + (a + b));\\n    }\\n\\n    public static void main(String[] args) {\\n        new Calculator();\\n        new Calculator(10, 20);\\n    }\\n}\"\n                }\n            ]\n        },\n        \"3\": {\n            \"title\": \"Exp 03: Method Overloading\",\n            \"notes\": \"\",\n            \"filename\": \"Calculator.java\",\n            \"language\": \"java\",\n            \"code\": \"class Calculator {\\n    int add() { return 5 + 10; }\\n    int add(int a, int b) { return a + b; }\\n    float add(float a, float b, float c) { return a + b + c; }\\n\\n    public static void main(String[] args) {\\n        Calculator c = new Calculator();\\n        System.out.println(\\\"No parameters: \\\" + c.add());\\n        System.out.println(\\\"Two integers: \\\" + c.add(20, 30));\\n        System.out.println(\\\"Three floats: \\\" + c.add(1.5f, 2.5f, 3.5f));\\n    }\\n}\",\n            \"files\": [\n                {\n                    \"name\": \"Calculator.java\",\n                    \"language\": \"java\",\n                    \"code\": \"class Calculator {\\n    int add() { return 5 + 10; }\\n    int add(int a, int b) { return a + b; }\\n    float add(float a, float b, float c) { return a + b + c; }\\n\\n    public static void main(String[] args) {\\n        Calculator c = new Calculator();\\n        System.out.println(\\\"No parameters: \\\" + c.add());\\n        System.out.println(\\\"Two integers: \\\" + c.add(20, 30));\\n        System.out.println(\\\"Three floats: \\\" + c.add(1.5f, 2.5f, 3.5f));\\n    }\\n}\"\n                }\n            ]\n        },\n        \"4\": {\n            \"title\": \"Exp 04: Single Inheritance\",\n            \"notes\": \"\",\n            \"filename\": \"SingleInheritance.java\",\n            \"language\": \"java\",\n            \"code\": \"class Person {\\n    String name = \\\"Varun\\\";\\n    int age = 20;\\n}\\n\\nclass Student extends Person {\\n    String course = \\\"B.Tech\\\";\\n    int roll = 101;\\n\\n    public static void main(String[] args) {\\n        Student s = new Student();\\n        System.out.println(\\\"Name: \\\" + s.name + \\\", Age: \\\" + s.age);\\n        System.out.println(\\\"Course: \\\" + s.course + \\\", Roll: \\\" + s.roll);\\n    }\\n}\",\n            \"files\": [\n                {\n                    \"name\": \"SingleInheritance.java\",\n                    \"language\": \"java\",\n                    \"code\": \"class Person {\\n    String name = \\\"Varun\\\";\\n    int age = 20;\\n}\\n\\nclass Student extends Person {\\n    String course = \\\"B.Tech\\\";\\n    int roll = 101;\\n\\n    public static void main(String[] args) {\\n        Student s = new Student();\\n        System.out.println(\\\"Name: \\\" + s.name + \\\", Age: \\\" + s.age);\\n        System.out.println(\\\"Course: \\\" + s.course + \\\", Roll: \\\" + s.roll);\\n    }\\n}\"\n                }\n            ]\n        },\n        \"5\": {\n            \"title\": \"Exp 05: Multilevel Inheritance\",\n            \"notes\": \"\",\n            \"filename\": \"MultilevelInheritance.java\",\n            \"language\": \"java\",\n            \"code\": \"class Person {\\n    String name = \\\"Varun\\\";\\n}\\n\\nclass Student extends Person {\\n    String course = \\\"B.Tech\\\";\\n}\\n\\nclass GraduateStudent extends Student {\\n    int year = 2026;\\n\\n    public static void main(String[] args) {\\n        GraduateStudent g = new GraduateStudent();\\n        System.out.println(\\\"Name: \\\" + g.name);\\n        System.out.println(\\\"Course: \\\" + g.course);\\n        System.out.println(\\\"Graduation Year: \\\" + g.year);\\n    }\\n}\",\n            \"files\": [\n                {\n                    \"name\": \"MultilevelInheritance.java\",\n                    \"language\": \"java\",\n                    \"code\": \"class Person {\\n    String name = \\\"Varun\\\";\\n}\\n\\nclass Student extends Person {\\n    String course = \\\"B.Tech\\\";\\n}\\n\\nclass GraduateStudent extends Student {\\n    int year = 2026;\\n\\n    public static void main(String[] args) {\\n        GraduateStudent g = new GraduateStudent();\\n        System.out.println(\\\"Name: \\\" + g.name);\\n        System.out.println(\\\"Course: \\\" + g.course);\\n        System.out.println(\\\"Graduation Year: \\\" + g.year);\\n    }\\n}\"\n                }\n            ]\n        },\n        \"6\": {\n            \"title\": \"Exp 06: Hierarchical Inheritance\",\n            \"notes\": \"\",\n            \"filename\": \"HierarchicalInheritance.java\",\n            \"language\": \"java\",\n            \"code\": \"class Person {\\n    String college = \\\"ABC College\\\";\\n}\\n\\nclass Student extends Person {\\n    String course = \\\"B.Tech\\\";\\n}\\n\\nclass Teacher extends Person {\\n    String subject = \\\"Java\\\";\\n}\\n\\nclass Administrator extends Person {\\n    String dept = \\\"Admissions\\\";\\n}\\n\\npublic class HierarchicalInheritance {\\n    public static void main(String[] args) {\\n        Student s = new Student();\\n        Teacher t = new Teacher();\\n        Administrator a = new Administrator();\\n        System.out.println(\\\"Student: \\\" + s.course + \\\" (\\\" + s.college + \\\")\\\");\\n        System.out.println(\\\"Teacher: \\\" + t.subject + \\\" (\\\" + t.college + \\\")\\\");\\n        System.out.println(\\\"Administrator: \\\" + a.dept + \\\" (\\\" + a.college + \\\")\\\");\\n    }\\n}\",\n            \"files\": [\n                {\n                    \"name\": \"HierarchicalInheritance.java\",\n                    \"language\": \"java\",\n                    \"code\": \"class Person {\\n    String college = \\\"ABC College\\\";\\n}\\n\\nclass Student extends Person {\\n    String course = \\\"B.Tech\\\";\\n}\\n\\nclass Teacher extends Person {\\n    String subject = \\\"Java\\\";\\n}\\n\\nclass Administrator extends Person {\\n    String dept = \\\"Admissions\\\";\\n}\\n\\npublic class HierarchicalInheritance {\\n    public static void main(String[] args) {\\n        Student s = new Student();\\n        Teacher t = new Teacher();\\n        Administrator a = new Administrator();\\n        System.out.println(\\\"Student: \\\" + s.course + \\\" (\\\" + s.college + \\\")\\\");\\n        System.out.println(\\\"Teacher: \\\" + t.subject + \\\" (\\\" + t.college + \\\")\\\");\\n        System.out.println(\\\"Administrator: \\\" + a.dept + \\\" (\\\" + a.college + \\\")\\\");\\n    }\\n}\"\n                }\n            ]\n        },\n        \"7\": {\n            \"title\": \"Exp 07: Servlet to display a welcome message (no web.xml)\",\n            \"notes\": \"Run at: http://localhost:8080/YourProject/welcome (For Tomcat 10+, use jakarta.servlet instead of javax.servlet)\",\n            \"filename\": \"WelcomeServlet.java\",\n            \"language\": \"java\",\n            \"code\": \"import java.io.*;\\nimport javax.servlet.annotation.WebServlet;\\nimport javax.servlet.http.*;\\n\\n@WebServlet(\\\"/welcome\\\")\\npublic class WelcomeServlet extends HttpServlet {\\n    protected void doGet(HttpServletRequest req, HttpServletResponse res) throws IOException {\\n        res.setContentType(\\\"text/html\\\");\\n        res.getWriter().println(\\\"<h1>Welcome to Servlet Programming!</h1>\\\");\\n    }\\n}\",\n            \"files\": [\n                {\n                    \"name\": \"WelcomeServlet.java\",\n                    \"language\": \"java\",\n                    \"code\": \"import java.io.*;\\nimport javax.servlet.annotation.WebServlet;\\nimport javax.servlet.http.*;\\n\\n@WebServlet(\\\"/welcome\\\")\\npublic class WelcomeServlet extends HttpServlet {\\n    protected void doGet(HttpServletRequest req, HttpServletResponse res) throws IOException {\\n        res.setContentType(\\\"text/html\\\");\\n        res.getWriter().println(\\\"<h1>Welcome to Servlet Programming!</h1>\\\");\\n    }\\n}\"\n                }\n            ]\n        },\n        \"8\": {\n            \"title\": \"Exp 08: Servlet to accept a name from an HTML form (no web.xml)\",\n            \"notes\": \"\",\n            \"files\": [\n                {\n                    \"name\": \"index.html\",\n                    \"language\": \"html\",\n                    \"code\": \"<form action=\\\"hello\\\" method=\\\"post\\\">\\n    Enter your name: <input type=\\\"text\\\" name=\\\"username\\\">\\n    <input type=\\\"submit\\\" value=\\\"Submit\\\">\\n</form>\"\n                },\n                {\n                    \"name\": \"HelloServlet.java\",\n                    \"language\": \"java\",\n                    \"code\": \"import java.io.*;\\nimport javax.servlet.annotation.WebServlet;\\nimport javax.servlet.http.*;\\n\\n@WebServlet(\\\"/hello\\\")\\npublic class HelloServlet extends HttpServlet {\\n    protected void doPost(HttpServletRequest req, HttpServletResponse res) throws IOException {\\n        res.setContentType(\\\"text/html\\\");\\n        res.getWriter().println(\\\"<h2>Hello, \\\" + req.getParameter(\\\"username\\\") + \\\"!</h2>\\\");\\n    }\\n}\"\n                }\n            ]\n        },\n        \"9\": {\n            \"title\": \"Exp 09: JSP welcome message\",\n            \"notes\": \"\",\n            \"filename\": \"welcome.jsp\",\n            \"language\": \"jsp\",\n            \"code\": \"<html>\\n<body>\\n    <h1>Welcome to JSP Programming!</h1>\\n</body>\\n</html>\",\n            \"files\": [\n                {\n                    \"name\": \"welcome.jsp\",\n                    \"language\": \"jsp\",\n                    \"code\": \"<html>\\n<body>\\n    <h1>Welcome to JSP Programming!</h1>\\n</body>\\n</html>\"\n                }\n            ]\n        },\n        \"10\": {\n            \"title\": \"Exp 10: JSP to display name, register number and department\",\n            \"notes\": \"\",\n            \"filename\": \"details.jsp\",\n            \"language\": \"jsp\",\n            \"code\": \"<html>\\n<body>\\n    <%\\n        String name = \\\"Varun\\\", regNo = \\\"2021001\\\", dept = \\\"Computer Science\\\";\\n    %>\\n    <h2>Student Details</h2>\\n    <p>Name: <%= name %></p>\\n    <p>Register Number: <%= regNo %></p>\\n    <p>Department: <%= dept %></p>\\n</body>\\n</html>\",\n            \"files\": [\n                {\n                    \"name\": \"details.jsp\",\n                    \"language\": \"jsp\",\n                    \"code\": \"<html>\\n<body>\\n    <%\\n        String name = \\\"Varun\\\", regNo = \\\"2021001\\\", dept = \\\"Computer Science\\\";\\n    %>\\n    <h2>Student Details</h2>\\n    <p>Name: <%= name %></p>\\n    <p>Register Number: <%= regNo %></p>\\n    <p>Department: <%= dept %></p>\\n</body>\\n</html>\"\n                }\n            ]\n        },\n        \"11\": {\n            \"title\": \"Exp 11: JDBC application (insert, update, delete, display)\",\n            \"notes\": \"Run SQL in MySQL first: CREATE DATABASE college; USE college; CREATE TABLE student (roll INT PRIMARY KEY, name VARCHAR(50), marks FLOAT);\",\n            \"files\": [\n                {\n                    \"name\": \"student.sql\",\n                    \"language\": \"sql\",\n                    \"code\": \"CREATE DATABASE college;\\nUSE college;\\nCREATE TABLE student (roll INT PRIMARY KEY, name VARCHAR(50), marks FLOAT);\"\n                },\n                {\n                    \"name\": \"StudentJDBC.java\",\n                    \"language\": \"java\",\n                    \"code\": \"import java.sql.*;\\nimport java.util.Scanner;\\n\\npublic class StudentJDBC {\\n    public static void main(String[] args) throws Exception {\\n        Connection con = DriverManager.getConnection(\\n                \\\"jdbc:mysql://localhost:3306/college\\\", \\\"root\\\", \\\"password\\\");\\n        Scanner sc = new Scanner(System.in);\\n        int ch;\\n\\n        do {\\n            System.out.print(\\\"\\\\n1.Insert 2.Update 3.Delete 4.Display 5.Exit: \\\");\\n            ch = sc.nextInt();\\n\\n            if (ch == 1) {\\n                System.out.print(\\\"Enter roll, name, marks: \\\");\\n                PreparedStatement ps = con.prepareStatement(\\\"INSERT INTO student VALUES (?,?,?)\\\");\\n                ps.setInt(1, sc.nextInt());\\n                ps.setString(2, sc.next());\\n                ps.setFloat(3, sc.nextFloat());\\n                ps.executeUpdate();\\n                System.out.println(\\\"Record inserted.\\\");\\n            } else if (ch == 2) {\\n                System.out.print(\\\"Enter roll and new marks: \\\");\\n                PreparedStatement ps = con.prepareStatement(\\\"UPDATE student SET marks=? WHERE roll=?\\\");\\n                int roll = sc.nextInt();\\n                ps.setFloat(1, sc.nextFloat());\\n                ps.setInt(2, roll);\\n                ps.executeUpdate();\\n                System.out.println(\\\"Record updated.\\\");\\n            } else if (ch == 3) {\\n                System.out.print(\\\"Enter roll to delete: \\\");\\n                PreparedStatement ps = con.prepareStatement(\\\"DELETE FROM student WHERE roll=?\\\");\\n                ps.setInt(1, sc.nextInt());\\n                ps.executeUpdate();\\n                System.out.println(\\\"Record deleted.\\\");\\n            } else if (ch == 4) {\\n                ResultSet rs = con.createStatement().executeQuery(\\\"SELECT * FROM student\\\");\\n                while (rs.next())\\n                    System.out.println(rs.getInt(1) + \\\" \\\" + rs.getString(2) + \\\" \\\" + rs.getFloat(3));\\n            }\\n        } while (ch != 5);\\n\\n        con.close();\\n    }\\n}\"\n                }\n            ]\n        },\n        \"12\": {\n            \"title\": \"Exp 12: Student registration form with CSS\",\n            \"notes\": \"\",\n            \"filename\": \"index.html\",\n            \"language\": \"html\",\n            \"code\": \"<!DOCTYPE html>\\n<html>\\n<head>\\n    <title>Student Registration</title>\\n    <style>\\n        form { width: 280px; margin: 40px auto; padding: 20px; border: 1px solid gray; font-family: Arial; }\\n        input, select, button { width: 100%; padding: 8px; margin: 6px 0; box-sizing: border-box; }\\n        button { background: green; color: white; border: none; }\\n    </style>\\n</head>\\n<body>\\n    <form>\\n        <h3>Student Registration</h3>\\n        <input type=\\\"text\\\" placeholder=\\\"Enter Name\\\">\\n        <input type=\\\"email\\\" placeholder=\\\"Enter Email\\\">\\n        <input type=\\\"password\\\" placeholder=\\\"Enter Password\\\">\\n        <select>\\n            <option>B.Tech</option>\\n            <option>BCA</option>\\n            <option>MCA</option>\\n        </select>\\n        <button type=\\\"submit\\\">Register</button>\\n    </form>\\n</body>\\n</html>\",\n            \"files\": [\n                {\n                    \"name\": \"index.html\",\n                    \"language\": \"html\",\n                    \"code\": \"<!DOCTYPE html>\\n<html>\\n<head>\\n    <title>Student Registration</title>\\n    <style>\\n        form { width: 280px; margin: 40px auto; padding: 20px; border: 1px solid gray; font-family: Arial; }\\n        input, select, button { width: 100%; padding: 8px; margin: 6px 0; box-sizing: border-box; }\\n        button { background: green; color: white; border: none; }\\n    </style>\\n</head>\\n<body>\\n    <form>\\n        <h3>Student Registration</h3>\\n        <input type=\\\"text\\\" placeholder=\\\"Enter Name\\\">\\n        <input type=\\\"email\\\" placeholder=\\\"Enter Email\\\">\\n        <input type=\\\"password\\\" placeholder=\\\"Enter Password\\\">\\n        <select>\\n            <option>B.Tech</option>\\n            <option>BCA</option>\\n            <option>MCA</option>\\n        </select>\\n        <button type=\\\"submit\\\">Register</button>\\n    </form>\\n</body>\\n</html>\"\n                }\n            ]\n        },\n        \"13\": {\n            \"title\": \"Exp 13: College department webpage\",\n            \"notes\": \"\",\n            \"filename\": \"index.html\",\n            \"language\": \"html\",\n            \"code\": \"<!DOCTYPE html>\\n<html>\\n<head>\\n    <title>CSE Department</title>\\n    <style>\\n        body { font-family: Arial; margin: 0; }\\n        header, footer { background: navy; color: white; text-align: center; padding: 10px; }\\n        nav { background: #ddd; text-align: center; padding: 6px; }\\n        section { padding: 10px 20px; }\\n        table, th, td { border: 1px solid black; border-collapse: collapse; padding: 6px; }\\n    </style>\\n</head>\\n<body>\\n    <header><h2>Department of Computer Science</h2></header>\\n    <nav><a href=\\\"#faculty\\\">Faculty</a> | <a href=\\\"#courses\\\">Courses</a> | <a href=\\\"#contact\\\">Contact</a></nav>\\n\\n    <section id=\\\"faculty\\\">\\n        <h3>Faculty</h3>\\n        <table>\\n            <tr><th>Name</th><th>Designation</th></tr>\\n            <tr><td>Dr. Ravi Kumar</td><td>Professor &amp; HOD</td></tr>\\n            <tr><td>Ms. Anita Sharma</td><td>Assistant Professor</td></tr>\\n        </table>\\n    </section>\\n\\n    <section id=\\\"courses\\\">\\n        <h3>Courses</h3>\\n        <table>\\n            <tr><th>Course</th><th>Duration</th></tr>\\n            <tr><td>B.Tech CSE</td><td>4 Years</td></tr>\\n            <tr><td>MCA</td><td>2 Years</td></tr>\\n        </table>\\n    </section>\\n\\n    <section id=\\\"contact\\\">\\n        <h3>Contact</h3>\\n        <p>Email: cse@abccollege.edu | Phone: 044-12345678</p>\\n    </section>\\n\\n    <footer>&copy; 2026 CSE Department</footer>\\n</body>\\n</html>\",\n            \"files\": [\n                {\n                    \"name\": \"index.html\",\n                    \"language\": \"html\",\n                    \"code\": \"<!DOCTYPE html>\\n<html>\\n<head>\\n    <title>CSE Department</title>\\n    <style>\\n        body { font-family: Arial; margin: 0; }\\n        header, footer { background: navy; color: white; text-align: center; padding: 10px; }\\n        nav { background: #ddd; text-align: center; padding: 6px; }\\n        section { padding: 10px 20px; }\\n        table, th, td { border: 1px solid black; border-collapse: collapse; padding: 6px; }\\n    </style>\\n</head>\\n<body>\\n    <header><h2>Department of Computer Science</h2></header>\\n    <nav><a href=\\\"#faculty\\\">Faculty</a> | <a href=\\\"#courses\\\">Courses</a> | <a href=\\\"#contact\\\">Contact</a></nav>\\n\\n    <section id=\\\"faculty\\\">\\n        <h3>Faculty</h3>\\n        <table>\\n            <tr><th>Name</th><th>Designation</th></tr>\\n            <tr><td>Dr. Ravi Kumar</td><td>Professor &amp; HOD</td></tr>\\n            <tr><td>Ms. Anita Sharma</td><td>Assistant Professor</td></tr>\\n        </table>\\n    </section>\\n\\n    <section id=\\\"courses\\\">\\n        <h3>Courses</h3>\\n        <table>\\n            <tr><th>Course</th><th>Duration</th></tr>\\n            <tr><td>B.Tech CSE</td><td>4 Years</td></tr>\\n            <tr><td>MCA</td><td>2 Years</td></tr>\\n        </table>\\n    </section>\\n\\n    <section id=\\\"contact\\\">\\n        <h3>Contact</h3>\\n        <p>Email: cse@abccollege.edu | Phone: 044-12345678</p>\\n    </section>\\n\\n    <footer>&copy; 2026 CSE Department</footer>\\n</body>\\n</html>\"\n                }\n            ]\n        },\n        \"14\": {\n            \"title\": \"Exp 14: JavaScript email validation\",\n            \"notes\": \"\",\n            \"filename\": \"index.html\",\n            \"language\": \"html\",\n            \"code\": \"<input type=\\\"text\\\" id=\\\"email\\\" placeholder=\\\"Enter email\\\">\\n<button onclick=\\\"validate()\\\">Validate</button>\\n<p id=\\\"res\\\"></p>\\n\\n<script>\\nfunction validate() {\\n    let e = document.getElementById(\\\"email\\\").value;\\n    let valid = /^[^\\\\s@]+@[^\\\\s@]+\\\\.[^\\\\s@]+$/.test(e);\\n    document.getElementById(\\\"res\\\").innerText = valid ? \\\"Valid Email ID\\\" : \\\"Invalid Email ID\\\";\\n}\\n</script>\",\n            \"files\": [\n                {\n                    \"name\": \"index.html\",\n                    \"language\": \"html\",\n                    \"code\": \"<input type=\\\"text\\\" id=\\\"email\\\" placeholder=\\\"Enter email\\\">\\n<button onclick=\\\"validate()\\\">Validate</button>\\n<p id=\\\"res\\\"></p>\\n\\n<script>\\nfunction validate() {\\n    let e = document.getElementById(\\\"email\\\").value;\\n    let valid = /^[^\\\\s@]+@[^\\\\s@]+\\\\.[^\\\\s@]+$/.test(e);\\n    document.getElementById(\\\"res\\\").innerText = valid ? \\\"Valid Email ID\\\" : \\\"Invalid Email ID\\\";\\n}\\n</script>\"\n                }\n            ]\n        },\n        \"15\": {\n            \"title\": \"Exp 15: Student registration form validation\",\n            \"notes\": \"\",\n            \"filename\": \"index.html\",\n            \"language\": \"html\",\n            \"code\": \"<form onsubmit=\\\"return validate()\\\">\\n    Name: <input id=\\\"n\\\"><br>\\n    Email: <input id=\\\"e\\\"><br>\\n    Password: <input type=\\\"password\\\" id=\\\"p\\\"><br>\\n    <input type=\\\"submit\\\" value=\\\"Register\\\">\\n</form>\\n\\n<script>\\nfunction validate() {\\n    if (n.value == \\\"\\\") { alert(\\\"Name is required\\\"); return false; }\\n    if (!/^[^\\\\s@]+@[^\\\\s@]+\\\\.[^\\\\s@]+$/.test(e.value)) { alert(\\\"Enter valid email\\\"); return false; }\\n    if (p.value.length < 6) { alert(\\\"Password must be 6+ chars\\\"); return false; }\\n    alert(\\\"Registration successful!\\\");\\n    return true;\\n}\\n</script>\",\n            \"files\": [\n                {\n                    \"name\": \"index.html\",\n                    \"language\": \"html\",\n                    \"code\": \"<form onsubmit=\\\"return validate()\\\">\\n    Name: <input id=\\\"n\\\"><br>\\n    Email: <input id=\\\"e\\\"><br>\\n    Password: <input type=\\\"password\\\" id=\\\"p\\\"><br>\\n    <input type=\\\"submit\\\" value=\\\"Register\\\">\\n</form>\\n\\n<script>\\nfunction validate() {\\n    if (n.value == \\\"\\\") { alert(\\\"Name is required\\\"); return false; }\\n    if (!/^[^\\\\s@]+@[^\\\\s@]+\\\\.[^\\\\s@]+$/.test(e.value)) { alert(\\\"Enter valid email\\\"); return false; }\\n    if (p.value.length < 6) { alert(\\\"Password must be 6+ chars\\\"); return false; }\\n    alert(\\\"Registration successful!\\\");\\n    return true;\\n}\\n</script>\"\n                }\n            ]\n        },\n        \"16\": {\n            \"title\": \"Exp 16: DOM: change background color every 5 seconds\",\n            \"notes\": \"\",\n            \"filename\": \"index.html\",\n            \"language\": \"html\",\n            \"code\": \"<!DOCTYPE html>\\n<html>\\n<body>\\n    <h2>Background changes every 5 seconds</h2>\\n\\n    <script>\\n        let colors = [\\\"lightblue\\\", \\\"lightgreen\\\", \\\"lightpink\\\", \\\"lightyellow\\\", \\\"lavender\\\"];\\n        let i = 0;\\n\\n        function changeColor() {\\n            document.body.style.backgroundColor = colors[i];\\n            i = (i + 1) % colors.length;\\n        }\\n\\n        changeColor();\\n        setInterval(changeColor, 5000);\\n    </script>\\n</body>\\n</html>\",\n            \"files\": [\n                {\n                    \"name\": \"index.html\",\n                    \"language\": \"html\",\n                    \"code\": \"<!DOCTYPE html>\\n<html>\\n<body>\\n    <h2>Background changes every 5 seconds</h2>\\n\\n    <script>\\n        let colors = [\\\"lightblue\\\", \\\"lightgreen\\\", \\\"lightpink\\\", \\\"lightyellow\\\", \\\"lavender\\\"];\\n        let i = 0;\\n\\n        function changeColor() {\\n            document.body.style.backgroundColor = colors[i];\\n            i = (i + 1) % colors.length;\\n        }\\n\\n        changeColor();\\n        setInterval(changeColor, 5000);\\n    </script>\\n</body>\\n</html>\"\n                }\n            ]\n        }\n    }\n}")

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
        return

    code = files[0].get("code", "").strip()
    if code:
        print(code)
    else:
        print("// (no code yet)")


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
    else:
        print("[warn] Could not access clipboard.")
        print("       Here is the code snippet:\n")
        print(code)


# -----------------------------------------------------------------------------
#  ENTRY POINT
# -----------------------------------------------------------------------------

USAGE = """\
helper.py -- Offline CLI study helper tool for Full Stack Java Programming (FSJP).

Usage:
  python helper.py fsjp <exp_num> [file|all]
  python helper.py <exp_num> [file|all]
  python helper.py list
  python helper.py show  [subject] <topic_or_exp> [file|all]
  python helper.py write [subject] <topic_or_exp> [filename|folder]
  python helper.py copy  [subject] <topic_or_exp> [file|all]

For FSJP experiments (Q1 to Q16), specify '1', 'exp1', 'exp 1', or 'q1'.
For multi-file experiments (Exp 8, Exp 11), pass a file number or 'all'.
"""

COMMANDS = {
    "list":  cmd_list,
    "show":  cmd_show,
    "write": cmd_write,
    "copy":  cmd_copy,
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
