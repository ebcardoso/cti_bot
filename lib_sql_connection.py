import sqlite3

class LibSqlConnection:

    # Inicia a instância do Banco de Dados
    def __init__(self):
        self._db = sqlite3.connect('database.db', check_same_thread = False)
        self._sql = self._db.cursor()
        self._sql.execute("CREATE TABLE IF NOT EXISTS users(chat_id TEXT)")
        self._db.commit()

    # Armazena o chat_id dos novos usuários do bot
    def store_chat_id(self, chat_id):
        # Verifica se o usuário já está existe, cadastra se ainda não existir
        verification = self._sql.execute(f"SELECT chat_id FROM users WHERE chat_id = '{chat_id}'").fetchone()
        if verification is None:
            self._sql.execute("INSERT INTO users(chat_id) VALUES(?)", ([str(chat_id)]))
            self._db.commit()

    # Deleta o chat_id de um usuário que se desinscreveu
    def delete_chat_id(self, chat_id):
        self._sql.execute("DELETE FROM users WHERE chat_id = (?)", ([str(chat_id)]))
        self._db.commit()

    # Retorna a lista com o ID de todos os usuários cadastrados no bot
    def get_chat_id_list(self):
        list_chat_id = self._sql.execute("SELECT chat_id FROM users")
        return [row[0] for row in list_chat_id.fetchall()]
