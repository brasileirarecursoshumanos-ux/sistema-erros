# app.py - SISTEMA WEB CORRIGIDO
from flask import Flask, render_template, request, jsonify, send_file, session
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os
import csv

app = Flask(__name__)
app.secret_key = 'sistema_erros_2024_seguro'
CORS(app)

# ========== ADICIONAR FILTRO DATE ==========
@app.template_filter('date')
def format_date(value, format='%Y-%m-%d'):
    """Filtro para formatar datas no Jinja2"""
    if value is None:
        return ''
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%d')
        except:
            return value
    if isinstance(value, datetime):
        return value.strftime(format)
    return value

# Adicionar data atual para todos os templates
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# ========== CONFIGURAÇÕES ==========
# app.py - SISTEMA WEB COM DADOS REAIS PARA RENDER
from flask import Flask, render_template, request, jsonify, send_file, session
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os
import csv
import json

app = Flask(__name__)
app.secret_key = 'sistema_erros_2024_seguro'
CORS(app)

# ========== ADICIONAR FILTRO DATE ==========
@app.template_filter('date')
def format_date(value, format='%Y-%m-%d'):
    """Filtro para formatar datas no Jinja2"""
    if value is None:
        return ''
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%d')
        except:
            return value
    if isinstance(value, datetime):
        return value.strftime(format)
    return value

# Adicionar data atual para todos os templates
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# ========== CONFIGURAÇÕES ==========
# USAR CAMINHO RELATIVO PARA RENDER
DATABASE = 'erros_filiais.db'

