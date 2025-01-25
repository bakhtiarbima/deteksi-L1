from ultralytics import YOLO
import cv2
import os
import tkinter as tk
from PIL import Image, ImageTk

# Load YOLO model
model = YOLO('coba05best.pt')  # Ganti dengan path model Anda

# Inisialisasi kamera
cap = cv2.VideoCapture(1)  # 0 untuk kamera default
if not cap.isOpened():
    print("Tidak dapat membuka kamera")
    exit()

# Buat folder untuk menyimpan foto
save_folder_ok = "deteksi_foto/cek oke"
save_folder_ng = "deteksi_foto/cek ng"

for folder in [save_folder_ok, save_folder_ng]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Hitung jumlah penyimpanan
count_ok = 0
count_ng = 0

# Variabel untuk menyimpan gambar terakhir
last_ok_img = None
last_ng_img = None

# Fungsi untuk menangkap frame dari kamera dan menampilkannya di label Tkinter
def update_frame():
    global count_ok, count_ng, last_ok_img, last_ng_img

    ret, frame = cap.read()
    if ret:
        # Deteksi objek menggunakan YOLO
        results = model.predict(frame, conf=0.5, imgsz=640)
        detected_objects = []
        for box in results[0].boxes:
            if box.conf >= 0.5:
                detected_objects.append(model.names[int(box.cls)])
        
        # Gambar hasil deteksi di frame
        result_img = results[0].plot()

        # Konversi frame ke format yang dapat ditampilkan di Tkinter
        frame_rgb = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (camera_width, camera_height))
        img = Image.fromarray(frame_resized)
        imgtk = ImageTk.PhotoImage(image=img)

        # Tampilkan frame ke GUI
        label_camera.imgtk = imgtk
        label_camera.config(image=imgtk)

        # Jika tombol 'p' ditekan, ambil gambar
        if key_pressed.get() == 'p':
            key_pressed.set('')  # Reset tombol
            total_detected = len(detected_objects)

            # Tentukan folder berdasarkan jumlah objek
            if total_detected == 3:
                count_ok += 1
                filename = f"cek oke ke-{count_ok}.jpg"
                save_path = os.path.join(save_folder_ok, filename)
                print(f"Deteksi OK - Jumlah objek: {total_detected}")
                last_ok_img = result_img  # Simpan gambar OK terakhir
            else:
                count_ng += 1
                filename = f"cek ng ke-{count_ng}.jpg"
                save_path = os.path.join(save_folder_ng, filename)
                print(f"Deteksi NG - Jumlah objek: {total_detected}")
                last_ng_img = result_img  # Simpan gambar NG terakhir

            # Simpan gambar hasil deteksi
            cv2.imwrite(save_path, result_img)
            print(f"Foto disimpan ke {save_path}")

            # Update label jumlah deteksi
            label_ok_count.config(text=str(count_ok))
            label_ng_count.config(text=str(count_ng))
            label_output_count.config(text=str(count_ok + count_ng))

            # Perbarui tampilan gambar terakhir
            update_last_images()

    # Perbarui frame secara berkala
    label_camera.after(10, update_frame)

# Fungsi untuk memperbarui gambar terakhir OK dan NG di GUI
def update_last_images():
    global last_ok_img, last_ng_img

    # Update gambar terakhir OK
    if last_ok_img is not None:
        img_ok = cv2.cvtColor(last_ok_img, cv2.COLOR_BGR2RGB)
        img_ok_resized = cv2.resize(img_ok, (300, 150))
        img_ok_tk = ImageTk.PhotoImage(image=Image.fromarray(img_ok_resized))
        label_last_ok.imgtk = img_ok_tk
        label_last_ok.config(image=img_ok_tk)

    # Update gambar terakhir NG
    if last_ng_img is not None:
        img_ng = cv2.cvtColor(last_ng_img, cv2.COLOR_BGR2RGB)
        img_ng_resized = cv2.resize(img_ng, (300, 150))
        img_ng_tk = ImageTk.PhotoImage(image=Image.fromarray(img_ng_resized))
        label_last_ng.imgtk = img_ng_tk
        label_last_ng.config(image=img_ng_tk)

