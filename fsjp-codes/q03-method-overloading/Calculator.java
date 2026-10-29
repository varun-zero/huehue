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