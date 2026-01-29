# app.py - SISTEMA COMPLETO COM EXPORTAÇÃO CSV FUNCIONANDO
from flask import Flask, render_template, request, jsonify, send_file, session, Response
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os
import csv
import json
import io

app = Flask(__name__)
app.secret_key = 'sistema_erros_2024_seguro'
CORS(app)

# ========== FILTRO DATE ==========
@app.template_filter('date')
def format_date(value, format='%Y-%m-%d'):
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

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# ========== CONFIGURAÇÕES ==========
DATABASE = 'erros_filiais.db'

def init_database():
    """Inicializa o banco de dados"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Tabelas
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
                filial TEXT NOT NULL
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
                registrado_por TEXT DEFAULT "Sistema Web",
                data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Dados das filiais
        filiais = [
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
        
        cursor.executemany('INSERT OR IGNORE INTO filiais (codigo, nome, gerente) VALUES (?, ?, ?)', filiais)
        
        # Vendedores
        vendedores = [
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
        
        cursor.executemany('INSERT OR IGNORE INTO vendedores (nome_completo, filial) VALUES (?, ?)', vendedores)
        
        # Tipos de erro
        tipos = [
            ("PROCESSOS ADMINISTRATIVOS", "Não atualizar cadastro de cliente", "CAD", "-3% por caso"),
            ("PROCESSOS ADMINISTRATIVOS", "Falha no registro de ponto", "PTO", "-2% por dia"),
            ("PROCESSOS ADMINISTRATIVOS", "Uniforme incorreto", "UNF", "-3% por dia"),
            ("PROCESSOS ADMINISTRATIVOS", "Não concluir tarefas/Procrastinação", "TAR", "-2% por ocorrência"),
            ("PÓS-VENDAS E CLIENTE", "Falta de acompanhamento - pós-venda", "PVD", "-3% por cliente"),
            ("PÓS-VENDAS E CLIENTE", "Não comunicar OS/Assistência Técnica em caso de defeito", "OSS", "-3% por ocorrência"),
            ("PÓS-VENDAS E CLIENTE", "Reclamar de comissão na frente de cliente", "COM", "-5% por ocorrência"),
            ("PÓS-VENDAS E CLIENTE", "Não prestar apoio com recebimento", "REC", "-3% por caso"),
            ("ESTOQUE E PROCESSOS", "Venda para terceiros sem comunicação", "V3S", "-8% por caso"),
            ("ESTOQUE E PROCESSOS", "Erro de etiquetagem/precificação", "ETQ", "-4% por divergência"),
            ("ESTOQUE E PROCESSOS", "Lançar venda do CD e entregar da loja", "CDL", "-4% por ocorrência"),
            ("ESTOQUE E PROCESSOS", "Prometer brindes/condições não autorizadas", "BRI", "-4% por caso"),
            ("COMPORTAMENTO PROFISSIONAL", "Não resolver problemas simples", "ATD", "-3% por ocorrência"),
            ("COMPORTAMENTO PROFISSIONAL", "Não ajudar na organização da loja", "ORG", "-3% por dia"),
            ("COMPORTAMENTO PROFISSIONAL", "Não participar da montagem da frente de loja até 09h00", "FDL", "-2% por dia")
        ]
        
        cursor.executemany('INSERT OR IGNORE INTO tipos_erro (categoria, criterio, sigla, penalizacao) VALUES (?, ?, ?, ?)', tipos)
        
        conn.commit()
        conn.close()
        print("✅ Banco de dados inicializado com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Inicializar banco
init_database()

# ========== ROTAS PRINCIPAIS ==========
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar')
def registrar():
    return render_template('registrar.html')

@app.route('/relatorios')
def relatorios():
    return render_template('relatorios.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# ========== APIs ==========
@app.route('/api/filiais')
def get_filiais():
    try:
        conn = get_db_connection()
        filiais = conn.execute('SELECT codigo, nome, gerente FROM filiais ORDER BY codigo').fetchall()
        conn.close()
        return jsonify([dict(f) for f in filiais])
    except:
        return jsonify([])

@app.route('/api/vendedores/<filial>')
def get_vendedores(filial):
    try:
        conn = get_db_connection()
        vendedores = conn.execute('SELECT nome_completo FROM vendedores WHERE filial = ? ORDER BY nome_completo', (filial,)).fetchall()
        conn.close()
        return jsonify([dict(v) for v in vendedores])
    except:
        return jsonify([])

@app.route('/api/todos-vendedores')
def get_todos_vendedores():
    try:
        conn = get_db_connection()
        vendedores = conn.execute('SELECT nome_completo, filial FROM vendedores ORDER BY nome_completo').fetchall()
        conn.close()
        return jsonify([dict(v) for v in vendedores])
    except:
        return jsonify([])

@app.route('/api/tipos-erro')
def get_tipos_erro():
    try:
        conn = get_db_connection()
        tipos = conn.execute('SELECT categoria, criterio, sigla, penalizacao FROM tipos_erro ORDER BY categoria').fetchall()
        conn.close()
        return jsonify([dict(t) for t in tipos])
    except:
        return jsonify([])

@app.route('/api/categorias-erro')
def get_categorias_erro():
    try:
        conn = get_db_connection()
        categorias = conn.execute('SELECT DISTINCT categoria FROM tipos_erro ORDER BY categoria').fetchall()
        conn.close()
        return jsonify([c['categoria'] for c in categorias])
    except:
        return jsonify([])

@app.route('/api/ultimos-registros')
def get_ultimos_registros():
    try:
        conn = get_db_connection()
        registros = conn.execute('''
            SELECT r.*, f.gerente, f.nome as nome_filial 
            FROM registros_erros r
            LEFT JOIN filiais f ON r.filial = f.codigo
            ORDER BY r.data_registro DESC LIMIT 10
        ''').fetchall()
        conn.close()
        return jsonify([dict(r) for r in registros])
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify([])

@app.route('/api/estatisticas')
def get_estatisticas():
    try:
        conn = get_db_connection()
        
        total = conn.execute('SELECT COUNT(*) FROM registros_erros').fetchone()[0]
        
        hoje = datetime.now().strftime('%Y-%m-%d')
        hoje_count = conn.execute('SELECT COUNT(*) FROM registros_erros WHERE DATE(data_registro) = ?', (hoje,)).fetchone()[0]
        
        por_filial = conn.execute('''
            SELECT r.filial, COUNT(*) as total, f.gerente
            FROM registros_erros r
            LEFT JOIN filiais f ON r.filial = f.codigo
            GROUP BY r.filial ORDER BY total DESC
        ''').fetchall()
        
        top_vendedores = conn.execute('''
            SELECT vendedor, COUNT(*) as total_erros
            FROM registros_erros
            GROUP BY vendedor
            ORDER BY total_erros DESC LIMIT 5
        ''').fetchall()
        
        por_categoria = conn.execute('''
            SELECT t.categoria, COUNT(*) as total
            FROM registros_erros r
            LEFT JOIN tipos_erro t ON r.sigla = t.sigla
            GROUP BY t.categoria ORDER BY total DESC
        ''').fetchall()
        
        conn.close()
        
        return jsonify({
            'total_registros': total,
            'registros_hoje': hoje_count,
            'por_filial': [dict(f) for f in por_filial],
            'top_vendedores': [dict(v) for v in top_vendedores],
            'por_categoria': [dict(c) for c in por_categoria],
            'status': 'ativo'
        })
        
    except:
        return jsonify({'total_registros': 0, 'registros_hoje': 0, 'status': 'offline'})

# ========== API DE RELATÓRIOS - FUNCIONANDO ==========
@app.route('/api/relatorio', methods=['POST'])
def gerar_relatorio():
    """API principal para buscar relatórios"""
    try:
        dados = request.json
        print(f"📊 API Relatório recebeu: {dados}")
        
        conn = get_db_connection()
        
        query = '''
            SELECT 
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
                f.nome as nome_filial,
                t.categoria
            FROM registros_erros r
            LEFT JOIN filiais f ON r.filial = f.codigo
            LEFT JOIN tipos_erro t ON r.sigla = t.sigla
            WHERE 1=1
        '''
        params = []
        
        if dados.get('filial'):
            query += ' AND r.filial = ?'
            params.append(dados['filial'])
            print(f"   Filial filtro: {dados['filial']}")
        
        if dados.get('data_inicio'):
            query += ' AND r.data_ocorrencia >= ?'
            params.append(dados['data_inicio'])
            print(f"   Data início: {dados['data_inicio']}")
        
        if dados.get('data_fim'):
            query += ' AND r.data_ocorrencia <= ?'
            params.append(dados['data_fim'])
            print(f"   Data fim: {dados['data_fim']}")
        
        query += ' ORDER BY r.data_ocorrencia DESC'
        
        print(f"   Query final: {query}")
        print(f"   Parâmetros: {params}")
        
        registros = conn.execute(query, params).fetchall()
        conn.close()
        
        registros_dict = [dict(r) for r in registros]
        print(f"   ✅ {len(registros_dict)} registros encontrados")
        
        # Verificar primeiro registro
        if registros_dict:
            print(f"   Primeiro registro: {registros_dict[0]}")
        
        return jsonify({
            'success': True,
            'message': f'Encontrados {len(registros_dict)} registros',
            'total_registros': len(registros_dict),
            'registros': registros_dict
        })
        
    except Exception as e:
        print(f"❌ Erro na API relatório: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/gerar-csv', methods=['POST'])
def gerar_csv():
    """API para gerar e baixar CSV"""
    try:
        dados = request.json
        print(f"📥 CSV solicitado com filtros: {dados}")
        
        conn = get_db_connection()
        
        query = '''
            SELECT 
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
                f.nome as nome_filial,
                t.categoria
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
        
        query += ' ORDER BY r.data_ocorrencia DESC'
        
        registros = conn.execute(query, params).fetchall()
        conn.close()
        
        if not registros:
            return jsonify({'success': False, 'message': 'Nenhum registro encontrado'}), 404
        
        # Criar CSV em memória
        output = io.StringIO()
        writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_ALL)
        
        # Cabeçalho
        writer.writerow([
            'Data Ocorrência', 'Filial', 'Gerente', 'Vendedor',
            'Categoria', 'Tipo Erro', 'Sigla', 'Penalização',
            'Quantidade', 'Observações', 'Registrado Por', 'Data Registro'
        ])
        
        # Dados
        for reg in registros:
            writer.writerow([
                reg['data_ocorrencia'],
                reg['filial'],
                reg['gerente'],
                reg['vendedor'],
                reg['categoria'],
                reg['tipo_erro'],
                reg['sigla'],
                reg['penalizacao'],
                reg['quantidade'],
                reg['observacoes'],
                reg['registrado_por'],
                reg['data_registro']
            ])
        
        output.seek(0)
        
        # Criar resposta
        filename = f"relatorio_erros_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )
        
    except Exception as e:
        print(f"❌ Erro ao gerar CSV: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/teste')
def teste():
    return jsonify({
        'status': 'online',
        'mensagem': 'Sistema funcionando!',
        'hora': datetime.now().isoformat()
    })

# ========== INICIAR SERVIDOR ==========
if __name__ == '__main__':
    print("="*70)
    print("🚀 SISTEMA DE ERROS - VERSÃO COMPLETA")
    print("="*70)
    print("✅ Banco inicializado")
    print("✅ APIs configuradas")
    print("✅ Exportação CSV pronta")
    print("="*70)
    
    # Criar pastas necessárias
    for pasta in ['relatorios', 'backup']:
        if not os.path.exists(pasta):
            os.makedirs(pasta)
    
    port = int(os.environ.get('PORT', 5000))
    print(f"🌐 Servidor iniciando na porta: {port}")
    print(f"📍 Acesse: http://localhost:{port}")
    print("="*70)
    
    app.run(debug=False, host='0.0.0.0', port=port)
