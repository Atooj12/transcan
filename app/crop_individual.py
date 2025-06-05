import json
import os

import cv2
from app.utils import build_path


def crop_individual(scan, obra, numero, pagina):
    print(f"🔪 Crop individual na página: {pagina}")

    input_folder = build_path('input', scan, obra, numero)
    output_folder = build_path('crops', scan, obra, numero)
    json_folder = os.path.join(output_folder, 'posicoes.json')

    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    caminho_img = os.path.join(input_folder, pagina)
    if not os.path.exists(caminho_img):
        print(f"❌ Imagem {pagina} não encontrada.")
        return

    imagem_original = cv2.imread(caminho_img)
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
            nome_crop = f"{pagina.split('.')[0]}_crop_{len(crops_atuais) + 1}.png"
            caminho_crop = os.path.join(output_folder, nome_crop)
            cv2.imwrite(caminho_crop, roi)

            imagem_processada[y:y + h, x:x + w] = (255, 255, 255)
            imagem_interface = cv2.resize(imagem_processada, (window_width, window_height))
            clone = imagem_interface.copy()

            crops_atuais.append({
                "scan": scan,
                "obra": obra,
                "numero": numero,
                "pagina": pagina,
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

        elif key == ord("q") or key == ord("c"):
            break

    cv2.destroyAllWindows()

    # Atualiza o JSON
    if os.path.exists(json_folder):
        with open(json_folder, 'r') as f:
            dados_existentes = json.load(f)
    else:
        dados_existentes = []

    dados_existentes.extend(crops_atuais)

    with open(json_folder, 'w') as f:
        json.dump(dados_existentes, f, indent=4)

    print(f"✅ JSON atualizado: {json_folder}")
