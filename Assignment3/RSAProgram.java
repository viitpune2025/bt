import java.util.*;
import java.io.*;

public class RSAProgram {

    public static String asciiVectorToWord(List<Integer> asciiValues) {
        StringBuilder result = new StringBuilder();

        for (int val : asciiValues) {
            result.append((char) val);
        }

        return result.toString();
    }

    public static boolean isPrime(int n) {
        if (n <= 1)
            return false;

        if (n <= 3)
            return true;

        if (n % 2 == 0 || n % 3 == 0)
            return false;

        for (int i = 5; i * i <= n; i += 6) {
            if (n % i == 0 || n % (i + 2) == 0)
                return false;
        }

        return true;
    }

    public static List<int[]> getOddPairs(int minProd, int maxProd) {

        List<int[]> pairs = new ArrayList<>();

        for (int i = 3; i < maxProd; i += 2) {

            for (int j = i; j < maxProd; j += 2) {

                int product = i * j;

                if (product > minProd && product < maxProd) {
                    pairs.add(new int[]{i, j});
                }
            }
        }

        return pairs;
    }

    public static int find_d(int e, int fi_n) {

        for (int d = 1; d < fi_n; d++) {

            if ((e * d) % fi_n == 1) {
                return d;
            }
        }

        return -1;
    }

    public static int gcd(int a, int b) {

        while (b != 0) {

            int temp = b;
            b = a % b;
            a = temp;
        }

        return a;
    }

    public static List<Integer> find_ascii_value(String message) {

        List<Integer> temp = new ArrayList<>();

        for (char character : message.toCharArray()) {
            temp.add((int) character);
        }

        return temp;
    }

    public static int find_e(int p, int q) {

        int fi_n = (p - 1) * (q - 1);

        int e = 3;

        while (gcd(e, fi_n) != 1) {
            e++;
        }

        return e;
    }

    public static int find_n(int p, int q) {
        return p * q;
    }

    public static int find_fi_n(int p, int q) {
        return (p - 1) * (q - 1);
    }

    public static int mod_exp(int base, int exp, int mod) {

        int result = 1;

        for (int i = 0; i < exp; i++) {
            result = (result * base) % mod;
        }

        return result;
    }

    public static void find_keys(String message) {

        List<int[]> oddPairs = getOddPairs(128, 255);

        if (oddPairs.isEmpty()) {
            System.out.println("No valid odd pairs found!");
            return;
        }

        System.out.println("All Possible Odd Pairs (Product between 128 and 255):");

        for (int[] pair : oddPairs) {
            System.out.print("(" + pair[0] + ", " + pair[1] + ") ");
        }

        System.out.println("\n");

        Random rand = new Random();

        int[] selectedPair = oddPairs.get(rand.nextInt(oddPairs.size()));

        int p = selectedPair[0];
        int q = selectedPair[1];

        System.out.println("Selected Pair: (" + p + ", " + q + ")");

        int n = find_n(p, q);

        int e = find_e(p, q);

        int d = find_d(e, find_fi_n(p, q));

        System.out.println("Public Key : (" + e + "," + n + ")");

        System.out.println("Private Key : (" + d + "," + n + ")");
    }

    public static void Encrypt_Message(String message, Scanner sc) {

        int public_key_e, public_key_n;

        System.out.print("Enter Public Key (e,n) : ");

        public_key_e = sc.nextInt();
        public_key_n = sc.nextInt();

        List<Integer> message_v = find_ascii_value(message);

        System.out.print("Encrypted Message is : ");

        for (int val : message_v) {

            int c = mod_exp(val, public_key_e, public_key_n);

            System.out.print(c + " ");
        }

        System.out.println();
    }

    public static void Decrypt_Message(int length, Scanner sc) {

        int d_message;

        int private_key_e, private_key_n;

        System.out.print("Enter Private Key (e,n) : ");

        private_key_e = sc.nextInt();
        private_key_n = sc.nextInt();

        List<Integer> dec_message = new ArrayList<>();

        System.out.println("Enter the Encrypted message : ");

        for (int i = 0; i < length; i++) {

            d_message = sc.nextInt();

            int c = mod_exp(d_message, private_key_e, private_key_n);

            dec_message.add(c);
        }

        System.out.print("Decrypted Message (ASCII) : ");

        for (int val : dec_message) {
            System.out.print(val + " ");
        }

        System.out.println();

        String final_text = asciiVectorToWord(dec_message);

        System.out.println("The Final Converted Text is : " + final_text);
    }

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        int choice;

        String message = "";

        try {

            BufferedReader br = new BufferedReader(new FileReader("message.txt"));

            message = br.readLine();

            br.close();

        } catch (IOException e) {

            System.out.println("Error: Unable to open message.txt");

            return;
        }

        System.out.println("Message Read From File: " + message);

        int length = message.length();

        do {

            System.out.println("\nChoose Operation:");
            System.out.println("1. Generate Keys (Using Odd Pairs)");
            System.out.println("2. Encrypt Message");
            System.out.println("3. Decrypt Message");
            System.out.println("4. Exit");

            choice = sc.nextInt();

            switch (choice) {

                case 1:
                    find_keys(message);
                    break;

                case 2:
                    Encrypt_Message(message, sc);
                    break;

                case 3:
                    Decrypt_Message(length, sc);
                    break;

                case 4:
                    System.out.println("Exiting Program");
                    break;

                default:
                    System.out.println("Invalid choice");
            }

        } while (choice != 4);

        sc.close();
    }
}