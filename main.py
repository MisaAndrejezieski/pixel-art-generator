import os

from PIL import Image, ImageDraw, ImageFont


def criar_diretorios():
    if not os.path.exists("exports"):
        os.makedirs("exports")

# ==========================================
# PERFIS DE PERSONAGENS (CORES + NOMES)
# ==========================================
PERSONAGENS = {
    "gyaru": {
        "nome": "HANA",
        "pele_base": (255, 220, 190, 255),
        "cabelo_base": (240, 195, 80, 255),
        "cabelo_sombra": (200, 150, 50, 255),
        "cabelo_brilho": (255, 230, 140, 255),
        "olho_cor": (180, 100, 40, 255),
        "roupa_top": (230, 205, 160, 255),
        "roupa_detalhe": (180, 50, 60, 255),
        "meias": (240, 240, 240, 255),
        "cor_tag": (180, 50, 60, 255)
    },
    "cyber": {
        "nome": "YUMI",
        "pele_base": (255, 230, 220, 255),
        "cabelo_base": (255, 140, 190, 255),
        "cabelo_sombra": (210, 90, 140, 255),
        "cabelo_brilho": (255, 200, 230, 255),
        "olho_cor": (130, 60, 210, 255),
        "roupa_top": (80, 220, 240, 255),
        "roupa_detalhe": (40, 30, 50, 255),
        "meias": (40, 30, 50, 255),
        "cor_tag": (130, 60, 210, 255)
    },
    "gothic": {
        "nome": "SORA",
        "pele_base": (250, 235, 230, 255),
        "cabelo_base": (210, 215, 225, 255),
        "cabelo_sombra": (150, 155, 170, 255),
        "cabelo_brilho": (255, 255, 255, 255),
        "olho_cor": (210, 40, 60, 255),
        "roupa_top": (35, 30, 45, 255),
        "roupa_detalhe": (220, 220, 230, 255),
        "meias": (35, 30, 45, 255),
        "cor_tag": (35, 30, 45, 255)
    }
}

def desenhar_personagem_com_nome(tamanho=64, respiracao=0, olho_fechado=False, id_personagem="gyaru"):
    p = PERSONAGENS.get(id_personagem, PERSONAGENS["gyaru"])
    
    img = Image.new("RGBA", (tamanho, tamanho + 12), (0, 0, 0, 0)) # Espaço extra para a tag do nome
    draw = ImageDraw.Draw(img)

    PELE_SOMBRA = (p["pele_base"][0]-25, p["pele_base"][1]-35, p["pele_base"][2]-40, 255)
    BOCHECHA = (255, 130, 150, 220)
    OUTLINE = (25, 20, 30, 255)
    BRANCO = (255, 255, 255, 255)

    dy = -respiracao

    # 1. CABELO DE TRÁS
    draw.rectangle([13, 18 + dy, 18, 52 + dy], fill=p["cabelo_sombra"])
    draw.rectangle([45, 18 + dy, 50, 52 + dy], fill=p["cabelo_sombra"])

    # 2. PERNAS E MEIAS
    draw.rectangle([24, 46, 29, 56], fill=p["meias"])
    draw.rectangle([34, 46, 39, 56], fill=p["meias"])
    draw.rectangle([23, 55, 30, 60], fill=OUTLINE)
    draw.rectangle([33, 55, 40, 60], fill=OUTLINE)

    # 3. ROUPA / CORPO
    draw.rectangle([22, 42 + dy, 41, 48 + dy], fill=p["roupa_detalhe"])
    draw.rectangle([22, 34 + dy, 41, 42 + dy], fill=p["roupa_top"])
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

    draw.rectangle([20, 28 + dy, 24, 30 + dy], fill=BOCHECHA)
    draw.rectangle([39, 28 + dy, 43, 30 + dy], fill=BOCHECHA)

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

    # 5. CABELO DA FRENTE
    draw.rectangle([16, 10 + dy, 47, 18 + dy], fill=p["cabelo_base"])
    draw.rectangle([18, 12 + dy, 45, 14 + dy], fill=p["cabelo_brilho"])
    draw.rectangle([17, 18 + dy, 20, 28 + dy], fill=p["cabelo_base"])
    draw.rectangle([43, 18 + dy, 46, 28 + dy], fill=p["cabelo_base"])
    draw.rectangle([28, 18 + dy, 31, 22 + dy], fill=p["cabelo_base"])

    # 6. PLACA COM O NOME DA PERSONAGEM
    draw.rectangle([14, 63, 50, 73], fill=OUTLINE)
    draw.rectangle([15, 64, 49, 72], fill=p["cor_tag"])
    draw.text((22, 64), p["nome"], fill=BRANCO)

    return img

def gerar_animacao(id_personagem="gyaru"):
    frames = []
    timeline = [
        (0, False), (0, False), 
        (1, False), (1, False), 
        (1, True),  
        (0, False), (0, False), (0, False)
    ]

    for resp, pisca in timeline:
        frame = desenhar_personagem_com_nome(respiracao=resp, olho_fechado=pisca, id_personagem=id_personagem)
        frames.append(frame)

    return frames

def exportar_todas():
    for id_p, dados in PERSONAGENS.items():
        frames = gerar_animacao(id_p)
        escala = 6
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
        spritesheet_hd.save(f"exports/spritesheet_{dados['nome'].lower()}.png")

        # GIF Animado
        frames_hd = [
            f.resize((largura * escala, altura * escala), resample=Image.NEAREST) 
            for f in frames
        ]
        frames_hd[0].save(
            f"exports/animacao_{dados['nome'].lower()}.gif",
            save_all=True,
            append_images=frames_hd[1:],
            duration=180,
            loop=0
        )

        print(f"✅ Personagem {dados['nome']} gerada com sucesso!")

if __name__ == "__main__":
    criar_diretorios()
    exportar_todas() # Gera a Hana, Yumi e Sora de uma vez só!