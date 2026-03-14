from flask import Flask, request, jsonify, render_template, send_file
import os
import core

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sucesso")
def sucesso():
    return render_template("index.html")

@app.route("/politica-privacidade")
def politica_privacidade():
    return render_template("politica-privacidade.html")

@app.route("/api/gerar_dossie", methods=["POST"])
def gerar_dossie():
    data = request.json
    
    # Monta os dados do alvo
    alvo = {
        "nome": data.get("nome"),
        "data": core.formatar_data(data.get("dataNascimento")),
        "hora": core.formatar_hora(data.get("horaNascimento")),
        "cidade": data.get("cidade"),
        "estado": data.get("estado"),
        "pais": data.get("pais", "Brasil")
    }
    
    protocolo_id = data.get("protocolo")
    idioma = data.get("idioma", "PT")
    
    if int(protocolo_id) not in range(1, 17):
        return jsonify({"erro": "Protocolo Inválido"}), 400

    try:
        # Dados do parceiro (opcional)
        parceiro = None
        if data.get("parceiro_nome") and data.get("parceiro_data"):
            parceiro = {
                "nome": data.get("parceiro_nome"),
                "data": core.formatar_data(data.get("parceiro_data"))
            }

        # Verifica se é God Mode (Dossiê Tático 01GURU)
        if protocolo_id == "16":
            arquivo_pdf = core.forjar_dossie_master(alvo, idioma=idioma)
            # Grava no banco de dados (God Mode)
            alvo_id = core.buscar_ou_criar_alvo(alvo)
            core.salvar_relatorio_db(alvo_id, "GOD MODE", idioma, arquivo_pdf)
        else:
            tipo = core.OPCOES[protocolo_id]
            # Passa o parceiro para o oráculo se existir
            texto_oraculo = core.consultar_oraculo(tipo, alvo, dados_parceiro=parceiro)
            if idioma == "EN":
                texto_oraculo = core.traduzir_para_ingles(texto_oraculo)
            
            # Passa o parceiro para o PDF se existir
        # Grava no banco de dados
        alvo_id = core.buscar_ou_criar_alvo(alvo)
        core.salvar_relatorio_db(alvo_id, tipo, idioma, arquivo_pdf)
            
        return send_file(arquivo_pdf, as_attachment=True)
    
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    core.inicializar_banco()
    app.run(debug=True, port=5000)
