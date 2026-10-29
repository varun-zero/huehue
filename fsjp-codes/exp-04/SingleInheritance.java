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