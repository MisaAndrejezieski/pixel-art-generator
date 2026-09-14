import math
import os

from PIL import Image, ImageDraw


def criar_diretorios():
    """Garante que a pasta de saída existe."""
    if not os.path.exists("exports"):
        os.makedirs("exports")

def gerar_chibi_base(tamanho=32):
    """Gera um modelo simples de garota Chibi em Pixel Art (32x32)."""
    corpo = Image.new("RGBA", (tamanho, tamanho), (0, 0, 0, 0))
    draw_c = ImageDraw.Draw(corpo)
    
    # Cabeça
    draw_c.rectangle([10, 4, 21, 14], fill=(255, 220, 177, 255))
    draw_c.rectangle([9, 2, 22, 7], fill=(255, 105, 180, 255))
    draw_c.rectangle([12, 9, 14, 11], fill=(50, 50, 150, 255))
    draw_c.rectangle([17, 9, 19, 11], fill=(50, 50, 150, 255))
    
    # Tronco e Pernas
    draw_c.rectangle([12, 15, 19, 22], fill=(60, 180, 220, 255))
    draw_c.rectangle([13, 23, 15, 28], fill=(255, 220, 177, 255))
    draw_c.rectangle([16, 23, 18, 28], fill=(255, 220, 177, 255))

    # Braço isolado para animação
    braco = Image.new("RGBA", (tamanho, tamanho), (0, 0, 0, 0))
    draw_b = ImageDraw.Draw(braco)
    draw_b.rectangle([20, 16, 24, 18], fill=(255, 220, 177, 255))

    return corpo, braco

def animar_soco_chibi(corpo, braco, total_frames=6):
    """Aplica deslocamento e transformações sequenciais para o golpe."""
    frames = []
    largura, altura = corpo.size

    for i in range(total_frames):
        frame = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
        
        if i < 2:  # Preparação
            shift_corpo_x, shift_corpo_y = 0, 0
            shift_braco_x = -2
        elif i < 4:  # Impacto
            shift_corpo_x, shift_corpo_y = 1, 1
            shift_braco_x = 5
        else:  # Retorno
            shift_corpo_x, shift_corpo_y = 0, 0
            shift_braco_x = 1

        frame.paste(corpo, (shift_corpo_x, shift_corpo_y), mask=corpo)
        frame.paste(braco, (shift_corpo_x + shift_braco_x, shift_corpo_y), mask=braco)
        frames.append(frame)

    return frames

def exportar_resultados(frames, escala=8):
    """Gera o Spritesheet PNG e o GIF animado em HD."""
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
        duration=120,
        loop=0
    )

    print("🚀 Animação gerada com sucesso na pasta 'exports/'!")

if __name__ == "__main__":
    criar_diretorios()
    corpo, braco = gerar_chibi_base()
    quadros = animar_soco_chibi(corpo, braco)
    exportar_resultados(quadros)