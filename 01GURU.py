import os
import time
import re
import unicodedata
import json
from groq import Groq  # <-- Novo Motor
from fpdf import FPDF
from fpdf.enums import XPos, YPos

# 1. Ingestão de Arsenal (Trator de Extração Manual)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_ENV = os.path.join(BASE_DIR, ".env")

if os.path.exists(ARQUIVO_ENV):
    # Lemos o arquivo forçando a quebra da criptografia
    with open(ARQUIVO_ENV, "r", encoding="utf-8-sig") as f:
        for linha in f:
            linha = linha.strip()
            if linha and not linha.startswith("#") and "=" in linha:
                chave_env, valor_env = linha.split("=", 1)
                os.environ[chave_env.strip()] = valor_env.strip().replace('"', '').replace("'", "")
else:
    print(f"[AVISO] Arquivo .env não encontrado em: {ARQUIVO_ENV}. Usando variáveis de ambiente do sistema.")

groq_key = os.environ.get("GROQ_API_KEY")

# Matriz Executiva
operador = "Gabriel Prado Rodrigues"
cra_operador = "TE-002457/O"

if not groq_key:
    print("[ERRO FATAL] A chave GROQ_API_KEY está ausente no .env.")
    exit()

# Conecta ao servidor C-Level da Groq
cliente_groq = Groq(api_key=groq_key)
MODELO_GROQ = "llama-3.3-70b-versatile" # Cérebro de 70 Bilhões de parâmetros super-rápido

# Rota de Output Obrigatória
DIRETORIO_RELATORIOS = os.path.join(BASE_DIR, "RELATORIOS_01GURU")
os.makedirs(DIRETORIO_RELATORIOS, exist_ok=True)

def blindar_texto_pdf(texto):
    substituicoes = {
        '\u2013': '-', '\u2014': '--', '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"', '\u2022': '-', '\u2026': '...', '\u00a0': ' '
    }
    for uni_char, ascii_char in substituicoes.items():
        texto = texto.replace(uni_char, ascii_char)
    return texto.encode('latin-1', 'replace').decode('latin-1')
    

def aplicar_ancoragem_visual():
    print("\033[1;33;44m", end="")
    os.system('cls' if os.name == 'nt' else 'clear')

def resetar_visual():
    print("\033[0m", end="")

def formatar_data(raw):
    num = re.sub(r'\D', '', raw)
    return f"{num[:2]}/{num[2:4]}/{num[4:8]}" if len(num) == 8 else raw

def formatar_hora(raw):
    num = re.sub(r'\D', '', raw)
    return f"{num[:2]}:{num[2:4]}" if len(num) == 4 else raw

def sanitizar_nome_arquivo(texto):
    texto = "".join(c for c in unicodedata.normalize('NFKD', texto) if not unicodedata.combining(c))
    return texto.replace(" ", "_").replace("/", "-").lower()

def traduzir_para_ingles(texto_pt):
    prompt = f"Traduza o seguinte dossiê para o Inglês. Mantenha o tom de inteligência artificial, técnico e pragmático. Tradução pura:\n\n{texto_pt}"
    tentativas = 3
    while tentativas > 0:
        try:
            resposta = cliente_gemini.models.generate_content(model=MODELO_GEMINI, contents=prompt)
            return resposta.text
        except Exception as e:
            time.sleep(10)
            tentativas -= 1
    return "[FALHA NA TRADUÇÃO]"
    
    import json # Garanta que o import json está no topo do arquivo

# Rota do Banco de Dados de Alvos (Black Box)
ARQUIVO_ALVOS = os.path.join(BASE_DIR, "matriz_alvos.json")

