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