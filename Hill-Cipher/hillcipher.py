# Nama Program    : hillcipher.py
# Nama            : Nazwa Nashatasya 
# NPM             : 140810230019
# Tanggal Buat    : Jumat, 5 September 2025
# Deskripsi       : Enkripsi, dekripsi, dan mencari kunci Hill Cipher

import numpy as np                     # library untuk operasi matriks
from math import gcd                   # untuk mencari gcd (greatest common divisor)
from itertools import combinations     # untuk memilih kombinasi kolom (pencarian kunci)

# ============================
# Fungsi bantu
# ============================

def egcd(a, b):                        # fungsi Extended Euclidean Algorithm
    if b == 0:                         # basis rekursi
        return (1, 0, a)               # mengembalikan koefisien x,y dan gcd
    x1, y1, g = egcd(b, a % b)         # rekursi dengan a % b
    return (y1, x1 - (a // b) * y1, g) # update koefisien

def mod_inverse(a, m):                 # mencari invers modulo dari a terhadap m
    """Mencari invers modulo dari a (a^-1 mod m) menggunakan Extended Euclidean Algorithm"""
    a %= m                             # reduksi a dalam mod m
    x, y, g = egcd(a, m)               # panggil egcd
    if g != 1:                         # kalau gcd != 1, tidak ada invers
        return None
    return x % m                       # hasil invers dalam bentuk positif

# ============================
# Fungsi Enkripsi
# ============================

def hill_encrypt(plaintext, key):      # enkripsi Hill Cipher
    """Enkripsi Hill Cipher"""
    n = key.shape[0]                   # ordo matriks kunci
    nums = [ord(c) - 65 for c in plaintext.upper() if c.isalpha()]  # konversi huruf ke angka (A=0,...,Z=25)

    while len(nums) % n != 0:          # padding bila panjang tidak kelipatan n
        nums.append(0)                 # tambahkan 'A' (0)

    ciphertext_numbers = []            
    for i in range(0, len(nums), n):   # ambil blok sebanyak n
        block = np.array(nums[i:i+n])  # bentuk array
        encrypted = (key.dot(block) % 26).astype(int)  # kalikan matriks kunci lalu mod 26
        ciphertext_numbers.extend([int(x) for x in encrypted])  # simpan hasil

    ciphertext = ''.join(chr(x + 65) for x in ciphertext_numbers)  # ubah angka jadi huruf
    return ciphertext

def hill_encrypt_verbose(plaintext, key):   # versi enkripsi dengan proses ditampilkan
    print("\n=== Proses Enkripsi ===")
    n = key.shape[0]
    nums = [ord(c) - 65 for c in plaintext.upper() if c.isalpha()]
    print("Plaintext angka:", nums)

    while len(nums) % n != 0:
        nums.append(0)
    print("Setelah padding:", nums)

    ciphertext_numbers = []
    for i in range(0, len(nums), n):
        block = np.array(nums[i:i+n])
        print(f"\nBlok {i//n+1}:", block)
        encrypted = (key.dot(block) % 26).astype(int)
        print("Key * Blok mod 26:", encrypted)
        ciphertext_numbers.extend([int(x) for x in encrypted])

    ciphertext = ''.join(chr(x + 65) for x in ciphertext_numbers)
    print("\nCiphertext angka:", ciphertext_numbers)
    print("Ciphertext huruf:", ciphertext)
    return ciphertext

# ============================
# Fungsi Dekripsi
# ============================

def hill_decrypt(ciphertext, key):     # dekripsi Hill Cipher
    """Dekripsi Hill Cipher"""
    n = key.shape[0]
    nums = [ord(c) - 65 for c in ciphertext.upper() if c.isalpha()]  # ubah huruf ke angka

    det = int(round(np.linalg.det(key)))     # determinan kunci
    det_mod = det % 26                       # determinan mod 26
    inv_det = mod_inverse(det_mod, 26)       # cari invers determinan

    if inv_det is None or gcd(det_mod, 26) != 1:  # cek invertibilitas
        raise ValueError("Kunci tidak invertible mod 26, dekripsi tidak dapat dilakukan.")

    key_inv = inv_det * np.round(det * np.linalg.inv(key)).astype(int) % 26  # inverse matriks mod 26

    plaintext_numbers = []
    for i in range(0, len(nums), n):         # proses blok per blok
        block = np.array(nums[i:i+n])
        decrypted = np.dot(key_inv, block) % 26  # kalikan dengan kunci inverse
        plaintext_numbers.extend([int(x) for x in decrypted])

    plaintext = ''.join(chr(x + 65) for x in plaintext_numbers)  # ubah ke huruf
    return plaintext

def hill_decrypt_verbose(ciphertext, key):   # versi verbose dekripsi
    print("\n=== Proses Dekripsi ===")
    n = key.shape[0]
    nums = [ord(c) - 65 for c in ciphertext.upper() if c.isalpha()]
    print("Ciphertext angka:", nums)

    det = int(round(np.linalg.det(key)))
    det_mod = det % 26
    inv_det = mod_inverse(det_mod, 26)
    print("det(K) =", det)
    print("det(K) mod 26 =", det_mod)
    print("inv_det =", inv_det)

    key_inv = inv_det * np.round(det * np.linalg.inv(key)).astype(int) % 26
    print("K^-1 mod 26:\n", key_inv)

    plaintext_numbers = []
    for i in range(0, len(nums), n):
        block = np.array(nums[i:i+n])
        print(f"\nBlok {i//n+1}:", block)
        decrypted = np.dot(key_inv, block) % 26
        print("K^-1 * Blok mod 26:", decrypted)
        plaintext_numbers.extend([int(x) for x in decrypted])

    plaintext = ''.join(chr(x + 65) for x in plaintext_numbers)
    print("\nPlaintext angka:", plaintext_numbers)
    print("Plaintext huruf:", plaintext)
    return plaintext

# ============================
# Fungsi Cari Kunci
# ============================

def to_blocks(nums, n):                # ubah deretan angka jadi blok matriks
    blocks = []
    for i in range(0, len(nums), n):
        blk = nums[i:i+n]
        if len(blk) < n:               # jika kurang panjang, abaikan
            break
        blocks.append(blk)
    return np.array(blocks).T          # transpose agar tiap kolom = blok

def find_key(plaintext, ciphertext, n):  # mencari kandidat kunci
    pt_nums = [ord(c) - 65 for c in plaintext.upper() if c.isalpha()]
    ct_nums = [ord(c) - 65 for c in ciphertext.upper() if c.isalpha()]

    pt_matrix = to_blocks(pt_nums, n)
    ct_matrix = to_blocks(ct_nums, n)

    block_count = pt_matrix.shape[1]
    if block_count < n:                # butuh minimal n blok untuk n×n
        raise ValueError(f"Tidak cukup data. Untuk kunci {n}x{n} diperlukan minimal {n*n} huruf.")

    candidate_keys = []
    for cols in combinations(range(block_count), n):  # coba kombinasi kolom
        pt_submatrix = pt_matrix[:, cols]
        ct_submatrix = ct_matrix[:, cols]

        det_pt = int(round(np.linalg.det(pt_submatrix)))
        det_pt_mod = det_pt % 26
        inv_det_pt = mod_inverse(det_pt_mod, 26)

        if inv_det_pt is None or gcd(det_pt_mod, 26) != 1:
            continue                   # lewati bila tidak invertible

        pt_inv_mod = (inv_det_pt * np.round(det_pt * np.linalg.inv(pt_submatrix)).astype(int)) % 26
        key_matrix = (ct_submatrix.dot(pt_inv_mod)) % 26  # K = C * P^-1
        candidate_keys.append(key_matrix.astype(int))

    return candidate_keys

def find_key_verbose(plaintext, ciphertext, n):   # versi verbose pencarian kunci
    print("\n=== Proses Pencarian Kunci ===")
    pt_nums = [ord(c) - 65 for c in plaintext.upper() if c.isalpha()]
    ct_nums = [ord(c) - 65 for c in ciphertext.upper() if c.isalpha()]
    print("Plaintext angka:", pt_nums)
    print("Ciphertext angka:", ct_nums)

    pt_matrix = to_blocks(pt_nums, n)
    ct_matrix = to_blocks(ct_nums, n)
    print("Matriks P:\n", pt_matrix)
    print("Matriks C:\n", ct_matrix)

    block_count = pt_matrix.shape[1]
    candidate_keys = []
    for cols in combinations(range(block_count), n):
        print("\nGunakan kolom:", cols)
        pt_submatrix = pt_matrix[:, cols]
        ct_submatrix = ct_matrix[:, cols]
        print("P_sub:\n", pt_submatrix)
        print("C_sub:\n", ct_submatrix)

        det_pt = int(round(np.linalg.det(pt_submatrix)))
        det_pt_mod = det_pt % 26
        inv_det_pt = mod_inverse(det_pt_mod, 26)
        print("det =", det_pt, "; det mod 26 =", det_pt_mod, "; inv_det =", inv_det_pt)

        if inv_det_pt is None or gcd(det_pt_mod, 26) != 1:
            print("-> Tidak invertible, dilewati")
            continue

        pt_inv_mod = (inv_det_pt * np.round(det_pt * np.linalg.inv(pt_submatrix)).astype(int)) % 26
        print("P^-1 mod 26:\n", pt_inv_mod)
        key_matrix = (ct_submatrix.dot(pt_inv_mod)) % 26
        print("Kandidat kunci:\n", key_matrix)
        candidate_keys.append(key_matrix.astype(int))

    return candidate_keys

# ============================
# Main Menu
# ============================

def main():
    while True:
        print("\n===== PROGRAM HILL CIPHER =====")
        print("Menu:")
        print("1. Enkripsi")
        print("2. Enkripsi (dengan proses)")
        print("3. Dekripsi")
        print("4. Dekripsi (dengan proses)")
        print("5. Mencari kunci dari plaintext dan ciphertext")
        print("6. Mencari kunci dari plaintext dan ciphertext (dengan proses)")
        print("7. Keluar")

        pilihan = input("Pilih menu (1-7): ")   # input menu

        if pilihan in ["1", "2"]:               # enkripsi
            plaintext = input("Masukkan plaintext: ")
            n = int(input("Masukkan ordo matriks kunci: "))
            key_elements = []
            for i in range(n):                  # input baris kunci
                row = list(map(int, input(f"Baris {i+1}: ").split()))
                key_elements.append(row)
            key = np.array(key_elements)
            if pilihan == "1":
                ciphertext = hill_encrypt(plaintext, key)
            else:
                ciphertext = hill_encrypt_verbose(plaintext, key)
            print("Ciphertext:", ciphertext)

        elif pilihan in ["3", "4"]:             # dekripsi
            ciphertext = input("Masukkan ciphertext: ")
            n = int(input("Masukkan ordo matriks kunci: "))
            key_elements = []
            for i in range(n):
                row = list(map(int, input(f"Baris {i+1}: ").split()))
                key_elements.append(row)
            key = np.array(key_elements)
            try:
                if pilihan == "3":
                    plaintext = hill_decrypt(ciphertext, key)
                else:
                    plaintext = hill_decrypt_verbose(ciphertext, key)
                print("Plaintext:", plaintext)
            except ValueError as e:
                print("Error:", e)

        elif pilihan in ["5", "6"]:             # pencarian kunci
            plaintext = input("Masukkan plaintext: ")
            ciphertext = input("Masukkan ciphertext: ")
            n = int(input("Masukkan ordo matriks kunci: "))
            try:
                if pilihan == "5":
                    candidate_keys = find_key(plaintext, ciphertext, n)
                else:
                    candidate_keys = find_key_verbose(plaintext, ciphertext, n)
                print(f"\nDitemukan {len(candidate_keys)} kandidat kunci:")
                for i, K in enumerate(candidate_keys, start=1):
                    print(f"\nKunci {i}:\n{K}")
            except Exception as e:
                print("Error:", e)

        elif pilihan == "7":                    # keluar program
            print("Program selesai. Terima kasih!")
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":                     # eksekusi utama
    main()
