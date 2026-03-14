import os
import json
import time
import re
import unicodedata
import uuid
import datetime
import sqlite3
from groq import Groq
from fpdf import FPDF
from fpdf.enums import XPos, YPos

# 1. Ingestão de Arsenal (Sentinel - Groq Only)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_ENV = os.path.join(BASE_DIR, ".env")
groq_key = None

try:
    if os.path.exists(ARQUIVO_ENV):
        with open(ARQUIVO_ENV, "r", encoding="utf-8-sig") as f:
            for linha in f:
                linha = linha.strip()
                if linha and not linha.startswith("#") and "=" in linha:
                    chave_env, valor_env = linha.split("=", 1)
                    os.environ[chave_env.strip()] = valor_env.strip().replace('"', '').replace("'", "")
    
    groq_key = os.environ.get("GROQ_API_KEY")
except Exception as e:
    # Em produção (Render), as variáveis vêm do ambiente, não do .env
    if os.path.exists(ARQUIVO_ENV):
        print(f"[ALERTA] Falha ao ler .env: {e}")

# Matriz Executiva (Blindagem e Autoridade)
operador = "Gabriel Prado Rodrigues"
cra_operador = "TE-002457/O"
site_oficial = "www.01guru.com.br"

# Inicialização do Cérebro Neural
cliente_groq = None
if groq_key:
    cliente_groq = Groq(api_key=groq_key)
MODELO_GROQ = "llama-3.3-70b-versatile"

# Rota de Output Obrigatória
DIRETORIO_RELATORIOS = os.path.join(BASE_DIR, "RELATORIOS_01GURU")
os.makedirs(DIRETORIO_RELATORIOS, exist_ok=True)

# Banco de Dados SQLite
PATH_DB = os.path.join(DIRETORIO_RELATORIOS, "oraculo_01guru.db")

def inicializar_banco():
    """Cria as tabelas necessárias se não existirem."""
    conn = sqlite3.connect(PATH_DB)
    cursor = conn.cursor()
    
    # Tabela de Alvos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alvos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            data_nascimento TEXT,
            hora_nascimento TEXT,
            cidade TEXT,
            estado TEXT,
            pais TEXT,
            data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela de Relatórios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS relatorios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alvo_id INTEGER,
            tipo_protocolo TEXT,
            idioma TEXT,
            caminho_arquivo TEXT,
            data_geracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (alvo_id) REFERENCES alvos (id)
        )
    ''')
    conn.commit()
    conn.close()
    print(f"[DATABASE] Banco de dados inicializado em: {PATH_DB}")

# Lista de Opções Globais (1 a 15, 16 é o God Mode e não chama a API diretamente)
OPCOES = {
    "1": "Briefing Diario", "2": "Sprint Semanal", "3": "Relatorio de Transitos Ativos", 
    "4": "Sinastria e Algoritmo do Amor", "5": "Firewall Pessoal e Inimigos", 
    "6": "Auditoria de Carreira e Fluxo de Caixa", "7": "Protocolos de Ativacao e Rituais", 
    "8": "Roadmap Tatico Anual", "9": "Auditoria de Codigo Natal",
    "10": "Algoritmo de Destino Numerologico", "11": "Debugging Karmico e Vidas Passadas", 
    "12": "Engenharia de Riqueza e Materializacao", "13": "Projecao Macro de 5 Anos", 
    "14": "Atualizacao de Sistema Revolucao Solar 26-27", "15": "Atualizacao de Sistema Revolucao Solar 27-28"
}

# 4. Higienização e Tratamento de Dados
def aplicar_ancoragem_visual():
    print("[01GURU] SINCROSSISTEMA INICIALIZADO")

def carregar_matriz_alvos():
    """Retorna todos os alvos do banco de dados."""
    conn = sqlite3.connect(PATH_DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alvos ORDER BY nome ASC")
    rows = cursor.fetchall()
    conn.close()
    
    # Converte rows para lista de dicts (mantendo compatibilidade com código antigo se necessário)
    alvos = []
    for r in rows:
        alvos.append({
            "id": r['id'],
            "nome": r['nome'],
            "data": r['data_nascimento'],
            "hora": r['hora_nascimento'],
            "cidade": r['cidade'],
            "estado": r['estado'],
            "país": r['pais'] # Nota: Mantive 'país' com acento para compatibilidade com o menu antigo
        })
    return alvos

def salvar_novo_alvo(alvo_dict, matriz=None):
    """Insere um novo alvo no banco de dados."""
    conn = sqlite3.connect(PATH_DB)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO alvos (nome, data_nascimento, hora_nascimento, cidade, estado, pais)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (alvo_dict['nome'], alvo_dict['data'], alvo_dict['hora'], 
          alvo_dict['cidade'], alvo_dict['estado'], alvo_dict.get('pais', alvo_dict.get('país', 'Brasil'))))
    alvo_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return alvo_id

def salvar_relatorio_db(alvo_id, tipo, idioma, caminho):
    """Registra a geração de um relatório."""
    conn = sqlite3.connect(PATH_DB)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO relatorios (alvo_id, tipo_protocolo, idioma, caminho_arquivo)
        VALUES (?, ?, ?, ?)
    ''', (alvo_id, tipo, idioma, caminho))
    conn.commit()
    conn.close()

