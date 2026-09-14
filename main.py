import os

from PIL import Image, ImageDraw


def criar_diretorios():
    if not os.path.exists("exports"):
        os.makedirs("exports")

def desenhar_frame_idle(tamanho=64, respiracao=0, olho_fechado=False, offset_cabelo=0):
    """
    Desenha a personagem completa parada.
    - respiracao: 0 (neutro) ou 1 (corpo sobe 1px ao respirar)
    - olho_fechado: True (pisca os olhos)
    - offset_cabelo: deslocamento sutil das chiquinhas
    """
    img = Image.new("RGBA", (tamanho, tamanho), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # PALETA DE CORES
    PELE_BASE = (255, 224, 189, 255)
    PELE_SOMBRA = (230, 185, 150, 255)
    BOCHECHA = (255, 150, 160, 255)
    CABELO_BASE = (255, 105, 180, 255)
    CABELO_SOMBRA = (210, 60, 130, 255)
    CABELO_BRILHO = (255, 180, 220, 255)
    ROUPA_BASE = (40, 150, 220, 255)
    ROUPA_SOMBRA = (25, 90, 150, 255)
    OUTLINE = (30, 20, 40, 255)
    OLHO_COR = (100, 50, 200, 255)
    BRANCO = (255, 255, 255, 255)

    # Deslocamento vertical da respiração (aplica do tronco para cima)
    dy = -respiracao

    # 1. CHIQUINHAS (Movem levemente com a respiração)
    draw.rectangle([10 + offset_cabelo, 18 + dy, 18 + offset_cabelo, 48 + dy], fill=CABELO_SOMBRA)
    draw.rectangle([45 - offset_cabelo, 18 + dy, 53 - offset_cabelo, 48 + dy], fill=CABELO_SOMBRA)
    draw.rectangle([12 + offset_cabelo, 20 + dy, 16 + offset_cabelo, 52 + dy], fill=CABELO_BASE)
    draw.rectangle([47 - offset_cabelo, 20 + dy, 51 - offset_cabelo, 52 + dy], fill=CABELO_BASE)

    # 2. PERNAS E SAPATOS (Ficam fixas no chão)
    draw.rectangle([24, 48, 29, 58], fill=PELE_BASE)
    draw.rectangle([23, 56, 30, 60], fill=OUTLINE)
    draw.rectangle([34, 48, 39, 58], fill=PELE_BASE)
    draw.rectangle([33, 56, 40, 60], fill=OUTLINE)

    # 3. TRONCO E BRAÇOS (Sobem 1px na respiração)
    # Braço Esquerdo
    draw.rectangle([17, 35 + dy, 22, 45 + dy], fill=OUTLINE)
    draw.rectangle([18, 36 + dy, 21, 41 + dy], fill=ROUPA_BASE)
    draw.rectangle([18, 42 + dy, 21, 44 + dy], fill=PELE_BASE)

    # Braço Direito
    draw.rectangle([41, 35 + dy, 46, 45 + dy], fill=OUTLINE)
    draw.rectangle([42, 36 + dy, 45, 41 + dy], fill=ROUPA_BASE)
    draw.rectangle([42, 42 + dy, 45, 44 + dy], fill=PELE_BASE)

    # Corpo / Vestido
    draw.rectangle([22, 34 + dy, 41, 48 + dy], fill=ROUPA_BASE)
    draw.rectangle([22, 44 + dy, 41, 48 + dy], fill=ROUPA_SOMBRA)
    draw.rectangle([29, 34 + dy, 34, 37 + dy], fill=BRANCO)

    # 4. CABEÇA / ROSTO
    draw.rectangle([16, 12 + dy, 47, 36 + dy], fill=OUTLINE)
    draw.rectangle([18, 14 + dy, 45, 34 + dy], fill=PELE_BASE)
    draw.rectangle([18, 30 + dy, 45, 34 + dy], fill=PELE_SOMBRA)

    # Bochechas Coradas
    draw.rectangle([20, 28 + dy, 24, 30 + dy], fill=BOCHECHA)
    draw.rectangle([39, 28 + dy, 43, 30 + dy], fill=BOCHECHA)

    # Olhos (Abertos ou Piscando)
    if not olho_fechado:
        # Olho Esquerdo Aberto
        draw.rectangle([22, 20 + dy, 28, 29 + dy], fill=OUTLINE)
        draw.rectangle([23, 21 + dy, 27, 28 + dy], fill=OLHO_COR)
        draw.rectangle([23, 21 + dy, 25, 23 + dy], fill=BRANCO)
        
        # Olho Direito Aberto
        draw.rectangle([35, 20 + dy, 41, 29 + dy], fill=OUTLINE)
        draw.rectangle([36, 21 + dy, 40, 28 + dy], fill=OLHO_COR)
        draw.rectangle([36, 21 + dy, 38, 23 + dy], fill=BRANCO)
    else:
        # Olhos Fechados (Cílios/Linha fofa)
        draw.rectangle([21, 24 + dy, 29, 26 + dy], fill=OUTLINE)
        draw.rectangle([34, 24 + dy, 42, 26 + dy], fill=OUTLINE)

    # Franja do Cabelo
    draw.rectangle([16, 10 + dy, 47, 18 + dy], fill=CABELO_BASE)
    draw.rectangle([18, 12 + dy, 45, 14 + dy], fill=CABELO_BRILHO)
    draw.rectangle([20, 18 + dy, 23, 22 + dy], fill=CABELO_BASE)
    draw.rectangle([30, 18 + dy, 33, 24 + dy], fill=CABELO_BASE)
    draw.rectangle([40, 18 + dy, 43, 22 + dy], fill=CABELO_BASE)

    return img

def gerar_animacao_idle():
    """Roteiro de quadros para um loop natural de Idle com piscar de olhos."""
    frames = []
    
    # Roteiro do Loop: (respiracao, olho_fechado, offset_cabelo)
    timeline = [
        (0, False, 0),  # Frame 0: Neutro
        (0, False, 0),  # Frame 1: Neutro
        (1, False, 1),  # Frame 2: Inhala (Corpo sobe 1px, cabelo abre)
        (1, False, 1),  # Frame 3: Inhala
        (1, True,  1),  # Frame 4: PISCA OS OLHOS!
        (0, False, 0),  # Frame 5: Exhala (Volta ao neutro)
        (0, False, 0),  # Frame 6: Neutro
        (0, False, 0),  # Frame 7: Neutro
    ]

    for resp, pisca, cab in timeline:
        frame = desenhar_frame_idle(respiracao=resp, olho_fechado=pisca, offset_cabelo=cab)
        frames.append(frame)

    return frames

def exportar_resultados(frames, escala=6):
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
    spritesheet_hd.save("exports/spritesheet_idle.png")

    # GIF Animado
    frames_hd = [
        f.resize((largura * escala, altura * escala), resample=Image.NEAREST) 
        for f in frames
    ]
    frames_hd[0].save(
        "exports/animacao_idle.gif",
        save_all=True,
        append_images=frames_hd[1:],
        duration=180,  # Tempo mais suave para Idle (180ms por frame)
        loop=0
    )

    print("✨ Animação IDLE (Parada + Piscando) gerada em 'exports/'!")

if __name__ == "__main__":
    criar_diretorios()
    quadros = gerar_animacao_idle()
    exportar_resultados(quadros)