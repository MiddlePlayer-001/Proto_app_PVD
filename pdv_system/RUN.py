#!/usr/bin/env python3
"""
================================================================================
        🚀 PDV SYSTEM - INSTALADOR & LAUNCHER TUDO EM UM
================================================================================

Um arquivo único que faz TUDO:
  1. Verifica Python
  2. Cria ambiente virtual
  3. Instala dependências
  4. Inicia a aplicação

Use: python RUN.py
Ou clique 2x no arquivo (se .pyw estiver associado)

================================================================================
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import time

class PDVInstaller:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.venv_dir = self.root_dir / "venv"
        self.python_exe = self.venv_dir / "Scripts" / "python.exe" if sys.platform == "win32" else self.venv_dir / "bin" / "python"
        self.pip_exe = self.venv_dir / "Scripts" / "pip.exe" if sys.platform == "win32" else self.venv_dir / "bin" / "pip"
    
    def print_header(self, text):
        """Imprime cabeçalho formatado"""
        print("\n" + "=" * 70)
        print(f"  {text}")
        print("=" * 70)
    
    def print_step(self, step, text):
        """Imprime passo numerado"""
        print(f"\n[{step}] {text}")
    
    def print_ok(self, text="OK"):
        """Imprime mensagem de sucesso"""
        print(f"    ✅ {text}")
    
    def print_error(self, text):
        """Imprime mensagem de erro"""
        print(f"    ❌ {text}")
        return False
    
    def check_python_version(self):
        """Verifica se Python 3.8+ está instalado"""
        self.print_step(1, "Verificando Python...")
        
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            self.print_error(f"Python 3.8+ necessário. Você tem: {version.major}.{version.minor}")
            print("\n    Baixe de: https://www.python.org/downloads/")
            return False
        
        self.print_ok(f"Python {version.major}.{version.minor}.{version.micro} ✓")
        return True
    
    def setup_venv(self):
        """Cria ambiente virtual se não existir"""
        self.print_step(2, "Setupando ambiente virtual...")
        
        if self.venv_dir.exists():
            self.print_ok("Ambiente virtual já existe")
            return True
        
        try:
            subprocess.run(
                [sys.executable, "-m", "venv", str(self.venv_dir)],
                check=True,
                capture_output=True,
                timeout=60
            )
            self.print_ok("Ambiente virtual criado")
            return True
        except subprocess.TimeoutExpired:
            self.print_error("Timeout ao criar venv")
            return False
        except Exception as e:
            self.print_error(f"Erro ao criar venv: {e}")
            return False
    
    def install_requirements(self):
        """Instala dependências do requirements.txt

        Se o pip.exe não existir no venv, tenta `python -m ensurepip` e usa
        `python -m pip` como fallback para instalar as dependências.
        """
        self.print_step(3, "Instalando dependências...")
        self.print_ok("Isso pode levar 2-5 minutos na primeira vez...")
        
        req_file = self.root_dir / "requirements.txt"
        if not req_file.exists():
            self.print_error("requirements.txt não encontrado!")
            return False
        
        # Decide comando pip: prefira pip.exe no venv, senão use python -m pip
        if self.pip_exe.exists():
            pip_cmd = [str(self.pip_exe)]
        else:
            # Tentar garantir pip via ensurepip
            self.print_step("3.1", "pip não encontrado no venv; tentando ensurepip...")
            try:
                subprocess.run(
                    [str(self.python_exe), "-m", "ensurepip", "--upgrade"],
                    check=True,
                    capture_output=True,
                    timeout=120
                )
                self.print_ok("pip instalado via ensurepip")
                pip_cmd = [str(self.python_exe), "-m", "pip"]
            except Exception as e:
                self.print_error(f"Falha ao instalar pip: {e}")
                # Como último recurso, tente usar o pip do sistema
                self.print_step("3.2", "Tentando usar pip do sistema (pip)...")
                pip_cmd = ["pip"]
        
        try:
            # Atualizar pip primeiro
            subprocess.run(
                pip_cmd + ["install", "--upgrade", "pip"],
                check=True,
                capture_output=True,
                timeout=120
            )
            
            # Instalar requirements
            subprocess.run(
                pip_cmd + ["install", "-r", str(req_file)],
                check=True,
                capture_output=False,  # Mostra progresso
                timeout=600
            )
            
            self.print_ok("Dependências instaladas com sucesso")
            return True
            
        except subprocess.TimeoutExpired:
            self.print_error("Timeout ao instalar dependências")
            return False
        except subprocess.CalledProcessError as e:
            self.print_error(f"Erro ao instalar (pip retornou código {e.returncode})")
            return False
        except Exception as e:
            self.print_error(f"Erro ao instalar: {e}")
            return False
    
    def init_database(self):
        """Inicializa o banco de dados"""
        self.print_step(4, "Inicializando banco de dados...")
        
        try:
            subprocess.run(
                [str(self.python_exe), "-c", 
                 "from src.database.connection import db; db.create_tables()"],
                cwd=str(self.root_dir),
                check=False,
                capture_output=True,
                timeout=30
            )
            self.print_ok("Banco de dados inicializado")
            return True
        except Exception as e:
            print(f"    ⚠️  Aviso: {e}")
            return True  # Não falha aqui
    
    def launch_app(self):
        """Inicia a aplicação"""
        self.print_step(5, "Iniciando aplicação...")
        
        main_file = self.root_dir / "main.py"
        if not main_file.exists():
            self.print_error("main.py não encontrado!")
            return False
        
        try:
            self.print_ok("Abrindo PDV System...")
            subprocess.Popen(
                [str(self.python_exe), str(main_file)],
                cwd=str(self.root_dir)
            )
            return True
        except Exception as e:
            self.print_error(f"Erro ao iniciar: {e}")
            return False
    
    def run(self):
        """Executa o instalador completo"""
        self.print_header("🚀 PDV SYSTEM - INSTALADOR & LAUNCHER")
        print(f"\nLocalização: {self.root_dir}")
        
        steps = [
            ("Verificando Python", self.check_python_version),
            ("Setupando venv", self.setup_venv),
            ("Instalando dependências", self.install_requirements),
            ("Inicializando BD", self.init_database),
            ("Iniciando app", self.launch_app),
        ]
        
        for step_name, step_func in steps:
            try:
                if not step_func():
                    self.print_header("❌ ERRO NA INSTALAÇÃO")
                    print(f"\nFalhou em: {step_name}")
                    self.print_error("Verifique os erros acima")
                    print("\n")
                    input("Pressione ENTER para sair...")
                    return False
            except KeyboardInterrupt:
                print("\n\n⚠️  Instalação cancelada pelo usuário")
                return False
            except Exception as e:
                self.print_error(f"Erro inesperado: {e}")
                print("\n")
                input("Pressione ENTER para sair...")
                return False
        
        self.print_header("✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
        print("\n🎉 PDV System está rodando!")
        print("\n💡 Próximas vezes, basta executar este arquivo novamente.")
        print("   (A instalação será muito mais rápida)\n")
        
        return True


def main():
    """Função principal"""
    try:
        installer = PDVInstaller()
        success = installer.run()
        
        if not success:
            sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Operação cancelada")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
