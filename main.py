import base64
import io

from PIL import Image


def decodificar_e_reproduzir_gif(dados_base64, nome_saida="arte_reproduzida.gif"):
    # Decodifica os dados binários do GIF armazenados diretamente no script
    gif_bytes = base64.b64decode(dados_base64)
    gif_original = Image.open(io.BytesIO(gif_bytes))
    
    largura, altura = gif_original.size
    total_frames = getattr(gif_original, 'n_frames', 1)
    frames_reconstruidos = []

    # Varre a matriz de pixels quadro por quadro
    for n in range(total_frames):
        gif_original.seek(n)
        frame_atual = gif_original.convert("RGBA")
        matriz_src = frame_atual.load()
        
        novo_quadro = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
        matriz_dst = novo_quadro.load()

        # Mapeamento e pintura ponto por ponto (X, Y)
        for y in range(altura):
            for x in range(largura):
                matriz_dst[x, y] = matriz_src[x, y]
                
        frames_reconstruidos.append(novo_quadro)

    # Reconstrução e exportação do GIF final
    duracao = gif_original.info.get('duration', 100)
    frames_reconstruidos[0].save(
        nome_saida,
        save_all=True,
        append_images=frames_reconstruidos[1:],
        duration=duracao if duracao > 0 else 100,
        loop=0
    )
    print(f"✅ Imagem gerada com sucesso: {nome_saida}")

# Dados brutos da imagem codificados diretamente no código (sem arquivos externos ou caminhos)
DADOS_GIF_BASE64 = """
R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7
""" # Substitua este placeholder pela string base64 completa da imagem se desejar embutir tudo no arquivo .py

if __name__ == "__main__":
    decodificar_e_reproduzir_gif(DADOS_GIF_BASE64)