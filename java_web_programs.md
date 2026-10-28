# Java, Servlet, JSP, JDBC and Web Programs (Q1 to Q16)

Servlets use @WebServlet, so no web.xml is needed.

---

## Q1. Student class with inputDetails() and displayDetails()

```java
import java.util.Scanner;

class Student {
    String name;
    int rollNumber;
    float marks;

    void inputDetails() {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter name: ");
        name = sc.nextLine();
        System.out.print("Enter roll number: ");
        rollNumber = sc.nextInt();
        System.out.print("Enter marks: ");
        marks = sc.nextFloat();
    }

    void displayDetails() {
        System.out.println("Name: " + name + ", Roll: " + rollNumber + ", Marks: " + marks);
    }

    public static void main(String[] args) {
        Student s = new Student();
        s.inputDetails();
        s.displayDetails();
    }
}
```

---

## Q2. Constructor Overloading

```java
class Calculator {
    Calculator() {
        System.out.println("Welcome to Calculator!");
    }

    Calculator(int a, int b) {
        System.out.println("Sum = " + (a + b));
    }

    public static void main(String[] args) {
        new Calculator();
        new Calculator(10, 20);
    }
}
```

---

## Q3. Method Overloading

```java
class Calculator {
    int add() { return 5 + 10; }
    int add(int a, int b) { return a + b; }
    float add(float a, float b, float c) { return a + b + c; }

    public static void main(String[] args) {
        Calculator c = new Calculator();
        System.out.println("No parameters: " + c.add());
        System.out.println("Two integers: " + c.add(20, 30));
        System.out.println("Three floats: " + c.add(1.5f, 2.5f, 3.5f));
    }
}
```

---

## Q4. Single Inheritance

```java
class Person {
    String name = "Varun";
    int age = 20;
}

class Student extends Person {
    String course = "B.Tech";
    int roll = 101;

    public static void main(String[] args) {
        Student s = new Student();
        System.out.println("Name: " + s.name + ", Age: " + s.age);
        System.out.println("Course: " + s.course + ", Roll: " + s.roll);
    }
}
```

---

## Q5. Multilevel Inheritance

```java
class Person {
    String name = "Varun";
}

class Student extends Person {
    String course = "B.Tech";
}

class GraduateStudent extends Student {
    int year = 2026;

    public static void main(String[] args) {
        GraduateStudent g = new GraduateStudent();
        System.out.println("Name: " + g.name);
        System.out.println("Course: " + g.course);
        System.out.println("Graduation Year: " + g.year);
    }
}
```

---

## Q6. Hierarchical Inheritance

```java
class Person {
    String college = "ABC College";
}

class Student extends Person {
    String course = "B.Tech";
}

class Teacher extends Person {
    String subject = "Java";
}

class Administrator extends Person {
    String dept = "Admissions";
}

public class HierarchicalInheritance {
    public static void main(String[] args) {
        Student s = new Student();
        Teacher t = new Teacher();
        Administrator a = new Administrator();
        System.out.println("Student: " + s.course + " (" + s.college + ")");
        System.out.println("Teacher: " + t.subject + " (" + t.college + ")");
        System.out.println("Administrator: " + a.dept + " (" + a.college + ")");
    }
}
```

---

## Q7. Servlet to display a welcome message (no web.xml)

WelcomeServlet.java. Run at: `http://localhost:8080/YourProject/welcome`

```java
import java.io.*;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;

@WebServlet("/welcome")
public class WelcomeServlet extends HttpServlet {
    protected void doGet(HttpServletRequest req, HttpServletResponse res) throws IOException {
        res.setContentType("text/html");
        res.getWriter().println("<h1>Welcome to Servlet Programming!</h1>");
    }
}
```

> For Tomcat 10 or newer, use `jakarta.servlet` instead of `javax.servlet`.

---

## Q8. Servlet to accept a name from an HTML form (no web.xml)

index.html

```html
<form action="hello" method="post">
    Enter your name: <input type="text" name="username">
    <input type="submit" value="Submit">
</form>
```

HelloServlet.java

```java
import java.io.*;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;

@WebServlet("/hello")
public class HelloServlet extends HttpServlet {
    protected void doPost(HttpServletRequest req, HttpServletResponse res) throws IOException {
        res.setContentType("text/html");
        res.getWriter().println("<h2>Hello, " + req.getParameter("username") + "!</h2>");
    }
}
```

---

## Q9. JSP welcome message

welcome.jsp

```jsp
<html>
<body>
    <h1>Welcome to JSP Programming!</h1>
</body>
</html>
```

---

## Q10. JSP to display name, register number and department

details.jsp

```jsp
<html>
<body>
    <%
        String name = "Varun", regNo = "2021001", dept = "Computer Science";
    %>
    <h2>Student Details</h2>
    <p>Name: <%= name %></p>
    <p>Register Number: <%= regNo %></p>
    <p>Department: <%= dept %></p>
</body>
</html>
```

---

## Q11. JDBC application (insert, update, delete, display)

Run this in MySQL first (add mysql-connector-j.jar to the classpath):

```sql
CREATE DATABASE college;
USE college;
CREATE TABLE student (roll INT PRIMARY KEY, name VARCHAR(50), marks FLOAT);
```

StudentJDBC.java

