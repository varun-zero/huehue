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