def init_database():
    """Inicializa o banco de dados com os dados reais fornecidos"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Criar tabelas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS filiais (
            codigo TEXT PRIMARY KEY,
            nome TEXT,
            gerente TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_completo TEXT NOT NULL,
            filial TEXT NOT NULL,
            FOREIGN KEY (filial) REFERENCES filiais(codigo)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tipos_erro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT NOT NULL,
            criterio TEXT NOT NULL,
            sigla TEXT UNIQUE NOT NULL,
            penalizacao TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registros_erros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filial TEXT NOT NULL,
            vendedor TEXT NOT NULL,
            tipo_erro TEXT NOT NULL,
            sigla TEXT NOT NULL,
            penalizacao TEXT NOT NULL,
            data_ocorrencia DATE NOT NULL,
            quantidade INTEGER DEFAULT 1,
            observacoes TEXT,
            registrado_por TEXT DEFAULT 'Sistema Web',
            data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (filial) REFERENCES filiais(codigo)
        )
    ''')
    
    # Inserir dados reais das filiais e gerentes
    filiais_gerentes = [
        ("F01", "Filial F01", "Alexandre"),
        ("F03", "Filial F03", "LINA"),
        ("F04", "Filial F04", "WELITON"),
        ("F05", "Filial F05", "EDNA"),
        ("F07", "Filial F07", "WELLITON T"),
        ("F08", "Filial F08", "JUNIOR"),
        ("F10", "Filial F10", "RENATO"),
        ("F12", "Filial F12", "MARIA"),
        ("F13", "Filial F13", "ANA KARLLA"),
        ("F14", "Filial F14", "ANDERSON"),
        ("F15", "Filial F15", "LUCÉLIA"),
        ("F16", "Filial F16", "TALITA"),
        ("F17", "Filial F17", "ADELAR")
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO filiais (codigo, nome, gerente) 
        VALUES (?, ?, ?)
    ''', filiais_gerentes)
    
    # Inserir vendedores reais
    vendedores_reais = [
        ("Everson Sampaio Tofoli", "F01"),
        ("Isaac Ribeiro Gonsalves", "F01"),
        ("Maila Cristina Cervantes Comim", "F01"),
        ("Maria Rosimeire Francisco Costa", "F01"),
        ("Nayara de Oliveira Martins", "F01"),
        ("Nelson Paulino", "F03"),
        ("Katia Mara Avelino dos Santos", "F04"),
        ("Regina dos Santos Souza", "F04"),
        ("Bruna Reser de Andrade", "F05"),
        ("Claudia da Silva", "F05"),
        ("Dienifer Gabriela Martins Britez", "F05"),
        ("Raiza da Costa Guth", "F07"),
        ("Vanessa Goncalves", "F07"),
        ("Adriana Mateus dos Santos", "F08"),
        ("Jessica Aline", "F08"),
        ("João Santiago Silva Cortinas Lopes", "F08"),
        ("Thais da Silva Rodolfo", "F08"),
        ("Franciele Rodrigues", "F10"),
        ("Kauan Melo da Silva", "F10"),
        ("Vanessa Daiane Cícero de Lima", "F10"),
        ("Jefter de Souza Prates", "F12"),
        ("Maira Carolina Avalo Urbieta", "F12"),
        ("Olivia Custodio Jorge Lima", "F12"),
        ("Ramona Martas Sanches de Almeida", "F12"),
        ("Francielly da Silva Vargas", "F13"),
        ("Geovana Figueiredo Salvatico Goncalves", "F13"),
        ("Leticia Clarindo da Silva", "F13"),
        ("Aline Ferreira de Araujo", "F14"),
        ("Geisiane dos Santos Lima", "F14"),
        ("Laura Martins Ponsiano", "F14"),
        ("Ana Paula de Souza Santos", "F15"),
        ("Chaiane Paola dos Santos Silva", "F15"),
        ("Lucineia Nogueira Aguiar Correa", "F15"),
        ("Fernanda Martins da Silva", "F15"),
        ("Ariene Castielle Olinto Costa", "F15"),
        ("Camila Rodrigues Ponte", "F16"),
        ("Elaine Arques de Souza", "F16"),
        ("Gederson Ferreira Moreira", "F16"),
        ("Edilaine Allenbrandt Pickler", "F17"),
        ("Larissa Vitoria Urbieta Goncalves", "F17"),
        ("Luana Carolina Magalhaes Mendonca", "F17"),
        ("Shirley Miguel Canuto", "F17")
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO vendedores (nome_completo, filial) 
        VALUES (?, ?)
    ''', vendedores_reais)
    
    # Inserir tipos de erro REAIS conforme tabela fornecida
    tipos_erro_reais = [
        # PROCESSOS ADMINISTRATIVOS
        ("PROCESSOS ADMINISTRATIVOS", "Não atualizar cadastro de cliente", "CAD", "-3% por caso"),
        ("PROCESSOS ADMINISTRATIVOS", "Falha no registro de ponto", "PTO", "-2% por dia"),
        ("PROCESSOS ADMINISTRATIVOS", "Uniforme incorreto", "UNF", "-3% por dia"),
        ("PROCESSOS ADMINISTRATIVOS", "Não concluir tarefas/Procrastinação", "TAR", "-2% por ocorrência"),
        
        # PÓS-VENDAS E CLIENTE
        ("PÓS-VENDAS E CLIENTE", "Falta de acompanhamento - pós-venda", "PVD", "-3% por cliente"),
        ("PÓS-VENDAS E CLIENTE", "Não comunicar OS/Assistência Técnica em caso de defeito no produto do cliente", "OSS", "-3% por ocorrência"),
        ("PÓS-VENDAS E CLIENTE", "Reclamar de comissão na frente de cliente", "COM", "-5% por ocorrência"),
        ("PÓS-VENDAS E CLIENTE", "Não prestar apoio com recebimento", "REC", "-3% por caso"),
        
        # ESTOQUE E PROCESSOS
        ("ESTOQUE E PROCESSOS", "Venda para terceiros sem comunicação", "V3S", "-8% por caso"),
        ("ESTOQUE E PROCESSOS", "Erro de etiquetagem/precificação", "ETQ", "-4% por divergência"),
        ("ESTOQUE E PROCESSOS", "Lançar venda do CD e entregar da loja", "CDL", "-4% por ocorrência"),
        ("ESTOQUE E PROCESSOS", "Prometer brindes/condições não autorizadas", "BRI", "-4% por caso"),
        
        # COMPORTAMENTO PROFISSIONAL
        ("COMPORTAMENTO PROFISSIONAL", "Não resolver problemas simples", "ATD", "-3% por ocorrência"),
        ("COMPORTAMENTO PROFISSIONAL", "Não ajudar na organização da loja", "ORG", "-3% por dia"),
        ("COMPORTAMENTO PROFISSIONAL", "Não participar da montagem da frente de loja até 09h00", "FDL", "-2% por dia")
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO tipos_erro (categoria, criterio, sigla, penalizacao) 
        VALUES (?, ?, ?, ?)
    ''', tipos_erro_reais)
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Conecta ao banco de dados"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Inicializar banco ao iniciar
init_database()

# ========== ROTAS PRINCIPAIS ==========

@app.route('/')
def index():
    """Página inicial"""
    return render_template('index.html')

@app.route('/registrar')
def registrar():
    """Página de registro de erros"""
    return render_template('registrar.html')

@app.route('/relatorios')
def relatorios():
    """Página de relatórios"""
    return render_template('relatorios.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard com estatísticas"""
    return render_template('dashboard.html')

