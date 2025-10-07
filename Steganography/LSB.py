# Nama Program    : LSB.py
# Nama            : Nazwa Nashatasya 
# NPM             : 140810230019
# Tanggal Buat    : Senin, 6 Oktober 2025
# Deskripsi       : Implementasi steganografi LSB untuk menyisipkan dan mengekstrak pesan teks dalam gambar.

from PIL import Image   # Library untuk manipulasi citra
import os               # Library untuk manajemen file & direktori

# ============================
# Konfigurasi Folder
# ============================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))     # Direktori skrip saat ini
COVER_DIR = os.path.join(SCRIPT_DIR, "cover-object")        # Folder untuk cover-object
STEGO_DIR = os.path.join(SCRIPT_DIR, "stego-object")        # Folder untuk stego-object
os.makedirs(STEGO_DIR, exist_ok=True)                       # Pastikan folder output ada


# ============================
# Fungsi bantu
# ============================
def text_to_binary(text):
    """Konversi string teks ke string biner."""
    binary = ''.join(format(ord(char), '08b') for char in text)     # Ubah tiap karakter ke biner 8-bit
    delimiter = '1111111111111110'                                  # Delimiter (penanda akhir pesan)
    return binary + delimiter                                       # Gabungkan teks biner dengan delimiter

def binary_to_text(binary):
    """Konversi string biner ke string teks."""
    chars = []                                                      # List penampung karakter
    for i in range(0, len(binary), 8):                              # Proses per 8 bit
        byte = binary[i:i+8]
        if not byte:                                                # Jika byte kosong, berhenti
            break
        chars.append(chr(int(byte, 2)))                             # Konversi biner ke karakter
    return "".join(chars)                                           # Satukan menjadi string


# ============================
# Fungsi Encode (Embedding)
# ============================
def encode(image_name, secret_message, output_name):
    """
    Menyembunyikan pesan rahasia ke dalam citra menggunakan LSB.
    """
    # Buat path absolut untuk input dan output
    image_path = os.path.join(COVER_DIR, image_name)
    output_path = os.path.join(STEGO_DIR, output_name)
    
    # Buka citra dan ubah ke mode RGB
    img = Image.open(image_path).convert("RGB")
    width, height = img.size
    
    # Konversi pesan ke biner dan tambahkan delimiter
    binary_message = text_to_binary(secret_message)
    msg_len = len(binary_message)
    
    # Setiap pixel RGB (3 byte) dapat menyimpan 3 bit pesan
    capacity = width * height * 3
    if msg_len > capacity:
        raise ValueError(f"Pesan terlalu besar! Kapasitas maksimal: {capacity} bit, pesan: {msg_len} bit.")

    # Inisialisasi indeks bit pesan
    msg_idx = 0

    # Iterasi semua pixel gambar
    for x in range(width):
        for y in range(height):
            r, g, b = img.getpixel((x, y))              # Ambil nilai RGB
            new_r, new_g, new_b = r, g, b               # Siapkan nilai RGB baru

            # Modifikasi setiap channel (R, G, B)
            for channel in ['r', 'g', 'b']:
                if msg_idx < msg_len:                   # Selama masih ada bit pesan tersisa
                    bit = int(binary_message[msg_idx])  # Ambil 1 bit pesan
                    
                    # Ganti LSB: (nilai & 0xFE) | bit
                    # 0xFE = 11111110. Ini akan membuat LSB menjadi 0, lalu di-OR dengan bit pesan
                    if channel == 'r':
                        new_r = (r & 0xFE) | bit
                    elif channel == 'g':
                        new_g = (g & 0xFE) | bit
                    elif channel == 'b':
                        new_b = (b & 0xFE) | bit

                    msg_idx += 1                        # Pindah ke bit pesan berikutnya
            
            # Simpan pixel yang sudah dimodifikasi
            img.putpixel((x, y), (new_r, new_g, new_b))

        if msg_idx >= msg_len:                          # Jika semua bit pesan sudah disisipkan, berhenti
            break
            
    img.save(output_path)                               # Simpan gambar hasil encode ke folder stego-object
    return output_path                                  # Kembalikan path file stego
    
    
# ============================
# Fungsi Decode (Extraction)
# ============================
def decode(stego_name):
    """
    Mengekstrak pesan rahasia dari citra Stego.
    """
    # Buat path absolut ke file stego
    stego_path = os.path.join(STEGO_DIR, stego_name)
    
    # Buka citra dan ubah ke mode RGB
    img = Image.open(stego_path).convert("RGB")
    width, height = img.size
    
    # Variabel untuk menampung hasil ekstraksi biner
    binary_data = ""
    delimiter = '1111111111111110'                      # Delimiter yang sama dengan encoder
    delimiter_len = len(delimiter)
    
    # Iterasi semua pixel untuk membaca bit LSB
    for x in range(width):
        for y in range(height):
            r, g, b = img.getpixel((x, y))              # Ambil nilai RGB
            
            # Ekstrak LSB: (nilai & 0x01)
            # 0x01 = 00000001. Ini hanya akan menyisakan bit LSB.
            binary_data += str(r & 1)
            if binary_data.endswith(delimiter):         # Jika sudah ketemu delimiter, berhenti
                break
            
            binary_data += str(g & 1)
            if binary_data.endswith(delimiter):
                break

            binary_data += str(b & 1)
            if binary_data.endswith(delimiter):
                break
        
        if binary_data.endswith(delimiter):
            break

    message_binary = binary_data[:-delimiter_len]       # Hapus delimiter
    secret_message = binary_to_text(message_binary)     # Konversi biner ke teks asli
    
    return secret_message                               # Kembalikan pesan rahasia


