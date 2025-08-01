from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'uma-chave-secreta-segura'  # Chave usada para proteger sessões e cookies

login_manager = LoginManager(app)  # Inicializa o Flask-Login no app Flask
login_manager.login_view = 'login'  # Define a rota de login para redirecionar usuários não autenticados

# Banco de dados temporário em memória para armazenar usuários
usuarios = {}

# Classe de usuário que o Flask-Login utiliza para gerenciar sessão
class Usuario(UserMixin):
    def __init__(self, id, nome, senha_hash):
        self.id = id  # ID do usuário, usado internamente pelo Flask-Login
        self.nome = nome  # Nome do usuário (para mostrar, por exemplo)
        self.senha_hash = senha_hash  # Senha armazenada em formato hash (não em texto)

# Função obrigatória para o Flask-Login carregar um usuário a partir do ID salvo na sessão
@login_manager.user_loader
def load_user(user_id):
    dados = usuarios.get(user_id)  # Busca usuário no "banco" pelo ID
    if dados:
        return Usuario(dados['id'], dados['nome'], dados['senha_hash'])  # Cria objeto usuário para sessão
    return None  # Retorna None se usuário não encontrado

@app.route('/')
def index():
    return render_template('index.html')  # Página inicial pública

# Rota protegida, só acessível se o usuário estiver logado
@app.route('/painel')
@login_required
def painel():
    return render_template('painel.html', nome=current_user.nome)  # Passa o nome do usuário logado para o template

# Outra rota protegida
@app.route('/conteudos')
@login_required
def conteudos():
    return render_template('conteudos.html')

@app.route('/sobre')
#@login_required
def sobre():
    return render_template('sobre.html')

# Rota para cadastro de novos usuários
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        # Captura os dados do formulário de forma segura
        email = request.form.get('email')
        senha = request.form.get('senha')
        nome = request.form.get('nome')
        data_nascimento = request.form.get('data_nascimento')

        # Verifica se algum campo está vazio
        if not email or not nome or not senha or not data_nascimento:
            flash('Por favor, preencha todos os campos.')
            return redirect(url_for('cadastro'))

        # Verifica se o usuário já existe
        if email in usuarios:
            flash('Usuário já existe! Escolha outro email.')
            return redirect(url_for('cadastro'))

        # Gera hash seguro da senha
        senha_hash = generate_password_hash(senha)

        # Salva o usuário no "banco de dados" em memória
        usuarios[email] = {
            'id': email,
            'nome': nome,
            'senha_hash': senha_hash,
            'data_nascimento': data_nascimento
        }

        flash('Cadastro realizado com sucesso! Faça login.')
        return redirect(url_for('login'))

    return render_template('cadastro.html')  

# Rota para login de usuários
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')  # email do usuário do formulário
        senha = request.form.get('senha')      # Senha digitada

        dados = usuarios.get(email)  # Busca o usuário no "banco"

        if dados and check_password_hash(dados['senha_hash'], senha):
            user = Usuario(dados['id'], dados['nome'], dados['senha_hash'])# Cria objeto usuário
            login_user(user)  # Realiza o login (cria sessão)
            flash('Login realizado com sucesso!')
            return redirect(url_for('painel'))  # Redireciona após login

        flash('Usuário ou senha incorretos.')
        return redirect(url_for('login'))

    return render_template('login.html')  # Mostra formulário de login

# Rota para logout do usuário
@app.route('/logout')
@login_required
def logout():
    logout_user()  # Remove sessão do usuário
    flash('Você saiu com sucesso.')
    return redirect(url_for('login'))  # Redireciona para a página de login

if __name__ == "__main__":
    app.run(debug=True)  