# ========== API - DADOS ==========

@app.route('/api/filiais')
def get_filiais():
    """API: Retorna todas as filiais"""
    try:
        conn = get_db_connection()
        filiais = conn.execute('''
            SELECT codigo, nome, gerente FROM filiais ORDER BY codigo
        ''').fetchall()
        conn.close()
        
        return jsonify([dict(filial) for filial in filiais])
    except Exception as e:
        print(f"Erro no banco: {e}")
        return jsonify([])

@app.route('/api/vendedores/<filial>')
def get_vendedores(filial):
    """API: Retorna vendedores de uma filial"""
    try:
        conn = get_db_connection()
        vendedores = conn.execute('''
            SELECT nome_completo, filial FROM vendedores 
            WHERE filial = ? ORDER BY nome_completo
        ''', (filial,)).fetchall()
        conn.close()
        
        return jsonify([dict(v) for v in vendedores])
    except Exception as e:
        print(f"Erro no banco: {e}")
        return jsonify([])

@app.route('/api/todos-vendedores')
def get_todos_vendedores():
    """API: Retorna todos os vendedores"""
    try:
        conn = get_db_connection()
        vendedores = conn.execute('''
            SELECT nome_completo, filial FROM vendedores 
            ORDER BY nome_completo
        ''').fetchall()
        conn.close()
        
        return jsonify([dict(v) for v in vendedores])
    except Exception as e:
        print(f"Erro no banco: {e}")
        return jsonify([])

@app.route('/api/tipos-erro')
def get_tipos_erro():
    """API: Retorna todos os tipos de erro"""
    try:
        conn = get_db_connection()
        tipos = conn.execute('''
            SELECT categoria, criterio, sigla, penalizacao 
            FROM tipos_erro ORDER BY categoria, criterio
        ''').fetchall()
        conn.close()
        
        return jsonify([dict(tipo) for tipo in tipos])
    except Exception as e:
        print(f"Erro no banco: {e}")
        return jsonify([])

@app.route('/api/categorias-erro')
def get_categorias_erro():
    """API: Retorna todas as categorias de erro"""
    try:
        conn = get_db_connection()
        categorias = conn.execute('''
            SELECT DISTINCT categoria FROM tipos_erro ORDER BY categoria
        ''').fetchall()
        conn.close()
        
        return jsonify([dict(cat)['categoria'] for cat in categorias])
    except Exception as e:
        print(f"Erro no banco: {e}")
        return jsonify([])

@app.route('/api/tipos-por-categoria/<categoria>')
def get_tipos_por_categoria(categoria):
    """API: Retorna tipos de erro por categoria"""
    try:
        conn = get_db_connection()
        tipos = conn.execute('''
            SELECT criterio, sigla, penalizacao 
            FROM tipos_erro 
            WHERE categoria = ? 
            ORDER BY criterio
        ''', (categoria,)).fetchall()
        conn.close()
        
        return jsonify([dict(tipo) for tipo in tipos])
    except Exception as e:
        print(f"Erro no banco: {e}")
        return jsonify([])

