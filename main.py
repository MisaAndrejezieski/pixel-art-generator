import os

from PIL import Image


def isolar_personagem_matriz():
    caminho_entrada = os.path.join("inputs", "personagem.gif")
    caminho_saida = os.path.join("exports", "garoto_isolado.gif")

    if not os.path.exists(caminho_entrada):
        print("❌ Coloque o GIF como 'personagem.gif' na pasta 'inputs'!")
        return

    gif_original = Image.open(caminho_entrada)
    largura, altura = gif_original.size
    total_frames = getattr(gif_original, 'n_frames', 1)
    frames_filtrados = []

    # Área de recorte aproximada do garoto no centro (Caixa Delimitadora / Bounding Box)
    # Coordenadas relativas aos pixels da imagem (X_inicio, Y_inicio, X_fim, Y_fim)
    x_min, y_min = int(largura * 0.32), int(altura * 0.22)
    x_max, y_max = int(largura * 0.68), int(altura * 0.92)

    print(f"Scaneando e isolando a matriz do garoto em {total_frames} quadros...")

    for n in range(total_frames):
        gif_original.seek(n)
        frame_atual = gif_original.convert("RGBA")
        matriz_src = frame_atual.load()

        # Cria uma nova tela com fundo 100% transparente
        novo_quadro = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
        matriz_dst = novo_quadro.load()

        # Scanner Ponto por Ponto
        for y in range(altura):
            for x in range(largura):
                # Mantém o pixel APENAS se ele estiver dentro dos limites do garoto
                if x_min <= x <= x_max and y_min <= y <= y_max:
                    matriz_dst[x, y] = matriz_src[x, y]
                else:
                    # Todo o resto da matriz (quadros, girassol, janela) vira transparente
                    matriz_dst[x, y] = (0, 0, 0, 0)

        frames_filtrados.append(novo_quadro)

    os.makedirs("exports", exist_ok=True)
    duracao = gif_original.info.get('duration', 100)

    # Salva o GIF final com o fundo removido
    frames_filtrados[0].save(
        caminho_saida,
        save_all=True,
        append_images=frames_filtrados[1:],
        duration=duracao if duracao > 0 else 100,
        loop=0,
        transparency=0,
        disposal=2
    )

    print(f"✅ Sucesso! Garoto isolado salvo em: {caminho_saida}")

if __name__ == "__main__":
    isolar_personagem_matriz()