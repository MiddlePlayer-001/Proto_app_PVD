"""
Gerenciamento de conexão com banco de dados SQLite
"""
from pathlib import Path
from peewee import SqliteDatabase

# Caminho do banco de dados
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "loja.db"

# Criar diretório de dados se não existir
DATA_DIR.mkdir(exist_ok=True)

# Instância única do banco de dados
_db_instance = None


def get_db():
    """Retorna a instância única do banco de dados"""
    global _db_instance
    if _db_instance is None:
        _db_instance = SqliteDatabase(
            str(DB_PATH),
            pragmas={
                'journal_mode': 'wal',
                'cache_size': -1 * 64000,  # 64MB
                'foreign_keys': 1,
                'synchronous': 1,
            }
        )
    return _db_instance


def init_db():
    """Inicializa o banco de dados criando as tabelas"""
    from .models import (
        Produto, Venda, ItemVenda, Transacao, FechamentoDia
    )
    
    db = get_db()
    
    try:
        db.connect()
        db.create_tables([
            Produto,
            Venda,
            ItemVenda,
            Transacao,
            FechamentoDia
        ], safe=True)
        print("✓ Banco de dados inicializado com sucesso")
        return True
    except OSError as e:
        print(f"✗ Erro ao inicializar banco de dados: {e}")
        return False
    finally:
        db.close()
