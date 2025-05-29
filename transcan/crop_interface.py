import cv2
import os
import json
import re


# === Função para ordenar corretamente ===
def ordenar_paginas(lista):
    def extrair_numero(nome):
        numeros = re.findall(r'\d+', nome)
        return int(numeros[0]) if numeros else 0

    return sorted(lista, key=extrair_numero)


# === Diretório base absoluto ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(BASE_DIR)


# === INPUT DINÂMICO ===
scan = input("📁 Digite o nome do scan: ").strip()
obra = input("📚 Digite o nome da obra: ").strip()
numero = input("🔢 Digite o número do capítulo: ").strip()


# === Diretórios organizados ===
input_folder = os.path.join(BASE_DIR, 'input', scan, obra, numero)
output_folder = os.path.join(BASE_DIR, 'crops', scan, obra, numero)
json_folder = os.path.join(output_folder, 'posicoes.json')

base_dirs = {
    "input": input_folder,
    "crops": output_folder,
    "json": json_folder
}


# === Cria pastas se não existirem ===
for chave, path in base_dirs.items():
    if chave != 'json':
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"📂 Pasta criada: {path}")


# === LISTAR IMAGENS DISPONÍVEIS ===
imagens_disponiveis = [f for f in os.listdir(base_dirs["input"]) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

if not imagens_disponiveis:
    print("❌ Nenhuma imagem encontrada na pasta.")
    exit()

imagens_disponiveis = ordenar_paginas(imagens_disponiveis)


# === LISTA DE CORTES ===
posicoes = []


# === LOOP INFINITO ===
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
        print("❌ Entrada inválida. Tente novamente.")
        continue

    print(f"✅ Imagem selecionada: {arquivo_imagem}")

    # === CARREGAR IMAGEM ORIGINAL ===
    imagem_original = cv2.imread(os.path.join(base_dirs["input"], arquivo_imagem))
    imagem_processada = imagem_original.copy()

    # === REDIMENSIONAR PARA INTERFACE ===
    screen_res = (1600, 900)
    scale_width = screen_res[0] / imagem_original.shape[1]
    scale_height = screen_res[1] / imagem_original.shape[0]
    scale = min(scale_width, scale_height)

    window_width = int(imagem_original.shape[1] * scale)
    window_height = int(imagem_original.shape[0] * scale)

    imagem_interface = cv2.resize(imagem_processada, (window_width, window_height))


    # === VARIÁVEIS DE CONTROLE ===
    cropping = False
    x_start, y_start, x_end, y_end = 0, 0, 0, 0
    crops_atuais = []


    # === FUNÇÃO DO MOUSE ===
    def mouse_crop(event, x, y, flags, param):
        global x_start, y_start, x_end, y_end, cropping, imagem_interface, clone

        if event == cv2.EVENT_LBUTTONDOWN:
            x_start, y_start, x_end, y_end = x, y, x, y
            cropping = True

        elif event == cv2.EVENT_MOUSEMOVE and cropping:
            x_end, y_end = x, y

        elif event == cv2.EVENT_LBUTTONUP:
            x_end, y_end = x, y
            cropping = False

            if x_start != x_end and y_start != y_end:
                # === REGRA DE 3 PARA COORDENADAS ORIGINAIS ===
                x = int(min(x_start, x_end) / scale)
                y = int(min(y_start, y_end) / scale)
                w = int(abs(x_start - x_end) / scale)
                h = int(abs(y_start - y_end) / scale)

                # === CROP NA IMAGEM ORIGINAL ===
                roi = imagem_original[y:y + h, x:x + w]

                nome_crop = f"{arquivo_imagem.split('.')[0]}_crop_{len(posicoes) + len(crops_atuais) + 1}.png"
                caminho_crop = os.path.join(base_dirs["crops"], nome_crop)
                cv2.imwrite(caminho_crop, roi)

                # === LIMPAR BALÃO (RETÂNGULO BRANCO) ===
                cv2.rectangle(imagem_processada, (x, y), (x + w, y + h), (255, 255, 255), -1)

                crop_info = {
                    "scan": scan,
                    "obra": obra,
                    "numero": numero,
                    "pagina": arquivo_imagem,
                    "crop": nome_crop,
                    "x": x,
                    "y": y,
                    "w": w,
                    "h": h
                }

                crops_atuais.append(crop_info)

                print(f"✅ Crop salvo: {nome_crop}")

                # === Atualiza interface ===
                imagem_interface = cv2.resize(imagem_processada, (window_width, window_height))
                clone = imagem_interface.copy()


    # === INTERFACE ===
    clone = imagem_interface.copy()
    cv2.namedWindow("Cropper")
    cv2.setMouseCallback("Cropper", mouse_crop)

    while True:
        i = clone.copy()

        if cropping:
            cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)

        cv2.imshow("Cropper", i)
        key = cv2.waitKey(1) & 0xFF

        # === RESET TODOS ===
        if key == ord("r"):
            print("🔄 Resetando todos os crops dessa imagem...")
            crops_atuais = []
            imagem_processada = imagem_original.copy()
            imagem_interface = cv2.resize(imagem_processada, (window_width, window_height))
            clone = imagem_interface.copy()

        # === DELETE ÚLTIMO ===
        elif key == ord("d"):
            if crops_atuais:
                ultimo = crops_atuais.pop()
                print(f"❌ Último crop removido: {ultimo['crop']}")

                # Reseta imagem processada e redesenha os crops restantes
                imagem_processada = imagem_original.copy()

                for c in crops_atuais:
                    cv2.rectangle(imagem_processada, (c['x'], c['y']), (c['x'] + c['w'], c['y'] + c['h']), (255, 255, 255), -1)

                imagem_interface = cv2.resize(imagem_processada, (window_width, window_height))
                clone = imagem_interface.copy()
            else:
                print("⚠️ Nenhum crop para deletar.")

        # === CONFIRMAR ===
        elif key == ord("c"):
            print("📝 Finalizando crop dessa imagem...")
            posicoes.extend(crops_atuais)
            break

        # === QUIT GERAL ===
        elif key == ord("q"):
            print("🚪 Saindo da interface.")
            exit()

    cv2.destroyAllWindows()


# === SALVAR JSON ===
if os.path.exists(base_dirs["json"]):
    with open(base_dirs["json"], 'r') as f:
        dados_existentes = json.load(f)
else:
    dados_existentes = []

dados_existentes.extend(posicoes)

with open(base_dirs["json"], 'w') as f:
    json.dump(dados_existentes, f, indent=4)

print(f"✅ JSON salvo: {base_dirs['json']}")
