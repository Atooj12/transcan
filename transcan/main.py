# app/main.py
from app import crop_interface, ocr, traducao, reinsercao

def main():
    print("🔧 Etapa 1: Crop manual")
    crop_interface.run()

    print("🔍 Etapa 2: OCR")
    ocr.run()

    print("🌐 Etapa 3: Tradução")
    traducao.run()

    print("🎨 Etapa 4: Reinserção")
    reinsercao.run()

if __name__ == "__main__":
    main()
