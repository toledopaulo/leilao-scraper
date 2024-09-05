from scraper import Scraper
import os
from sty import fg, bg, ef, rs
from leiloes import Leiloes
import excel
import sys
from windows_toasts import WindowsToaster, Toast

pyexcel = excel.Excel()
app = Leiloes()

all_imoveis_dict = []


def open_planilha_path(path):
    os.startfile(os.getcwd() + "/planilhas")
    os.startfile(os.getcwd() + path)


def run_toast_notification(path):
    toaster = WindowsToaster('Leiloeiro')
    notificacao = Toast()
    notificacao.text_fields = ['Planilha foi gerada com sucesso, clique aqui para visualizar']
    notificacao.on_activated = lambda _: open_planilha_path(path)
    toaster.show_toast(notificacao)


def gerar_planilha():
    os.system("cls")
    welcome_ascii()
    os.system("color a")
    planilha_path = pyexcel.dict_to_pandas_excel(all_imoveis_dict)
    run_toast_notification(path=planilha_path)


def welcome_ascii():
    print("""
.__         .__.__                .__               
|  |   ____ |__|  |   ____   ____ |__|______  ____  
|  | _/ __ \|  |  |  /  _ \_/ __ \|  \_  __ \/  _ \ 
|  |_\  ___/|  |  |_(  <_> )  ___/|  ||  | \(  <_> )
|____/\___  >__|____/\____/ \___  >__||__|   \____/ 
          \/                    \/                  
""")
    print()


def run_megaleiloes():
    print("[Leiloeiro] Raspagem de dados do Mega Leilões iniciada.")
    url_pg_megaleiloes = app.generate_megaleiloes_url(
        nome_categoria="imoveis",
        nome_subcategoria="apartamentos",
        estado="sp",
        cidade="praia-grande",
    )

    url_santos_megaleiloes = app.generate_megaleiloes_url(
        nome_categoria="imoveis",
        nome_subcategoria="apartamentos",
        estado="sp",
        cidade="santos",
    )

    url_saovicente_megaleiloes = app.generate_megaleiloes_url(
        nome_categoria="imoveis",
        nome_subcategoria="apartamentos",
        estado="sp",
        cidade="sao-vicente",
    )

    megaleiloes_urls_all_imoveis_pg = app.get_all_megaleiloes_pagelink_by_url(url_pg_megaleiloes)
    megaleiloes_urls_all_imoveis_santos = app.get_all_megaleiloes_pagelink_by_url(url_santos_megaleiloes)
    megaleiloes_urls_all_imoveis_sao_vicente = app.get_all_megaleiloes_pagelink_by_url(url_saovicente_megaleiloes)

    all_urls_megaleiloes = megaleiloes_urls_all_imoveis_pg + megaleiloes_urls_all_imoveis_santos + megaleiloes_urls_all_imoveis_sao_vicente

    for url in all_urls_megaleiloes:
        temp_dict = app.scrape_megaleiloes_page_by_url(leilao_url=url, imovel_count=len(all_imoveis_dict))
        all_imoveis_dict.extend(temp_dict)

    print("[Leiloeiro] Raspagem de dados do Mega Leilões finalizada!")

def run_caixa_leiloes():
    caixa_pg_dict = app.scrape_caixa_leiloes("praia_grande", "licitacao_aberta")
    caixa_santos_dict = app.scrape_caixa_leiloes("santos", "licitacao_aberta")
    caixa_sao_vicente_dict = app.scrape_caixa_leiloes("sao_vicente", "licitacao_aberta")
    caixa_pg_dict_direta = app.scrape_caixa_leiloes("praia_grande", "venda_direta")
    caixa_santos_dict_direta = app.scrape_caixa_leiloes("santos", "venda_direta")
    caixa_sao_vicente_dict_direta = app.scrape_caixa_leiloes("sao_vicente", "venda_direta")
    caixa_pg_dict_online = app.scrape_caixa_leiloes("praia_grande", "venda_online")
    caixa_santos_dict_online = app.scrape_caixa_leiloes("santos", "venda_online")
    caixa_sao_vicente_dict_online = app.scrape_caixa_leiloes("sao_vicente", "venda_online")
    all_caixa_leiloes_dict = caixa_pg_dict + caixa_santos_dict + caixa_sao_vicente_dict + caixa_pg_dict +  caixa_pg_dict_direta + caixa_santos_dict_direta + caixa_sao_vicente_dict_direta + caixa_pg_dict_online + caixa_santos_dict_online + caixa_sao_vicente_dict_online
    all_imoveis_dict.extend(all_caixa_leiloes_dict)

def run_caixa_leiloes_v2():
    print("[Leiloeiro] Raspagem de dados do Caixa Leilões iniciada.")
    leiloes = app.scrape_caixa_leiloes_v2("SP", ["PRAIA GRANDE", "SANTOS", "SAO VICENTE"])
    all_imoveis_dict.extend(leiloes)
    print("[Leiloeiro] Raspagem de dados do Caixa Leilões finalizada!")

def run_frazao_leiloes():
    leiloes = app.scrape_frazao_leiloes("praia_grande")
    all_imoveis_dict.extend(leiloes)

def iniciar():
    run_caixa_leiloes_v2()
    run_megaleiloes()
    gerar_planilha()

# if __name__ in "__main__":
#     os.system("title Leiloeiro - Leilões da Baixada Santista && color f &&cls")
#     welcome_ascii()
#     resposta_gerar_planilha = str(input("[Leiloeiro] Gerar planilha? (S/N): "))
#     if resposta_gerar_planilha.upper() == "S":
#         iniciar()
#     else:
#         sys.exit()
