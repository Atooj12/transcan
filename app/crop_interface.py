from PIL import Image
import cv2
import os
import json
import re
from app.utils import build_path, BASE_DIR

def executar_crop(scan, obra, numero):
    print("🔪 Iniciando Crop Interface...")

    # === Diretórios organizados (corrigido para pasta 'data/') ===
    input_folder = build_path('input', scan, obra, numero)
    output_folder = build_path('crops', scan, obra, numero)
    json_folder = os.path.join(output_folder, 'posicoes.json')

    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    def dividir_se_preciso(caminho_imagem):
        imagem = Image.open(caminho_imagem)
        largura, altura = imagem.size
        if altura > 1800:  # Limite definido para dividir (ajustável)
            metade = altura // 2
            nome = os.path.splitext(os.path.basename(caminho_imagem))[0]
            pasta = os.path.dirname(caminho_imagem)

            parte1 = imagem.crop((0, 0, largura, metade))
            parte2 = imagem.crop((0, metade, largura, altura))

            caminho1 = os.path.join(pasta, f"{nome}_parte1.png")
            caminho2 = os.path.join(pasta, f"{nome}_parte2.png")

            parte1.save(caminho1)
            parte2.save(caminho2)

            os.remove(caminho_imagem)
            print(f"🔪 Imagem dividida automaticamente: {nome}")
            return [os.path.basename(caminho1), os.path.basename(caminho2)]
        return [os.path.basename(caminho_imagem)]

    # --- Lista e divide automaticamente ---
    imagens_raw = [f for f in os.listdir(input_folder) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    if not imagens_raw:
        print("❌ Nenhuma imagem encontrada na pasta.")
        return

    imagens_disponiveis = []
    for img in imagens_raw:
        caminho = os.path.join(input_folder, img)
        imagens_disponiveis.extend(dividir_se_preciso(caminho))

    def ordenar_paginas(lista):
        def extrair_numero(nome):
            numeros = re.findall(r'\d+', nome)
            return int(numeros[0]) if numeros else 0
        return sorted(lista, key=extrair_numero)

    imagens_disponiveis = ordenar_paginas(imagens_disponiveis)
    posicoes = []

    while True:
        print("\n📂 Imagens disponíveis:")
        for idx, img in enumerate(imagens_disponiveis):
            print(f"[{idx}] {img}")

        escolha = input("\n🔍 Digite o número da imagem que você quer abrir (ou 'q' pra sair): ")
        if escolha.lower() == 'q':
            print("🚪 Saindo do Crop Interface.")
            break

        try:
            indice = int(escolha)
            arquivo_imagem = imagens_disponiveis[indice]
        except:
            print("❌ Entrada inválida.")
            continue

        imagem_original = cv2.imread(os.path.join(input_folder, arquivo_imagem))
        imagem_processada = imagem_original.copy()

        screen_res = (1600, 900)
        scale_width = screen_res[0] / imagem_original.shape[1]
        scale_height = screen_res[1] / imagem_original.shape[0]
        scale = min(scale_width, scale_height)
        window_width = int(imagem_original.shape[1] * scale)
        window_height = int(imagem_original.shape[0] * scale)

        imagem_interface = cv2.resize(imagem_processada, (window_width, window_height))
        cropping = False
        x_start = y_start = x_end = y_end = 0
        crops_atuais = []

        def mouse_crop(event, x, y, flags, param):
            nonlocal x_start, y_start, x_end, y_end, cropping, imagem_interface, clone

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

                # Cor base
                cor_pixel = imagem_original[y, x].tolist()
                tolerancia = 30
                min_cor = [max(c - tolerancia, 0) for c in cor_pixel]
                max_cor = [min(c + tolerancia, 255) for c in cor_pixel]

                # Limpeza por cor
                mascara = cv2.inRange(imagem_original, tuple(min_cor), tuple(max_cor))
                imagem_processada[mascara > 0] = (255, 255, 255)

                # Salvar crop
                roi = imagem_original[y:y + h, x:x + w]
                nome_crop = f"{arquivo_imagem.split('.')[0]}_crop_{len(posicoes) + len(crops_atuais) + 1}.png"
                caminho_crop = os.path.join(output_folder, nome_crop)
                cv2.imwrite(caminho_crop, roi)

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
                imagem_interface = cv2.resize(imagem_processada, (window_width, window_height))
                clone = imagem_interface.copy()


        clone = imagem_interface.copy()
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
                    print(f"❌ Removido: {ultimo['crop']}")
                    imagem_processada = imagem_original.copy()
                    for c in crops_atuais:
                        cv2.rectangle(imagem_processada, (c['x'], c['y']), (c['x'] + c['w'], c['y'] + c['h']), (255, 255, 255), -1)
                    imagem_interface = cv2.resize(imagem_processada, (window_width, window_height))
                    clone = imagem_interface.copy()
            elif key == ord("c"):
                posicoes.extend(crops_atuais)
                break
            elif key == ord("q"):
                print("🚪 Saindo da interface.")
                cv2.destroyAllWindows()
                return

        cv2.destroyAllWindows()

    # === SALVAR JSON ===
    if os.path.exists(json_folder):
        with open(json_folder, 'r') as f:
            dados_existentes = json.load(f)
    else:
        dados_existentes = []

    dados_existentes.extend(posicoes)

    with open(json_folder, 'w') as f:
        json.dump(dados_existentes, f, indent=4)

    print(f"✅ JSON salvo: {json_folder}")