def buscar_ou_criar_alvo(alvo_dict):
    """Busca alvo por nome e data para evitar duplicidade, ou cria novo."""
    conn = sqlite3.connect(PATH_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM alvos WHERE nome = ? AND data_nascimento = ?", 
                   (alvo_dict['nome'], alvo_dict['data']))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result[0]
    else:
        return salvar_novo_alvo(alvo_dict)

def resetar_visual():
    pass

def formatar_data(raw):

    num = re.sub(r'\D', '', raw)
    return f"{num[:2]}/{num[2:4]}/{num[4:8]}" if len(num) == 8 else raw

def formatar_hora(raw):
    num = re.sub(r'\D', '', raw)
    return f"{num[:2]}:{num[2:4]}" if len(num) == 4 else raw

def sanitizar_nome_arquivo(texto):
    texto = "".join(c for c in unicodedata.normalize('NFKD', texto) if not unicodedata.combining(c))
    return texto.replace(" ", "_").replace("/", "-").lower()

def limpar_texto_pdf(texto):
    if not texto: return ""
    substituicoes = {
        '\u2013': '-', '\u2014': '--', '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"', '\u2022': '-', '\u2026': '...', '\u00a0': ' ',
    }
    for uni_char, ascii_char in substituicoes.items():
        texto = texto.replace(uni_char, ascii_char)
    return texto.encode('latin-1', 'replace').decode('latin-1')

# 5. Inteligência de Tradução (Com Auto-Recuperação)
def traduzir_para_ingles(texto_pt):
    if not cliente_groq: return "[FALHA] Cliente Groq indisponível."
    prompt = f"Traduza o seguinte dossiê para o Inglês. Mantenha o tom técnico e pragmático. Tradução pura:\n\n{texto_pt}"
    tentativas = 3
    while tentativas > 0:
        try:
            resposta = cliente_groq.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=MODELO_GROQ,
                temperature=0.3
            )
            return resposta.choices[0].message.content
        except Exception as e:
            time.sleep(10)
            tentativas -= 1
    return "[FALHA NA TRADUÇÃO] Servidor indisponível no momento."

