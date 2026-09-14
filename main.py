import os

from PIL import Image


def animar_sprite_profissional(caminho_imagem, nome_saida="guerreira_animada"):
    if not os.path.exists(caminho_imagem):
        print(f"Erro: Arquivo não encontrado em '{caminho_imagem}'")
        return

    base = Image.open(caminho_imagem).convert("RGBA")
    w, h = base.size
    frames = []

    # Criação de quadros com movimento simples
    for i in range(4):
        frame = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        
        # Parte inferior fixa (pernas/chão)
        pernas = base.crop((0, int(h * 0.5), w, h))
        frame.paste(pernas, (0, int(h * 0.5)))
        
        # Parte superior com deslocamento leve
        offset_y = -1 if i in [1, 2] else 0
        tronco = base.crop((0, 0, w, int(h * 0.5)))
        frame.paste(tronco, (0, offset_y), mask=tronco)
        
        # Redimensionamento sem perder a qualidade dos pixels (NEAREST)
        escala = 4
        frame_hd = frame.resize((w * escala, h * escala), Image.NEAREST)
        frames.append(frame_hd)

    os.makedirs("exports", exist_ok=True)
    caminho_saida = f"exports/{nome_saida}.gif"
    frames[0].save(
        caminho_saida,
        save_all=True,
        append_images=frames[1:],
        duration=200,
        loop=0
    )
    print(f"✅ Animação salva com sucesso em: {os.path.abspath(caminho_saida)}")

if __name__ == "__main__":
    # Caminho exato apontando para o seu Disco Local (D:)
    CAMINHO_EXATO = r"D:\exemplo001.jpg"
    
    animar_sprite_profissional(CAMINHO_EXATO, nome_saida="exemplo_animado")