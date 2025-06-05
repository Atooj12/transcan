from app.crop_interface import executar_crop
from app.crop_individual import crop_individual
from app.divisor import dividir_imagem
from app.ocr import executar_ocr
from app.reinsercao import executar_reinsercao


def separador():
    print("\n" + "━" * 50 + "\n")

def main():
    print("📌 Bem-vindo ao Transcan")

    print("\nEscolha uma opção:")
    print("1 - Processar uma página específica")
    print("2 - Processar capítulo completo (crop, OCR, reinserção)")
    print("3 - Apenas Crop")
    print("4 - Apenas OCR")
    print("5 - Apenas Reinserção")
    print("q - Sair")

    opcao = input("\nDigite a opção desejada: ").strip()

    if opcao == "q":
        print("🚪 Encerrando...")
        return

    scan = input("📁 Nome do scan: ").strip()
    obra = input("📚 Nome da obra: ").strip()
    cap = input("📖 Número do capítulo: ").strip()

    if opcao == "1":
        nome_img = input("🖼️ Nome EXATO da imagem a ser croppada (com extensão): ").strip()
        dividir = input("✂️ Deseja dividir a imagem antes do crop? (s/n): ").strip().lower()
        if dividir == 's':
            dividir_imagem(scan, obra, cap, nome_img)
        separador()
        print("🔪 Crop de Página Específica")
        crop_individual(scan, obra, cap, nome_img)

    elif opcao == "2":
        dividir = input("✂️ Deseja dividir as imagens antes do crop? (s/n): ").strip().lower()
        separador()
        print("🔪 Etapa 1: Crop Manual")
        executar_crop(scan, obra, cap, dividir == 's')

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

    elif opcao == "3":
        dividir = input("✂️ Deseja dividir as imagens antes do crop? (s/n): ").strip().lower()
        separador()
        print("🔪 Etapa: Crop Manual")
        executar_crop(scan, obra, cap, dividir == 's')

    elif opcao == "4":
        separador()
        print("🧠 Etapa: OCR")
        executar_ocr(scan, obra, cap)

    elif opcao == "5":
        separador()
        print("🎨 Etapa: Reinserção do Texto")
        executar_reinsercao(scan, obra, cap)

    else:
        print("⚠️ Opção inválida.")

if __name__ == "__main__":
    main()
