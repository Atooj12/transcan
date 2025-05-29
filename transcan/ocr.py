import os
import json
import easyocr


# === INPUT DINÂMICO ===
scan = input("📁 Digite o nome do scan: ").strip()
obra = input("📚 Digite o nome da obra: ").strip()
numero = input("📖 Digite o número do capítulo: ").strip()

# === BASE DIR ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(BASE_DIR)

# === PASTAS ===
crops_folder = os.path.join(BASE_DIR, 'crops', scan, obra, numero)
ocr_folder = os.path.join(BASE_DIR, 'ocr', scan, obra, numero)
json_file = os.path.join(crops_folder, 'posicoes.json')

os.makedirs(ocr_folder, exist_ok=True)

# === VERIFICA SE O JSON EXISTE ===
if not os.path.exists(json_file):
    print("❌ Arquivo de posições não encontrado.")
    exit()

# === CARREGAR JSON ===
with open(json_file, 'r', encoding='utf-8') as f:
    posicoes = json.load(f)

# === INICIAR EASYOCR ===
print("🔍 Iniciando OCR...")
reader = easyocr.Reader(['en'], gpu=False)

# === JSON FINAL COM TODOS OS TEXTOS ===
ocr_resultado = {}

# === RODAR OCR ===
for item in posicoes:
    crop_name = item['crop']
    pagina = item['pagina'].replace('.jpg', '').replace('.png', '').replace('.jpeg', '')

    crop_path = os.path.join(crops_folder, crop_name)

    if not os.path.exists(crop_path):
        print(f"❌ Crop não encontrado: {crop_name}")
        continue

    # Criar subpasta da página
    pagina_folder = os.path.join(ocr_folder, pagina)
    os.makedirs(pagina_folder, exist_ok=True)

    # OCR
    result = reader.readtext(crop_path, detail=0)
    texto = '\n'.join(result).strip()

    # Salvar em TXT individual
    output_txt = crop_name.replace('.png', '.txt')
    output_path = os.path.join(pagina_folder, output_txt)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(texto)

    print(f"✅ OCR salvo: {output_txt}")

    # Salvar no JSON geral
    if pagina not in ocr_resultado:
        ocr_resultado[pagina] = []

    ocr_resultado[pagina].append({
        "crop": crop_name,
        "texto": texto
    })

# === SALVAR JSON GERAL ===
json_output = os.path.join(ocr_folder, 'ocr_completo.json')
with open(json_output, 'w', encoding='utf-8') as f:
    json.dump(ocr_resultado, f, indent=4, ensure_ascii=False)

print("\n🚀 OCR concluído para todos os crops.")
print(f"📄 JSON geral salvo em: {json_output}")
