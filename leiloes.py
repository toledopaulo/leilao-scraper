import scraper
import requests
from sty import fg, bg, ef, rs
import pandas as pd
import datetime
from io import StringIO

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

            imovel_desocupado = "OCUPADO"
            if "Imóvel desocupado" in get_descricao_detalhada:
                imovel_desocupado = "DESOCUPADO"
            
            imoveis_disponiveis_list.append({
                "Site do Leilão": "MEGA LEILÕES",
                "Link do Leilão": link_leilao_especificio.strip(),
                "Estado da Ocupação": imovel_desocupado,
                "Endereço": endereco_leilao.strip(),
                "Estado": "SP",
                "Cidade": cidade.strip(),
                "Bairro": bairro.strip(),
                "Modalidade do Leilão": tipo_leilao.strip(),
                "Tipo do Imóvel": tipo_do_imovel.strip(),
                "N° do Lote": numero_do_lote.strip(),
                "Data 1° praça": data_1_praca_formatada.strip(),
                "Valor 1° praça": valor_primeira_praca,
                "Data 2° praça": data_2_praca_formatada.strip(),
                "Valor 2° praça": valor_segunda_praca.strip(),
                "Valor avaliado do imóvel": "Sem informação",
                "Preço final do imóvel": "Sem informação" 
            })
        return imoveis_disponiveis_list

    # def download_caixa_imoveis(self, estado: str):
    #     r = requests.Session()
    #     r.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"}
    #     lista_imoveis_array = []
    #     get_imoveis_csv = r.get(f"https://venda-imoveis.caixa.gov.br/listaweb/Lista_imoveis_{estado.upper()}.csv").text
    #     df = pd.read_csv(get_imoveis_csv.split(" N°")[1])
    #     print(df.head())
    #     # data = pd.read_csv(lista_imoveis_csv.text)
    #     # print(data.head(2))
    def scrape_caixa_leiloes_v2(self, estado, cidades: list):
        r = requests.Session()
        imoveis_disponiveis_list = []
        r.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"}
        get_imoveis_csv = r.get(f"https://venda-imoveis.caixa.gov.br/listaweb/Lista_imoveis_{estado.upper()}.csv").text
        cidades_list = ["PRAIA GRANDE", "SAO VICENTE", "SANTOS"]
        df = pd.read_csv(StringIO(get_imoveis_csv), index_col=0, encoding="ISO-8859-1", on_bad_lines='skip', skiprows=2, sep=';')
        df_filtrado_pg = df[df["Cidade"].str.contains("PRAIA GRANDE")]
        df_filtrado_sv = df[df["Cidade"].str.contains("SAO VICENTE")]
        df_filtrado_santos = df[df["Cidade"].str.contains("SANTOS")]
        df_geral = pd.concat([df_filtrado_pg, df_filtrado_sv, df_filtrado_santos])
        for i in range(df_geral.shape[0]):
            link_leilao = df_geral.columns[9]
            descricao = df_geral.columns[7]
            valor_imovel = df_geral.columns[4]
            endereco = df_geral.columns[3]
            tipo_imovel = str(descricao).split(",")[0]
            tipo_venda = df_geral.columns[8]
            cidade = df_geral.columns[1]
            bairro = df_geral.columns[2]
            valor_avaliado_imovel = df_geral.columns[5]
            imoveis_disponiveis_list.append({
                "Site do Leilão": "CAIXA LEILÕES",
                "Link do Leilão": link_leilao,
                "Estado da Ocupação": "Sem informação",
                "Endereço": endereco,
                "Estado": df_geral.columns[0],
                "Cidade": cidade,
                "Bairro": bairro,
                "Modalidade do Leilão": tipo_venda,
                "Tipo do Imóvel": tipo_imovel,
                "N° do Lote": "Sem informação",
                "Data 1° praça": "Sem informação",
                "Valor 1° praça": "Sem informação",
                "Data 2° praça": "Sem informação",
                "Valor 2° praça": "Sem informação",
                "Valor avaliado do imóvel": valor_avaliado_imovel,
                "Preço final do imóvel": valor_imovel 
            })
        return imoveis_disponiveis_list


    def scrape_caixa_leiloes(self, cidade, tipo_venda):
        # Scraper só está puxando os imóveis de licitação aberta, alterar o filtro caso queira todos
        imoveis_disponiveis_list = []
        r = requests.Session()
        r.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"}
        codigo_cidade = {"praia_grande": "9717", "santos": "9827", "sao_vicente": "9869"}
        cidade_formatada = {"praia_grande": "Praia Grande", "sao_vicente": "São Vicente", "santos": "Santos"}
        codigo_venda = {"licitacao_aberta": "21", "venda_direta": "34", "venda_online": "33"}
        form_data = {
            "hdn_estado": "SP",
            "hdn_cidade": codigo_cidade[cidade],
            "hdn_bairro": "",
            "hdn_tp_venda": codigo_venda[tipo_venda],
            "hdn_tp_imovel": "Selecione",
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
        get_all_inputs = self.scrape.find_all_elements_by_element_name(html=self.scrape.get_beautifulsoup_by_html(pesquisa_imoveis.text), element_name="input")
        imoveis_id_list = []
        for form in get_all_inputs:
            if "hdnImov" in form["name"]:
                imoveis_id_list.append(form["value"])

        imoveis_id = '||'.join(imoveis_id_list)
        carregar_lista_imoveis = r.post("https://venda-imoveis.caixa.gov.br/sistema/carregaListaImoveis.asp",
            data={"hdnImov": imoveis_id}       
        )
        for imovel_id in imoveis_id.split("||"):
            try:
                link_leilao = f"https://venda-imoveis.caixa.gov.br/sistema/detalhe-imovel.asp?hdnOrigem=index&hdnimovel={imovel_id}"
                html = r.get(link_leilao).text
                get_all_spans = self.scrape.find_all_elements_by_element_name(html=self.scrape.find_specific_element_by_class(html=self.scrape.get_beautifulsoup_by_html(html), element_name="div", class_name="control-item control-span-6_12"),
                                                            element_name="span"
                                                            )
                
                get_endereco_text = self.scrape.find_all_elements_by_element_name(html=self.scrape.find_specific_element_by_class(html=self.scrape.get_beautifulsoup_by_html(html), class_name="related-box", element_name="div"), element_name="p")
                endereco = str(get_endereco_text[0].text).replace("Endereço:", "")
                bairro = str(get_endereco_text[0].text).split(" - CEP")[0].split(", ")[1]
                for i in get_all_spans:
                    if "Tipo de imóvel: " in i.text:
                        tipo_imovel = str(i.text).replace("Tipo de imóvel: ", "")
                if 'desocupado' in html.lower():
                    imovel_desocupado = True
                else:
                    imovel_desocupado = False
                imoveis_disponiveis_list.append({
                    "imovel_link": link_leilao,
                    "imovel_descricao": "",
                    "imovel_desocupado": imovel_desocupado,
                    "endereco": endereco,
                    "estado": "SP",
                    "cidade": cidade_formatada[cidade],
                    "bairro": bairro,
                    "tipo_leilao": tipo_venda,
                    "tipo_imovel": tipo_imovel,
                    "codigo_leilao": "",
                    "numero_lote": "",
                    "data_1_praca": "",
                    "valor_1_praca": "",
                    "data_2_praca": "",
                    "valor_2_praca": ""
                })
            except Exception as e:
                print(e)

        return imoveis_disponiveis_list 
        # lista_imoveis = self.scrape.find_all_elements_by_class(html=carregar_lista_imoveis.text, element_name="ul", class_name="control-group no-bullets")
        
    def scrape_frazao_leiloes(self, cidade):
        get_primeira_pagina = self.scrape.get_page_html('https://www.frazaoleiloes.com.br/lotes/busca/e/SP/todas-as-cidades?pagina=1')
        total_leiloes = self.scrape.find_specific_element_by_id(html=get_primeira_pagina, element_name="div", element_id="content_list_lote")
        print(total_leiloes)
        # for imovel in lista_imoveis:
        #     div_titulo = self.scrape.find_specific_element_by_class(html=str(imovel), 
        #                                                class_name="control-item control-span-12_12" ,
        #                                                element_name="div"
        #     )
        #     titulo = self.scrape.find_specific_element_by_class(html=str(div_titulo), element_name="font", class_name="").text
