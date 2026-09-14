import os

from PIL import Image, ImageDraw


def gerar_walkcycle_guerreira(nome_saida="guerreira_andando_perfeito"):
    # Resolução base de cada sprite (Aproximadamente 60x100)
    w, h = 64, 96
    
    # ---------------------------------------------------------
    # PALETA DE CORES OFICIAL DA GUERREIRA
    # ---------------------------------------------------------
    C = {
        "transp": (0, 0, 0, 0),
        "outline": (35, 25, 40, 255),
        
        # Cabelo Loiro (com Hue Shift / Sombras Castanhas)
        "hair_light": (245, 210, 150, 255),
        "hair_mid": (210, 160, 100, 255),
        "hair_shadow": (140, 90, 70, 255),
        
        # Pele
        "skin_light": (255, 220, 200, 255),
        "skin_mid": (240, 180, 160, 255),
        "skin_shadow": (210, 140, 130, 255),
        
        # Roupa Vermelha
        "cloth_light": (240, 100, 110, 255),
        "cloth_mid": (220, 70, 80, 255),
        "cloth_shadow": (160, 40, 55, 255),
        
        # Machado e Armadura (Metal e Madeira)
        "metal_light": (230, 235, 240, 255),
        "metal_mid": (150, 155, 165, 255),
        "metal_dark": (80, 80, 90, 255),
        "wood": (90, 70, 60, 255)
    }

    # ---------------------------------------------------------
    # ESTRUTURA DOS 6 QUADROS DA CAMINHADA (ANATOMIA REAL)
    # ---------------------------------------------------------
    # Cada quadro altera: altura do corpo, posição das pernas, 
    # balanço do tronco, movimento dos braços e inclinação do machado.
    quadros_config = [
        # Frame 0: Perna Esquerda à Frente (Contacto Inicial)
        {"body_y": 0, "leg_l": (-8, 18), "leg_r": (8, 14), "arm_angle": -5, "axe_tilt": -2},
        
        # Frame 1: Recuo / Impacto (Down Pose - Corpo Baixa)
        {"body_y": 3, "leg_l": (-10, 16), "leg_r": (4, 12), "arm_angle": 0, "axe_tilt": -5},
        
        # Frame 2: Passagem (Passing Pose - Perna Direita Cruzando)
        {"body_y": 1, "leg_l": (-2, 18), "leg_r": (-2, 8), "arm_angle": 5, "axe_tilt": 0},
        
        # Frame 3: Perna Direita à Frente (Contacto Inicial)
        {"body_y": 0, "leg_l": (8, 14), "leg_r": (-8, 18), "arm_angle": 8, "axe_tilt": 3},
        
        # Frame 4: Recuo / Impacto Direito (Down Pose - Corpo Baixa)
        {"body_y": 3, "leg_l": (4, 12), "leg_r": (-10, 16), "arm_angle": 3, "axe_tilt": 5},
        
        # Frame 5: Passagem Esquerda (Passing Pose - Perna Esquerda Cruzando)
        {"body_y": 1, "leg_l": (-2, 8), "leg_r": (-2, 18), "arm_angle": -3, "axe_tilt": 0}
    ]

    sprites = []

    for idx, cfg in enumerate(quadros_config):
        img = Image.new("RGBA", (w, h), C["transp"])
        draw = ImageDraw.Draw(img)

        off_y = cfg["body_y"]
        
        # 1. SOMBRA NO CHÃO (Suave)
        draw.ellipse([18, 88, 46, 94], fill=(20, 20, 30, 90))

        # 2. MACHADO (PARTE DE TRÁS - CABO E HASTE)
        axe_x = 42 + cfg["axe_tilt"]
        draw.line([axe_x, 10 + off_y, axe_x - 2, 88], fill=C["wood"], width=3)
        draw.polygon([(axe_x - 12, 12 + off_y), (axe_x + 14, 4 + off_y), (axe_x + 8, 38 + off_y), (axe_x - 8, 28 + off_y)], fill=C["metal_mid"])
        draw.polygon([(axe_x + 2, 8 + off_y), (axe_x + 12, 6 + off_y), (axe_x + 6, 26 + off_y)], fill=C["metal_light"])

        # 3. PERNAS E BOTAS (ANATOMIA DA PASSADA)
        # Perna Traseira
        lx_r, ly_r = cfg["leg_r"]
        draw.polygon([(32 + lx_r, 58 + off_y), (38 + lx_r, 74), (32 + lx_r, 88)], fill=C["cloth_shadow"])
        draw.polygon([(28 + lx_r, 76), (36 + lx_r, 76), (34 + lx_r, 88), (26 + lx_r, 88)], fill=C["outline"]) # Bota

        # Perna Dianteira
        lx_l, ly_l = cfg["leg_l"]
        draw.polygon([(24 + lx_l, 58 + off_y), (18 + lx_l, 74), (22 + lx_l, 88)], fill=C["cloth_mid"])
        draw.polygon([(16 + lx_l, 76), (24 + lx_l, 76), (22 + lx_l, 88), (14 + lx_l, 88)], fill=C["outline"]) # Bota

        # 4. QUADRIL E MACACÃO VERMELHO
        draw.polygon([(20, 48 + off_y), (42, 48 + off_y), (38, 64 + off_y), (22, 64 + off_y)], fill=C["cloth_mid"])
        draw.polygon([(22, 48 + off_y), (32, 48 + off_y), (30, 62 + off_y), (22, 62 + off_y)], fill=C["cloth_light"])

        # 5. BUSTO E CORPO (Curvas e Iluminação)
        draw.ellipse([22, 36 + off_y, 36, 48 + off_y], fill=C["cloth_light"]) # Seios / Decote
        draw.ellipse([30, 37 + off_y, 42, 48 + off_y], fill=C["cloth_mid"])

        # 6. CABEÇA E CABELO LOIRO (Com Hue Shift e Volume)
        head_y = 18 + off_y
        # Cabelo Traseiro / Volume
        draw.ellipse([12, head_y - 4, 38, head_y + 24], fill=C["hair_shadow"])
        draw.ellipse([14, head_y - 2, 36, head_y + 20], fill=C["hair_mid"])
        
        # Rosto
        draw.rectangle([22, head_y + 6, 34, head_y + 18], fill=C["skin_light"])
        draw.rectangle([30, head_y + 8, 33, head_y + 14], fill=C["cloth_shadow"]) # Olho roxo
        
        # Cabelo Franja / Frentes
        draw.polygon([(16, head_y), (28, head_y - 4), (26, head_y + 12)], fill=C["hair_light"])
        draw.polygon([(26, head_y - 2), (38, head_y + 2), (32, head_y + 16)], fill=C["hair_light"])

        # 7. BRAÇOS E MÃOS (Segurando o Machado)
        arm_x = cfg["arm_angle"]
        draw.line([28, 42 + off_y, 38 + arm_x, 50 + off_y], fill=C["skin_mid"], width=4)
        draw.rectangle([36 + arm_x, 48 + off_y, 42 + arm_x, 54 + off_y], fill=C["outline"]) # Luva preta

        sprites.append(img)

    # ---------------------------------------------------------
    # EXPORTAÇÃO EM SPRITESHEET E GIF ANIMADO
    # ---------------------------------------------------------
    os.makedirs("exports", exist_ok=True)
    escala = 5  # Mantém a nitidez perfeita dos pixels em alta definição

    # 1. Salva a Spritesheet (PNG com transparência)
    spritesheet = Image.new("RGBA", (w * len(sprites), h), C["transp"])
    for idx, s in enumerate(sprites):
        spritesheet.paste(s, (idx * w, 0))
    
    spritesheet_hd = spritesheet.resize((spritesheet.width * escala, spritesheet.height * escala), Image.NEAREST)
    spritesheet_hd.save(f"exports/{nome_saida}_spritesheet.png")

    # 2. Salva o GIF Animado da Caminhada Infinita
    frames_hd = [s.resize((w * escala, h * escala), Image.NEAREST) for s in sprites]
    frames_hd[0].save(
        f"exports/{nome_saida}.gif",
        save_all=True,
        append_images=frames_hd[1:],
        duration=130, # Tempo exato por frame para uma caminhada fluida
        loop=0
    )

    print(f"✨ Sucesso! Spritesheet e GIF gerados em 'exports/{nome_saida}.gif'")

if __name__ == "__main__":
    gerar_walkcycle_guerreira()