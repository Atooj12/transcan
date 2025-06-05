# 🧾 Changelog — Transcan

Todas as mudanças notáveis neste projeto serão documentadas aqui.

---

## [v0.1.0] — 2025-06-05
🔖 **MVP Estável – Versão Inicial Pública**

### ✨ Features
- `crop_interface.py`: Interface de crop manual funcional, com tecla D (deletar crop) corrigida.
- `ocr.py`: Módulo de OCR usando EasyOCR (sem alterações nesta versão).
- `main.py`: Refatorado com menu interativo e funções separadas para cada etapa.
- `crop_individual.py`: Novo módulo que permite cropar uma única página específica.
- `divisor.py`: Novo módulo que divide páginas verticais automaticamente.

### 🧼 Refatorações
- Modularização de `main.py` com separação de funcionalidades.
- Padronização da estrutura de diretórios do projeto (`app/`, `data/`, etc).

### 🐛 Correções
- Corrigido bug no `crop_interface` onde o crop deletado não apagava da imagem original.
- Corrigido redimensionamento de interface com tela adaptativa.

---

## 🔜 Próxima versão (v0.2.0) – Em desenvolvimento
- Separação de reinserção em dois módulos: `limpeza` e `inserção`.
- Suporte a painéis coloridos no crop e reinserção.
- Melhorias visuais no typer (fonte, cor, adaptação).

---

**Autor:** João Pedro — [@atooj12](https://github.com/atooj12)