@app.route('/api/registrar-erro', methods=['POST'])
def registrar_erro():
    """API: Registra um novo erro - AGORA ACEITA MULTIPLOS ERROS"""
    try:
        dados = request.json
        
        # Verificar se é um único erro ou múltiplos
        if isinstance(dados, dict):
            erros = [dados]
        elif isinstance(dados, list):
            erros = dados
        else:
            return jsonify({'success': False, 'message': 'Formato de dados inválido!'}), 400
        
        resultados = []
        erros_falhos = []
        
        for i, erro in enumerate(erros):
            try:
                # Validar dados obrigatórios
                campos_obrigatorios = ['filial', 'vendedor', 'tipo_erro', 'sigla', 'penalizacao', 'data_ocorrencia']
                campos_faltantes = []
                for campo in campos_obrigatorios:
                    if campo not in erro or not erro[campo]:
                        campos_faltantes.append(campo)
                
                if campos_faltantes:
                    erros_falhos.append({
                        'indice': i,
                        'erro': f'Campos obrigatórios faltando: {", ".join(campos_faltantes)}',
                        'dados': erro
                    })
                    continue
                
                # Inserir no banco
                conn = get_db_connection()
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO registros_erros 
                    (filial, vendedor, tipo_erro, sigla, penalizacao, 
                     data_ocorrencia, quantidade, observacoes, registrado_por)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    erro['filial'],
                    erro['vendedor'],
                    erro['tipo_erro'],
                    erro['sigla'],
                    erro['penalizacao'],
                    erro['data_ocorrencia'],
                    erro.get('quantidade', 1),
                    erro.get('observacoes', ''),
                    erro.get('registrado_por', 'Sistema Web')
                ))
                
                registro_id = cursor.lastrowid
                conn.commit()
                conn.close()
                
                resultados.append({
                    'success': True,
                    'indice': i,
                    'registro_id': registro_id,
                    'vendedor': erro['vendedor'],
                    'tipo_erro': erro['tipo_erro'],
                    'sigla': erro['sigla']
                })
                
            except Exception as e:
                erros_falhos.append({
                    'indice': i,
                    'erro': str(e),
                    'dados': erro
                })
        
        # Se todos falharam, retornar erro
        if len(resultados) == 0 and len(erros_falhos) > 0:
            return jsonify({
                'success': False,
                'message': 'Falha ao registrar todos os erros!',
                'erros': erros_falhos
            }), 400
        
        # Se alguns falharam, retornar parcial
        if len(erros_falhos) > 0:
            return jsonify({
                'success': True,
                'message': f'Registrados {len(resultados)} de {len(erros)} erros',
                'resultados': resultados,
                'erros_falhos': erros_falhos,
                'total_registrados': len(resultados)
            })
        
        # Se todos foram bem sucedidos
        return jsonify({
            'success': True,
            'message': f'Todos os {len(resultados)} erros registrados com sucesso!',
            'resultados': resultados,
            'total_registrados': len(resultados)
        })
        
    except Exception as e:
        print(f"Erro geral no registro: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/registrar-multiplos', methods=['POST'])
def registrar_multiplos():
    """API: Registra múltiplos erros de uma vez - ENDPOINT ALTERNATIVO"""
    return registrar_erro()

@app.route('/api/ultimos-registros')
def get_ultimos_registros():
    """API: Retorna últimos registros"""
    try:
        conn = get_db_connection()
        registros = conn.execute('''
            SELECT 
                r.id, 
                r.filial, 
                r.vendedor, 
                r.tipo_erro, 
                r.sigla, 
                r.penalizacao, 
                r.data_ocorrencia, 
                r.quantidade,
                r.observacoes, 
                r.registrado_por, 
                r.data_registro,
                f.gerente, 
                f.nome as nome_filial
            FROM registros_erros r
            LEFT JOIN filiais f ON r.filial = f.codigo
            ORDER BY r.data_registro DESC
            LIMIT 15
        ''').fetchall()
        conn.close()
        
        return jsonify([dict(reg) for reg in registros])
    except Exception as e:
        print(f"Erro ao buscar registros: {e}")
        return jsonify([])

@app.route('/api/estatisticas')
def get_estatisticas():
    """API: Retorna estatísticas do sistema"""
    try:
        conn = get_db_connection()
        
        # Total de registros
        total_registros = conn.execute('SELECT COUNT(*) FROM registros_erros').fetchone()[0]
        
        # Registros hoje
        hoje = datetime.now().strftime('%Y-%m-%d')
        registros_hoje = conn.execute('''
            SELECT COUNT(*) FROM registros_erros WHERE DATE(data_registro) = ?
        ''', (hoje,)).fetchone()[0]
        
        # Total por filial
        por_filial = conn.execute('''
            SELECT 
                r.filial, 
                f.nome, 
                COUNT(*) as total,
                f.gerente
            FROM registros_erros r
            LEFT JOIN filiais f ON r.filial = f.codigo
            GROUP BY r.filial
            ORDER BY total DESC
        ''').fetchall()
        
        # Top vendedores com mais erros
        top_vendedores = conn.execute('''
            SELECT vendedor, COUNT(*) as total_erros
            FROM registros_erros
            GROUP BY vendedor
            ORDER BY total_erros DESC
            LIMIT 8
        ''').fetchall()
        
        # Erros por categoria
        por_categoria = conn.execute('''
            SELECT 
                t.categoria,
                COUNT(*) as total,
                SUM(CASE 
                    WHEN DATE(r.data_registro) = DATE('now') THEN 1 
                    ELSE 0 
                END) as hoje
            FROM registros_erros r
            LEFT JOIN tipos_erro t ON r.sigla = t.sigla
            GROUP BY t.categoria
            ORDER BY total DESC
        ''').fetchall()
        
        # Último registro
        ultimo_registro = conn.execute('''
            SELECT MAX(data_registro) as ultimo FROM registros_erros
        ''').fetchone()
        
        conn.close()
        
        return jsonify({
            'total_registros': total_registros,
            'registros_hoje': registros_hoje,
            'status_banco': 'ativo',
            'ultima_atualizacao': datetime.now().isoformat(),
            'ultimo_registro': ultimo_registro['ultimo'] if ultimo_registro else None,
            'por_filial': [dict(f) for f in por_filial],
            'top_vendedores': [dict(v) for v in top_vendedores],
            'por_categoria': [dict(c) for c in por_categoria]
        })
        
    except Exception as e:
        print(f"Erro em estatísticas: {e}")
        return jsonify({
            'total_registros': 0,
            'registros_hoje': 0,
            'status_banco': 'offline',
            'ultima_atualizacao': datetime.now().isoformat(),
            'ultimo_registro': None
        })

@app.route('/api/relatorio', methods=['POST'])
def gerar_relatorio():
    """API: Gera relatório"""
    try:
        dados = request.json
        
        conn = get_db_connection()
        
        query = '''
            SELECT 
                r.filial, 
                f.nome as nome_filial,
                f.gerente,
                r.data_ocorrencia,
                r.vendedor,
                r.tipo_erro,
                t.categoria,
                r.sigla,
                r.penalizacao,
                r.quantidade,
                r.observacoes,
                r.registrado_por,
                r.data_registro
            FROM registros_erros r
            LEFT JOIN filiais f ON r.filial = f.codigo
            LEFT JOIN tipos_erro t ON r.sigla = t.sigla
            WHERE 1=1
        '''
        params = []
        
        if dados.get('filial'):
            query += ' AND r.filial = ?'
            params.append(dados['filial'])
        
        if dados.get('data_inicio'):
            query += ' AND r.data_ocorrencia >= ?'
            params.append(dados['data_inicio'])
        
        if dados.get('data_fim'):
            query += ' AND r.data_ocorrencia <= ?'
            params.append(dados['data_fim'])
        
        if dados.get('sigla'):
            query += ' AND r.sigla = ?'
            params.append(dados['sigla'])
        
        if dados.get('vendedor'):
            query += ' AND r.vendedor = ?'
            params.append(dados['vendedor'])
        
        if dados.get('categoria'):
            query += ' AND t.categoria = ?'
            params.append(dados['categoria'])
        
        query += ' ORDER BY r.data_ocorrencia DESC, r.filial, r.vendedor'
        
        registros = conn.execute(query, params).fetchall()
        conn.close()
        registros = [dict(reg) for reg in registros]
        
        if not registros:
            return jsonify({'success': False, 'message': 'Nenhum registro encontrado!'})
        
        # Gerar arquivo CSV
        if not os.path.exists('relatorios'):
            os.makedirs('relatorios')
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tipo = dados.get('filial', 'geral') if not dados.get('sigla') else dados.get('sigla')
        filename = f"relatorio_{tipo}_{timestamp}.csv"
        filepath = os.path.join('relatorios', filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            
            writer.writerow([
                'COD. FILIAL', 
                'NOME FILIAL', 
                'GERENTE', 
                'DATA OCORRÊNCIA',
                'VENDEDOR', 
                'CATEGORIA ERRO',
                'TIPO ERRO', 
                'SIGLA', 
                'PENALIZAÇÃO',
                'QUANTIDADE', 
                'OBSERVAÇÕES', 
                'REGISTRADO POR', 
                'DATA REGISTRO'
            ])
            
            for reg in registros:
                writer.writerow([
                    reg.get('filial', ''),
                    reg.get('nome_filial', ''),
                    reg.get('gerente', ''),
                    reg.get('data_ocorrencia', ''),
                    reg.get('vendedor', ''),
                    reg.get('categoria', ''),
                    reg.get('tipo_erro', ''),
                    reg.get('sigla', ''),
                    reg.get('penalizacao', ''),
                    reg.get('quantidade', 1),
                    reg.get('observacoes', ''),
                    reg.get('registrado_por', ''),
                    reg.get('data_registro', '')
                ])
        
        return jsonify({
            'success': True,
            'message': f'Relatório gerado com {len(registros)} registros!',
            'filename': filename,
            'filepath': f'/download/{filename}',
            'total_registros': len(registros)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download do arquivo CSV"""
    try:
        filepath = os.path.join('relatorios', filename)
        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename,
            mimetype='text/csv'
        )
    except Exception as e:
        return f"Erro ao baixar arquivo: {e}", 404

# ========== ROTAS ADICIONAIS PARA DASHBOARD ==========

@app.route('/api/resumo-mensal/<ano>/<mes>')
def get_resumo_mensal(ano, mes):
    """API: Retorna resumo mensal"""
    try:
        conn = get_db_connection()
        
        # Filiais com mais erros no mês
        top_filiais = conn.execute('''
            SELECT 
                r.filial,
                f.nome,
                f.gerente,
                COUNT(*) as total_erros
            FROM registros_erros r
            LEFT JOIN filiais f ON r.filial = f.codigo
            WHERE strftime('%Y-%m', r.data_ocorrencia) = ?
            GROUP BY r.filial
            ORDER BY total_erros DESC
            LIMIT 5
        ''', (f"{ano}-{mes}",)).fetchall()
        
        # Tipos mais frequentes
        tipos_frequentes = conn.execute('''
            SELECT 
                r.sigla,
                r.tipo_erro,
                t.categoria,
                COUNT(*) as total
            FROM registros_erros r
            LEFT JOIN tipos_erro t ON r.sigla = t.sigla
            WHERE strftime('%Y-%m', r.data_ocorrencia) = ?
            GROUP BY r.sigla
            ORDER BY total DESC
            LIMIT 10
        ''', (f"{ano}-{mes}",)).fetchall()
        
        # Total geral do mês
        total_mes = conn.execute('''
            SELECT COUNT(*) as total
            FROM registros_erros
            WHERE strftime('%Y-%m', data_ocorrencia) = ?
        ''', (f"{ano}-{mes}",)).fetchone()
        
        conn.close()
        
        return jsonify({
            'success': True,
            'ano': ano,
            'mes': mes,
            'total_mes': total_mes['total'] if total_mes else 0,
            'top_filiais': [dict(f) for f in top_filiais],
            'tipos_frequentes': [dict(t) for t in tipos_frequentes]
        })
        
    except Exception as e:
        print(f"Erro no resumo mensal: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

# ========== ROTA DE TESTE ==========
@app.route('/teste')
def teste():
    """Página de teste para verificar dados"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sistema de Erros - Dados Reais</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #333; }
            h2 { color: #555; margin-top: 30px; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            .container { max-width: 1200px; margin: 0 auto; }
            .btn { display: inline-block; padding: 10px 15px; margin: 5px; 
                   background: #4CAF50; color: white; text-decoration: none; 
                   border-radius: 4px; }
            .btn:hover { background: #45a049; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>✅ Sistema de Erros - Dados Reais</h1>
            <p><strong>Status:</strong> Banco de dados inicializado com dados reais</p>
            
            <h2>Links de Teste:</h2>
            <p>
                <a href="/api/filiais" class="btn">Testar Filiais (13 filiais)</a>
                <a href="/api/todos-vendedores" class="btn">Testar Vendedores (42 vendedores)</a>
                <a href="/api/tipos-erro" class="btn">Testar Tipos Erro (15 tipos reais)</a>
                <a href="/api/estatisticas" class="btn">Testar Estatísticas</a>
                <a href="/api/ultimos-registros" class="btn">Últimos Registros</a>
                <a href="/registrar" class="btn" style="background: #2196F3;">Ir para Registro</a>
                <a href="/dashboard" class="btn" style="background: #FF9800;">Ir para Dashboard</a>
            </p>
            
            <h2>Funcionalidades Implementadas:</h2>
            <ul>
                <li><strong>✅ Banco de dados REAL</strong> com todos os vendedores fornecidos</li>
                <li><strong>✅ Gerentes reais</strong> para cada filial</li>
                <li><strong>✅ Tipos de erro REAIS</strong> (15 tipos conforme tabela)</li>
                <li><strong>✅ Registro de MÚLTIPLOS erros</strong> simultâneos</li>
                <li><strong>✅ Relatórios detalhados</strong> com exportação CSV</li>
                <li><strong>✅ Dashboard completo</strong> com estatísticas</li>
                <li><strong>✅ Sistema otimizado</strong> para Render/GitHub</li>
            </ul>
            
            <h2>Categorias de Erro Implementadas:</h2>
            <ol>
                <li><strong>PROCESSOS ADMINISTRATIVOS</strong> (4 tipos)</li>
                <li><strong>PÓS-VENDAS E CLIENTE</strong> (4 tipos)</li>
                <li><strong>ESTOQUE E PROCESSOS</strong> (4 tipos)</li>
                <li><strong>COMPORTAMENTO PROFISSIONAL</strong> (3 tipos)</li>
            </ol>
            
            <p><em>Sistema pronto para produção. Todos os dados são reais e correspondem aos fornecidos.</em></p>
        </div>
    </body>
    </html>
    '''

# ========== INICIAR SERVIDOR ==========

if __name__ == '__main__':
    print("="*70)
    print("🌐 SISTEMA WEB DE REGISTRO DE ERROS - DADOS REAIS")
    print("="*70)
    print("📍 Banco inicializado com:")
    print(f"   • 13 Filiais com gerentes reais")
    print(f"   • 42 Vendedores reais")
    print(f"   • 15 Tipos de erro reais (4 categorias)")
    print("📍 Acesse: http://localhost:5000")
    print("📍 Teste: http://localhost:5000/teste")
    print("="*70)
    
    # Criar pastas necessárias
    for pasta in ['relatorios', 'backup']:
        if not os.path.exists(pasta):
            os.makedirs(pasta)
    
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)