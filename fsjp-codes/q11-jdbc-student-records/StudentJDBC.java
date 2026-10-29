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