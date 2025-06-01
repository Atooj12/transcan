import os
import json
from PIL import Image, ImageDraw, ImageFont
from app.utils import build_path

def executar_reinsercao(scan, obra, numero):
    print("🎨 Executando reinserção final...")

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    input_folder     = build_path('input', scan, obra, numero)
    traducao_folder  = build_path('ocr', scan, obra, numero)
    crop_folder      = build_path('crops', scan, obra, numero)
    output_folder    = build_path('output', scan, obra, numero)

    json_traducao    = os.path.join(traducao_folder, 'traducao_completa.json')
    json_posicoes    = os.path.join(crop_folder, 'posicoes.json')

    os.makedirs(output_folder, exist_ok=True)

    main_font_path = os.path.join(BASE_DIR, 'assets', 'inter.ttf')
    if not os.path.exists(main_font_path):
        print("⚠️ Fonte principal não encontrada, usando padrão.")
        main_font_path = None

    watermark_font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    watermark_font = ImageFont.truetype(watermark_font_path, 14)

    with open(json_traducao, 'r', encoding='utf-8') as f:
        traducao = json.load(f)

    with open(json_posicoes, 'r', encoding='utf-8') as f:
        posicoes = json.load(f)

    posicoes_por_pagina = {}
    for item in posicoes:
        pagina_limpa = os.path.splitext(item['pagina'])[0]
        if pagina_limpa not in posicoes_por_pagina:
            posicoes_por_pagina[pagina_limpa] = []
        posicoes_por_pagina[pagina_limpa].append(item)

    def desenhar_texto(draw, box, texto, fonte_path):
        x, y, w, h = box
        font_size = 14
        font = ImageFont.truetype(fonte_path, font_size) if fonte_path else ImageFont.load_default()

        while True:
            font = ImageFont.truetype(fonte_path, font_size) if fonte_path else ImageFont.load_default()
            linhas = texto.split('\n')
            largura_maxima = max([draw.textbbox((0, 0), linha, font=font)[2] for linha in linhas]) if linhas else 0
            altura_total = len(linhas) * (font.getbbox('A')[3] - font.getbbox('A')[1] + 5)
            if largura_maxima < w - 10 and altura_total < h - 10:
                font_size += 1
            else:
                font_size -= 1
                break

        altura_texto = len(linhas) * (font.getbbox('A')[3] - font.getbbox('A')[1] + 5)
        y_texto = y + (h - altura_texto) // 2

        for linha in linhas:
            largura_linha = draw.textbbox((0, 0), linha, font=font)[2]
            x_texto = x + (w - largura_linha) // 2
            draw.text((x_texto, y_texto), linha, fill="black", font=font)
            y_texto += font.getbbox('A')[3] - font.getbbox('A')[1] + 5

    for pagina, conteudos in traducao.items():
        input_path = None
        for ext in ['.jpg', '.jpeg', '.png']:
            tentativa = os.path.join(input_folder, pagina + ext)
            if os.path.exists(tentativa):
                input_path = tentativa
                break

        if input_path is None:
            print(f"❌ Página não encontrada: {pagina}")
            continue

        img = Image.open(input_path).convert("RGB")
        draw = ImageDraw.Draw(img)

        for item in conteudos:
            crop_name = item['crop']
            texto = item['texto'].strip()
            pos_crop = next((p for p in posicoes_por_pagina.get(pagina, []) if p['crop'] == crop_name), None)

            if pos_crop:
                x, y, w, h = pos_crop['x'], pos_crop['y'], pos_crop['w'], pos_crop['h']
                draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
                desenhar_texto(draw, (x, y, w, h), texto, main_font_path)

        watermark = "TranScan"
        margin = 10
        x_wm = img.width - draw.textbbox((0, 0), watermark, font=watermark_font)[2] - margin
        y_wm = img.height - draw.textbbox((0, 0), watermark, font=watermark_font)[3] - margin

        draw.text((x_wm + 1, y_wm + 1), watermark, font=watermark_font, fill="white")  # sombra leve
        draw.text((x_wm, y_wm), watermark, font=watermark_font, fill="black")          # texto principal

        nome_output = pagina + '_final.png'
        output_path = os.path.join(output_folder, nome_output)
        img.save(output_path)
        print(f"✅ Página salva: {output_path}")

    print("\n🚀 Reinserção finalizada com sucesso!")