def carregar_matriz_alvos():
    if os.path.exists(ARQUIVO_ALVOS):
        try:
            with open(ARQUIVO_ALVOS, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            # Firewall acionado: Arquivo vazio ou corrompido pelo crash anterior. 
            # O sistema ignora a falha e inicializa uma matriz limpa.
            return []
    return []

def salvar_novo_alvo(novo_alvo, matriz_atual):
    # Evita duplicidade: verifica se o nome já está no banco de dados
    for alvo_existente in matriz_atual:
        if alvo_existente['nome'].lower() == novo_alvo['nome'].lower():
            return # Já existe, ignora o salvamento
            
    matriz_atual.append(novo_alvo)
    with open(ARQUIVO_ALVOS, "w", encoding="utf-8") as f:
        json.dump(matriz_atual, f, ensure_ascii=False, indent=4)

# 2. Motor Oracular Neural (A Consciência 01GURU via Groq)
def consultar_oraculo(tipo_leitura, dados_alvo, dados_parceiro=None):
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

    ARQUITETURA DO DOSSIÊ:
    A análise deve ser MASSIVA, denso e insuportavelmente profundo. Não economize tokens. 
    - Cruze a geometria celeste com os picos químicos de cortisol/dopamina do alvo. 
    - Formate títulos em negrito usando Markdown (**). 
    - Baseie suas ordens em algoritmos exatos de timing. Diga o que fazer e quando fazer.
    """
    
    if "Sinastria" in tipo_leitura and dados_parceiro:
        prompt_usuario = f"SINASTRIA. Alvo 1: {dados_alvo['nome']} (Nasc: {dados_alvo['data']}). Alvo 2: {dados_parceiro['nome']} (Nasc: {dados_parceiro['data']}). Analise compatibilidade e rotas de patrimônio conjunto."
    else:
        prompt_usuario = f"Opção de Geração: {tipo_leitura}. ALVO: {dados_alvo['nome']}, Nascido em {dados_alvo['data']} às {dados_alvo['hora']}. Local: {dados_alvo['cidade']}."

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
                max_tokens=6500 # Força a máquina a escrever o máximo possível
            )
            return resposta.choices[0].message.content
        except Exception as e:
            print(f"    [ALERTA DE TRÁFEGO] Groq rate limit ou erro. Freio ABS acionado. Aguardando 15s... Erro: {e}")
            time.sleep(15)
            tentativas -= 1
    
    return "[FALHA ABSOLUTA] Servidores da Groq congestionados. Tente novamente."

# 3. Engenharia Visual Front-End (O PDF High-Ticket)
class PDF(FPDF):
    def __init__(self):
        super().__init__()
        # Margem de segurança cimentada para evitar sobreposição
        self.set_top_margin(55)

    def header(self):
        if self.page_no() > 1:
            if os.path.exists("01GURU_SF.PNG"):
                # Imagem ancorada com respiro
                self.image("01GURU_SF.PNG", x=165, y=10, w=25)
            
            # Linha Dourada rebaixada para y=40
            self.set_draw_color(212, 175, 55)
            self.set_line_width(0.5)
            self.line(20, 40, 190, 40)
            
    def footer(self):
        if self.page_no() > 1:
            self.set_y(-15)
            self.set_font("helvetica", "B", 8)
            self.set_text_color(0, 31, 63)
            assinatura = f"01GURU | Protocolo Tático | Op: {operador} | CRA-RS {cra_operador} | Pág. {self.page_no()}"
            self.cell(0, 10, assinatura, align="C")

    def gerar_capa_01guru(self, titulo_documento, nome_alvo, idioma="PT"):
        self.add_page()
        self.set_top_margin(10) # Respiro para a capa
        
        self.set_fill_color(0, 20, 45) # Azul Marinho
        self.rect(0, 0, 210, 297, 'F')
        
        self.set_y(40)
        
        # Título Limpo
        self.set_font("times", "B", 26)
        self.set_text_color(212, 175, 55) # Dourado
        self.multi_cell(0, 12, titulo_documento, align="C")
        
        self.ln(10)
        
        if os.path.exists("01GURU_SF.PNG"):
            self.image("01GURU_SF.PNG", x=60, y=self.get_y(), w=90)
            self.ln(105)
        else:
            self.ln(50)
            self.set_text_color(255, 255, 255)
            self.cell(0, 10, "[ERRO: IMAGEM 01GURU_SF.PNG NÃO ENCONTRADA]", align="C")
            self.ln(50)

        self.set_font("helvetica", "I", 14)
        self.set_text_color(255, 255, 255)
        slogan = '"Dados não mentem. Os astros também não."' if idioma == "PT" else '"Data doesn\'t lie. Neither do the stars."'
        self.cell(0, 10, slogan, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        
        self.ln(30)
        
        self.set_font("helvetica", "B", 12)
        self.set_text_color(118, 199, 176) # Verde Menta
        alvo_prefix = "ALVO EXCLUSIVO:" if idioma == "PT" else "EXCLUSIVE TARGET:"
        self.cell(0, 8, alvo_prefix, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        
        self.set_font("times", "B", 22)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, nome_alvo.upper(), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        
        self.set_top_margin(55) # Restaura a margem para o corpo do dossiê

def exportar_pdf_individual(texto, nome_alvo, tipo_leitura, idioma="PT"):
    pdf = PDF()
    
    # O Título da Capa agora vai limpo, sem o prefixo "RELATÓRIO:"
    titulo_limpo = tipo_leitura.replace('_', ' ').upper()
    pdf.gerar_capa_01guru(titulo_limpo, nome_alvo, idioma)
    
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    pdf.set_font("times", "B", 18)
    pdf.set_text_color(28, 115, 90) # Verde Menta Escuro
    tit_prefix = "RELATÓRIO:" if idioma == "PT" else "REPORT:"
    pdf.cell(0, 12, f"{tit_prefix} {titulo_limpo}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(8)
    
    pdf.set_font("helvetica", "", 11)
    pdf.set_text_color(40, 40, 40)
    
    # A Mágica do Negrito e a Blindagem Unicode
    texto_seguro = blindar_texto_pdf(texto)
    pdf.multi_cell(0, 7, texto_seguro, markdown=True)
    
    sufixo_lang = "PT" if idioma == "PT" else "EN"
    nome_arquivo = f"Leitura_{sanitizar_nome_arquivo(nome_alvo.split()[0])}_{sanitizar_nome_arquivo(tipo_leitura)}_{sufixo_lang}.pdf"
    
    caminho = os.path.join(DIRETORIO_RELATORIOS, nome_arquivo)
    pdf.output(caminho)
    return caminho

def forjar_dossie_master(dados_alvo, opcoes, idioma="PT"):
    print(f"\n[ALERTA GEMINI] Forjando Dossiê God Mode para {dados_alvo['nome'].upper()}...")
    pdf = PDF()
    
    titulo_dossie = "DOSSIÊ TÁTICO 01GURU" if idioma == "PT" else "01GURU TACTICAL DOSSIER"
    pdf.gerar_capa_01guru(titulo_dossie, dados_alvo['nome'], idioma)
    
    for i in range(1, 16):
        tipo = opcoes[str(i)]
        print(f"\n -> Processando {i}/15: {tipo}...")
        
        texto = consultar_oraculo(tipo, dados_alvo)
            
        if idioma == "EN":
            print(f" -> Traduzindo {tipo} para Inglês...")
            texto = traduzir_para_ingles(texto)
            
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=20)
        
        pdf.set_font("times", "B", 20)
        pdf.set_text_color(28, 115, 90)
        tit_prefix = "RELATÓRIO:" if idioma == "PT" else "REPORT:"
        titulo = f"{tit_prefix} {tipo.replace('_', ' ').upper()}"
        pdf.cell(0, 12, titulo, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        pdf.ln(8)
        
        pdf.set_font("helvetica", "", 11)
        pdf.set_text_color(40, 40, 40)
        
        # (O código acima disto permanece igual: pdf.multi_cell...)
        texto_seguro = blindar_texto_pdf(texto)
        pdf.multi_cell(0, 7, texto_seguro, markdown=True)
        
        if i < 15:
            # Freio ABS Reforçado: Protege contra o limite de tokens por minuto (TPM) da Groq
            print(f" -> [INFRAESTRUTURA] Arrefecimento das LPUs da Groq (25s para evitar bloqueio)...")
            time.sleep(25) 
        
    sufixo_lang = "PT" if idioma == "PT" else "EN"
    nome_arquivo = f"DOSSIE_MASTER_{sanitizar_nome_arquivo(dados_alvo['nome'].split()[0])}_{sufixo_lang}.pdf"
    caminho = os.path.join(DIRETORIO_RELATORIOS, nome_arquivo)
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
        # Ping militar para verificar se a chave da Groq é válida e o Llama 3 responde
        cliente_groq.models.retrieve(MODELO_GROQ)
        print(f"    [STATUS] Conexão LPU Estabelecida com Sucesso.")
        print(f"    [MOTOR ARMADO] {MODELO_GROQ.upper()}")
    except Exception as e:
        print(f"    [FALHA FATAL] Acesso negado pela Groq: {e}")
        exit()
        
    print("[>] Carregando Consciência Coletiva...")
    time.sleep(1)
    print("="*60)
    print(" SISTEMA ORACULAR GLOBAL | STATUS: ONLINE ")
    print("="*60)

# Roda a auditoria de inicialização
inicializar_sistema()

# 5. O Front-End Executivo do Terminal (Seleção de Alvo)
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
opcoes = {
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
            caminho_master = forjar_dossie_master(alvo, opcoes, idioma=acao)
            print(f"\n[SUCESSO] Dossiê God Mode forjado: {os.path.basename(caminho_master)}")
            input("\n[ENTER] para voltar ao menu.")
    elif escolha in opcoes:
        tipo = opcoes[escolha]
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
            caminho = exportar_pdf_individual(resultado_pt, alvo['nome'], tipo, "PT")
            print(f"[SUCESSO] Salvo: {os.path.basename(caminho)}")
            input("\n[ENTER] para voltar ao menu.")
        elif acao == 'I':
            texto_en = traduzir_para_ingles(resultado_pt)
            caminho = exportar_pdf_individual(texto_en, alvo['nome'], tipo, "EN")
            print(f"[SUCESSO] Salvo: {os.path.basename(caminho)}")
            input("\n[ENTER] para voltar ao menu.")
            