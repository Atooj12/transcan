from PIL import Image
import os
from app.utils import build_path

def dividir_imagem(scan, obra, cap, nome_img):
    caminho = build_path('input', scan, obra, cap, nome_img)

    imagem = Image.open(caminho)
    largura, altura = imagem.size

    if altura <= 1800:
        return [caminho]

    # Dividir em duas partes
    metade = altura // 2
    nome_base = os.path.splitext(nome_img)[0]
    pasta = os.path.dirname(caminho)

    parte1 = imagem.crop((0, 0, largura, metade))
    parte2 = imagem.crop((0, metade, largura, altura))

    caminho1 = os.path.join(pasta, f"{nome_base}_parte1.png")
    caminho2 = os.path.join(pasta, f"{nome_base}_parte2.png")

    parte1.save(caminho1)
    parte2.save(caminho2)

    os.remove(caminho)
    print(f"✂️ Imagem dividida automaticamente em: {caminho1} e {caminho2}")

    return [caminho1, caminho2]
