from app.crop_interface import executar_crop
from app.ocr import executar_ocr
from app.reinsercao import executar_reinsercao


def separador():
    print("\n" + "━" * 50 + "\n")

def main():
    print("📌 Bem-vindo ao Transcan")

    scan = input("📁 Nome do scan: ").strip()
    obra = input("📚 Nome da obra: ").strip()
    cap = input("📖 Número do capítulo: ").strip()

    separador()
    print("🔪 Etapa 1: Crop Manual")
    executar_crop(scan, obra, cap)

    separador()
    print("🧠 Etapa 2: OCR")
    executar_ocr(scan, obra, cap)

    input("\n📝 Após traduzir os arquivos, pressione ENTER para continuar para a reinserção...")

    separador()
    print("🎨 Etapa 3: Reinserção do Texto")
    executar_reinsercao(scan, obra, cap)

    separador()
    print("✅ Capítulo finalizado com sucesso!")
    print(f"📂 Arquivos finais: data/output/{scan}/{obra}/{cap}/")

if __name__ == "__main__":
    main()
