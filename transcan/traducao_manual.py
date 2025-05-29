import os
import json


# === INPUT DINÂMICO ===
scan = input("📁 Digite o nome do scan: ").strip()
obra = input("📚 Digite o nome da obra: ").strip()
numero = input("📖 Digite o número do capítulo: ").strip()

# === BASE DIR ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(BASE_DIR)

# === PASTAS ===
ocr_folder = os.path.join(BASE_DIR, 'ocr', scan, obra, numero)
trad_folder = os.path.join(BASE_DIR, 'traducao', scan, obra, numero)
json_file = os.path.join(ocr_folder, 'ocr_completo.json')

os.makedirs(trad_folder, exist_ok=True)

# === VERIFICA SE O JSON EXISTE ===
if not os.path.exists(json_file):
    print("❌ Arquivo 'ocr_completo.json' não encontrado.")
    exit()

# === CARREGAR JSON DO OCR ===
with open(json_file, 'r', encoding='utf-8') as f:
    ocr_data = json.load(f)

# === GERAR OS ARQUIVOS PARA TRADUZIR ===
print("\n🔄 Gerando arquivos para tradução manual...")

for pagina, conteudos in ocr_data.items():
    pagina_folder = os.path.join(trad_folder, pagina)
    os.makedirs(pagina_folder, exist_ok=True)

    for item in conteudos:
        nome = item['crop'].replace('.png', '.txt')
        texto_original = item['texto']

        path_txt = os.path.join(pagina_folder, nome)

        # Se já existe, não sobrescreve
        if not os.path.exists(path_txt):
            with open(path_txt, 'w', encoding='utf-8') as f:
                f.write(texto_original)

            print(f"✅ Arquivo gerado: {pagina}/{nome}")
        else:
            print(f"⚠️ Arquivo já existe (não sobrescrito): {pagina}/{nome}")

print("\n🚀 Arquivos gerados! Agora traduza manualmente na pasta:")
print(f"➡️ {trad_folder}")

# === OPCIONAL ===
opcao = input("\n🎯 Deseja gerar o JSON com as traduções agora? (s/n): ").strip().lower()

if opcao == 's':
    print("\n🔍 Gerando JSON com traduções...")

    traducao_final = {}

    for pagina in os.listdir(trad_folder):
        pagina_folder = os.path.join(trad_folder, pagina)

        if not os.path.isdir(pagina_folder):
            continue

        arquivos_txt = [f for f in os.listdir(pagina_folder) if f.endswith('.txt')]

        traducao_final[pagina] = []

        for arquivo in arquivos_txt:
            path_txt = os.path.join(pagina_folder, arquivo)

            with open(path_txt, 'r', encoding='utf-8') as f:
                texto_traduzido = f.read().strip()

            traducao_final[pagina].append({
                "crop": arquivo.replace('.txt', '.png'),
                "texto": texto_traduzido
            })

            print(f"✅ Tradução lida: {pagina}/{arquivo}")

    # === SALVAR JSON FINAL ===
    json_output = os.path.join(trad_folder, 'traducao_completa.json')
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump(traducao_final, f, indent=4, ensure_ascii=False)

    print("\n🚀 Tradução salva em JSON:")
    print(f"➡️ {json_output}")

else:
    print("\n🚫 JSON não gerado. Você pode rodar esse script depois para gerar.")
