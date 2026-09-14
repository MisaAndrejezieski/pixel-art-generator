import os

from PIL import Image


def animar_sprite_profissional(caminho_imagem, nome_saida="guerreira_animada"):
    if not os.path.exists(caminho_imagem):
        print(f"Coloque a imagem '{caminho_imagem}' na mesma pasta do script.")
        return

    # Carrega a arte de alta qualidade
    base = Image.open(caminho_imagem).convert("RGBA")
    w, h = base.size

    frames = []
    
    # Criando animação de respiração deslocando o tronco/cabeça
    for i in range(4):
        frame = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        
        # Sombra/Chão e Pernas ficam fixos
        pernas = base.crop((0, int(h * 0.5), w, h))
        frame.paste(pernas, (0, int(h * 0.5)))
        
        # Parte superior (corpo/cabeça/machado) sobe e desce 1 pixel
        offset_y = -1 if i in [1, 2] else 0
        tronco = base.crop((0, 0, w, int(h * 0.5)))
        frame.paste(tronco, (0, offset_y), mask=tronco)
        
        # Redimensiona para HD sem perder a nitidez dos pixels
        escala = 4
        frame_hd = frame.resize((w * escala, h * escala), Image.NEAREST)
        frames.append(frame_hd)

    # Exporta o GIF final com a arte profissional
    os.makedirs("exports", exist_ok=True)
    frames[0].save(
        f"exports/{nome_saida}.gif",
        save_all=True,
        append_images=frames[1:],
        duration=200,
        loop=0
    )
    print(f"✅ GIF salvo em exports/{nome_saida}.gif")

if __name__ == "__main__":
    # Nome do arquivo da imagem que você baixou
    animar_sprite_profissional("exemplo001.jpg")