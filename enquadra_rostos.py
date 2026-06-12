import os
import cv2
import numpy as np
from pdf2image import convert_from_path

def recortar_e_enquadrar_rostos():
    # Define o tamanho final
    tamanho = (320, 320)
    
    # PEGA O CAMINHO EXATO ONDE O SCRIPT ESTÁ SENDO EXECUTADO
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    pasta_saida = os.path.join(pasta_atual, "rostos_recortados")

    print(f"Diretório atual: {pasta_atual}")
    print(f"Tentando criar a pasta de saída em: {pasta_saida}")

    # Força a criação da pasta se ela não existir
    if not os.path.exists(pasta_saida):
        try:
            os.makedirs(pasta_saida, exist_ok=True)
            print("Pasta 'rostos_recortados' criada com sucesso!")
        except Exception as e:
            print(f"Erro crítico ao criar a pasta: {e}")
            return

    # Carrega o classificador de rostos do OpenCV
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)

    # Extensões de imagem comuns que o OpenCV processa direto
    formatos_imagem = ('.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp', '.webp')
    
    # Lista todos os arquivos da pasta que sejam imagens ou PDFs
    arquivos = [f for f in os.listdir(pasta_atual) if f.lower().endswith(formatos_imagem) or f.lower().endswith('.pdf')]

    if not arquivos:
        print("\n[AVISO] Nenhum arquivo de imagem ou PDF válido foi encontrado nesta pasta!")
        return

    print(f"\nEncontrados {len(arquivos)} arquivos para processar...")

    for nome_arquivo in arquivos:
        caminho_arquivo = os.path.join(pasta_atual, nome_arquivo)
        imagens_para_processar = []

        # Tratamento especial se o arquivo for PDF
        if nome_arquivo.lower().endswith('.pdf'):
            try:
                print(f"Convertendo páginas do PDF: {nome_arquivo}...")
                paginas = convert_from_path(caminho_arquivo)
                for idx, pagina in enumerate(paginas):
                    # Converte a página do formato PIL para o formato que o OpenCV entende (BGR)
                    imagem_np = cv2.cvtColor(np.array(pagina), cv2.COLOR_RGB2BGR)
                    # Define um nome virtual para salvar a página depois
                    nome_virtual = f"{os.path.splitext(nome_arquivo)[0]}_pag_{idx+1}.png"
                    imagens_para_processar.append((imagem_np, nome_virtual))
            except Exception as e:
                print(f"Erro ao processar o PDF {nome_arquivo}: {e}")
                continue
        else:
            # Se for imagem normal, lê direto com o OpenCV
            imagem = cv2.imread(caminho_arquivo)
            if imagem is None:
                print(f"Erro ao carregar a imagem: {nome_arquivo}")
                continue
            imagens_para_processar.append((imagem, nome_arquivo))

        # Processa cada imagem carregada (ou cada página do PDF)
        for imagem_atual, nome_salvamento in imagens_para_processar:
            cinza = cv2.cvtColor(imagem_atual, cv2.COLOR_BGR2GRAY)
            rostos = face_cascade.detectMultiScale(cinza, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            if len(rostos) == 0:
                print(f"Nenhum rosto detectado em: {nome_salvamento}")
                continue

            alt_img, larg_img, _ = imagem_atual.shape

            for i, (x, y, w, h) in enumerate(rostos):
                centro_x = x + (w // 2)
                centro_y = y + (h // 2)

                tamanho_corte = int(max(w, h) * 1.8)

                x_ini = max(0, centro_x - (tamanho_corte // 2))
                y_ini = max(0, centro_y - (tamanho_corte // 2))
                x_fim = min(larg_img, x_ini + tamanho_corte)
                y_fim = min(alt_img, y_ini + tamanho_corte)

                rosto_recortado = imagem_atual[y_ini:y_fim, x_ini:x_fim]
                rosto_redimensionado = cv2.resize(rosto_recortado, tamanho, interpolation=cv2.INTER_AREA)

                # Mantém o mesmo nome do arquivo original (ou o nome_pag_X.png para PDFs)
                # Se houver mais de um rosto na mesma imagem, o último irá sobrescrever para manter o nome idêntico.
                nome_saida = nome_salvamento
                
                # Se o arquivo original era PDF, salvamos o recorte como .png por padrão
                if nome_saida.lower().endswith('.pdf'):
                    nome_saida = os.path.splitext(nome_saida)[0] + ".png"

                caminho_saida = os.path.join(pasta_saida, nome_saida)
                
                # Salva o arquivo
                cv2.imwrite(caminho_saida, rosto_redimensionado)
                print(f"Sucesso: {nome_saida} salvo na pasta de saída.")

if __name__ == "__main__":
    recortar_e_enquadrar_rostos()