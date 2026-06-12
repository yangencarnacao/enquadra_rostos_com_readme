# Recortador e Enquadrador de Rostos Automático

Este script em Python automatiza o processo de detecção, recorte e redimensionamento de rostos presentes em imagens e arquivos PDF. Ele varre a pasta onde está localizado, processa os arquivos compatíveis e salva os rostos encontrados em uma pasta separada, centralizados e padronizados no tamanho de **320x320 pixels**.

## 🚀 Funcionalidades

* **Detecção Automática:** Identifica rostos utilizando o classificador Haar Cascade do OpenCV.
* **Suporte a PDFs:** Converte e processa páginas de arquivos PDF em busca de rostos.
* **Enquadramento Inteligente:** Calcula uma margem de segurança ao redor do rosto para que o corte não fique muito justo.
* **Padronização:** Redimensiona automaticamente todas as saídas para **320x320 pixels** (ideal para fotos de perfil, crachás ou datasets).
* **Organização:** Cria automaticamente a pasta `rostos_recortados` para salvar os resultados sem bagunçar seus arquivos originais.

---

## 📦 Pré-requisitos

Antes de executar o script, você precisará instalar o Python (versão 3.7 ou superior) e algumas bibliotecas de terceiros.

### 1. Dependências do Python

Instale os pacotes necessários via terminal utilizando o `pip`:

```bash
pip install opencv-python numpy pdf2image

```

### 2. Dependência do Sistema (Para suporte a PDF)

A biblioteca `pdf2image` exige uma ferramenta do sistema chamada **poppler** para converter as páginas do PDF em imagens.

* **Windows:** 1. Baixe o Poppler para Windows (ex: via @oschwartz10612 no GitHub).
2. Extraia os arquivos e adicione a pasta `bin` às Variáveis de Ambiente do seu sistema (PATH).
* **Linux (Ubuntu/Debian):**
```bash
sudo apt-get install poppler-utils

```


* **macOS (via Homebrew):**
```bash
brew install poppler

```



---

## 🛠️ Como Usar

1. Coloque o script (ex: `enquadrar_rostos.py`) dentro da pasta onde estão as fotos ou PDFs que você deseja processar.
2. Abra o terminal/prompt de comando nessa mesma pasta.
3. Execute o script:

```bash
python enquadrar_rostos.py

```

### O que acontece em seguida?

* O script criará uma pasta chamada `rostos_recortados/` no mesmo local.
* Ele processará todas as imagens (`.jpg`, `.png`, `.webp`, etc.) e arquivos `.pdf`.
* As imagens finais serão salvas com o mesmo nome do arquivo original (para PDFs, será gerado um arquivo por página contendo rosto, ex: `documento_pag_1.png`).

---

## ⚙️ Detalhes Técnicos do Script

> **Nota sobre sobreposição:** Se uma mesma imagem ou página de PDF contiver mais de um rosto, o script atualmente salvará o último rosto encontrado sobrescrevendo o arquivo, mantendo o nome idêntico ao original. Caso precise de múltiplos rostos da mesma imagem, recomenda-se adicionar um contador `_i` ao nome do arquivo de saída.

* **Tamanho padrão de saída:** $320 \times 320$ pixels.
* **Margem de corte:** O script calcula $1.8\times$ o tamanho detectado do rosto para garantir que o cabelo e o queixo não sejam cortados bruscamente.
* **Algoritmo de Detecção:** `haarcascade_frontalface_default.xml` (OpenCV).
