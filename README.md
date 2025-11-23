# 🚀 Transcan (MVP)

Sistema **automatizado** de tradução de mangás — do **crop** ao **texto reinserido**.

> ⚠️ Repositório público, porém o projeto continua em fase beta e com objetivo de monetização futura.

---

## 🔧 Módulos do Sistema

- 🖼️ **Crop Manual** com interface interativa (OpenCV)
- 🧠 **OCR com EasyOCR** (texto extraído por crop)
- 📝 **Tradução Manual/Automática** (estrutura pronta)
- 🎨 **Type (Reinserção)** com fonte, centralização e marca d’água
- 🧩 **Pipeline Completa** via `main.py`

---

## ⚙️ Tecnologias

- Python 3.12+
- EasyOCR
- Pillow
- OpenCV
- TTF Font (Inter)

---

## 📁 Estrutura do Projeto

transcan-mvp/
├── app/ # Código principal
│ ├── assets/ # Fontes (.ttf)
│ ├── crop_interface.py
│ ├── ocr.py
│ ├── reinsercao.py
│ ├── utils.py
│ └── main.py # Executável CLI principal
├── data/ # Ignorado no Git (.gitignore)
│ ├── input/ # Imagens originais
│ ├── crops/ # Crops gerados
│ ├── ocr/ # OCR + JSON de tradução
│ ├── traducao/ # (não utilizado no MVP atual)
│ └── output/ # Páginas finais com texto reinserido
├── .gitignore
├── requirements.txt
└── README.md

---

## ▶️ Como Rodar

```bash
# 1. Ambiente virtual (recomendado)
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Rodar o sistema
python -m app.main
🧠 Fluxo
Você seleciona o capítulo (scan, obra e número)

Corta os balões com o mouse (Crop)

O sistema faz OCR dos crops

Você traduz os .txt (manualmente ou com IA)

Reinserção automática do texto nas imagens originais

👨‍💻 Autor
João Pedro
Projeto Transcan (Beta)
GitHub / LinkedIn: em construção

❌ Licença
Distribuição e uso proibidos sem autorização explícita do autor.
