"""
Aplicação principal com Flet
"""
import flet as ft
from src.ui.styles import AppTheme
from src.ui.pdv_view import PDVView


def main():
    """Função principal da aplicação Flet"""
    
    def app_main(page: ft.Page):
        """Função interna que recebe a página do Flet"""
        
        page.title = "PDV - Sistema de Vendas"
        page.theme_mode = ft.ThemeMode.DARK
        page.bgcolor = AppTheme.BACKGROUND
        
        def route_change(_route):
            # Limpar e adicionar nova view
            page.clean()
            
            # Log para debug
            try:
                from src.utils.logger import log_info
                log_info(f"Mudando rota: {page.route}")
            except Exception:
                pass
            
            if page.route == "/":
                page.add(home_view())
            elif page.route == "/produtos":
                page.add(produtos_view())
            elif page.route == "/vendas":
                page.add(vendas_view())
            elif page.route == "/financeiro":
                page.add(financeiro_view())
            elif page.route == "/relatorios":
                page.add(relatorios_view())
            # Forçar atualização da página para garantir renderização
            try:
                page.update()
            except Exception:
                pass

        def create_menu_button(text: str, route: str):
            """Cria um botão de menu"""
            return ft.ElevatedButton(
                content=ft.Text(text, size=16),
                width=300,
                height=AppTheme.BUTTON_HEIGHT_LARGE,
                on_click=lambda _: page.go(route),
                style=ft.ButtonStyle(
                    bgcolor={ft.MaterialState.DEFAULT: AppTheme.PRIMARY},
                    color={ft.MaterialState.DEFAULT: AppTheme.TEXT_PRIMARY},
                ),
            )

        def home_view():
            """Página inicial do PDV"""
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.AppBar(
                            title=ft.Text("PDV - Sistema de Vendas", size=24, weight="bold"),
                            center_title=True,
                            bgcolor=AppTheme.PRIMARY,
                        ),
                        ft.Container(height=20),
                        # Banner de debug visual para garantir renderização (visível em tema escuro)
                        ft.Container(
                            content=ft.Text("DEBUG: Home carregada - se não vir os botões, contate o suporte", size=14, weight="bold", color="#000000"),
                            bgcolor="#FFEB3B",
                            padding=10,
                            border_radius=6,
                        ),
                        ft.Container(height=10),
                        ft.Text("Bem-vindo ao Sistema de PDV", size=28, weight="bold"),
                        ft.Container(height=10),
                        ft.Text("Selecione uma opção no menu:", size=14, color=AppTheme.TEXT_SECONDARY),
                        ft.Container(height=30),
                        create_menu_button("📦 Produtos", "/produtos"),
                        create_menu_button("💳 Vendas/PDV", "/vendas"),
                        create_menu_button("💰 Financeiro", "/financeiro"),
                        create_menu_button("📊 Relatórios", "/relatorios"),
                    ],
                    spacing=10,
                    padding=20,
                ),
                bgcolor=AppTheme.BACKGROUND,
                expand=True,
            )

        def produtos_view():
            """Página de gerenciamento de produtos"""
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.AppBar(
                            title=ft.Text("Produtos"),
                            bgcolor=AppTheme.PRIMARY,
                        ),
                        ft.Container(
                            content=ft.Text("Módulo de Produtos (em desenvolvimento)", size=16),
                            padding=20,
                        ),
                        ft.ElevatedButton(
                            "← Voltar",
                            on_click=lambda _: page.go("/"),
                            style=ft.ButtonStyle(
                                bgcolor={ft.MaterialState.DEFAULT: "#1f77d2"},
                            ),
                        ),
                    ],
                    padding=20,
                ),
                bgcolor=AppTheme.BACKGROUND,
                expand=True,
            )

        def vendas_view():
            """Página de vendas/PDV com interface completa"""
            pdv = PDVView(page)
            return pdv.criar_interface()

        def financeiro_view():
            """Página financeira"""
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.AppBar(
                            title=ft.Text("Financeiro"),
                            bgcolor=AppTheme.PRIMARY,
                        ),
                        ft.Container(
                            content=ft.Text("Módulo Financeiro (em desenvolvimento)", size=16),
                            padding=20,
                        ),
                        ft.ElevatedButton(
                            "← Voltar",
                            on_click=lambda _: page.go("/"),
                            style=ft.ButtonStyle(
                                bgcolor={ft.MaterialState.DEFAULT: "#1f77d2"},
                            ),
                        ),
                    ],
                    padding=20,
                ),
                bgcolor=AppTheme.BACKGROUND,
                expand=True,
            )

        def relatorios_view():
            """Página de relatórios"""
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.AppBar(
                            title=ft.Text("Relatórios"),
                            bgcolor=AppTheme.PRIMARY,
                        ),
                        ft.Container(
                            content=ft.Text("Módulo de Relatórios (em desenvolvimento)", size=16),
                            padding=20,
                        ),
                        ft.ElevatedButton(
                            "← Voltar",
                            on_click=lambda _: page.go("/"),
                            style=ft.ButtonStyle(
                                bgcolor={ft.MaterialState.DEFAULT: "#1f77d2"},
                            ),
                        ),
                    ],
                    padding=20,
                ),
                bgcolor=AppTheme.BACKGROUND,
                expand=True,
            )

        # Configurar rotas
        page.on_route_change = route_change
        page.go("/")
    
    # Executar aplicação Flet
    ft.app(target=app_main)


if __name__ == "__main__":
    main()
