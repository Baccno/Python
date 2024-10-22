import os
import mammoth
from bs4 import BeautifulSoup
import base64

# Função para adicionar CSS diretamente no HTML
def adicionar_css(html_content):
    return f'''
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            var url = window.location.href;
            var parts = url.split('/');
            var fileName = parts[parts.length - 1].split('.')[0]; // Remove a extensão do arquivo
            document.title = fileName; // Define o título da página como o nome do arquivo
        }});
    </script>
    <style>
        .menu-lateral {{
            position: fixed;
            left: -300px;
            top: 0;
            height: 100%;
            background-color: rgb(27, 94, 100);
            padding: 10px;
            border-radius: 5px;
            overflow-y: auto;
            width: 250px;
            font-family: Arial, sans-serif;
            transition: left 0.3s ease-in-out;
        }}

        .menu-lateral.menu-aberto {{
            left: 0; /* Move o menu para a esquerda quando está aberto */
        }}

        .menu-lateral ul {{
            list-style-type: none;
            padding: 0;
            margin-bottom: 5px;
        }}

        .menu-lateral li {{
            margin-bottom: 5px;
        }}

        .menu-lateral a {{
            color: #000000;
            text-decoration: none;
        }}

        .menu-lateral .seta {{
            content: '\\2192'; /* Adiciona uma seta à esquerda dos itens do menu */
            margin-right: 5px; /* Adiciona espaço entre a seta e o texto */
        }}

        .conteudo {{
            padding: 20px;
            transition: margin-left 0.3s ease-in-out; /* Adiciona transição de animação */
            border-bottom: 3px solid #000000;
        }}

        .menu-lateral.menu-aberto + .conteudo {{
            margin-left: 10px; /* Alterado para 10 */
            margin-left: 255px; /* Move o conteúdo para a direita quando o menu está aberto */
        }}

        body {{
            font-family: Arial, sans-serif;
            font-size: 12px;
            text-align: justify; /* Justifica todo o texto */
            margin: 0; /* Remove margens padrão do corpo */
        }}

        table {{
            justify-content: center;
            border-collapse: collapse;
            text-align: justify; /* Justifica todo o texto */
            height: 63.75pt;
        }}

        table, th, td {{
            justify-content: center;
            border: 1px solid black;
        }}

        th, td {{
            justify-content: center;
            padding: 8px;
            text-align: left;
        }}

        table td,
        table th {{
            justify-content: center;
            font-size: 12px;
            font-family: Arial, sans-serif;
            margin: 0; /* Remove margens padrão do corpo */
        }}

        img {{
            display: block; /* Evita espaços extras abaixo da imagem */
            margin-right: auto;
            max-width: 100%; /* Ajusta a largura máxima da imagem */
            height: auto; /* Mantém a proporção da imagem */
        }}

        table img {{
            justify-content: center;
            width: 470px;
            height: auto;
        }}

        .menu-btn:hover {{
            background-color: #006666; /* Cor alterada quando o mouse está sobre o botão */
        }}

        .logo-img {{
            float: right;  /* ou use 'margin-right' conforme necessário */
            margin-left: 0; /* Remova a margem à esquerda */
        }}

    </style>{html_content}
    '''


# Função para adicionar divs por página de elemento
def adicionar_divs_por_pagina_de_elemento(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Adicionar divs por elemento
    elementos = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'img'])
    for idx, elemento in enumerate(elementos):
        div_elemento = soup.new_tag('div', id=f'elemento_{idx}')
        elemento.wrap(div_elemento)

    return str(soup)


