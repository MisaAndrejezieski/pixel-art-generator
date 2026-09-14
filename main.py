import os

from PIL import Image, ImageDraw


def criar_diretorios():
    if not os.path.exists("exports"):
        os.makedirs("exports")

# ==========================================
# DEFINIÇÃO DE PALETAS DE ESTILO (ANIME)
# ==========================================
PALETAS = {
    "gyaru": {
        "pele_base": (255, 220, 190, 255),
        "cabelo_base": (240, 195, 80, 255),    # Loiro Dourado
        "cabelo_sombra": (200, 150, 50, 255),
        "cabelo_brilho": (255, 230, 140, 255),
        "olho_cor": (180, 100, 40, 255),        # Castanho Mel
        "roupa_top": (230, 205, 160, 255),      # Cardigan Beje
        "roupa_detalhe": (180, 50, 60, 255),    # Saia Xadrez Vermelha
        "meias": (240, 240, 240, 255),          # Meias Brancas Soltas
    },
    "cyber": {
        "pele_base": (255, 230, 220, 255),
        "cabelo_base": (255, 140, 190, 255),   # Rosa Pastel
        "cabelo_sombra": (210, 90, 140, 255),
        "cabelo_brilho": (255, 200, 230, 255),
        "olho_cor": (130, 60, 210, 255),       # Violeta Brilhante
        "roupa_top": (80, 220, 240, 255),       # Jaqueta Ciano
        "roupa_detalhe": (40, 30, 50, 255),     # Saia Escura
        "meias": (40, 30, 50, 255),             # Meia 3/4 Preta
    },
    "gothic": {
        "pele_base": (250, 235, 230, 255),
        "cabelo_base": (210, 215, 225, 255),   # Prata / Branco
        "cabelo_sombra": (150, 155, 170, 255),
        "cabelo_brilho": (255, 255, 255, 255),
        "olho_cor": (210, 40, 60, 255),        # Vermelho Carmim
        "roupa_top": (35, 30, 45, 255),        # Vestido Preto
        "roupa_detalhe": (220, 220, 230, 255),  # Babados Brancos
        "meias": (35, 30, 45, 255),
    }
}