```java
import java.sql.*;
import java.util.Scanner;

public class StudentJDBC {
    public static void main(String[] args) throws Exception {
        Connection con = DriverManager.getConnection(
                "jdbc:mysql://localhost:3306/college", "root", "password");
        Scanner sc = new Scanner(System.in);
        int ch;

        do {
            System.out.print("\n1.Insert 2.Update 3.Delete 4.Display 5.Exit: ");
            ch = sc.nextInt();

            if (ch == 1) {
                System.out.print("Enter roll, name, marks: ");
                PreparedStatement ps = con.prepareStatement("INSERT INTO student VALUES (?,?,?)");
                ps.setInt(1, sc.nextInt());
                ps.setString(2, sc.next());
                ps.setFloat(3, sc.nextFloat());
                ps.executeUpdate();
                System.out.println("Record inserted.");
            } else if (ch == 2) {
                System.out.print("Enter roll and new marks: ");
                PreparedStatement ps = con.prepareStatement("UPDATE student SET marks=? WHERE roll=?");
                int roll = sc.nextInt();
                ps.setFloat(1, sc.nextFloat());
                ps.setInt(2, roll);
                ps.executeUpdate();
                System.out.println("Record updated.");
            } else if (ch == 3) {
                System.out.print("Enter roll to delete: ");
                PreparedStatement ps = con.prepareStatement("DELETE FROM student WHERE roll=?");
                ps.setInt(1, sc.nextInt());
                ps.executeUpdate();
                System.out.println("Record deleted.");
            } else if (ch == 4) {
                ResultSet rs = con.createStatement().executeQuery("SELECT * FROM student");
                while (rs.next())
                    System.out.println(rs.getInt(1) + " " + rs.getString(2) + " " + rs.getFloat(3));
            }
        } while (ch != 5);

        con.close();
    }
}
```

---

## Q12. Student registration form with CSS

```html
<!DOCTYPE html>
<html>
<head>
    <title>Student Registration</title>
    <style>
        form { width: 280px; margin: 40px auto; padding: 20px; border: 1px solid gray; font-family: Arial; }
        input, select, button { width: 100%; padding: 8px; margin: 6px 0; box-sizing: border-box; }
        button { background: green; color: white; border: none; }
    </style>
</head>
<body>
    <form>
        <h3>Student Registration</h3>
        <input type="text" placeholder="Enter Name">
        <input type="email" placeholder="Enter Email">
        <input type="password" placeholder="Enter Password">
        <select>
            <option>B.Tech</option>
            <option>BCA</option>
            <option>MCA</option>
        </select>
        <button type="submit">Register</button>
    </form>
</body>
</html>
```

---

## Q13. College department webpage

```html
<!DOCTYPE html>
<html>
<head>
    <title>CSE Department</title>
    <style>
        body { font-family: Arial; margin: 0; }
        header, footer { background: navy; color: white; text-align: center; padding: 10px; }
        nav { background: #ddd; text-align: center; padding: 6px; }
        section { padding: 10px 20px; }
        table, th, td { border: 1px solid black; border-collapse: collapse; padding: 6px; }
    </style>
</head>
<body>
    <header><h2>Department of Computer Science</h2></header>
    <nav><a href="#faculty">Faculty</a> | <a href="#courses">Courses</a> | <a href="#contact">Contact</a></nav>

    <section id="faculty">
        <h3>Faculty</h3>
        <table>
            <tr><th>Name</th><th>Designation</th></tr>
            <tr><td>Dr. Ravi Kumar</td><td>Professor &amp; HOD</td></tr>
            <tr><td>Ms. Anita Sharma</td><td>Assistant Professor</td></tr>
        </table>
    </section>

    <section id="courses">
        <h3>Courses</h3>
        <table>
            <tr><th>Course</th><th>Duration</th></tr>
            <tr><td>B.Tech CSE</td><td>4 Years</td></tr>
            <tr><td>MCA</td><td>2 Years</td></tr>
        </table>
    </section>

    <section id="contact">
        <h3>Contact</h3>
        <p>Email: cse@abccollege.edu | Phone: 044-12345678</p>
    </section>

    <footer>&copy; 2026 CSE Department</footer>
</body>
</html>
```

---

## Q14. JavaScript email validation

```html
<input type="text" id="email" placeholder="Enter email">
<button onclick="validate()">Validate</button>
<p id="res"></p>

<script>
function validate() {
    let e = document.getElementById("email").value;
    let valid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e);
    document.getElementById("res").innerText = valid ? "Valid Email ID" : "Invalid Email ID";
}
</script>
```

---

## Q15. Student registration form validation

```html
<form onsubmit="return validate()">
    Name: <input id="n"><br>
    Email: <input id="e"><br>
    Password: <input type="password" id="p"><br>
    <input type="submit" value="Register">
</form>

<script>
function validate() {
    if (n.value == "") { alert("Name is required"); return false; }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e.value)) { alert("Enter valid email"); return false; }
    if (p.value.length < 6) { alert("Password must be 6+ chars"); return false; }
    alert("Registration successful!");
    return true;
}
</script>
```

---

## Q16. DOM: change background color every 5 seconds

```html
<!DOCTYPE html>
<html>
<body>
    <h2>Background changes every 5 seconds</h2>

    <script>
        let colors = ["lightblue", "lightgreen", "lightpink", "lightyellow", "lavender"];
        let i = 0;

        function changeColor() {
            document.body.style.backgroundColor = colors[i];
            i = (i + 1) % colors.length;
        }

        changeColor();
        setInterval(changeColor, 5000);
    </script>
</body>
</html>
```