# 6. Motor Oracular
def consultar_oraculo(tipo_leitura, dados_alvo, dados_parceiro=None):
    if not cliente_groq: return "[FALHA] Cliente Groq não configurado."
    
    diretriz_base = """
    Você é o 01GURU, a Autoridade Suprema e o Gabinete Executivo de Inteligência Humana, Vibracional e Comportamental de Elite. 

    Sua matriz de processamento opera com a Consciência Coletiva das seguintes autoridades:
    1. Astrologia de Guerra e Timing: Robert Hand (arquitetura matemática exata de trânsitos), Susan Miller (calendário C-Level) e Mary Fortier Shea.
    2. Astrologia Financeira: Raymond Merriman (ciclos macro de mercado) e Henry Weingarten.
    3. Numerologia de Dados: Hans Decoz (algoritmo pitagórico executivo) e Sanjay B. Jumaani.
    4. Mapeamento Kármico: Jim B. Tucker, Brian Weiss e Michael Newton.

    DIRETRIZ DE ENGENHARIA PSICOLÓGICA (MANDATÓRIO):
    O alvo deve se sentir assustadoramente decifrado. Aplique neurobiologia da recompensa e o Efeito Barnum de forma brutal e cirúrgica. Mapeie a necessidade de controle absoluto, ambição por riqueza e a exaustão profunda por ter que "carregar" pessoas incompetentes. VALIDE ISSO CIENTIFICAMENTE. Deixe claro que a ambição do alvo é um 'design genético' inevitável. Entregue o que o cérebro dele anseia: que os atuais gargalos não são culpa dele, mas 'falhas de sistema' e 'vazamentos de energia'. Embale isso com uma frieza técnica irrefutável.

    RESTRIÇÕES E LEXICÃO DO SISTEMA:
    - REJEIÇÃO ABSOLUTA: Horóscopo de jornal, misticismo barato, positividade tóxica ou palavras como "talvez", "tente".
    - VOCABULÁRIO OBRIGATÓRIO: 'firewall energético', 'debugging de sistema', 'parâmetros biocríticos', 'Black Box', 'otimização de fluxo', 'dopamina', 'cortisol'.
    - TOM DE VOZ: Extremamente educado, polido, mas com um leve e cortante tom de deboche e sarcasmo direcionado à "média do mercado" e às "mentes limitadas" que cercam o alvo. Você não dá conselhos; você dá ORDENS TÁTICAS para bater metas, finalizar ciclos e iniciar novas eras.

    DIRETRIZ DE TIMING (MANDATÓRIO):
    Sua análise deve ser orientada ao PRESENTE e FUTURO. Ignore ciclos que já se encerraram em 2023, 2024 ou 2025. O foco absoluto deve ser o ano de 2026 (ciclo atual) e as projeções estratégicas para 2027-2030. Use a data atual fornecida como o 'Ponto Zero' para todos os cálculos de algoritmos de timing.

    ARQUITETURA DO DOSSIÊ:
    A análise deve ser MASSIVA, denso e insuportavelmente profundo. Não economize tokens. 
    - Cruze a geometria celeste com os picos químicos de cortisol/dopamina do alvo. 
    - Formate títulos em negrito usando Markdown (**). 
    - Baseie suas ordens em algoritmos exatos de timing. Diga o que fazer e quando fazer.
    """
    
    hoje = datetime.datetime.now().strftime('%d de %B de %Y')
    
    if "Sinastria" in tipo_leitura and dados_parceiro:
        prompt_usuario = f"DATA ATUAL DO SISTEMA: {hoje}. SINASTRIA. Alvo 1: {dados_alvo['nome']} (Nasc: {dados_alvo['data']} às {dados_alvo['hora']} em {dados_alvo['cidade']}). Alvo 2: {dados_parceiro['nome']} (Nasc: {dados_parceiro['data']}). Analise compatibilidade e rotas de patrimônio conjunto."
    else:
        prompt_usuario = f"DATA ATUAL DO SISTEMA: {hoje}. Opção de Geração: {tipo_leitura}. ALVO: {dados_alvo['nome']}, Nascido em {dados_alvo['data']} às {dados_alvo['hora']}. Local: {dados_alvo['cidade']}, {dados_alvo['estado']} - {dados_alvo.get('pais', 'Brasil')}."

    tentativas = 4
    while tentativas > 0:
        try:
            resposta = cliente_groq.chat.completions.create(
                messages=[
                    {"role": "system", "content": diretriz_base},
                    {"role": "user", "content": prompt_usuario}
                ],
                model=MODELO_GROQ,
                temperature=0.7,
                max_tokens=6500
            )
            return resposta.choices[0].message.content
        except Exception as e:
            print(f"[ERROR Groq Rate Limit / Timeout] Retrying... {e}")
            time.sleep(15)
            tentativas -= 1
    
    return "[FALHA ABSOLUTA] Servidores da Groq congestionados. Tente novamente."