def desenhar_personagem_custom(tamanho=64, respiracao=0, olho_fechado=False, estilo="gyaru"):
    p = PALETAS.get(estilo, PALETAS["gyaru"])
    
    img = Image.new("RGBA", (tamanho, tamanho), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    PELE_SOMBRA = (p["pele_base"][0]-25, p["pele_base"][1]-35, p["pele_base"][2]-40, 255)
    BOCHECHA = (255, 130, 150, 220)
    OUTLINE = (25, 20, 30, 255)
    BRANCO = (255, 255, 255, 255)

    dy = -respiracao

    # 1. CABELO DE TRÁS (Longo)
    draw.rectangle([13, 18 + dy, 18, 52 + dy], fill=p["cabelo_sombra"])
    draw.rectangle([45, 18 + dy, 50, 52 + dy], fill=p["cabelo_sombra"])

    # 2. PERNAS E MEIAS
    draw.rectangle([24, 46, 29, 56], fill=p["meias"])
    draw.rectangle([34, 46, 39, 56], fill=p["meias"])
    # Sapatos
    draw.rectangle([23, 55, 30, 60], fill=OUTLINE)
    draw.rectangle([33, 55, 40, 60], fill=OUTLINE)

    # 3. ROUPA / CORPO
    # Saia / Parte Inferior
    draw.rectangle([22, 42 + dy, 41, 48 + dy], fill=p["roupa_detalhe"])
    # Blusa / Jaqueta
    draw.rectangle([22, 34 + dy, 41, 42 + dy], fill=p["roupa_top"])
    
    # Detalhe do Peito (Laço ou Zíper)
    draw.rectangle([30, 36 + dy, 33, 40 + dy], fill=p["roupa_detalhe"])

    # Braços
    draw.rectangle([17, 35 + dy, 21, 44 + dy], fill=OUTLINE)
    draw.rectangle([18, 36 + dy, 20, 42 + dy], fill=p["roupa_top"])
    draw.rectangle([18, 43 + dy, 20, 44 + dy], fill=p["pele_base"])

    draw.rectangle([42, 35 + dy, 46, 44 + dy], fill=OUTLINE)
    draw.rectangle([43, 36 + dy, 45, 42 + dy], fill=p["roupa_top"])
    draw.rectangle([43, 43 + dy, 45, 44 + dy], fill=p["pele_base"])

    # 4. CABEÇA E ROSTO
    draw.rectangle([16, 12 + dy, 47, 36 + dy], fill=OUTLINE)
    draw.rectangle([18, 14 + dy, 45, 34 + dy], fill=p["pele_base"])
    draw.rectangle([18, 30 + dy, 45, 34 + dy], fill=PELE_SOMBRA)

    # Bochechas Coradas
    draw.rectangle([20, 28 + dy, 24, 30 + dy], fill=BOCHECHA)
    draw.rectangle([39, 28 + dy, 43, 30 + dy], fill=BOCHECHA)

    # Olhos Anime
    if not olho_fechado:
        draw.rectangle([22, 20 + dy, 28, 29 + dy], fill=OUTLINE)
        draw.rectangle([23, 21 + dy, 27, 28 + dy], fill=p["olho_cor"])
        draw.rectangle([23, 21 + dy, 25, 23 + dy], fill=BRANCO)

        draw.rectangle([35, 20 + dy, 41, 29 + dy], fill=OUTLINE)
        draw.rectangle([36, 21 + dy, 40, 28 + dy], fill=p["olho_cor"])
        draw.rectangle([36, 21 + dy, 38, 23 + dy], fill=BRANCO)
    else:
        draw.rectangle([21, 24 + dy, 29, 26 + dy], fill=OUTLINE)
        draw.rectangle([34, 24 + dy, 42, 26 + dy], fill=OUTLINE)

    # 5. CABELO DA FRENTE (Franja Estilizada)
    draw.rectangle([16, 10 + dy, 47, 18 + dy], fill=p["cabelo_base"])
    draw.rectangle([18, 12 + dy, 45, 14 + dy], fill=p["cabelo_brilho"])
    
    # Mechas Caídas
    draw.rectangle([17, 18 + dy, 20, 28 + dy], fill=p["cabelo_base"])
    draw.rectangle([43, 18 + dy, 46, 28 + dy], fill=p["cabelo_base"])
    draw.rectangle([28, 18 + dy, 31, 22 + dy], fill=p["cabelo_base"])

    return img

def gerar_animacao(estilo="gyaru"):
    frames = []
    timeline = [
        (0, False), (0, False), 
        (1, False), (1, False), 
        (1, True),  # Pisca o olho
        (0, False), (0, False), (0, False)
    ]

    for resp, pisca in timeline:
        frame = desenhar_personagem_custom(respiracao=resp, olho_fechado=pisca, estilo=estilo)
        frames.append(frame)

    return frames

def exportar_resultados(frames, nome_estilo, escala=6):
    largura, altura = frames[0].size
    total_frames = len(frames)

    # Spritesheet
    spritesheet = Image.new("RGBA", (largura * total_frames, altura), (0, 0, 0, 0))
    for idx, frame in enumerate(frames):
        spritesheet.paste(frame, (idx * largura, 0))

    spritesheet_hd = spritesheet.resize(
        (spritesheet.width * escala, spritesheet.height * escala), 
        resample=Image.NEAREST
    )
    spritesheet_hd.save(f"exports/spritesheet_{nome_estilo}.png")

    # GIF
    frames_hd = [
        f.resize((largura * escala, altura * escala), resample=Image.NEAREST) 
        for f in frames
    ]
    frames_hd[0].save(
        f"exports/animacao_{nome_estilo}.gif",
        save_all=True,
        append_images=frames_hd[1:],
        duration=180,
        loop=0
    )

    print(f"✨ Variação '{nome_estilo}' exportada com sucesso!")

if __name__ == "__main__":
    criar_diretorios()
    
    # QUAL ESTILO VOCÊ QUER GERAR? ("gyaru", "cyber" ou "gothic")
    ESTILO_ESCOLHIDO = "gyaru" 
    
    quadros = gerar_animacao(estilo=ESTILO_ESCOLHIDO)
    exportar_resultados(quadros, ESTILO_ESCOLHIDO)