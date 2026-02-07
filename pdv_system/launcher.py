#!/usr/bin/env python3
"""
Launcher para o PDV System
Inicia a aplicação principal com tratamento de erros
"""
import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

try:
    # Importa e executa a aplicação principal
    from src.ui.main_app import main
    
    if __name__ == '__main__':
        main()
        
except ImportError as e:
    print(f"❌ ERRO: Módulo não encontrado: {e}")
    print("\nTente instalar as dependências:")
    print("  pip install -r requirements.txt")
    input("\nPressione ENTER para sair...")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ ERRO ao iniciar aplicação: {e}")
    import traceback
    traceback.print_exc()
    input("\nPressione ENTER para sair...")
    sys.exit(1)
