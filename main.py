import os

from PIL import Image, ImageDraw


def criar_diretorios():
    if not os.path.exists("exports"):
        os.makedirs("exports")

def desenhar_kira_hd(respiracao=0, olho_fechado=False):
    # Canvas maior (64x128) para permitir detalhes anatômicos e quimono
    largura, altura = 64, 128
    img = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # PALETA AVANÇADA COM RAMPAS DE SOMBRA (ESTILO SASKIA/RPG JAPONÊS)
    OUTLINE = (35, 25, 45, 255)
    
    # Pele
    PELE_BRILHO = (255, 235, 220, 255)
    PELE_BASE = (255, 210, 190, 255)
    PELE_SOMBRA = (225, 160, 145, 255)
    BOCHECHA = (240, 120, 140, 200)

    # Cabelo Roxo/Preto
    CABELO_BRILHO = (120, 95, 145, 255)
    CABELO_BASE = (55, 40, 70, 255)
    CABELO_SOMBRA = (30, 20, 40, 255)

    # Quimono Lilás e Branco
    TECIDO_BRANCO = (245, 240, 250, 255)
    TECIDO_BRANCO_SOMBRA = (200, 190, 215, 255)
    KIMONO_LILAS = (85, 65, 120, 255)
    KIMONO_SOMBRA = (55, 40, 80, 255)

    # Faixa Obi e Flor
    OBI_VERMELHO = (210, 50, 75, 255)
    OBI_SOMBRA = (140, 30, 50, 255)
    OBI_AMARELO = (240, 180, 60, 255)
    FLOR_ROSA = (240, 140, 170, 255)

    dy = -respiracao  # Respiração suave

    # 1. SOMBRA ISOMÉTRICA NO CHÃO
    draw.ellipse([18, 114, 46, 124], fill=(20, 15, 30, 100))

    # 2. CABELO DE TRÁS (Coque Baixo + Mechas Caídas)
    draw.polygon([(20, 30+dy), (14, 65+dy), (22, 70+dy), (26, 40+dy)], fill=CABELO_SOMBRA)
    draw.polygon([(44, 30+dy), (50, 65+dy), (42, 70+dy), (38, 40+dy)], fill=CABELO_SOMBRA)

    # 3. PERNAS E PÉS (Tamancos Zori e Meias Tabi)
    # Pernas e Meias
    draw.rectangle([25, 90, 30, 116], fill=PELE_BASE)
    draw.rectangle([34, 90, 39, 116], fill=PELE_BASE)
    draw.rectangle([24, 108, 30, 116], fill=TECIDO_BRANCO)
    draw.rectangle([34, 108, 40, 116], fill=TECIDO_BRANCO)
    # Sapatos / Zori
    draw.rectangle([23, 115, 31, 118], fill=OBI_SOMBRA)
    draw.rectangle([33, 115, 41, 118], fill=OBI_SOMBRA)

    # 4. QUIMONO (SAIA E DOBRAS)
    draw.polygon([(20, 65+dy), (44, 65+dy), (46, 92+dy), (18, 92+dy)], fill=KIMONO_LILAS)
    draw.polygon([(20, 65+dy), (32, 65+dy), (30, 92+dy), (18, 92+dy)], fill=KIMONO_SOMBRA) # Sombra da dobra
    draw.rectangle([22, 90+dy, 42, 93+dy], fill=OUTLINE) # Borda do quimono

    # 5. FAIXA OBI (CINTURA)
    draw.rectangle([20, 56+dy, 44, 66+dy], fill=OBI_VERMELHO)
    draw.rectangle([20, 63+dy, 44, 66+dy], fill=OBI_SOMBRA)
    draw.rectangle([20, 59+dy, 44, 61+dy], fill=OBI_AMARELO) # Cordão acentuado

    # 6. TRONCO E DECOTE TRADICIONAL
    draw.polygon([(18, 38+dy), (46, 38+dy), (44, 57+dy), (20, 57+dy)], fill=TECIDO_BRANCO)
    draw.polygon([(22, 42+dy), (42, 42+dy), (38, 57+dy), (20, 57+dy)], fill=TECIDO_BRANCO_SOMBRA)
    
    # Decote / Pele
    draw.polygon([(26, 38+dy), (38, 38+dy), (32, 50+dy)], fill=PELE_BASE)
    draw.polygon([(28, 38+dy), (36, 38+dy), (32, 46+dy)], fill=PELE_BRILHO)

    # Mangas Caídas (Estilo Elegante)
    draw.polygon([(12, 40+dy), (20, 40+dy), (16, 75+dy), (10, 70+dy)], fill=TECIDO_BRANCO)
    draw.polygon([(12, 40+dy), (16, 40+dy), (13, 72+dy), (10, 70+dy)], fill=TECIDO_BRANCO_SOMBRA)
    
    draw.polygon([(44, 40+dy), (52, 40+dy), (54, 70+dy), (48, 75+dy)], fill=TECIDO_BRANCO)
    draw.polygon([(48, 40+dy), (52, 40+dy), (54, 70+dy), (50, 72+dy)], fill=TECIDO_BRANCO_SOMBRA)

    # Mãos delicadas
    draw.rectangle([13, 68+dy, 16, 73+dy], fill=PELE_BASE)
    draw.rectangle([48, 68+dy, 51, 73+dy], fill=PELE_BASE)

    # 7. CABEÇA E ROSTO (Proporção Anime Dedicada)
    draw.rectangle([21, 15+dy, 43, 38+dy], fill=PELE_BASE)
    draw.rectangle([21, 33+dy, 43, 38+dy], fill=PELE_SOMBRA) # Sombra do queixo

    # Bochechas e Rubor
    draw.rectangle([23, 30+dy, 27, 32+dy], fill=BOCHECHA)
    draw.rectangle([37, 30+dy, 41, 32+dy], fill=BOCHECHA)

    # Olhos expressivos em gradiente
    if not olho_fechado:
        # Olho Esquerdo
        draw.rectangle([24, 23+dy, 29, 31+dy], fill=OUTLINE)
        draw.rectangle([25, 24+dy, 28, 30+dy], fill=KIMONO_LILAS)
        draw.rectangle([25, 24+dy, 27, 26+dy], fill=(255, 255, 255, 255))
        
        # Olho Direito
        draw.rectangle([35, 23+dy, 40, 31+dy], fill=OUTLINE)
        draw.rectangle([36, 24+dy, 39, 30+dy], fill=KIMONO_LILAS)
        draw.rectangle([36, 24+dy, 38, 26+dy], fill=(255, 255, 255, 255))
    else:
        # Olhos fechados elegantes
        draw.line([(24, 28+dy), (29, 28+dy)], fill=OUTLINE, width=2)
        draw.line([(35, 28+dy), (40, 28+dy)], fill=OUTLINE, width=2)

    # BOCA DELICADA
    draw.rectangle([31, 34+dy, 33, 35+dy], fill=OBI_SOMBRA)

    # 8. CABELO ESTILIZADO (FRANJA E ORNAMENTO DE FLOR)
    draw.rectangle([20, 10+dy, 44, 22+dy], fill=CABELO_BASE)
    draw.rectangle([22, 12+dy, 42, 15+dy], fill=CABELO_BRILHO) # Brilho no topo

    # Franja Reta Anime com corte lateral
    draw.rectangle([20, 20+dy, 24, 32+dy], fill=CABELO_BASE)
    draw.rectangle([40, 20+dy, 44, 32+dy], fill=CABELO_BASE)
    draw.polygon([(24, 20+dy), (28, 26+dy), (32, 20+dy)], fill=CABELO_BASE)
    draw.polygon([(32, 20+dy), (36, 26+dy), (40, 20+dy)], fill=CABELO_BASE)

    # Flor Enfeite de Cabelo (Kanzashi)
    draw.ellipse([40, 14+dy, 48, 22+dy], fill=FLOR_ROSA)
    draw.ellipse([42, 16+dy, 46, 20+dy], fill=OBI_AMARELO)

    # 9. PLACA COM O NOME "KIRA"
    draw.rectangle([18, 120, 46, 127], fill=OUTLINE)
    draw.rectangle([19, 121, 45, 126], fill=KIMONO_LILAS)
    draw.text((24, 119), "KIRA", fill=(255, 255, 255, 255))

    return img

def gerar_animacao_kira():
    frames = []
    timeline = [
        (0, False), (0, False),
        (1, False), (1, False),
        (1, True),   # Pisca suavemente
        (0, False), (0, False), (0, False)
    ]

    for resp, pisca in timeline:
        frame = desenhar_kira_hd(respiracao=resp, olho_fechado=pisca)
        frames.append(frame)

    return frames

def exportar_kira():
    frames = gerar_animacao_kira()
    escala = 5
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
    spritesheet_hd.save("exports/spritesheet_kira.png")

    # GIF Animado
    frames_hd = [
        f.resize((largura * escala, altura * escala), resample=Image.NEAREST) 
        for f in frames
    ]
    frames_hd[0].save(
        "exports/animacao_kira.gif",
        save_all=True,
        append_images=frames_hd[1:],
        duration=190,
        loop=0
    )

    print("🌸 Personagem KIRA em alta resolução gerada na pasta 'exports/'!")

if __name__ == "__main__":
    criar_diretorios()
    exportar_kira()