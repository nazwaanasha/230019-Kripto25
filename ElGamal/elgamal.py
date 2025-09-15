# Nama Program    : elgamal.py
# Nama            : Nazwa Nashatasya 
# NPM             : 140810230019
# Tanggal Buat    : Senin, 15 September 2025
# Deskripsi       : Enkripsi dan dekripsi ElGamal


# ============================
# Fungsi bantu
# ============================
def char_to_num(c):
    """
    Mengubah huruf A-Z menjadi angka 0-25.
    Contoh: A=0, B=1, ..., Z=25
    """
    return ord(c.upper()) - ord('A')

def num_to_char(n):
    """
    Mengubah angka 0-25 menjadi huruf A-Z.
    """
    return chr((n % 26) + ord('A'))

def mod_inverse(a, p):
    """
    Menghitung invers modulo (a^-1 mod p).
    Gunakan Extended Euclidean Algorithm.
    """
    return pow(a, -1, p) 

# ============================
# Fungsi Enkripsi
# ============================
def elgamal_encrypt(plaintext, p, g, x, k):
    """
    Fungsi enkripsi ElGamal.
    - Input: plaintext (string), p (prima), g (generator), x (kunci privat), k (kunci acak)
    - Output: ciphertext (list pasangan (C1,C2))
    """
    print("\nPROSES ENKRIPSI:")
    
    # Langkah 1: Plaintext
    print(f"Plaintext = {plaintext}")
    
    # Langkah 2: Konversi Plaintext ke angka
    m_list = [char_to_num(ch) for ch in plaintext]
    print(f"n(PT) = {m_list}")
    
    # Langkah 3: Hitung kunci publik y = g^x mod p
    y = pow(g, x, p)
    print(f"y = g^x mod p = {g}^{x} mod {p} = {y}")
    
    # Langkah 4: Hitung C1 = g^k mod p
    C1 = pow(g, k, p)
    print(f"C1 = g^k mod p = {g}^{k} mod {p} = {C1}")
    
    # Langkah 5: Hitung C2 = M * y^k mod p untuk setiap karakter M
    ciphertext = []
    yk = pow(y, k, p)
    print(f"y^k = {y}^{k} mod {p} = {yk}")
    for i, M in enumerate(m_list):
        C2 = (M * yk) % p
        print(f" {i}: M={M} -> C2 = {M} * {yk} mod {p} = {C2}")
        ciphertext.append((C1, C2))
    
    # Langkah 6: Hasil Ciphertext adalah pasangan (C1, C2)
    return ciphertext, m_list
    
def print_enc_table(plaintext, m_list, ciphertext):
    """
    Mencetak tabel enkripsi rapi:
    Index | PT | n(PT) | C1 | C2 | CT
    """
    print("\nTabel Enkripsi ElGamal")
    print("=" * 72)
    print(f"{'Index':<6}{'PT':<6}{'n(PT)':<8}{'C1':<8}{'C2':<8}{'CT':<12}")
    print("-" * 72)
    for i, (ch, m, (C1, C2)) in enumerate(zip(plaintext, m_list, ciphertext)):
        print(f"{i:<6}{ch:<6}{m:<8}{C1:<8}{C2:<8}{str((C1, C2)):<12}")
    print("=" * 72)


# ============================
# Fungsi Dekripsi
# ============================
def elgamal_decrypt(ciphertext, p, x):
    """
    Fungsi dekripsi ElGamal.
    - Input: ciphertext (list pasangan (C1,C2)), p (prima), x (kunci privat)
    - Output: plaintext string
    """
    print("\nPROSES DEKRIPSI:")
    plaintext_nums = []
    
    for i, (C1, C2) in enumerate(ciphertext):
        # Langkah 1: Ciphertext
        print(f"\nHuruf ke-{i}:")
        print(f"Ciphertext (C1, C2) = ({C1}, {C2})")

        # Langkah 2: Hitung nilai C1^x mod p
        s = pow(C1, x, p)
        print(f"s = C1^x mod p = {C1}^{x} mod {p} = {s}")

        # Langkah 3: Hitung nilai modulo inverse dari C1^x mod p -> (C1^x)^-1 = modinverse(C1^x, p)
        s_inv = mod_inverse(s, p)
        print(f"s^-1 mod p = {s_inv}")

        # Langkah 4: Hitung M = C2 * (C1^x)^-1 mod p untuk setiap karakter C2
        M = (C2 * s_inv) % p
        print(f"M = C2 * s^-1 mod p = {C2} * {s_inv} mod {p} = {M}")

        plaintext_nums.append(M)

    # Langkah 5: Konversi angka M ke karakter
    plaintext = "".join(num_to_char(m) for m in plaintext_nums)
    print(f"\nKonversi angka -> huruf = {plaintext}")
    
    # Langkah 6: Hasil Plaintext adalah karakter-karakter M
    return plaintext, plaintext_nums

def print_dec_table(ciphertext, plaintext_nums, plaintext):
    """
    Mencetak tabel dekripsi rapi:
    Index | C1 | C2 | M | PT
    """
    print("\nTabel Dekripsi ElGamal")
    print("=" * 72)
    print(f"{'Index':<6}{'C1':<8}{'C2':<8}{'M':<8}{'PT':<6}")
    print("-" * 72)
    for i, ((C1, C2), M, ch) in enumerate(zip(ciphertext, plaintext_nums, plaintext)):
        print(f"{i:<6}{C1:<8}{C2:<8}{M:<8}{ch:<6}")
    print("=" * 72)

# ============================
# Main Menu
# ============================
def main():
    while True:
        print("\n===== PROGRAM ELGAMAL =====")
        print("Menu:")
        print("1. Enkripsi") 
        print("2. Dekripsi")
        print("3. Keluar")

        pilihan = input("Pilih menu (1-3): ")   # input menu

        if pilihan == "1":
            p = int(input("Masukkan p (prima besar): ").strip())
            g = int(input("Masukkan g (generator/basis): ").strip())
            x = int(input("Masukkan x (kunci privat): ").strip())
            k = int(input("Masukkan k (kunci acak): ").strip())
            plaintext = input("Masukkan plaintext: ").replace(" ", "").upper()
            
            ciphertext, m_list = elgamal_encrypt(plaintext, p, g, x, k)
            print_enc_table(plaintext, m_list, ciphertext)
            print("\nCiphertext (list pasangan):", ciphertext)

        elif pilihan == "2":
            p = int(input("Masukkan p (prima besar): ").strip())
            x = int(input("Masukkan x (kunci privat): ").strip())
            n = int(input("Masukkan jumlah pasangan ciphertext: "))
            ciphertext = []
            for i in range(n):
                C1 = int(input(f"Masukkan C1 pasangan {i+1}: "))
                C2 = int(input(f"Masukkan C2 pasangan {i+1}: "))
                ciphertext.append((C1, C2))
                
            plaintext, plaintext_nums = elgamal_decrypt(ciphertext, p, x)
            print_dec_table(ciphertext, plaintext_nums, plaintext)
            print("\nPlaintext:", plaintext)

        elif pilihan == "3":                    # keluar program
            print("Program selesai. Terima kasih!")
            break
        
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":                     # eksekusi utama
    main()
    