# Fungsi untuk menangkap tombol keyboard
def on_keypress(event):
    key_pressed.set(event.char)

# Inisialisasi GUI Tkinter
root = tk.Tk()
root.title("Live Inspection Camera")
root.attributes('-fullscreen', True)  # Fullscreen mode

# Mendapatkan ukuran layar
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()

# Dimensi kamera dengan margin
camera_width = (window_width // 2) - 80
camera_height = window_height - 200

# Frame untuk kamera
frame_camera = tk.Frame(root, bg="white", width=camera_width + 20, height=camera_height + 20, highlightbackground="black", highlightthickness=2)
frame_camera.place(x=40, y=40)

label_camera = tk.Label(frame_camera, bg="black")
label_camera.pack(padx=10, pady=10)

# Tombol navigasi di bawah kamera
frame_buttons = tk.Frame(root, bg="orange", width=camera_width, height=50)
frame_buttons.place(x=40, y=40 + camera_height + 30)

tk.Button(frame_buttons, text="MAIN MENU", bg="orange", fg="black", font=("Arial", 16, "bold"), width=15).grid(row=0, column=0, padx=20)
tk.Button(frame_buttons, text="SETTING", bg="orange", fg="black", font=("Arial", 16, "bold"), width=15).grid(row=0, column=1, padx=20)
tk.Button(frame_buttons, text="BACK", bg="orange", fg="black", font=("Arial", 16, "bold"), width=15).grid(row=0, column=2, padx=20)

# Frame untuk informasi di bagian kanan
frame_info = tk.Frame(root, bg="lightblue", width=(window_width // 2) - 60, height=window_height - 80)
frame_info.place(x=(window_width // 2) + 20, y=40)

# OK PART Section
frame_ok = tk.Frame(frame_info, bg="green", width=300, height=300)
frame_ok.place(x=50, y=50)
tk.Label(frame_ok, text="OK PART", bg="green", fg="white", font=("Arial", 20, "bold")).pack()
label_ok_count = tk.Label(frame_ok, text="0", bg="white", font=("Arial", 16))
label_ok_count.pack()

label_last_ok = tk.Label(frame_ok, bg="white", width=300, height=150)
label_last_ok.pack(pady=10)

# NG PART Section
frame_ng = tk.Frame(frame_info, bg="red", width=300, height=300)
frame_ng.place(x=50, y=400)
tk.Label(frame_ng, text="NG PART", bg="red", fg="white", font=("Arial", 20, "bold")).pack()
label_ng_count = tk.Label(frame_ng, text="0", bg="white", font=("Arial", 16))
label_ng_count.pack()

label_last_ng = tk.Label(frame_ng, bg="white", width=300, height=150)
label_last_ng.pack(pady=10)

# Panel untuk jumlah count
frame_count = tk.Frame(frame_info, bg="gray", width=300, height=150)
frame_count.place(x=50, y=750)

tk.Label(frame_count, text="OUTPUT COUNT", bg="gray", fg="white", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=5)
label_output_count = tk.Label(frame_count, text="0", bg="lightgray", width=10, font=("Arial", 16))
label_output_count.grid(row=0, column=1)

# Variabel untuk mendeteksi tombol yang ditekan
key_pressed = tk.StringVar()

# Bind tombol keyboard
root.bind("<Key>", on_keypress)

# Jalankan fungsi update frame untuk menampilkan kamera secara live
update_frame()

# Fungsi untuk keluar dari fullscreen dengan tombol ESC
def keluar(event):
    root.attributes('-fullscreen', False)
    root.quit()

root.bind("<Escape>", keluar)

# Jalankan aplikasi
root.mainloop()

# Pastikan kamera dilepas setelah jendela ditutup
cap.release()
cv2.destroyAllWindows()
