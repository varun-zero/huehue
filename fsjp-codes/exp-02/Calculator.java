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