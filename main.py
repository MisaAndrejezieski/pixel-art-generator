import os

from PIL import Image


def criar_diretorios():
    if not os.path.exists("exports"):
        os.makedirs("exports")

# ==========================================
# DEFINIÇÃO DA PALETA DE CORES
# ==========================================
PALETA = {
    ".": (0, 0, 0, 0),         # Transparente
    "K": (28, 18, 38, 255),     # Outline / Contorno Escuro
    "C": (58, 42, 75, 255),     # Cabelo Base
    "B": (105, 80, 135, 255),    # Cabelo Brilho
    "P": (255, 215, 190, 255),   # Pele Base
    "S": (225, 165, 145, 255),   # Pele Sombra
    "R": (245, 120, 140, 255),   # Rubor / Bochecha
    "O": (90, 60, 130, 255),     # Olho Lilás
    "W": (255, 255, 255, 255),   # Branco
    "V": (240, 235, 248, 255),   # Vestido Branco/Lilás
    "v": (190, 180, 210, 255),   # Vestido Sombra
    "Q": (75, 55, 110, 255),     # Quimono Roxo
    "q": (45, 30, 70, 255),      # Quimono Roxo Escuro
    "F": (210, 45, 70, 255),     # Faixa Obi
    "f": (140, 25, 45, 255),     # Faixa Sombra
    "A": (240, 180, 50, 255),    # Amarelo / Detalhes
    "L": (245, 140, 175, 255),   # Flor Rosa
    "H": (30, 20, 35, 80)        # Sombra do Chão (Semitransparente)
}

# ==========================================
# MAPA DE PIXELS (DESENHO ANATÔMICO 32x50)
# ==========================================
# Desenho pixel a pixel para evitar o aspecto de blocos retangulares
MAPA_BASE = [
    "................................",
    ".............KKKKKK.............",
    "............KCCCCBBK............",
    "...........KCCCCBBBCLK..........",
    "..........KCCCCBBBBLLLK.........",
    "..........KCCCCBBBBLLAK.........",
    "..........KCCCCCCBBBLLK.........",
    ".........KCCCCPCCCCCCCK.........",
    ".........KCCPCCCCCCCPCK.........",
    ".........KCPPPPPPSSSPCK.........",
    ".........KCPWWP..PWWPCK.........",
    ".........KCPWOP..PWOPCK.........",
    ".........KCPPSPPPPSPSCK.........",
    ".........KCPPPRPPRPPSCK.........",
    "..........KSPPPPPPPPSK..........",
    "..........KSSSSSSSSS1K..........",
    ".........KVVSSSSSSSSVV..........",
    "........KVVVVSSSSSSVVVV.........",
    ".......KVVVVVVPPPPVVVVVV........",
    "......KVVVVVVVPSSPVVVVVVV.......",
    "......KVvvvvVFFFFFFVvvvvV.......",
    "......KVvvvFFFFFFFFFFvvvV.......",
    "......KvvvFFFFffffFFFFvvK.......",
    "......KvvfFFFFfAAfFFFFfvK.......",
    "......KvvfFFFFffffFFFFfvK.......",
    "......KvvfFFFFFFFFFFfffvK.......",
    ".......KvfQQQQQQQQQQffvK........",
    ".......KvQQQQQQQQQQQQQvK........",
    ".......KvQQQQQQQQQQQQQvK........",
    ".......KvQQQqQQQQQqQQQvK........",
    "........KQqqqQQQQQqqqQK.........",
    "........KQqqqQQQQQqqqQK.........",
    "........KQQqqQQQQQqqqQK.........",
    ".........KQQqQQQQQqqqK..........",
    ".........KQQqQQQQQqqqK..........",
    "..........KqqQQQQQqK............",
    "..........KSPPPPPPSK............",
    "..........KSPPPPPPSK............",
    "..........KSSSSSSSSK............",
    "..........KSSSSSSSSK............",
    "..........KSPPPPSPSK............",
    "..........KSPPPPSPSK............",
    "..........KVVPPPPSVV............",
    "..........KFFFPPPSFF............",
    "..........KFFFPPPSFF............",
    ".........KffffSSSSfffK..........",
    "........HHHHHHHHHHHHHHHH........",
    ".......HHHHHHHHHHHHHHHHHH......."
]

def renderizar_frame(respiracao=0, piscar=False):
    largura = len(MAPA_BASE[0])
    altura = len(MAPA_BASE)
    img = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
    pixels = img.load()

    dy = -respiracao

    for y, linha in enumerate(MAPA_BASE):
        for x, char in enumerate(linha):
            if char == ".":
                continue
                
            cor = PALETA.get(char, (0, 0, 0, 0))
            
            # Ajuste dinâmico de piscar de olhos
            if piscar and char in ["W", "O"]:
                cor = PALETA["K"]
                
            # Aplica o deslocamento de respiração da cintura para cima
            y_final = y + dy if y < 36 else y
            
            if 0 <= y_final < altura:
                pixels[x, y_final] = cor

    return img

def exportar_personagem(nome_arquivo):
    frames = []
    # Animação de respiração e piscar
    timeline = [(0, False), (0, False), (1, False), (1, False), (1, True), (0, False)]

    for resp, pisca in timeline:
        frames.append(renderizar_frame(respiracao=resp, piscar=pisca))

    escala = 6
    largura, altura = frames[0].size
    total_frames = len(frames)

    # 1. Salva Spritesheet
    spritesheet = Image.new("RGBA", (largura * total_frames, altura), (0, 0, 0, 0))
    for idx, frame in enumerate(frames):
        spritesheet.paste(frame, (idx * largura, 0))

    spritesheet_hd = spritesheet.resize((spritesheet.width * escala, spritesheet.height * escala), Image.NEAREST)
    spritesheet_hd.save(f"exports/spritesheet_{nome_arquivo.lower()}.png")

    # 2. Salva GIF usando o nome da variável (SEM DESENHAR O NOME NA TELA)
    frames_hd = [f.resize((largura * escala, altura * escala), Image.NEAREST) for f in frames]
    frames_hd[0].save(
        f"exports/{nome_arquivo.lower()}.gif",
        save_all=True,
        append_images=frames_hd[1:],
        duration=180,
        loop=0
    )

    print(f"✨ Arquivo 'exports/{nome_arquivo.lower()}.gif' gerado com sucesso!")

if __name__ == "__main__":
    criar_diretorios()
    
    # DEFINA O NOME DO ARQUIVO AQUI (ex: "saskia", "kira", "miku")
    NOME_PERSONAGEM = "saskia_v2"
    
    exportar_personagem(NOME_PERSONAGEM)