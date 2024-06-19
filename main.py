import math


# A function to print all prime factors of a given number n
def prime_factors(n):
    a = []

    # Print the number of two's that divide n
    while n % 2 == 0:
        a.append(2)
        n = n // 2

    # n must be odd at this point
    # so a skip of 2 ( i = i + 2) can be used
    for i in range(3, int(math.sqrt(n)) + 1, 2):

        # While i divides n , print i ad divide n
        while n % i == 0:
            a.append(i)
            n = n // i

    # Condition if n is a prime
    # Number greater than 2
    if n > 2:
        a.append(n)

    return a


# Check if n is prime
def is_prime(n):
    for i in range(2, n):
        if (n % i) == 0:
            return False
    return True


# Check if two arrays have at least one common element
def common_elem(arr1, arr2):
    for x in arr1:
        for y in arr2:
            if x == y:
                return True

    return False


# Extended euclidian algorithm
# Finds GCD of two numbers
# Finds integers (t and s) to represent the GCD as a linear combination with the two original numbers
# GCD(a,b) = d * a + k * b
def ext_gcd(a, b) -> tuple[int, int, int]:
    if b == 0:
        return a, 1, 0
    else:
        gct, u, d = ext_gcd(b, a % b)
        q = a // b
        k = u - q * d
        return gct, d, k


# Create public and private key
def createKeys():
    # Enter prime numbers p and q to calculate N and φ(N)
    invalid = True
    while invalid:
        print("Only enter prime numbers less than 1000 and are not equal")
        print("p = ", end="")
        p = int(input())
        print("q = ", end="")
        q = int(input())

        if q >= 1000 or q < 2 or not is_prime(q):
            print("q is an invalid number")
            invalid = True
        elif p >= 1000 or p < 2 or not is_prime(p):
            print("p is an invalid number")
            invalid = True
        elif p == q:
            print("p and q are not allowed to be equal")
        else:
            invalid = False

    N = p * q
    print("N =", str(N), end=", ")
    phi = (p - 1) * (q - 1)
    print("φ(N) =", str(phi))

    # Enter encryption exponent e which is coprime to φ(N)
    invalid = True
    while invalid:
        print(
            "Choose a number e that is coprime to φ(N) = "
            + str(phi)
            + " for which 1 < e < φ(N) - 1: ",
            end="",
        )
        e = int(input())

        if e < 2 or e >= phi - 1:
            print("e is not in the valid range")
            input()
            continue

        prime_factors_phi = prime_factors(phi)
        prime_factors_e = prime_factors(e)
        if common_elem(prime_factors_phi, prime_factors_e):
            print("e is not coprime to φ(N)" + str(phi))
        else:
            invalid = False

    # Calculate decryption exponent d using the extended euclidean algorithm
    # e * d + k * φ(N) = GCT(a,b) = 1
    d = ext_gcd(e, phi)[1]

    # A negative encryption exponent won't work
    # Adding φ(N) doesn't change the result
    if d < 0 and (d + phi > 0):
        d += phi
    else:
        return print(
            "Your decryption exponent is less than 0, thus you have to change your public and private key"
        )

    # Save public key to file
    print("Enter filename to save public key (default public.txt): ", end="")
    filename = input()
    if filename == "":
        filename = "public.txt"

    f = open(filename, "w")
    f.write("e = " + str(e) + "\n")
    f.write("N = " + str(N))
    f.close
    print("Success")

    # Save private key to file
    print("Enter filename to save private key (default private.txt): ", end="")
    filename = input()
    if filename == "":
        filename = "private.txt"

    f = open(filename, "w")
    f.write("d = " + str(d) + "\n")
    f.write("N = " + str(N))
    f.close
    print("Success")


# Convert a string into an array containing each character as an ascii code
def conv_ascii(data):
    # Split into characters
    data = [*data]

    for char in data:
        data[data.index(char)] = str(ord(char))

    return data


# Convert an array of ascii code into a string
def conv_str(data):
    for value in data:
        data[data.index(value)] = str(chr(int(value)))

    return "".join(data)


# Encrypt message
def encrypt():
    # Open file containing decrypted message
    invalid = True
    while invalid:
        print("Choose a file to encrypt (default decrypted.txt): ", end="")
        filename = input()
        if filename == "":
            filename = "decrypted.txt"

        try:
            f1 = open(filename, "r")
            invalid = False
            print("File found")
        except FileNotFoundError:
            print("File not found")

    # Open file containing public key
    invalid = True
    while invalid:
        print("Choose a file containing the public key (default public.txt): ", end="")
        filename = input()
        if filename == "":
            filename = "public.txt"

        try:
            f2 = open(filename, "r")
            invalid = False
            print("File found")
        except FileNotFoundError:
            print("File not found")

    # Convert string ascii
    data_as_ascii = conv_ascii(f1.read())
    f1.close

    # Get public key
    e = int(f2.readline().strip().split("e = ")[1])
    N = int(f2.readline().strip().split("N = ")[1])
    f2.close

    # Encrypt ascii
    data_encrypted = []
    for value in data_as_ascii:
        data_encrypted.append(str(pow(int(value), e) % N))

    data_encrypted = " ".join(data_encrypted)

    print(data_encrypted)

    # Save encrypted message
    print("Choose a file to save encrypted message (default encrypted.txt): ", end="")
    filename = input()
    if filename == "":
        filename = "encrypted.txt"

    f3 = open(filename, "w")
    f3.write(data_encrypted)
    f3.close
    print("Success")


# Decrypt message
def decrypt():
    # Open file containing encrypted message
    invalid = True
    while invalid:
        print("Choose a file to decrypt (default encrypted.txt): ", end="")
        filename = input()
        if filename == "":
            filename = "encrypted.txt"

        try:
            f1 = open(filename, "r")
            invalid = False
        except FileNotFoundError:
            print("File not found")

    # Open file containing private key
    invalid = True
    while invalid:
        print(
            "Choose a file containing the private key (default private.txt): ", end=""
        )
        filename = input()
        if filename == "":
            filename = "private.txt"

        try:
            f2 = open(filename, "r")
            invalid = False
        except FileNotFoundError:
            print("File not found")

    # Get private key
    d = int(f2.readline().strip().split("d = ")[1])
    N = int(f2.readline().strip().split("N = ")[1])
    f2.close

    # Get encrypted data
    data_encrypted = f1.read().split(" ")
    f1.close

    # Decrypt to ascii
    data_as_ascii = []
    for value in data_encrypted:
        data_as_ascii.append(str(pow(int(value), d) % N))

    # Convert back to string
    data_decrypted = conv_str(data_as_ascii)
    print(data_decrypted)

    # Save into file
    print("Choose a file to save decrypted message (default decrypted.txt): ", end="")
    filename = input()
    if filename == "":
        filename = "decrypted.txt"

    f3 = open(filename, "w")
    f3.write(data_decrypted)
    f3.close
    print("Success")


#################################
########### CONSOLE #############
#################################

while True:
    print("1) Create keys")
    print("2) Encrypt")
    print("3) Decrypt")
    print("4) Exit (default)")

    print("Enter a number: ", end="")
    option = input()

    match option:
        case "1":
            createKeys()

        case "2":
            encrypt()

        case "3":
            decrypt()

        case _:
            raise SystemExit(0)
