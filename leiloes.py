import scraper
import requests
from sty import fg, bg, ef, rs

class Leiloes(object):
    def __init__(self):
        self.scrape = scraper.Scraper()
    
    def generate_megaleiloes_url(self, nome_categoria: str, nome_subcategoria: str, estado: str, cidade: str, valor_maximo = 5000000):
        url_schema = f"https://www.megaleiloes.com.br/{nome_categoria}/{nome_subcategoria}/{estado}/{cidade}?tov=igbr&valor_max={valor_maximo}&tipo%5B0%5D=1&tipo%5B1%5D=2&pagina=1"
        return url_schema
    def get_all_megaleiloes_pagelink_by_url(self, leilao_url: str):
        urls = []
        leilao_page =  self.scrape.get_page_html(url=leilao_url)
        imoveis_disponiveis_div = self.scrape.find_specific_element_by_class(
            html=self.scrape.find_specific_element_by_class(html=leilao_page, element_name="div",class_name="col-xs-12 col-sm-6"),
            element_name="div",
            class_name="summary"
        ).text
        pagina_imoveis = imoveis_disponiveis_div.split("Página ")[1]
        numero_pagina_atual = pagina_imoveis.split(" de")[0]
        total_paginas = pagina_imoveis.split(" de ")[1].replace(".", "")
        for i in range(int(total_paginas)):
            urls.append(leilao_url.replace(f"pagina={numero_pagina_atual}", f"pagina={i + 1}"))
        
        return urls
        
    def scrape_megaleiloes_page_by_url(self, leilao_url: str, imovel_count: int):
        leiloes_disponiveis = []
        tipo_do_imovel = leilao_url.split("/imoveis/")[1].split("/")[0]
        leilao_page =  self.scrape.get_page_html(url=leilao_url)
        imoveis_disponiveis_div = self.scrape.find_specific_element_by_class(
            html=leilao_page, 
            element_name="div",
            class_name="col-xs-12 col-sm-6"
        ).text
        pagina_imoveis = imoveis_disponiveis_div.split("Página ")[1]
        get_numero_pagina_atual = pagina_imoveis.split(" de")[0]
        get_total_paginas = pagina_imoveis.split(" de ")[1].replace(".", "")
        get_todos_imoveis_div = self.scrape.find_all_elements_by_class(
            html=leilao_page, 
            element_name="div", 
            class_name="col-sm-6 col-md-4 col-lg-3"
        )
        imoveis_disponiveis_list = []
        for imovel in get_todos_imoveis_div:
            imovel_count = imovel_count + 1
            link_leilao_especificio = self.scrape.find_specific_element_by_class(html=imovel, element_name="a", class_name="card-title")['href']
            html_leilao_especifico = self.scrape.get_page_html(url=link_leilao_especificio)
            # print(html_leilao_especifico)

            titulo_leilao = self.scrape.find_specific_element_by_class(
                html=imovel,
                element_name="a",
                class_name="card-title"
            ).text
            get_data_1_praca = self.scrape.find_specific_element_by_class(
                html=imovel,
                element_name="span",
                class_name="card-first-instance-date"
            ).text
            data_1_praca_formatada = get_data_1_praca.replace("1ª Praça: ", "").replace("Data: ", "")
            get_dia_1_praca = data_1_praca_formatada.split("/")[0]
            get_mes_1_praca = data_1_praca_formatada.split("/")[1]
            get_ano_1_praca = data_1_praca_formatada.split("/")[2].split(" às")[0] 
            get_hora_1_praca = data_1_praca_formatada.split("/")[2].split(" às ")[1]
            data_1_praca = f"{get_dia_1_praca}/{get_mes_1_praca}/{get_ano_1_praca}"
            get_data_2_praca = self.scrape.find_specific_element_by_class(
                html=imovel,
                element_name="span",
                class_name="card-second-instance-date"
            )
            data_2_praca = "Não possui"
            if get_data_2_praca != None:
                data_2_praca_formatada = get_data_2_praca.text.replace("2ª Praça: ", "").replace("Data: ", "")
                get_dia_2_praca = data_2_praca_formatada.split("/")[0]
                get_mes_2_praca = data_2_praca_formatada.split("/")[1]
                get_ano_2_praca = data_2_praca_formatada.split("/")[2].split(" às")[0] 
                get_hora_2_praca = data_2_praca_formatada.split("/")[2].split(" às ")[1]
                data_2_praca = f"{get_dia_2_praca}/{get_mes_2_praca}/{get_ano_2_praca}"
            endereco_leilao = self.scrape.find_specific_element_by_class(
                html=self.scrape.find_specific_element_by_class(html=html_leilao_especifico,element_name="div",class_name="locality item"),
                element_name="div",
                class_name="value"   
            ).text
            tipo_leilao = self.scrape.find_specific_element_by_class(
                html=html_leilao_especifico,
                element_name="div",
                class_name="batch-type",
            ).text
            get_leilao_praca_div = self.scrape.find_specific_element_by_class(
                html=html_leilao_especifico,
                element_name="div",
                class_name="col-xs-12 col-sm-4 col-md-3 summary-info"
            )
            get_all_auction_ids = self.scrape.find_all_elements_by_class(html=html_leilao_especifico,element_name="div",class_name="auction-id")
            codigo_leilao = self.scrape.find_specific_element_by_class(
                html=get_all_auction_ids[0],
                element_name="div",
                class_name="value"
            ).text
            codigo_lote = self.scrape.find_specific_element_by_class(
                html=get_all_auction_ids[1],
                element_name="div",
                class_name="value"
            ).text
            get_praca_valores = self.scrape.find_all_elements_by_class(
                html=get_leilao_praca_div,
                element_name="span",
                class_name="card-instance-value"
            )
            valor_primeira_praca = get_praca_valores[0].text
            valor_segunda_praca = "Não possui"
            numero_do_lote = "1"
            endereco_dividido = endereco_leilao.strip().split(", ")
            bairro = endereco_dividido[len(endereco_dividido) - 3]
            cidade = endereco_dividido[len(endereco_dividido) - 2]
            estado = endereco_dividido[len(endereco_dividido) - 1]
            get_descricao_detalhada = self.scrape.find_specific_element_by_class(
                html=html_leilao_especifico,
                element_name="div",
                class_name="tab-pane active"
            ).text
            if len(get_all_auction_ids) > 2:
                numero_do_lote = str(get_all_auction_ids[2].text).strip().replace("Lote", "").replace("Número", "")
            if len(get_praca_valores) > 1:
                valor_segunda_praca = get_praca_valores[1].text

            imovel_desocupado = False
            if "Imóvel desocupado" in get_descricao_detalhada:
                imovel_desocupado = True
            
            imoveis_disponiveis_list.append({
                "imovel_link": link_leilao_especificio,
                "imovel_descricao": titulo_leilao.strip(),
                "imovel_desocupado": imovel_desocupado,
                "endereco": endereco_leilao.strip(),
                "estado": estado,
                "cidade": cidade,
                "bairro": bairro,
                "tipo_leilao": tipo_leilao.strip(),
                "tipo_imovel": tipo_do_imovel.strip().capitalize(),
                "codigo_leilao": codigo_leilao.strip(),
                "numero_lote": numero_do_lote.strip(),
                "data_1_praca": data_1_praca.strip(),
                "valor_1_praca": valor_primeira_praca.strip(),
                "data_2_praca": data_2_praca.strip(),
                "valor_2_praca": valor_segunda_praca.strip()
            })
        print("------ LEILOES.PY -------")
        print(imoveis_disponiveis_list)
        return imoveis_disponiveis_list
    
    def scrape_caixa_leiloes(self, cidade):
        # Scraper só está puxando os imóveis de licitação aberta, alterar o filtro caso queira todos
        r = requests.Session()
        r.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"}
        codigo_cidade = {"praia_grande": "9717"}
        form_data = {
            "hdn_estado": "SP",
            "hdn_cidade": codigo_cidade[cidade],
            "hdn_bairro": "",
            "hdn_tp_venda": "21",
            "hdn_tp_imovel": "4",
            "hdn_area_util": "Selecione",
            "hdn_faixa_vlr": "Selecione",
            "hdn_quartos": "Selecione",
            "hdn_vg_garagem": "Selecione",
            "strValorSimulador": "",
            "strAceitaFGTS": "",
            "strAceitaFinanciamento": ""
        }
        pesquisa_imoveis = r.post("https://venda-imoveis.caixa.gov.br/sistema/carregaPesquisaImoveis.asp",
            data=form_data
        )
        soup = self.scrape.get_beautifulsoup_by_html(pesquisa_imoveis.text)
        get_all_inputs = self.scrape.find_all_elements_by_element_name(html=soup, element_name="input")
        imoveis_id_list = []
        for form in get_all_inputs:
            if "hdnImov" in form["name"]:
                imoveis_id_list.append(form["value"])

        imoveis_id = ''.join(imoveis_id_list)
        carregar_lista_imoveis = r.post("https://venda-imoveis.caixa.gov.br/sistema/carregaListaImoveis.asp",
            data={"hdnImov": imoveis_id}       
        )
        lista_imoveis = self.scrape.find_all_elements_by_class(html=carregar_lista_imoveis.text, class_name="control-group no-bullets")
        for imovel in lista_imoveis:
            pass
        # ) # Carregar Lista Imóveis