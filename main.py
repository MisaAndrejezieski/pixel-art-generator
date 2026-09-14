import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

class SpritesheetAnimatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Animador & Visualizador de Spritesheets (Aseprite / LibreSprite)")
        self.root.geometry("900x650")
        self.root.minsize(800, 550)

        # Configurações de tema escuro básico
        self.root.configure(bg="#2b2b2b")
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(".", background="#2b2b2b", foreground="#ffffff")
        self.style.configure("TButton", background="#3c3f41", foreground="#ffffff", borderwidth=1)
        self.style.configure("TLabel", background="#2b2b2b", foreground="#ffffff")
        self.style.configure("TFrame", background="#2b2b2b")

        # Variáveis de Estado
        self.image_path = None
        self.original_spritesheet = None
        self.frames = []
        self.current_frame_idx = 0
        self.is_playing = False
        self.animation_job = None

        # Configurações do Grid / Spritesheet
        self.cols_var = tk.IntVar(value=6)
        self.rows_var = tk.IntVar(value=1)
        self.fps_var = tk.IntVar(value=8)
        self.zoom_var = tk.DoubleVar(value=3.0)

        self._build_ui()

    def _build_ui(self):
        # Container Principal
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Painel Esquerdo (Controles)
        control_panel = ttk.Frame(main_container, width=280)
        control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # Painel Direito (Visualização / Canvas)
        preview_panel = ttk.Frame(main_container)
        preview_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- CONTROLES DE ARQUIVO ---
        file_group = ttk.LabelFrame(control_panel, text=" Arquivo ", padding=10)
        file_group.pack(fill=tk.X, pady=(0, 10))

        btn_load = ttk.Button(file_group, text="📁 Carregar Imagem / Spritesheet", command=self.load_image)
        btn_load.pack(fill=tk.X, pady=2)

        # --- CONFIGURAÇÕES DE RECORTE ---
        slice_group = ttk.LabelFrame(control_panel, text=" Divisão da Spritesheet ", padding=10)
        slice_group.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(slice_group, text="Colunas (Frames X):").pack(anchor=tk.W)
        sp_cols = ttk.Spinbox(slice_group, from_=1, to=64, textvariable=self.cols_var, command=self.update_slicing)
        sp_cols.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(slice_group, text="Linhas (Frames Y):").pack(anchor=tk.W)
        sp_rows = ttk.Spinbox(slice_group, from_=1, to=64, textvariable=self.rows_var, command=self.update_slicing)
        sp_rows.pack(fill=tk.X, pady=(0, 5))

        # --- CONTROLES DE ANIMAÇÃO ---
        anim_group = ttk.LabelFrame(control_panel, text=" Animação ", padding=10)
        anim_group.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(anim_group, text="Velocidade (FPS):").pack(anchor=tk.W)
        sp_fps = ttk.Spinbox(anim_group, from_=1, to=60, textvariable=self.fps_var)
        sp_fps.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(anim_group, text="Zoom de Visualização:").pack(anchor=tk.W)
        sc_zoom = ttk.Scale(anim_group, from_=1.0, to=8.0, variable=self.zoom_var, command=lambda e: self.render_current_frame())
        sc_zoom.pack(fill=tk.X, pady=(0, 10))

        btn_play = ttk.Button(anim_group, text="▶ Play / Pause", command=self.toggle_play)
        btn_play.pack(fill=tk.X, pady=2)

        # --- EXPORTAÇÃO ---
        export_group = ttk.LabelFrame(control_panel, text=" Exportação ", padding=10)
        export_group.pack(fill=tk.X, pady=(0, 10))

        btn_export_gif = ttk.Button(export_group, text="💾 Exportar Animação (.GIF)", command=self.export_gif)
        btn_export_gif.pack(fill=tk.X, pady=2)

        # --- ÁREA DE VISUALIZAÇÃO (CANVAS) ---
        self.canvas_frame = ttk.Frame(preview_panel, relief=tk.SUNKEN, borderwidth=2)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Barra de Status
        self.status_label = ttk.Label(preview_panel, text="Abra um arquivo exportado do Aseprite/LibreSprite para começar.", anchor=tk.W)
        self.status_label.pack(fill=tk.X, pady=(5, 0))

    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Selecionar Spritesheet ou Imagem",
            filetypes=[("Imagens PNG/JPG", "*.png *.jpg *.jpeg *.bmp"), ("Todos os arquivos", "*.*")]
        )
        if not file_path:
            return

        try:
            self.image_path = file_path
            self.original_spritesheet = Image.open(file_path).convert("RGBA")
            self.update_slicing()
            self.status_label.config(text=f"Carregado: {os.path.basename(file_path)} ({self.original_spritesheet.width}x{self.original_spritesheet.height}px)")
        except Exception as e:
            messagebox.showerror("Erro ao Carregar", f"Não foi possível abrir a imagem:\n{str(e)}")

    def update_slicing(self):
        if not self.original_spritesheet:
            return

        cols = max(1, self.cols_var.get())
        rows = max(1, self.rows_var.get())

        sw = self.original_spritesheet.width // cols
        sh = self.original_spritesheet.height // rows

        if sw <= 0 or sh <= 0:
            return

        self.frames = []
        for r in range(rows):
            for c in range(cols):
                box = (c * sw, r * sh, (c + 1) * sw, (r + 1) * sh)
                frame_img = self.original_spritesheet.crop(box)
                self.frames.append(frame_img)

        self.current_frame_idx = 0
        self.render_current_frame()

    def render_current_frame(self):
        if not self.frames:
            return

        frame = self.frames[self.current_frame_idx]
        zoom = max(1.0, self.zoom_var.get())

        new_w = int(frame.width * zoom)
        new_h = int(frame.height * zoom)

        # Resizing sem perda de qualidade (Pixel Perfect)
        resized_frame = frame.resize((new_w, new_h), Image.NEAREST)
        self.tk_image = ImageTk.PhotoImage(resized_frame)

        self.canvas.delete("all")
        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()

        if cw <= 1: cw = 500
        if ch <= 1: ch = 400

        # Centralização
        x = max(0, (cw - new_w) // 2)
        y = max(0, (ch - new_h) // 2)

        self.canvas.create_image(x, y, anchor=tk.NW, image=self.tk_image)

    def next_frame(self):
        if not self.frames or not self.is_playing:
            return

        self.current_frame_idx = (self.current_frame_idx + 1) % len(self.frames)
        self.render_current_frame()

        fps = max(1, self.fps_var.get())
        interval_ms = int(1000 / fps)
        self.animation_job = self.root.after(interval_ms, self.next_frame)

    def toggle_play(self):
        if not self.frames:
            return

        self.is_playing = not self.is_playing
        if self.is_playing:
            self.next_frame()
        elif self.animation_job:
            self.root.after_cancel(self.animation_job)

    def export_gif(self):
        if not self.frames:
            messagebox.showwarning("Aviso", "Nenhum frame fatiado para exportar!")
            return

        save_path = filedialog.asksaveasfilename(
            title="Salvar GIF Animado",
            defaultextension=".gif",
            filetypes=[("Arquivo GIF", "*.gif")]
        )
        if not save_path:
            return

        fps = max(1, self.fps_var.get())
        duration_ms = int(1000 / fps)

        try:
            self.frames[0].save(
                save_path,
                save_all=True,
                append_images=self.frames[1:],
                duration=duration_ms,
                loop=0,
                disposal=2
            )
            messagebox.showinfo("Sucesso", f"GIF exportado com sucesso para:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Erro de Exportação", f"Erro ao gerar GIF:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SpritesheetAnimatorApp(root)
    root.mainloop()