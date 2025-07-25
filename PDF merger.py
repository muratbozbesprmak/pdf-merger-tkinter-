import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PyPDF2 import PdfMerger

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Birleştirici")
        self.root.geometry("520x480")
        self.root.configure(bg="#2c3e50")
        self.pdf_files = []

        # Başlık etiketi (Title Label)
        title_label = tk.Label(root, text="PDF Birleştirici", font=("Segoe UI", 20, "bold"),
                               fg="white", bg="#2c3e50")
        title_label.pack(pady=10)

        # Dosya listesi ve scrollbar (File listbox and scrollbar)
        frame = tk.Frame(root, bg="#34495e")
        frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        self.file_listbox = tk.Listbox(frame, selectmode=tk.SINGLE, font=("Segoe UI", 12),
                                       bg="#ecf0f1", fg="#2c3e50", activestyle='none')
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)

        scrollbar = tk.Scrollbar(frame, command=self.file_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        self.file_listbox.config(yscrollcommand=scrollbar.set)

        # Butonlar (Buttons Frame)
        btn_frame = tk.Frame(root, bg="#2c3e50")
        btn_frame.pack(pady=10)

        add_button = tk.Button(btn_frame, text="Dosya Ekle", command=self.add_files,
                               font=("Segoe UI", 12), bg="#2980b9", fg="white", relief=tk.FLAT, width=12)
        add_button.grid(row=0, column=0, padx=5)

        up_button = tk.Button(btn_frame, text="Yukarı Taşı", command=self.move_up,
                              font=("Segoe UI", 12), bg="#27ae60", fg="white", relief=tk.FLAT, width=12)
        up_button.grid(row=0, column=1, padx=5)

        down_button = tk.Button(btn_frame, text="Aşağı Taşı", command=self.move_down,
                                font=("Segoe UI", 12), bg="#c0392b", fg="white", relief=tk.FLAT, width=12)
        down_button.grid(row=0, column=2, padx=5)

        # İlerleme çubuğu (Progressbar)
        self.progress = ttk.Progressbar(root, orient="horizontal", length=460, mode="determinate")
        self.progress.pack(pady=10)

        # Birleştir butonu (Merge Button)
        merge_button = tk.Button(root, text="PDF'leri Birleştir", command=self.merge_pdfs,
                                 font=("Segoe UI", 14, "bold"), bg="#f39c12", fg="white", relief=tk.FLAT, width=25)
        merge_button.pack(pady=10)

    def add_files(self):
        # Dosya ekle (Add files)
        files = filedialog.askopenfilenames(filetypes=[("PDF Dosyaları", "*.pdf")])
        for file in files:
            if file not in self.pdf_files:
                self.pdf_files.append(file)
                self.file_listbox.insert(tk.END, file.split("/")[-1])

    def move_up(self):
        # Seçili dosyayı yukarı taşı (Move selected file up)
        selection = self.file_listbox.curselection()
        if not selection or selection[0] == 0:
            return
        index = selection[0]
        self.pdf_files[index], self.pdf_files[index - 1] = self.pdf_files[index - 1], self.pdf_files[index]
        self.refresh_list(index - 1)

    def move_down(self):
        # Seçili dosyayı aşağı taşı (Move selected file down)
        selection = self.file_listbox.curselection()
        if not selection or selection[0] == len(self.pdf_files) - 1:
            return
        index = selection[0]
        self.pdf_files[index], self.pdf_files[index + 1] = self.pdf_files[index + 1], self.pdf_files[index]
        self.refresh_list(index + 1)

    def refresh_list(self, selected_index):
        # Listeyi güncelle ve seçili öğeyi koru (Refresh listbox and keep selection)
        self.file_listbox.delete(0, tk.END)
        for file in self.pdf_files:
            self.file_listbox.insert(tk.END, file.split("/")[-1])
        self.file_listbox.selection_set(selected_index)

    def merge_pdfs(self):
        # PDF birleştirme işlemi (PDF merge process)
        if len(self.pdf_files) < 2:
            messagebox.showwarning("Uyarı", "Lütfen en az iki PDF dosyası ekleyin.")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                 filetypes=[("PDF Dosyaları", "*.pdf")])
        if not save_path:
            return

        self.progress["maximum"] = len(self.pdf_files)
        self.progress["value"] = 0
        self.root.update_idletasks()

        try:
            merger = PdfMerger()
            for idx, pdf_file in enumerate(self.pdf_files, start=1):
                merger.append(pdf_file)
                self.progress["value"] = idx
                self.root.update_idletasks()  # Progressbar güncellemesi için
            merger.write(save_path)
            merger.close()
            messagebox.showinfo("Başarılı", "PDF dosyaları başarıyla birleştirildi.")
            self.progress["value"] = 0
        except Exception as e:
            messagebox.showerror("Hata", f"Birleştirme sırasında hata oluştu:\n{str(e)}")
            self.progress["value"] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
