#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import glob
import shutil

os.chdir(r'c:\Users\Usuario\Downloads\aplicativo\pdv_system')

# Listar o que está lá
items = glob.glob('tmpclaude-*-cwd')
print(f"Encontrados {len(items)} arquivos temporarios")

# Remover um por um
removed = 0
failed = 0

for item in items:
    try:
        path = os.path.abspath(item)
        if os.path.isfile(path):
            os.remove(path)
            removed += 1
        elif os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=True)
            removed += 1
        print(f"[OK] Removido: {item}")
    except Exception as e:
        print(f"[ERRO] {item}: {e}")
        failed += 1

print(f"\nResultado: {removed} removidos, {failed} falhados")
