import java.util.*;

public class DigitalWallet {

    // GCD Function
    static int gcd(int a, int b) {

        while (b != 0) {

            int temp = b;

            b = a % b;

            a = temp;
        }

        return a;
    }

    // Find Public Key e
    static int findE(int phi) {

        int e = 2;

        while (e < phi) {

            if (gcd(e, phi) == 1) {
                return e;
            }

            e++;
        }

        return -1;
    }

    // Find Private Key d
    static int findD(int e, int phi) {

        int d = 1;

        while ((d * e) % phi != 1) {
            d++;
        }

        return d;
    }

    public static void main(String[] args) {

        // Step 1: Choose Prime Numbers
        int p = 11;
        int q = 13;

        // Step 2: Calculate n = p*q
        int n = p * q;

        // Step 3: Calculate Euler Totient phi(n)
        int phi = (p - 1) * (q - 1);

        // Step 4: Generate Public Key
        int e = findE(phi);

        // Step 5: Generate Private Key
        int d = findD(e, phi);

        // Step 6: Display Wallet Information
        System.out.println("===== DIGITAL WALLET =====");

        System.out.println("Public Key: (" + e + ", " + n + ")");

        System.out.println("Private Key: (" + d + ", " + n + ")");

        /*
        OUTPUT STEPS

        Step 1:
        Choose two prime numbers
        p = 11
        q = 13

        Step 2:
        Calculate n
        n = p * q
        n = 143

        Step 3:
        Calculate phi(n)
        phi = (p-1)*(q-1)
        phi = 120

        Step 4:
        Find public key e
        e = 7

        Step 5:
        Find private key d
        d = 103

        Step 6:
        Display Digital Wallet Keys
        Public Key  = (7,143)
        Private Key = (103,143)
        */
    }
}