import math
import os

from PIL import Image, ImageDraw


def criar_diretorios():
    if not os.path.exists("exports"):
        os.makedirs("exports")

def gerar_chibi_partes(tamanho=64):
    """Gera o corpo base e a estrutura modular do braço/ombro."""
    corpo = Image.new("RGBA", (tamanho, tamanho), (0, 0, 0, 0))
    draw_c = ImageDraw.Draw(corpo)

    # Cores
    PELE_BASE = (255, 224, 189, 255)
    PELE_SOMBRA = (230, 185, 150, 255)
    CABELO_BASE = (255, 105, 180, 255)
    CABELO_SOMBRA = (210, 60, 130, 255)
    CABELO_BRILHO = (255, 180, 220, 255)
    ROUPA_BASE = (40, 150, 220, 255)
    ROUPA_SOMBRA = (25, 90, 150, 255)
    OUTLINE = (30, 20, 40, 255)
    OLHO_COR = (100, 50, 200, 255)
    BRANCO = (255, 255, 255, 255)

    # 1. CHIQUINHAS (Separadas para dar efeito de balanço)
    chiquinhas = Image.new("RGBA", (tamanho, tamanho), (0, 0, 0, 0))
    draw_ch = ImageDraw.Draw(chiquinhas)
    draw_ch.rectangle([10, 18, 18, 48], fill=CABELO_SOMBRA)
    draw_ch.rectangle([45, 18, 53, 48], fill=CABELO_SOMBRA)
    draw_ch.rectangle([12, 20, 16, 52], fill=CABELO_BASE)
    draw_ch.rectangle([47, 20, 51, 52], fill=CABELO_BASE)

    # 2. PERNAS E SAPATOS
    draw_c.rectangle([24, 48, 29, 58], fill=PELE_BASE)
    draw_c.rectangle([23, 56, 30, 60], fill=OUTLINE)
    draw_c.rectangle([34, 48, 39, 58], fill=PELE_BASE)
    draw_c.rectangle([33, 56, 40, 60], fill=OUTLINE)

    # 3. TRONCO / VESTIDO
    draw_c.rectangle([22, 34, 41, 48], fill=ROUPA_BASE)
    draw_c.rectangle([22, 44, 41, 48], fill=ROUPA_SOMBRA)
    draw_c.rectangle([29, 34, 34, 38], fill=BRANCO)

    # 4. CABEÇA E ROSTO
    draw_c.rectangle([16, 12, 47, 36], fill=OUTLINE)
    draw_c.rectangle([18, 14, 45, 34], fill=PELE_BASE)
    draw_c.rectangle([18, 30, 45, 34], fill=PELE_SOMBRA)

    # Olhos
    draw_c.rectangle([22, 20, 28, 29], fill=OUTLINE)
    draw_c.rectangle([23, 21, 27, 28], fill=OLHO_COR)
    draw_c.rectangle([23, 21, 25, 23], fill=BRANCO)
    draw_c.rectangle([24, 28, 28, 29], fill=PELE_SOMBRA)

    draw_c.rectangle([35, 20, 41, 29], fill=OUTLINE)
    draw_c.rectangle([36, 21, 40, 28], fill=OLHO_COR)
    draw_c.rectangle([36, 21, 38, 23], fill=BRANCO)
    draw_c.rectangle([35, 28, 39, 29], fill=PELE_SOMBRA)

    # Franja
    draw_c.rectangle([16, 10, 47, 18], fill=CABELO_BASE)
    draw_c.rectangle([18, 12, 45, 14], fill=CABELO_BRILHO)
    draw_c.rectangle([20, 18, 23, 22], fill=CABELO_BASE)
    draw_c.rectangle([30, 18, 33, 24], fill=CABELO_BASE)
    draw_c.rectangle([40, 18, 43, 22], fill=CABELO_BASE)

    return corpo, chiquinhas

def desenhar_braco_articulado(tamanho, extensao):
    """
    Desenha o braço conectado ao ombro (x=38, y=36)
    e estica a parte do antebraço de acordo com a extensão.
    """
    braco = Image.new("RGBA", (tamanho, tamanho), (0, 0, 0, 0))
    draw_b = ImageDraw.Draw(braco)
    
    PELE_BASE = (255, 224, 189, 255)
    ROUPA_BASE = (40, 150, 220, 255)
    OUTLINE = (30, 20, 40, 255)

    # Manga / Ombro fixo no corpo
    draw_b.rectangle([38, 35, 43, 41], fill=OUTLINE)
    draw_b.rectangle([39, 36, 42, 40], fill=ROUPA_BASE)

    # Antebraço + Mão (Extensão dinâmica sem desconectar do ombro)
    x_inicio = 42
    x_fim = 48 + extensao
    
    draw_b.rectangle([x_inicio, 36, x_fim, 41], fill=OUTLINE)
    draw_b.rectangle([x_inicio, 37, x_fim - 1, 40], fill=PELE_BASE)

    return braco

def animar_soco_corrigido(corpo, chiquinhas, total_frames=8):
    frames = []
    largura, altura = corpo.size

    # Tabela da animação: (offset_corpo_x, extensao_braco, offset_cabelo_x)
    timeline = [
        (0,  0,  0),   # Frame 0: Neutro
        (-1, -2, 0),   # Frame 1: Antecipação (Recua o corpo, encolhe o braço)
        (2,  8, -1),   # Frame 2: IMPACTO! (Avança corpo, estica braço, cabelo atrasa)
        (2,  10, 1),   # Frame 3: Extensão Máxima + Efeito
        (1,  6,  2),   # Frame 4: Início do recuo
        (0,  2,  1),   # Frame 5: Retornando
        (0,  0,  0),   # Frame 6: Quase neutro
        (0,  0,  0),   # Frame 7: Neutro
    ]

    for i in range(total_frames):
        frame = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
        draw_f = ImageDraw.Draw(frame)

        c_x, extensao, cab_x = timeline[i]

        # 1. Desenha chiquinhas (com atraso de movimento)
        frame.paste(chiquinhas, (c_x + cab_x, 0), mask=chiquinhas)

        # 2. Desenha corpo
        frame.paste(corpo, (c_x, 0), mask=corpo)

        # 3. Gera e desenha o braço perfeitamente articulado
        braco = desenhar_braco_articulado(largura, extensao)
        frame.paste(braco, (c_x, 0), mask=braco)

        # 4. Linhas de efeito de velocidade no momento do impacto (Frames 2 e 3)
        if i in (2, 3):
            draw_f.line([56, 37, 62, 37], fill=(255, 255, 255, 220), width=1)
            draw_f.line([54, 40, 60, 40], fill=(255, 255, 255, 180), width=1)

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
    spritesheet_hd.save("exports/spritesheet_soco.png")

    frames_hd = [
        f.resize((largura * escala, altura * escala), resample=Image.NEAREST) 
        for f in frames
    ]
    frames_hd[0].save(
        "exports/animacao_soco.gif",
        save_all=True,
        append_images=frames_hd[1:],
        duration=90,
        loop=0
    )

    print("⚡ Animação corrigida com sucesso em 'exports/'!")

if __name__ == "__main__":
    criar_diretorios()
    corpo, chiquinhas = gerar_chibi_partes()
    quadros = animar_soco_corrigido(corpo, chiquinhas)
    exportar_resultados(quadros)