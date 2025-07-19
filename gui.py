import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from linear_regression import linear_regr_model  # Senin modülün

# Global değişken
file_path = None

# Ana pencere
form = tk.Tk()
form.title("Linear Regression Calculator")
form.geometry("900x750")
form.configure(bg="#f0f0f0")  # Açık gri arka plan

# === Dosya seçme fonksiyonu ===
def select_file():
    global file_path
    file_path = filedialog.askopenfilename(
        title="CSV dosyası seç",
        filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
    )
    if file_path:
        status_label.config(text=f"Seçilen dosya: {file_path.split('/')[-1]}")
    else:
        status_label.config(text="Dosya seçilmedi.")

# === Hesaplamayı başlatan fonksiyon ===
def start_regression():
    if not file_path:
        messagebox.showerror("Hata", "Lütfen önce bir CSV dosyası seçin.")
        return
    try:
        df, r_val, r2_val = linear_regr_model(
            csv_name=file_path, plot_ax=ax, r=True,
            xlabel="x", ylabel="y"
        )

        # Grafiği güncelle
        canvas.draw()
        if not hasattr(canvas, '_shown'):
            canvas.get_tk_widget().pack(pady=10)
            canvas._shown = True

        # Tabloyu temizle ve güncelle
        for row in tree.get_children():
            tree.delete(row)
        for _, row in df.iterrows():
            tree.insert("", tk.END, values=(row['x'], row['y'], row['predicted_values']))

        table_frame.pack(pady=10, fill="both", expand=True)

        # r ve R² gösterimi
        r_label.config(text=f"r: {r_val:.4f}    R²: {r2_val:.4f}")
        r_label.pack(pady=(5, 15))

        messagebox.showinfo("Başarılı", "Regresyon tamamlandı.")
    except Exception as e:
        messagebox.showerror("Hata", f"Hesaplama sırasında hata oluştu:\n{str(e)}")

# === ÜST BİLEŞENLER ===

select_button = tk.Button(form, text="CSV Dosyası Yükle", command=select_file, bg="#d9d9d9")
select_button.pack(pady=10)

status_label = tk.Label(form, text="Henüz dosya seçilmedi.", bg="#f0f0f0")
status_label.pack()

start_button = tk.Button(form, text="Hesaplamayı Başlat", command=start_regression, bg="#d9d9d9")
start_button.pack(pady=10)

# === Matplotlib Figür Ayarları ===

fig = Figure(figsize=(6.5, 4.5), dpi=100, facecolor="#f0f0f0")  # Arka plan uyumlu
ax = fig.add_subplot(111)
fig.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.15)

canvas = FigureCanvasTkAgg(fig, master=form)

# === Scrollable Treeview ===

table_frame = tk.Frame(form)
tree = ttk.Treeview(table_frame, columns=("x", "y", "predicted"), show="headings", height=10)
tree.heading("x", text="x")
tree.heading("y", text="y")
tree.heading("predicted", text="Tahmin y")

scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# === r ve R² etiketi ===

r_label = tk.Label(form, text="", font=("Arial", 12), bg="#f0f0f0")

# === Mainloop ===
form.mainloop()
