import os

from PIL import Image, ImageDraw


def criar_diretorios():
    if not os.path.exists("exports"):
        os.makedirs("exports")

def desenhar_frame_estudante(tamanho=64, respiracao=0, olho_fechado=False, offset_cabelo=0):
    img = Image.new("RGBA", (tamanho, tamanho), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # PALETA TRADICIONAL JAPONESA (SEIFUKU)
    PELE_BASE = (255, 228, 205, 255)
    PELE_SOMBRA = (230, 190, 165, 255)
    BOCHECHA = (255, 140, 160, 220)
    
    # Cabelo Preto / Castanho Escuro com Brilho Violeta
    CABELO_BASE = (30, 28, 38, 255)
    CABELO_SOMBRA = (18, 16, 24, 255)
    CABELO_BRILHO = (75, 70, 95, 255)

    # Uniforme Escolar (Sailor Fuku)
    UNIFORME_BRANCO = (240, 242, 250, 255)
    UNIFORME_AZUL = (25, 35, 65, 255)       # Azul-marinho clássico
    LACO_VERMELHO = (220, 40, 50, 255)       # Fita de marinheiro
    OUTLINE = (20, 18, 25, 255)
    OLHO_COR = (60, 90, 160, 255)            # Azul escuro límpido
    BRANCO = (255, 255, 255, 255)

    dy = -respiracao

    # 1. CABELO DE TRÁS (Longo e liso)
    draw.rectangle([14 + offset_cabelo, 18 + dy, 18 + offset_cabelo, 50 + dy], fill=CABELO_SOMBRA)
    draw.rectangle([45 - offset_cabelo, 18 + dy, 49 - offset_cabelo, 50 + dy], fill=CABELO_SOMBRA)

    # 2. PERNAS E SAPATOS (Meias Altas + Loafers)
    # Pernas com Meias Escuras
    draw.rectangle([24, 46, 29, 56], fill=UNIFORME_AZUL)  # Meia Esq
    draw.rectangle([34, 46, 39, 56], fill=UNIFORME_AZUL)  # Meia Dir
    # Sapatos Loafers
    draw.rectangle([23, 55, 30, 60], fill=OUTLINE)
    draw.rectangle([33, 55, 40, 60], fill=OUTLINE)

    # 3. TRONCO / UNIFORME DE MARINHEIRO
    # Saia Plissada Azul Marinho
    draw.rectangle([22, 42 + dy, 41, 48 + dy], fill=UNIFORME_AZUL)
    # Blusa Branca
    draw.rectangle([22, 34 + dy, 41, 42 + dy], fill=UNIFORME_BRANCO)
    
    # Gola Marinheiro (Azul) + Fita Vermelha
    draw.rectangle([22, 34 + dy, 41, 37 + dy], fill=UNIFORME_AZUL)
    draw.rectangle([30, 36 + dy, 33, 40 + dy], fill=LACO_VERMELHO) # Laço do peito

    # Braços (Mangas da Blusa)
    draw.rectangle([17, 35 + dy, 21, 44 + dy], fill=OUTLINE)
    draw.rectangle([18, 36 + dy, 20, 41 + dy], fill=UNIFORME_BRANCO)
    draw.rectangle([18, 42 + dy, 20, 43 + dy], fill=PELE_BASE)

    draw.rectangle([42, 35 + dy, 46, 44 + dy], fill=OUTLINE)
    draw.rectangle([43, 36 + dy, 45, 41 + dy], fill=UNIFORME_BRANCO)
    draw.rectangle([43, 42 + dy, 45, 43 + dy], fill=PELE_BASE)

    # 4. CABEÇA E ROSTO
    draw.rectangle([16, 12 + dy, 47, 36 + dy], fill=OUTLINE)
    draw.rectangle([18, 14 + dy, 45, 34 + dy], fill=PELE_BASE)
    draw.rectangle([18, 30 + dy, 45, 34 + dy], fill=PELE_SOMBRA)

    # Bochechas Coradas
    draw.rectangle([20, 28 + dy, 24, 30 + dy], fill=BOCHECHA)
    draw.rectangle([39, 28 + dy, 43, 30 + dy], fill=BOCHECHA)

    # Olhos
    if not olho_fechado:
        draw.rectangle([22, 20 + dy, 28, 29 + dy], fill=OUTLINE)
        draw.rectangle([23, 21 + dy, 27, 28 + dy], fill=OLHO_COR)
        draw.rectangle([23, 21 + dy, 25, 23 + dy], fill=BRANCO)

        draw.rectangle([35, 20 + dy, 41, 29 + dy], fill=OUTLINE)
        draw.rectangle([36, 21 + dy, 40, 28 + dy], fill=OLHO_COR)
        draw.rectangle([36, 21 + dy, 38, 23 + dy], fill=BRANCO)
    else:
        # Cílios piscando
        draw.rectangle([21, 24 + dy, 29, 26 + dy], fill=OUTLINE)
        draw.rectangle([34, 24 + dy, 42, 26 + dy], fill=OUTLINE)

    # 5. CABELO CORTE HIME (Franja reta + mechas laterais)
    draw.rectangle([16, 10 + dy, 47, 18 + dy], fill=CABELO_BASE)
    draw.rectangle([18, 12 + dy, 45, 14 + dy], fill=CABELO_BRILHO)
    # Mechas laterais características do estilo Hime
    draw.rectangle([16, 18 + dy, 20, 32 + dy], fill=CABELO_BASE)
    draw.rectangle([43, 18 + dy, 47, 32 + dy], fill=CABELO_BASE)
    # Franja Reta
    draw.rectangle([21, 18 + dy, 42, 21 + dy], fill=CABELO_BASE)

    return img

def gerar_animacao_idle():
    frames = []
    timeline = [
        (0, False, 0),
        (0, False, 0),
        (1, False, 1),
        (1, False, 1),
        (1, True,  1),  # Pisca
        (0, False, 0),
        (0, False, 0),
        (0, False, 0),
    ]

    for resp, pisca, cab in timeline:
        frame = desenhar_frame_estudante(respiracao=resp, olho_fechado=pisca, offset_cabelo=cab)
        frames.append(frame)

    return frames

def exportar_resultados(frames, escala=6):
    largura, altura = frames[0].size
    total_frames = len(frames)

    spritesheet = Image.new("RGBA", (largura * total_frames, altura), (0, 0, 0, 0))
    for idx, frame in enumerate(frames):
        spritesheet.paste(frame, (idx * largura, 0))

    spritesheet_hd = spritesheet.resize(
        (spritesheet.width * escala, spritesheet.height * escala), 
        resample=Image.NEAREST
    )
    spritesheet_hd.save("exports/spritesheet_idle.png")

    frames_hd = [
        f.resize((largura * escala, altura * escala), resample=Image.NEAREST) 
        for f in frames
    ]
    frames_hd[0].save(
        "exports/animacao_idle.gif",
        save_all=True,
        append_images=frames_hd[1:],
        duration=180,
        loop=0
    )

    print("🎌 Estudante japonesa em Pixel Art gerada em 'exports/'!")

if __name__ == "__main__":
    criar_diretorios()
    quadros = gerar_animacao_idle()
    exportar_resultados(quadros)