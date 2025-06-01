import os
import json
import easyocr

from app.utils import build_path

def executar_ocr(scan, obra, numero):
    print("🔍 Iniciando OCR...")

    # === BASE DIR ===
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.dirname(BASE_DIR)

    # === PASTAS ===
    crops_folder = build_path('crops', scan, obra, numero)
    ocr_folder = build_path('ocr', scan, obra, numero)
    json_file = os.path.join(crops_folder, 'posicoes.json')

    os.makedirs(ocr_folder, exist_ok=True)

    if not os.path.exists(json_file):
        print("❌ Arquivo de posições não encontrado.")
        return

    with open(json_file, 'r', encoding='utf-8') as f:
        posicoes = json.load(f)

    reader = easyocr.Reader(['en'], gpu=False)
    ocr_resultado = {}

    for item in posicoes:
        crop_name = item['crop']
        pagina = item['pagina'].replace('.jpg', '').replace('.png', '').replace('.jpeg', '')
        crop_path = os.path.join(crops_folder, crop_name)

        if not os.path.exists(crop_path):
            print(f"❌ Crop não encontrado: {crop_name}")
            continue

        pagina_folder = os.path.join(ocr_folder, pagina)
        os.makedirs(pagina_folder, exist_ok=True)

        result = reader.readtext(crop_path, detail=0)
        texto = '\n'.join(result).strip()

        output_txt = crop_name.replace('.png', '.txt')
        output_path = os.path.join(pagina_folder, output_txt)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(texto)

        print(f"✅ OCR salvo: {output_txt}")

        if pagina not in ocr_resultado:
            ocr_resultado[pagina] = []

        ocr_resultado[pagina].append({
            "crop": crop_name,
            "texto": texto
        })

    json_ocr = os.path.join(ocr_folder, 'ocr_completo.json')
    json_traducao = os.path.join(ocr_folder, 'traducao_completa.json')

    with open(json_ocr, 'w', encoding='utf-8') as f:
        json.dump(ocr_resultado, f, indent=4, ensure_ascii=False)

    with open(json_traducao, 'w', encoding='utf-8') as f:
        json.dump(ocr_resultado, f, indent=4, ensure_ascii=False)

    print("\n🚀 OCR concluído para todos os crops.")
    print(f"📄 JSONs salvos:\n→ OCR: {json_ocr}\n→ Tradução: {json_traducao}")
