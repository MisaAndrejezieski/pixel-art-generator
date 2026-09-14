import math
import os

from PIL import Image, ImageDraw


def criar_diretorios():
    if not os.path.exists("exports"):
        os.makedirs("exports")

def gerar_chibi_detalhada(tamanho=64):
    """
    Desenha uma personagem Chibi rica em detalhes usando resolução 64x64:
    Cabelo longo com chiquinhas, shading, sombras e contornos.
    """
    corpo = Image.new("RGBA", (tamanho, tamanho), (0, 0, 0, 0))
    draw_c = ImageDraw.Draw(corpo)

    # PALETA DE CORES
    PELE_BASE = (255, 224, 189, 255)
    PELE_SOMBRA = (230, 185, 150, 255)
    CABELO_BASE = (255, 105, 180, 255)    # Rosa Anime
    CABELO_SOMBRA = (210, 60, 130, 255)
    CABELO_BRILHO = (255, 180, 220, 255)
    ROUPA_BASE = (40, 150, 220, 255)      # Azul
    ROUPA_SOMBRA = (25, 90, 150, 255)
    OUTLINE = (30, 20, 40, 255)            # Contorno escuro
    OLHO_COR = (100, 50, 200, 255)
    BRANCO = (255, 255, 255, 255)

    # 1. CABELO DE TRÁS / CHIQUINHAS (atrás do tronco)
    draw_c.rectangle([10, 18, 18, 48], fill=CABELO_SOMBRA) # Chiquinha Esq
    draw_c.rectangle([45, 18, 53, 48], fill=CABELO_SOMBRA) # Chiquinha Dir
    draw_c.rectangle([12, 20, 16, 52], fill=CABELO_BASE)
    draw_c.rectangle([47, 20, 51, 52], fill=CABELO_BASE)

    # 2. PERNAS E SAPATOS
    # Perna Esquena
    draw_c.rectangle([24, 48, 29, 58], fill=PELE_BASE)
    draw_c.rectangle([23, 56, 30, 60], fill=OUTLINE)       # Sapato
    # Perna Direita
    draw_c.rectangle([34, 48, 39, 58], fill=PELE_BASE)
    draw_c.rectangle([33, 56, 40, 60], fill=OUTLINE)       # Sapato

    # 3. TRONCO / VESTIDO
    draw_c.rectangle([22, 34, 41, 48], fill=ROUPA_BASE)
    draw_c.rectangle([22, 44, 41, 48], fill=ROUPA_SOMBRA)  # Sombra da saia
    draw_c.rectangle([29, 34, 34, 38], fill=BRANCO)        # Gola da roupa

    # 4. CABEÇA / ROSTO (Formato Chibi Redondo)
    draw_c.rectangle([16, 12, 47, 36], fill=OUTLINE)       # Contorno
    draw_c.rectangle([18, 14, 45, 34], fill=PELE_BASE)     # Rosto
    draw_c.rectangle([18, 30, 45, 34], fill=PELE_SOMBRA)   # Sombra do queixo

    # Olho Esquerdo (Estilo Anime com brilho)
    draw_c.rectangle([22, 20, 28, 29], fill=OUTLINE)
    draw_c.rectangle([23, 21, 27, 28], fill=OLHO_COR)
    draw_c.rectangle([23, 21, 25, 23], fill=BRANCO)        # Brilho
    draw_c.rectangle([24, 28, 28, 29], fill=PELE_SOMBRA)   # Bochecha corada

    # Olho Direito
    draw_c.rectangle([35, 20, 41, 29], fill=OUTLINE)
    draw_c.rectangle([36, 21, 40, 28], fill=OLHO_COR)
    draw_c.rectangle([36, 21, 38, 23], fill=BRANCO)        # Brilho
    draw_c.rectangle([35, 28, 39, 29], fill=PELE_SOMBRA)

    # 5. FRANJA DO CABELO
    draw_c.rectangle([16, 10, 47, 18], fill=CABELO_BASE)
    draw_c.rectangle([18, 12, 45, 14], fill=CABELO_BRILHO) # Brilho no cabelo
    # Mechas caindo no rosto
    draw_c.rectangle([20, 18, 23, 22], fill=CABELO_BASE)
    draw_c.rectangle([30, 18, 33, 24], fill=CABELO_BASE)
    draw_c.rectangle([40, 18, 43, 22], fill=CABELO_BASE)

    # -------------------------------------------------------------
    # 6. BRAÇO SEPARADO (Para animação de soco)
    braco = Image.new("RGBA", (tamanho, tamanho), (0, 0, 0, 0))
    draw_b = ImageDraw.Draw(braco)
    # Ombro + Braço + Luva/Mão
    draw_b.rectangle([40, 35, 52, 41], fill=OUTLINE)
    draw_b.rectangle([41, 36, 48, 40], fill=ROUPA_BASE)
    draw_b.rectangle([47, 35, 53, 41], fill=PELE_BASE)     # Mãozinha/Punho

    return corpo, braco

def animar_soco_chibi(corpo, braco, total_frames=8):
    frames = []
    largura, altura = corpo.size

    for i in range(total_frames):
        frame = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
        draw_f = ImageDraw.Draw(frame)

        # Lógica fluida de Soco (Antecipação -> Impacto -> Efeito -> Retorno)
        if i == 0:    # Neutro
            offset_x, offset_y, braco_x = 0, 0, 0
        elif i == 1:  # Recuo/Antecipação (Puxa para trás e abaixa)
            offset_x, offset_y, braco_x = -2, 1, -4
        elif i in (2, 3): # IMPACTO! (Avança o corpo e estica o braço)
            offset_x, offset_y, braco_x = 3, 0, 12
            # Desenha linhas de efeito de velocidade (Hit lines)
            draw_f.line([54, 36, 62, 36], fill=(255, 255, 255, 200), width=2)
            draw_f.line([52, 40, 60, 40], fill=(255, 255, 255, 200), width=1)
        elif i == 4:  # Sustentação do impacto
            offset_x, offset_y, braco_x = 2, 0, 10
        elif i in (5, 6): # Retorno
            offset_x, offset_y, braco_x = 1, 0, 4
        else:         # Volta ao neutro
            offset_x, offset_y, braco_x = 0, 0, 0

        # Aplica o corpo e depois o braço por cima
        frame.paste(corpo, (offset_x, offset_y), mask=corpo)
        frame.paste(braco, (offset_x + braco_x, offset_y), mask=braco)
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
    spritesheet_hd.save("exports/spritesheet_soco.png")

    # GIF
    frames_hd = [
        f.resize((largura * escala, altura * escala), resample=Image.NEAREST) 
        for f in frames
    ]
    frames_hd[0].save(
        "exports/animacao_soco.gif",
        save_all=True,
        append_images=frames_hd[1:],
        duration=90, # Velocidade da animação (ms)
        loop=0
    )

    print("✨ Animação Chibi gerada com sucesso na pasta 'exports/'!")

if __name__ == "__main__":
    criar_diretorios()
    corpo, braco = gerar_chibi_detalhada()
    quadros = animar_soco_chibi(corpo, braco)
    exportar_resultados(quadros)