# Função para adicionar hashtags
def adicionar_hashtags(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    for header in headers:
        hashtag = soup.new_tag('span')
        hashtag.string = '#'
        header.insert(0, hashtag)

    return str(soup)


# Função para remover elementos antes da #
def remover_elementos_antes_da_hashtag(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    elemento_hashtag = soup.find(lambda tag: tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'] and '#' in tag.text)

    if elemento_hashtag:
        elementos_a_remover = list(elemento_hashtag.previous_elements)

        for elemento in elementos_a_remover:
            elemento.extract()

    return str(soup)


# Função para remover hashtags dos títulos
def remover_hashtags_dos_titulos(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

    for header in headers:
        header.string = header.text.replace('#', '')

    return str(soup)


# Função para criar o índice
def criar_indice_com_botoes(html_content, nome_documento):
    soup = BeautifulSoup(html_content, 'html.parser')

    indices = []
    headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    for idx, header in enumerate(headers):
        header['id'] = f'section_{idx}'
        indices.append({'tag': header.name, 'texto': header.text, 'ancora': header['id']})

    titulo_pagina = os.path.splitext(os.path.basename(nome_documento))[0]

    indice_html = f'<h1 style="font-size: 14px; background-color: rgb(27, 94, 100); text-decoration: underline; display: inline-block;">{titulo_pagina}</h1>'

    # Adicionar botões de Pesquisar e Imprimir com script de impressão
    botoes_html = '<div style="margin-top: 5px;">' \
                  '<input type="text" id="pesquisar_texto" placeholder="- STRING_BUTTON_SEARCH -" style=" font-size: 11px; color: #808080; border: 1px solid #000000;">' \
                  '<button onclick="pesquisarTexto();" style=" font-size: 11px; color: #000000; border: 1px solid #000000; background-color: transparent; font-weight: bold;">STRING_BUTTON_GO</button>' \
                  '<button onclick="imprimirConteudo();" style=" font-size: 11px; color: #000000; border: 1px solid #000000; background-color: transparent; font-weight: bold;">STRING_BUTTON_PRINTOUT</button>' \
                  '</div>' \
 \
        # Adicionar script de impressão
    script_imprimir = '''
    <script>
    function imprimirConteudo() {
        var conteudo = document.querySelector('.conteudo');
        var janela = window.open('', '', 'width=800,height=600');
        janela.document.write('<html><head><title>Modo Leitura</title>');
        janela.document.write('<style>body { font-size: 16px; line-height: 1.6; }</style></head><body>'); // Adicionando estilo para leitura
        janela.document.write(conteudo.innerHTML);
        janela.document.write('</body></html>');
        janela.document.close();
        janela.print();
    }
    </script>
    '''

    # Combinar os botões com o script
    botoes_html = script_imprimir + botoes_html

    indice_html += botoes_html

    indice_html += '<ul>'
    submenu_aberto = False
    for ancora in indices:
        tag = int(ancora['tag'][1])
        if tag == 1:
            if submenu_aberto:
                indice_html += '</ul></details></li>'
                submenu_aberto = False
            indice_html += f'<li style="margin-bottom: 5px;"><details><summary style=" font-size: 12px; border-bottom: 1px solid #000000; font-size: 16px;">' \
                           f'<a href="#{ancora["ancora"]}" style="text-decoration: none; font-weight: bold;">{ancora["texto"]}</a></summary>' \
                           f'<ul style="list-style-type: none; padding-left: 10px;">'
        else:
            if not submenu_aberto:
                indice_html += '<ul>'
                submenu_aberto = True

            tag_name = 'h' + str(tag)
            tag_text = f'<{tag_name} style="display: inline; margin-right: 5px;">-</{tag_name}>'
            indice_html += f'<li style="margin-bottom: 2px;">{tag_text} <a href="#{ancora["ancora"]}" style="font-size: 12px; text-decoration: none; display: inline; text-decoration: underline;">{ancora["texto"]}</a></li>'

    if submenu_aberto:
        indice_html += '</ul></details></li>'
    indice_html += '</ul>'

    with open(Imagem_indice, 'rb') as nova_imagem_file:
        nova_imagem_data = base64.b64encode(nova_imagem_file.read()).decode('utf-8')
        nova_imagem_tag = f'<img src="data:image/jpg;base64,\n{nova_imagem_data}" class="nova-imagem" style="bottom: 0; left: 0;">'

    nova_imagem_tag = f'<div class="nova-imagem-container">{nova_imagem_tag}</div>'

    # Adicione um botão de fechar ao índice
    botao_fechar = '<button id="botao-fechar-indice" style="background-color: rgb(27, 94, 100); color: #00000; border: none; padding: 5px 10px; cursor: pointer; position: absolute; right: 10px; top: 10px;">X</button>'
    indice_html = botao_fechar + indice_html + nova_imagem_tag

    # Adicione o JavaScript para lidar com os cliques nos links do índice
    script_click_link = '''
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            var links = document.querySelectorAll('.menu-lateral a');
            links.forEach(function(link) {
                link.addEventListener('click', function(e) {
                    var targetId = this.getAttribute('href').substring(1);
                    var targetElement = document.getElementById(targetId);
                    if (targetElement) {
                        e.preventDefault();
                        window.scrollTo({
                            top: targetElement.offsetTop,
                            behavior: 'smooth'
                        });
                    }
                });
            });
        });
    </script>
    '''

    return str(soup), indice_html + script_click_link


# Função para adicionar titulo na pagina
def adicionar_titulo_aba(html_content, nome_arquivo):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Adicionar o título da página no início do documento
    title_tag = soup.new_tag('title')
    title_tag.string = nome_arquivo

    if soup.title:
        soup.title.replace_with(title_tag)
    else:
        soup.insert(0, title_tag)

    # Adicionar bloco de código JavaScript para pesquisa
    script_tag = soup.new_tag('script')
    script_tag.string = """
        function pesquisarTexto() {
            var texto = document.getElementById('pesquisar_texto').value;
            window.find(texto);
        }
    """
    soup.insert(0, script_tag)

    return str(soup)


# Função para adicionar quebra de linha após cada imagem
def adicionar_quebra_de_linha(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    imagens = soup.find_all('img')
    for imagem in imagens:
        quebra_de_linha = soup.new_tag('br')
        imagem.insert_after(quebra_de_linha)
    return str(soup)


# Função de remover ul
def remover_ul(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    for ul in soup.find_all('ul'):
        ul.unwrap()

    return str(soup)


# Função de adicionar um menu para ser aberto e fechado
def adicionar_botao_menu(html_content):
    return f'<button id="botao-menu" class="menu-btn" style="position: fixed; left: 20px; top: 10px; background-color: #1b5e64; font-weight: bold; color: #00000; border: none; padding: 8px; cursor: pointer; border-radius: 10%; font-size: 11px; font-family: Arial, sans-serif;"> STRING_BUTTON_INDEX_SEARCH_PRINTOUT</button>{html_content}'


def formatar_titulos(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    for i in range(1, 7):
        tag = f'h{i}'
        estilo = 'border-bottom: 1px solid; margin-top: 10px;'

        if i <= 2:
            estilo = 'border-bottom: 1px solid; margin-top: 10px;'
        else:
            estilo = 'border-bottom: 1px solid; margin-top: 8px;'

        headers = soup.find_all(tag)
        for idx, header in enumerate(headers):
            header['style'] = estilo

            # Adicionando verificação para garantir que header.string não seja None
            if header.string:
                header.string.wrap(soup.new_tag('span', style='color: black; font-weight: bold;'))
                header['data-title-index'] = idx

    return str(soup)


def adicionar_meta_charset(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Procurar a tag head no documento
    head_tag = soup.find('head')

    if not head_tag:
        # Se a tag head não existir, crie uma e adicione a tag meta
        head_tag = soup.new_tag('head')
        soup.insert(0, head_tag)

    # Remover qualquer tag meta existente com charset
    for meta_tag in head_tag.find_all('meta', {'charset': True}):
        meta_tag.extract()

    # Criar e adicionar a nova tag meta com o charset
    meta_tag = soup.new_tag('meta')
    meta_tag['charset'] = 'ISO-8859-1'  # Alteração para ISO-8859-1
    head_tag.insert(0, meta_tag)

    return str(soup)

# Diretório de entrada e saída
pasta_entrada = 'ArquivosEntradaDocx'
pasta_saida = 'ArquivosSaidaHtml'

# Caminho do arquivo do logo
logo_path = 'Logo/logo.gif'

# Imagem para o indice
Imagem_indice = 'Logo/Untitled.png'

# Listar todos os arquivos na pasta de entrada
arquivos_docx = [arq for arq in os.listdir(pasta_entrada) if arq.endswith('.docx')]

def substituir_caracteres_especiais(texto):
    substituicoes = {
        '\u2013': '-',
        '\u2014': '--',
        '\u201c': '"',
        '\u201d': '"',
        '\u2018': "'",
        '\u2019': "'",
        '\u2022': '*',
        '\u25a0': '-',
        '\u2590': '-',
        '\u2126': 'Ohm',
        '\u03a9': 'Omega',
        '\u2026': '...',
        'ú': '&uacute;',
        'Ç': '&Ccedil;',  # ç
        'ç': '&ccedil;',  # Ç
        'ã': '&atilde;',
        'Ã': '&Atilde;',  # ã
        'õ': '&otilde;',
        'Õ': '&Otilde;',  # õ
        '\u2192': '->',  # Adicionado para tratar '\u2192'
        '\u2191': '^',  # Adicionado para tratar '\u2191'
        '\u2012': '-',
        # Adicione mais substituições conforme necessário
    }

    texto_corrigido = texto
    for chave, valor in substituicoes.items():
        texto_corrigido = texto_corrigido.replace(chave, valor)

    # Converter o texto para a codificação 'latin-1'
    texto_corrigido = texto_corrigido.encode('latin-1', errors='ignore').decode('latin-1')

    return texto_corrigido

# Itere sobre os arquivos
def Document(caminho_entrada):
    pass



for arq in arquivos_docx:
    caminho_entrada = os.path.join(pasta_entrada, arq)
    doc = Document(caminho_entrada)

    with open(caminho_entrada, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        html = result.value

    # Substituir caracteres especiais
    html = substituir_caracteres_especiais(html)

    nome_arquivo_saida = os.path.splitext(arq)[0] + '.html'
    caminho_saida = os.path.join(pasta_saida, nome_arquivo_saida)

    with open(caminho_saida, "w", encoding="ISO-8859-1") as arquivo_html:
        arquivo_html.write(html)

    with open(caminho_saida, "w", encoding="latin-1") as arquivo_html:
        arquivo_html.write(html)

    with open(caminho_saida, "r", encoding="ISO-8859-1") as arquivo_html:
        conteudo_html = arquivo_html.read()

    conteudo_html = adicionar_hashtags(conteudo_html)
    conteudo_html = remover_elementos_antes_da_hashtag(conteudo_html)
    conteudo_html = remover_hashtags_dos_titulos(conteudo_html)
    conteudo_html = remover_ul(conteudo_html)
    conteudo_html = adicionar_divs_por_pagina_de_elemento(conteudo_html)

    with open(logo_path, 'rb') as logo_file:
        logo_data = base64.b64encode(logo_file.read()).decode('ISO-8859-1')
        logo_tag = f'<img src="data:image/gif;base64,{logo_data}" class="logo-img" style="float: right; max-width: 100px; height: auto; margin-left: 5px;">'

    conteudo_html = f'<div style="background-color: rgba(255, 255, 255, 0.8); padding: 10px;">{logo_tag}</div>{conteudo_html}'

    conteudo_html = adicionar_css(conteudo_html)
    conteudo_html = formatar_titulos(conteudo_html)
    conteudo_html, indice = criar_indice_com_botoes(conteudo_html, nome_arquivo_saida)
    conteudo_html = f'<div class="menu-lateral">{indice}</div><div class="conteudo">{conteudo_html}</div>'
    conteudo_html = adicionar_quebra_de_linha(conteudo_html)
    conteudo_html = adicionar_titulo_aba(conteudo_html, nome_arquivo_saida)
    conteudo_html = adicionar_botao_menu(conteudo_html)
    conteudo_html = adicionar_meta_charset(conteudo_html)

    # lida com a abertura e fechamento do menu
    conteudo_html += """
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            var botaoMenu = document.getElementById('botao-menu');
            var botaoFechar = document.getElementById('botao-fechar-indice');
            var menuLateral = document.querySelector('.menu-lateral');
            var conteudo = document.querySelector('.conteudo');

            function toggleMenu() {
                menuLateral.classList.toggle('menu-aberto');
                conteudo.classList.toggle('conteudo-lateral');
            }

            botaoMenu.addEventListener('click', toggleMenu);
            botaoFechar.addEventListener('click', toggleMenu);

            menuLateral.style.display = 'block'; // Abre o menu no início

        });
    </script>
    """

    conteudo_html += """
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            var botaoMenu = document.getElementById('botao-menu');
            var botaoImprimir = document.querySelector('button[onclick="imprimirConteudo();"]');
            var botaoGo = document.querySelector('button[onclick="pesquisarTexto();"]');

            botaoMenu.addEventListener('mouseover', function() {
                this.style.backgroundColor = '#00d6af'; // Cor alterada quando o mouse está sobre o botão
            });
            botaoMenu.addEventListener('mouseout', function() {
                this.style.backgroundColor = 'rgb(27, 94, 100)'; // Cor original restaurada quando o mouse sai do botão
            });

            botaoImprimir.addEventListener('mouseover', function() {
                this.style.backgroundColor = '#00d6af'; // Cor alterada quando o mouse está sobre o botão
            });
            botaoImprimir.addEventListener('mouseout', function() {
                this.style.backgroundColor = 'transparent'; // Cor original restaurada quando o mouse sai do botão
            });

            botaoGo.addEventListener('mouseover', function() {
                this.style.backgroundColor = '#00d6af'; // Cor alterada quando o mouse está sobre o botão
            });
            botaoGo.addEventListener('mouseout', function() {
                this.style.backgroundColor = 'transparent'; // Cor original restaurada quando o mouse sai do botão
             });
        });
    </script>
    """

    with open(caminho_saida, "w", encoding="ISO-8859-1") as arquivo_html:
        arquivo_html.write(conteudo_html)

# Itere sobre os arquivos
documentos_convertidos = 0
imagens_nao_convertidas = []

for arq in arquivos_docx:
    caminho_entrada = os.path.join(pasta_entrada, arq)
    doc = Document(caminho_entrada)

    # Verifique se a conversão foi bem-sucedida
    if os.path.exists(caminho_saida):
        documentos_convertidos += 1
    else:
        print(f"A conversão do documento {arq} falhou!")

    # Verifique se as imagens foram convertidas e adiciona à lista
    if not os.path.exists(Imagem_indice):
        imagens_nao_convertidas.append(Imagem_indice)

# Exiba informações no terminal
print(f"\nConversão concluída:")
print(f"Total de documentos convertidos: {documentos_convertidos}")

if imagens_nao_convertidas:
    print("\nImagens que não foram convertidas:")
    for img_path in imagens_nao_convertidas:
        print(img_path)
else:
    print("Todos os documentos foram convertidos com sucesso!")
