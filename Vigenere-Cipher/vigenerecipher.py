# Nama Program    : vigenerecipher.py
# Nama            : Nazwa Nashatasya 
# NPM             : 140810230019
# Tanggal Buat    : Senin, 15 September 2025
# Deskripsi       : Enkripsi dan dekripsi Vigenere Cipher


# ============================
# Fungsi bantu
# ============================
def generate_key(text, key):
    """
    Fungsi untuk memperpanjang key agar sama panjang dengan plaintext/ciphertext.
    Key akan diulang (extend) sampai panjangnya sama dengan text.
    """
    key = key.upper()
    if len(text) == len(key):
        return key
    else:
        key = list(key)
        for i in range(len(text) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)

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


# ============================
# Fungsi Enkripsi
# ============================
def vigenere_encrypt(plaintext, key):
    """
    Fungsi enkripsi Vigenere Cipher.
    - Input: plaintext (teks asli), key (kata kunci)
    - Output: ciphertext (hasil enkripsi), key_full (key yang sudah dipanjangkan)
    """
    key_full = generate_key(plaintext, key)    # extend key
    ciphertext = ""
    print("\nPROSES ENKRIPSI:")
    
    # Langkah 1: Plaintext
    print("PT      :", " ".join(list(plaintext.upper())))
    
    # Langkah 2: Konversi PT ke angka
    print("n(PT)   :", " ".join(str(char_to_num(p)) for p in plaintext.upper()))
    
    # Langkah 3: Konversi key ke angka
    print("n(K)    :", " ".join(str(char_to_num(k)) for k in key_full))
    
    # Langkah 4: Operasi enkripsi (n(PT)+n(K)) mod 26
    print("(n(PT)+n(K)) mod 26:")
    for i, (p, k) in enumerate(zip(plaintext.upper(), key_full)):
        p_num = char_to_num(p)
        k_num = char_to_num(k)
        s = p_num + k_num
        mod = s % 26
        c = num_to_char(mod)
        print(f" {i:>2}: {p} ({p_num}) + {k} ({k_num}) = {s} -> {s}%26 = {mod} -> {c}")
        ciphertext += c
    
    # Langkah 5: Hasil Ciphertext
    print("CT      :", " ".join(list(ciphertext)))
    
    return ciphertext, key_full

def print_enc_table(plaintext, key, ciphertext):
    """
    Mencetak tabel enkripsi rapi:
    Index | PT | n(PT) | Key | n(K) | (n(PT)+n(K))%26 | CT
    """
    key_full = generate_key(plaintext, key)
    print("\nTabel Enkripsi Vigenere")
    print("="*72)
    print(f"{'Index':<6}{'PT':<6}{'n(PT)':<8}{'Key':<6}{'n(K)':<8}{'(n(PT)+n(K))%26':<18}{'CT':<6}")
    print("-"*72)
    for i, (p, k, c) in enumerate(zip(plaintext.upper(), key_full, ciphertext)):
        pt_num = char_to_num(p)
        k_num = char_to_num(k)
        ct_num = (pt_num + k_num) % 26
        print(f"{i:<6}{p:<6}{pt_num:<8}{k:<6}{k_num:<8}{ct_num:<18}{c:<6}")
    print("="*72)


# ============================
# Fungsi Dekripsi
# ============================
def vigenere_decrypt(ciphertext, key):
    """
    Fungsi dekripsi Vigenere Cipher.
    - Input: ciphertext (teks terenkripsi), key (kata kunci)
    - Output: plaintext (hasil dekripsi), key_full (key yang sudah dipanjangkan)
    """
    key_full = generate_key(ciphertext, key)   # extend key
    plaintext = ""
    print("\nPROSES DEKRIPSI:")
    
    # Langkah 1: Ciphertext
    print("CT      :", " ".join(list(ciphertext.upper())))
    
    # Langkah 2: Konversi Ciphertext ke angka
    print("n(CT)   :", " ".join(str(char_to_num(c)) for c in ciphertext.upper()))
    
    # Langkah 3: Konversi key ke angka
    print("n(K)    :", " ".join(str(char_to_num(k)) for k in key_full))
    
    # Langkah 4: Operasi dekripsi (n(CT)-n(K)) mod 26
    print("(n(CT)-n(K)) mod 26:")
    for i, (c, k) in enumerate(zip(ciphertext.upper(), key_full)):
        c_num = char_to_num(c)
        k_num = char_to_num(k)
        raw = c_num - k_num
        mod = raw % 26
        p = num_to_char(mod)
        print(f" {i:>2}: {c} ({c_num}) - {k} ({k_num}) = {raw} -> {raw}%26 = {mod} -> {p}")
        plaintext += p
    
    # Langkah 5: Hasil Plaintext
    print("PT      :", " ".join(list(plaintext)))
    
    return plaintext, key_full

def print_dec_table(ciphertext, key, plaintext):
    """
    Mencetak tabel dekripsi rapi:
    Index | CT | n(CT) | Key | n(K) | n(CT)-n(K))%26 | PT
    """
    key_full = generate_key(ciphertext, key)
    print("\nTabel Dekripsi Vigenere")
    print("="*72)
    print(f"{'Index':<6}{'CT':<6}{'n(CT)':<8}{'Key':<6}{'n(K)':<8}{'(n(CT)-n(K))%26':<18}{'PT':<6}")
    print("-"*72)
    for i, (c, k, p) in enumerate(zip(ciphertext.upper(), key_full, plaintext)):
        ct_num = char_to_num(c)
        k_num = char_to_num(k)
        pt_num = (ct_num - k_num) % 26
        print(f"{i:<6}{c:<6}{ct_num:<8}{k:<6}{k_num:<8}{pt_num:<18}{p:<6}")
    print("="*72)


# ============================
# Main Menu
# ============================
def main():
    while True:
        print("\n===== PROGRAM VIGENERE CIPHER =====")
        print("Menu:")
        print("1. Enkripsi") 
        print("2. Dekripsi")
        print("3. Keluar")

        pilihan = input("Pilih menu (1-3): ")   # input menu

        if pilihan == "1":
            plaintext = input("Masukkan plaintext: ").replace(" ", "").upper()
            key = input("Masukkan key: ").upper()
            ciphertext, key_full = vigenere_encrypt(plaintext, key)
            print_enc_table(plaintext, key_full, ciphertext)
            print("\nCiphertext:", ciphertext)

        elif pilihan == "2":
            ciphertext = input("Masukkan ciphertext: ").replace(" ", "").upper()
            key = input("Masukkan key: ").upper()
            plaintext, key_full = vigenere_decrypt(ciphertext, key)
            print_dec_table(ciphertext, key_full, plaintext)
            print("\nPlaintext:", plaintext)

        elif pilihan == "3":                    # keluar program
            print("Program selesai. Terima kasih!")
            break
        
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":                     # eksekusi utama
    main()