# ============================
# Main Menu
# ============================
def main():
    while True:
        print("\n===== PROGRAM STEGANOGRAPHY LEAST SIGNIFICANT BITS (LSB) =====")
        print("Menu:")
        print("1. Encode (Sisipkan Pesan ke Gambar)") 
        print("2. Decode (Ekstrak Pesan dari Gambar)")
        print("3. Keluar")

        pilihan = input("Pilih menu (1-3): ")   
        
        # =============================
        # MENU 1: ENCODE
        # =============================
        if pilihan == "1":
            try:
                print(f"\n[INFO] Folder cover-object: {COVER_DIR}")

                # Pastikan folder cover-object tersedia
                if not os.path.exists(COVER_DIR):
                    print(f"[PERINGATAN] Folder 'cover-object' tidak ditemukan di lokasi:\n{COVER_DIR}")
                    print("Pastikan folder tersebut ada dan berisi gambar cover!\n")
                    continue

                # Input nama file cover
                image_name = input("Masukkan nama file cover object (contoh: cover-1.png): ").strip()
                if not image_name:
                    print("[PERINGATAN] Nama file cover tidak boleh kosong!")
                    continue

                # Cek apakah file cover tersedia
                image_path = os.path.join(COVER_DIR, image_name)
                if not os.path.exists(image_path):
                    print(f"[PERINGATAN] File cover '{image_name}' tidak ditemukan di folder cover-object!")
                    available = [f for f in os.listdir(COVER_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                    if available:
                        print(f"File yang tersedia: {', '.join(available)}")
                    else:
                        print("Tidak ada file gambar yang ditemukan di folder cover-object!")
                    continue

                # Input pesan rahasia
                secret = input("Masukkan pesan rahasia: ").strip()
                if not secret:
                    print("[PERINGATAN] Pesan rahasia tidak boleh kosong!")
                    continue

                # Input nama file output
                output_name = input("Masukkan nama file output (contoh: stego-1.png): ").strip()
                if not output_name:
                    print("[PERINGATAN] Nama file output tidak boleh kosong!")
                    continue
                if not output_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    print("[PERINGATAN] File output harus berformat PNG, JPG, atau JPEG!")
                    continue

                # Jalankan proses encodee
                stego_path = encode(image_name, secret, output_name)
                print(f"\n✅ [SUKSES] Pesan berhasil disisipkan!\nFile stego disimpan di: {stego_path}")

            except Exception as e:
                print(f"\n❌ [ERROR] Terjadi kesalahan saat proses encoding: {e}")
                
        # =============================
        # MENU 2: DECODE
        # =============================
        elif pilihan == "2":
            try:
                print(f"\n[INFO] Folder stego-object: {STEGO_DIR}")
                
                # Pastikan folder stego-object tersedia
                if not os.path.exists(STEGO_DIR):
                    print(f"[PERINGATAN] Folder 'stego-object' tidak ditemukan di lokasi:\n{STEGO_DIR}")
                    print("Pastikan folder tersebut ada dan berisi gambar stego!\n")
                    continue

                # Input nama file stego
                stego_name = input("Masukkan nama file stego object (contoh: stego-1.png): ").strip()
                if not stego_name:
                    print("[PERINGATAN] Nama file stego tidak boleh kosong!")
                    continue

                # Cek apakah file stego tersedia
                stego_path = os.path.join(STEGO_DIR, stego_name)
                if not os.path.exists(stego_path):
                    print(f"[PERINGATAN] File stego '{stego_name}' tidak ditemukan di folder stego-object!")
                    available = [f for f in os.listdir(STEGO_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                    if available:
                        print(f"File yang tersedia: {', '.join(available)}")
                    else:
                        print("Tidak ada file gambar yang ditemukan di folder stego-object!")
                    continue

                # Jalankan proses decode
                message = decode(stego_name)
                if message.strip() == "":
                    print("[PERINGATAN] Tidak ditemukan pesan tersembunyi di gambar ini!")
                else:
                    print(f"\n✅ [SUKSES] Pesan yang diekstrak:\n{message}")

            except Exception as e:
                print(f"\n❌ [ERROR] Terjadi kesalahan saat proses decoding: {e}")

        # =============================
        # MENU 3: KELUAR
        # =============================
        elif pilihan == "3":                   
            print("Program selesai. Terima kasih!")
            break
        
        # =============================
        # INPUT TIDAK VALID
        # =============================
        else:                                 
            print("Pilihan tidak valid!")

# Jalankan program
if __name__ == "__main__":                    
    main()