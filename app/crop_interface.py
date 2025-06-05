from PIL import Image
import cv2
import os
import json
import re
from app.utils import build_path, BASE_DIR
from app.divisor import dividir_imagem

def executar_crop(scan, obra, numero, dividir=False):
    print("🔪 Iniciando Crop Interface...")

    input_folder = build_path('input', scan, obra, numero)
    output_folder = build_path('crops', scan, obra, numero)
    json_folder = os.path.join(output_folder, 'posicoes.json')

    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    imagens_raw = [f for f in os.listdir(input_folder) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    if not imagens_raw:
        print("❌ Nenhuma imagem encontrada na pasta.")
        return

    imagens_divididas = []
    for img in imagens_raw:
        if dividir:
            partes = dividir_imagem(scan, obra, numero, img)
            if partes:
                imagens_divididas.extend([os.path.basename(p) for p in partes])
        else:
            imagens_divididas.append(img)

    def ordenar_paginas(lista):
        def extrair_numero(nome):
            numeros = re.findall(r'\d+', nome)
            return int(numeros[0]) if numeros else 0
        return sorted(lista, key=extrair_numero)

    imagens_disponiveis = ordenar_paginas(imagens_divididas)
    posicoes = []
    screen_res = (1600, 900)
    indice_atual = 0

    while indice_atual < len(imagens_disponiveis):
        arquivo_imagem = imagens_disponiveis[indice_atual]
        caminho_img = os.path.join(input_folder, arquivo_imagem)

        imagem_original = cv2.imread(caminho_img)
        imagem_processada = imagem_original.copy()

        scale_width = screen_res[0] / imagem_original.shape[1]
        scale_height = screen_res[1] / imagem_original.shape[0]
        scale = min(scale_width, scale_height)
        window_width = int(imagem_original.shape[1] * scale)
        window_height = int(imagem_original.shape[0] * scale)

        imagem_interface = cv2.resize(imagem_processada, (window_width, window_height))
        cropping = False
        x_start = y_start = x_end = y_end = 0
        crops_atuais = []
        clone = imagem_interface.copy()

        def mouse_crop(event, x, y, flags, param):
            nonlocal x_start, y_start, x_end, y_end, cropping, imagem_interface, clone, imagem_processada

            if event == cv2.EVENT_LBUTTONDOWN:
                x_start, y_start = x, y
                cropping = True

            elif event == cv2.EVENT_MOUSEMOVE and cropping:
                x_end, y_end = x, y

            elif event == cv2.EVENT_LBUTTONUP:
                cropping = False
                x = int(min(x_start, x_end) / scale)
                y = int(min(y_start, y_end) / scale)
                w = int(abs(x_start - x_end) / scale)
                h = int(abs(y_start - y_end) / scale)

                if w < 5 or h < 5:
                    print("⚠️ Crop muito pequeno.")
                    return

                roi = imagem_original[y:y + h, x:x + w]
                nome_crop = f"{arquivo_imagem.split('.')[0]}_crop_{len(posicoes) + len(crops_atuais) + 1}.png"
                caminho_crop = os.path.join(output_folder, nome_crop)
                cv2.imwrite(caminho_crop, roi)

                imagem_processada[y:y + h, x:x + w] = (255, 255, 255)
                imagem_interface = cv2.resize(imagem_processada, (window_width, window_height))
                clone = imagem_interface.copy()

                crops_atuais.append({
                    "scan": scan,
                    "obra": obra,
                    "numero": numero,
                    "pagina": arquivo_imagem,
                    "crop": nome_crop,
                    "x": x,
                    "y": y,
                    "w": w,
                    "h": h
                })

                print(f"✅ Crop salvo com limpeza: {nome_crop}")

        cv2.namedWindow("Cropper")
        cv2.setMouseCallback("Cropper", mouse_crop)

        while True:
            i = clone.copy()
            if cropping:
                cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
            cv2.imshow("Cropper", i)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("r"):
                crops_atuais = []
                imagem_processada = imagem_original.copy()
                imagem_interface = cv2.resize(imagem_processada, (window_width, window_height))
                clone = imagem_interface.copy()

            elif key == ord("d"):
                if crops_atuais:
                    ultimo = crops_atuais.pop()
                    crop_path = os.path.join(output_folder, ultimo['crop'])
                    if os.path.exists(crop_path):
                        os.remove(crop_path)
                        print(f"❌ Crop deletado: {ultimo['crop']}")
                    imagem_processada = imagem_original.copy()
                    for c in crops_atuais:
                        imagem_processada[c['y']:c['y'] + c['h'], c['x']:c['x'] + c['w']] = (255, 255, 255)
                    imagem_interface = cv2.resize(imagem_processada, (window_width, window_height))
                    clone = imagem_interface.copy()

            elif key == ord("b"):
                if indice_atual > 0:
                    print("⏪ Voltando para a imagem anterior...")
                    indice_atual -= 1
                    break

            elif key == ord("c"):
                posicoes.extend(crops_atuais)
                indice_atual += 1
                break

            elif key == ord("q"):
                print("🚪 Saindo da interface.")
                cv2.destroyAllWindows()
                return

        cv2.destroyAllWindows()

    if os.path.exists(json_folder):
        with open(json_folder, 'r') as f:
            dados_existentes = json.load(f)
    else:
        dados_existentes = []

    dados_existentes.extend(posicoes)

    with open(json_folder, 'w') as f:
        json.dump(dados_existentes, f, indent=4)

    print(f"✅ JSON salvo: {json_folder}")
