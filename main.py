import os

from PIL import Image


def gerar_frame1_respiracao(caminho_imagem=r"D:\exemplo002.jpg", nome_saida="frame1_respiracao.png"):
    if not os.path.exists(caminho_imagem):
        print(f"Erro: Arquivo não encontrado em '{caminho_imagem}'")
        return

    # Carrega a imagem base original
    base = Image.open(caminho_imagem).convert("RGBA")
    w, h = base.size

    # Imagem para o Frame 1
    frame1 = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    # 1. Base fixa: Pernas, saia inferior, sapatos e bolsa
    corte_inferior = int(h * 0.48)
    pernas_e_base = base.crop((0, corte_inferior, w, h))
    frame1.paste(pernas_e_base, (0, corte_inferior))

    # 2. Variação: Elevação de 1 pixel no tronco, jaqueta e cabeça (Inspiração)
    deslocamento_y = -1
    tronco_e_cabeca = base.crop((0, 0, w, corte_inferior))
    frame1.paste(tronco_e_cabeca, (0, deslocamento_y), mask=tronco_e_cabeca)

    # Salva em uma pasta organizada
    pasta_destino = r"D:\Frames_Animacao"
    os.makedirs(pasta_destino, exist_ok=True)
    
    caminho_final = os.path.join(pasta_destino, nome_saida)
    frame1.save(caminho_final)

    print(f"✅ Frame 1 (Respiração) salvo com sucesso em: {caminho_final}")

if __name__ == "__main__":
    gerar_frame1_respiracao()