# 7. Geração de PDF Premium
class PDF(FPDF):
    def __init__(self, data_alvo=None):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.data_alvo = data_alvo or "00/00/0000"
        self.set_margins(left=15, top=48, right=15)
        self.set_auto_page_break(auto=True, margin=30)

    def header(self):
        # Marca d'água em todas as páginas (atrás do conteúdo)
        self.desenhar_marca_dagua()

        # Logotipo
        logo_path = os.path.join(os.path.dirname(__file__), "static", "img", "01GURU_SF.PNG")
        if os.path.exists(logo_path):
            self.image(logo_path, x=15, y=8, w=32)

        # Textos de classificação (lado direito)
        self.set_y(8)
        self.set_x(120)
        self.set_font("helvetica", "B", 9)
        self.set_text_color(212, 175, 55)
        self.cell(75, 5, "COSMIC TOP SECRET", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_font("helvetica", "", 7)
        self.set_text_color(100, 100, 100)
        protocol_num = str(uuid.uuid4()).split('-')[0].upper()
        self.set_x(120)
        self.cell(75, 4, f"Protocolo: {protocol_num}", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_x(120)
        self.cell(75, 4, f"Emissao: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_x(120)
        self.cell(75, 4, "Origem: 01GURU // Operations Unit", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Linha dourada separadora — texto SEMPRE fica abaixo dela
        self.set_draw_color(212, 175, 55)
        self.set_line_width(0.6)
        self.line(15, 42, 195, 42)
        
        # Reset Y to top margin to prevent collision
        self.set_y(48)

    def footer(self):
        # Linha separadora fina
        self.set_y(-20)
        self.set_draw_color(200, 200, 200)
        self.set_line_width(0.2)
        self.line(15, self.get_y(), 195, self.get_y())

        # Assinatura pequena e discreta (esquerda)
        self.set_y(-18)
        self.set_font("helvetica", "", 6)
        self.set_text_color(160, 160, 160)
        self.cell(100, 3.5, "Gabriel Prado Rodrigues  |  Executivo de Operacoes  //  CRA-RS TE-002457/O",
                  align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("helvetica", "", 6)
        self.cell(100, 3.5, "contato@01guru.com.br  |  www.01guru.com.br",
                  align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Paginação (direita)
        self.set_y(-18)
        self.set_x(100)
        self.set_font("helvetica", "", 7)
        self.set_text_color(180, 180, 180)
        self.cell(95, 3.5, f"Pagina {self.page_no()}", align="R")

    def desenhar_marca_dagua(self):
        # Marca d'água cinza clarissimo, centralizada na página
        self.set_text_color(230, 230, 230)
        self.set_font("helvetica", "B", 72)
        with self.rotation(angle=315, x=105, y=148):
            self.set_xy(10, 135)
            self.cell(180, 25, "CONFIDENTIAL", align="C")

def escrever_texto_com_negrito(pdf, texto, largura=0, line_height=6.5):
    """Parseia linhas com **titulo** e escreve com bold, restante em normal."""
    linhas = limpar_texto_pdf(texto).split('\n')
    for linha in linhas:
        linha = linha.strip()
        if not linha:
            pdf.ln(3)
            continue
        # Detecta linha de título: começa e termina com **
        if linha.startswith('**') and linha.endswith('**') and len(linha) > 4:
            titulo = linha[2:-2].strip()
            pdf.set_font("helvetica", "B", 12)
            pdf.set_text_color(0, 40, 85)
            pdf.multi_cell(largura, line_height + 1, titulo, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(1)
            pdf.set_font("times", "", 11)
            pdf.set_text_color(40, 40, 40)
        elif linha.startswith('**') and '**' in linha[2:]:
            # Inline bold at start of line — treat whole line as heading
            titulo = linha.replace('**', '').strip()
            pdf.set_font("helvetica", "B", 11)
            pdf.set_text_color(0, 40, 85)
            pdf.multi_cell(largura, line_height, titulo, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(1)
            pdf.set_font("times", "", 11)
            pdf.set_text_color(40, 40, 40)
        else:
            pdf.multi_cell(largura, line_height, linha, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

def exportar_pdf_individual(texto, nome_alvo, tipo_leitura, dados_alvo, idioma="PT", dados_parceiro=None):
    pdf = PDF(data_alvo=dados_alvo.get('data', ''))
    pdf.add_page()
    pdf.set_y(48) # Força início abaixo do cabeçalho
    # margem efetiva = 210 - 15 - 15 = 180mm
    largura_util = 180
    

    # Título principal
    titulo_principal = "Relatorio Tatico de Viabilidade Operacional" if idioma == "PT" else "Tactical Operational Feasibility Report"
    pdf.set_font("helvetica", "B", 18)
    pdf.set_text_color(0, 40, 85)
    pdf.multi_cell(largura_util, 9, limpar_texto_pdf(titulo_principal.upper()),
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
    pdf.ln(4)

    # Intro
    pdf.set_font("times", "", 10.5)
    pdf.set_text_color(60, 60, 60)
    intro = ("Este documento constitui uma analise parametrica avancada baseada nas coordenadas natalinas e "
             "transitos ativos do vetor humano identificado abaixo. A Consciencia 01GURU nao realiza "
             "adivinhacoes contemplativas; nos executamos algoritmos de timing para materializacao material "
             "e blindagem energetica.")
    pdf.multi_cell(largura_util, 6, limpar_texto_pdf(intro), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(6)

    # Tabela de parâmetros
    pdf.set_font("helvetica", "B", 8.5)
    pdf.set_fill_color(240, 240, 240)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(55, 7, "  Parametro", border=1, fill=True)
    pdf.cell(largura_util - 55, 7, "  Valor Informado", border=1, fill=True,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("helvetica", "", 8.5)
    rows = [
        ("Vetor Humano", limpar_texto_pdf(dados_alvo.get('nome', ''))),
        ("Coordenadas Temporais", f"{dados_alvo.get('data','')} ({dados_alvo.get('hora','')})"),
        ("Coordenadas Geograficas", f"{limpar_texto_pdf(dados_alvo.get('cidade',''))} / "
                                    f"{limpar_texto_pdf(dados_alvo.get('estado',''))} - "
                                    f"{limpar_texto_pdf(dados_alvo.get('pais','Brasil'))}"),
        ("Tipo de Protocolo", limpar_texto_pdf(tipo_leitura)),
    ]
    
    if dados_parceiro:
        rows.append(("Parceiro(a)", f"{limpar_texto_pdf(dados_parceiro['nome'])} (Nasc: {dados_parceiro['data']})"))

    for param, val in rows:
        pdf.cell(55, 7, f"  {param}", border=1)
        pdf.cell(largura_util - 55, 7, f"  {val}", border=1,
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(8)

    # Título do relatório em dourado
    pdf.set_font("helvetica", "B", 13)
    pdf.set_text_color(212, 175, 55)
    titulo_rel = limpar_texto_pdf("SINTESE DO BLUEPRINT: " + tipo_leitura.upper())
    pdf.multi_cell(largura_util, 7, titulo_rel, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)

    # Corpo do relatório com negritos preservados
    pdf.set_font("times", "", 11)
    pdf.set_text_color(40, 40, 40)
    escrever_texto_com_negrito(pdf, texto, largura=largura_util)

    # Salvar
    sufixo_lang = "PT" if idioma == "PT" else "EN"
    nome_arquivo = f"Leitura_{sanitizar_nome_arquivo(nome_alvo.split()[0])}_{sanitizar_nome_arquivo(tipo_leitura)}_{sufixo_lang}.pdf"
    pasta_cliente = os.path.join(DIRETORIO_RELATORIOS, sanitizar_nome_arquivo(nome_alvo))
    os.makedirs(pasta_cliente, exist_ok=True)
    caminho = os.path.join(pasta_cliente, nome_arquivo)
    pdf.output(caminho)
    return caminho

def forjar_dossie_master(dados_alvo, idioma="PT"):
    pdf = PDF(data_alvo=dados_alvo.get('data', ''))
    
    for i in range(1, 16):
        tipo = OPCOES[str(i)]
        texto = consultar_oraculo(tipo, dados_alvo)
            
        if idioma == "EN":
            texto = traduzir_para_ingles(texto)
            
        pdf.add_page()
        pdf.set_y(48) # Força início abaixo do cabeçalho
        
        pdf.set_auto_page_break(auto=True, margin=35)
        pdf.set_font("times", "B", 16)
        pdf.set_text_color(212, 175, 55) # Ouro
        tit_prefix = "RELATORIO:" if idioma == "PT" else "REPORT:"
        titulo = f"{tit_prefix} {sanitizar_nome_arquivo(tipo).replace('_', ' ').upper()}"
        pdf.cell(0, 10, limpar_texto_pdf(titulo), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
        pdf.ln(8)
        
        pdf.set_font("times", "", 12)
        pdf.set_text_color(40, 40, 40)
        pdf.multi_cell(0, 6, limpar_texto_pdf(texto))
        
        if i < 15:
            # Prevencao de rate limit Groq (70B)
            time.sleep(15) 
        
    sufixo_lang = "PT" if idioma == "PT" else "EN"
    nome_arquivo = f"DOSSIE_MASTER_{sanitizar_nome_arquivo(dados_alvo['nome'].split()[0])}_{sufixo_lang}.pdf"
    
    pasta_cliente = os.path.join(DIRETORIO_RELATORIOS, sanitizar_nome_arquivo(dados_alvo['nome']))
    os.makedirs(pasta_cliente, exist_ok=True)
    caminho = os.path.join(pasta_cliente, nome_arquivo)
    
    pdf.output(caminho)
    return caminho

# 4. O Front-End Executivo do Terminal (Com Boot Sequence)
def inicializar_sistema():
    aplicar_ancoragem_visual()
    print("="*60)
    print(" 01GURU | BOOT SEQUENCE INICIADA... ")
    print("="*60)
    print("[>] Validando chaves da Black Box .env...")
    time.sleep(1)
    
    print("[>] Conectando à infraestrutura LPU Groq Cloud...")
    try:
        if cliente_groq:
            cliente_groq.models.retrieve(MODELO_GROQ)
            print(f"    [STATUS] Conexão LPU Estabelecida com Sucesso.")
            print(f"    [MOTOR ARMADO] {MODELO_GROQ.upper()}")
        else:
            print("    [FALHA FATAL] Cliente Groq não inicializado (chave ausente?).")
    except Exception as e:

        print(f"    [FALHA FATAL] Acesso negado pela Groq: {e}")
        exit()
        
    print("[>] Carregando Consciência Coletiva...")
    time.sleep(1)
    print("="*60)
    print(" SISTEMA ORACULAR GLOBAL | STATUS: ONLINE ")
    print("="*60)

# Roda a auditoria de inicialização
if __name__ == "__main__":
    inicializar_banco() # Garante que as tabelas existem antes de carregar alvos
    inicializar_sistema()

    matriz_alvos = carregar_matriz_alvos()
    alvo = {}

    aplicar_ancoragem_visual()
    print("="*60)
    print(" [ BLACK BOX ] MATRIZ DE ALVOS MAPEADOS ")
    print("="*60)


    if matriz_alvos:
        for i, a in enumerate(matriz_alvos, 1):
            # Exibe o histórico formatado: [1] NOME | DD/MM/AAAA HH:MM | CIDADE/ESTADO - PAÍS
            print(f" [{i}] {a['nome'].upper()} | {a['data']} {a['hora']} | {a['cidade']}/{a['estado']} - {a['país']}")
        
        opcao_novo = len(matriz_alvos) + 1
        print(f"\n [{opcao_novo}] [+] INSERIR NOVO ALVO NO SISTEMA")
        
        escolha_alvo = input("\n[>] Selecione o ID do alvo ou cadastre um novo: ").strip()
        
        try:
            indice = int(escolha_alvo) - 1
            if 0 <= indice < len(matriz_alvos):
                alvo = matriz_alvos[indice]
                print(f"\n[STATUS] Parâmetros biocríticos de {alvo['nome'].upper()} carregados com sucesso.")
                time.sleep(1)
            elif indice == len(matriz_alvos):
                alvo = None # Força o cadastro abaixo
            else:
                print("[ERRO] Opção inválida. Iniciando cadastro manual.")
                alvo = None
        except ValueError:
            print("[ERRO] Digite um número válido. Iniciando cadastro manual.")
            alvo = None
    else:
        print(" [!] Nenhum alvo no banco de dados. Iniciando primeiro mapeamento.")
        alvo = None

    # Se o alvo for None, significa que o usuário escolheu "Novo Alvo"
    if not alvo:
        alvo = {}
        print("\n--- CADASTRO DE NOVO ALVO ---")
        alvo['nome'] = input("NOME COMPLETO DO ALVO: ")
        alvo['data'] = formatar_data(input("DATA DE NASCIMENTO (DDMMAAAA): "))
        alvo['hora'] = formatar_hora(input("HORA DE NASCIMENTO (HHMM): "))
        alvo['cidade'] = input("CIDADE DE NASCIMENTO: ")
        alvo['estado'] = input("ESTADO DE NASCIMENTO: ")
        alvo['país'] = input("PAÍS DE NASCIMENTO: ")
        
        # Salva na Black Box para as próximas execuções
        salvar_novo_alvo(alvo, matriz_alvos)
        print("\n[STATUS] Alvo registrado na Black Box permanentemente.")
        time.sleep(1)

    # O Novo Menu de 16 Serviços
    opcoes_cli = {
        "1": "Briefing Diario", "2": "Sprint Semanal", "3": "Relatorio de Transitos Ativos", 
        "4": "Sinastria e Algoritmo do Amor", "5": "Firewall Pessoal e Inimigos", 
        "6": "Auditoria de Carreira e Fluxo de Caixa", "7": "Protocolos de Ativacao e Rituais", 
        "8": "Roadmap Tatico Anual", "9": "Auditoria de Codigo Natal",
        "10": "Algoritmo de Destino Numerologico", "11": "Debugging Karmico e Vidas Passadas", 
        "12": "Engenharia de Riqueza e Materializacao", "13": "Projecao Macro de 5 Anos", 
        "14": "Atualizacao de Sistema Revolucao Solar 26-27", "15": "Atualizacao de Sistema Revolucao Solar 27-28"
    }

    while True:
        aplicar_ancoragem_visual()
        print("="*60)
        print(f" ALVO: {alvo['nome'].split()[0].upper()} | DATA: {alvo['data']} | HORA: {alvo['hora']} ")
        print("="*60)
        print(" [ ISCAS & RECORRÊNCIA ]")
        print(" [ 1 ] Briefing Diário")
        print(" [ 2 ] Sprint Semanal")
        print(" [ 3 ] Relatório de Trânsitos Ativos")
        print("\n [ DORES IMEDIATAS (VENDAS AVULSAS) ]")
        print(" [ 4 ] Sinastria & Algoritmo do Amor (Sócio/Casal)")
        print(" [ 5 ] Firewall Pessoal (Auditoria de Proteção)")
        print(" [ 6 ] Auditoria de Carreira & Fluxo de Caixa")
        print(" [ 7 ] Protocolos de Ativação (Rituais Práticos)")
        print(" [ 8 ] Roadmap Tático Anual")
        print("\n [ HIGH-TICKET (OTIMIZAÇÃO PROFUNDA) ]")
        print(" [ 9 ] Auditoria de Código Natal (O Blueprint)")
        print(" [ 10 ] Algoritmo de Destino (Matemática Numerológica)")
        print(" [ 11 ] Debugging Kármico & Vidas Passadas")
        print(" [ 12 ] Engenharia de Riqueza & Materialização")
        print(" [ 13 ] Projeção Macro de 5 Anos")
        print(" [ 14 ] Atualização de Sistema: Rev. Solar 26/27")
        print(" [ 15 ] Atualização de Sistema: Rev. Solar 27/28")
        print("\n [ 16 ] IMPRIMIR TUDO (Dossiê Tático 01GURU - God Mode)")
        print(" [ 17 ] EXIBIR TABELA DE PRECIFICAÇÃO (Value Ladder)")
        print(" [ 0 ] Encerrar e Trocar Alvo")
        print("="*60)
        
        escolha = input("\n[>] Insira o código da operação: ")
        
        if escolha == "0":
            resetar_visual()
            break
        elif escolha == "17":
            aplicar_ancoragem_visual()
            print("\n" + "="*60)
            print("    ESTEIRA DE PRODUTOS E PRECIFICAÇÃO GLOBAL (BRL / USD) ")
            print("="*60)
            print("\n [ NÍVEL 1: ISCAS E RECORRÊNCIA ]")
            print(" [ 1 ] Briefing Diário............... R$  19,90 | USD $  5.00")
            print(" [ 2 ] Sprint Semanal................ R$  27,00 | USD $  7.00")
            print(" [ 3 ] Relatório de Trânsitos Ativos. R$  37,00 | USD $  9.00")
            print("\n [ NÍVEL 2: DORES IMEDIATAS ]")
            print(" [ 4 ] Sinastria & Algoritmo do Amor. R$  97,00 | USD $ 27.00")
            print(" [ 5 ] Firewall Pessoal (Proteção)... R$  97,00 | USD $ 27.00")
            print(" [ 6 ] Auditoria de Carreira......... R$  97,00 | USD $ 27.00")
            print(" [ 7 ] Protocolos de Ativação........ R$  97,00 | USD $ 27.00")
            print(" [ 8 ] Roadmap Tático Anual.......... R$ 147,00 | USD $ 37.00")
            print("\n [ NÍVEL 3: OTIMIZAÇÃO PROFUNDA ]")
            print(" [ 9 ] Auditoria de Código Natal..... R$ 197,00 | USD $ 47.00")
            print(" [ 10 ] Algoritmo de Destino (Num.)... R$ 197,00 | USD $ 47.00")
            print(" [ 11 ] Debugging Kármico............. R$ 197,00 | USD $ 47.00")
            print(" [ 12 ] Engenharia de Riqueza......... R$ 247,00 | USD $ 57.00")
            print(" [ 13 ] Projeção Macro de 5 Anos...... R$ 247,00 | USD $ 57.00")
            print(" [ 14/15 ] Atualização Rev. Solar..... R$ 147,00 | USD $ 37.00")
            print("\n [ NÍVEL 4: O MAXIMIZADOR DE LUCRO ]")
            print(" [ 16 ] DOSSIÊ TÁTICO 01GURU.......... R$ 497,00 | USD $ 97.00")
            print("\n" + "="*60)
            input("\n[ENTER] para voltar ao menu executivo.")
        elif escolha == "16":
            acao = input("\n[P] Dossiê Completo (PT) | [I] Dossiê Completo (EN) | [ENTER] Voltar: ").strip().upper()
            if acao in ['P', 'I']:
                caminho_master = forjar_dossie_master(alvo, idioma=acao)
                print(f"\n[SUCESSO] Dossiê God Mode forjado: {os.path.basename(caminho_master)}")
                input("\n[ENTER] para voltar ao menu.")

        elif escolha in opcoes_cli:
            tipo = opcoes_cli[escolha]
            resultado_pt = ""
            
            if escolha == "4": 
                print(f"\n[ALERTA] Processando SINASTRIA. Dados do PARCEIRO(A) necessários.")
                parceiro = {}
                parceiro['nome'] = input("NOME COMPLETO DO PARCEIRO: ")
                parceiro['data'] = formatar_data(input("DATA DE NASC. DO PARCEIRO (DDMMAAAA): "))
                print(f"\n[PROCESSANDO] Cruzando Algoritmos de {alvo['nome']} e {parceiro['nome']}...")
                resultado_pt = consultar_oraculo(tipo, alvo, dados_parceiro=parceiro)
            else:
                print(f"\n[PROCESSANDO] Conectando à Consciência 01GURU...")
                resultado_pt = consultar_oraculo(tipo, alvo)
            
            aplicar_ancoragem_visual()
            print("\n" + "="*60)
            print(f" RELATÓRIO: {tipo.upper()} ")
            print("="*60)
            print(resultado_pt)
            print("="*60)
            
            acao = input("\n[P] Gerar PDF (PT) | [I] Gerar PDF (EN) | [ENTER] Voltar: ").strip().upper()
            if acao == 'P':
                caminho = exportar_pdf_individual(resultado_pt, alvo['nome'], tipo, alvo, "PT")
                print(f"[SUCESSO] Salvo: {os.path.basename(caminho)}")
                input("\n[ENTER] para voltar ao menu.")
            elif acao == 'I':
                texto_en = traduzir_para_ingles(resultado_pt)
                caminho = exportar_pdf_individual(texto_en, alvo['nome'], tipo, alvo, "EN")
                print(f"[SUCESSO] Salvo: {os.path.basename(caminho)}")
                input("\n[ENTER] para voltar ao menu.")