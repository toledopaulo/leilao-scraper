import openpyxl
import datetime
from openpyxl.styles import Color, PatternFill, Font, Border
from openpyxl.styles import colors
from openpyxl.cell import Cell

class Excel(object):
    def __init__(self):
        return
    
    def dict_to_excel(self, dictionary: dict):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Apartamentos'
        hyperlink_font = Font(underline="single", color="0808FF")
        blueFill = PatternFill(start_color='0000FF',
                   end_color='0000FF',
                   fill_type='solid')
        ws['A1'].fill = blueFill
        ws['B1'].fill = blueFill
        ws['C1'].fill = blueFill
        ws['D1'].fill = blueFill
        ws['E1'].fill = blueFill
        ws['F1'].fill = blueFill
        ws['G1'].fill = blueFill
        ws['H1'].fill = blueFill
        ws['I1'].fill = blueFill
        ws['J1'].fill = blueFill
        ws['K1'].fill = blueFill
        ws['L1'].fill = blueFill
        ws['M1'].fill = blueFill
        ws['N1'].fill = blueFill

        ws['A1'] = "Link Imóvel"
        ws['B1'] = "Descrição Imóvel"
        ws['C1'] = "Imóvel Desocupado"
        ws['D1'] = "Endereço"
        ws['E1'] = "Estado"
        ws['F1'] = "Cidade"
        ws['G1'] = "Bairro"
        ws['H1'] = "Tipo do Leilão"
        ws['I1'] = "Tipo do Imóvel"
        ws['J1'] = "Data 1° praça"
        ws['K1'] = "Valor 1° praça"
        ws['L1'] = "Data 2° praça"
        ws['M1'] = "Valor 2° praça"
        ws['N1'] = "Número do Lote"

        for imovel in dictionary:
            imovel_desocupado = ""
            if dictionary[imovel]["imovel_desocupado"] == 0:
                imovel_desocupado = "Sim"
            else:
                imovel_desocupado = "Não"
            ws['A' + str(imovel + 1)].hyperlink = dictionary[imovel]["imovel_link"]
            ws['B' + str(imovel + 1)] = dictionary[imovel]["imovel_descricao"]
            ws['C' + str(imovel + 1)] = imovel_desocupado
            ws['D' + str(imovel + 1)] = dictionary[imovel]["endereco"]
            ws['E' + str(imovel + 1)] = dictionary[imovel]["estado"]
            ws['F' + str(imovel + 1)] = dictionary[imovel]["cidade"]
            ws['G' + str(imovel + 1)] = dictionary[imovel]["bairro"]
            ws['H' + str(imovel + 1)] = dictionary[imovel]["tipo_leilao"]
            ws['I' + str(imovel + 1)] = dictionary[imovel]["tipo_imovel"]
            ws['J' + str(imovel + 1)] = dictionary[imovel]["data_1_praca"]
            ws['K' + str(imovel + 1)] = dictionary[imovel]["valor_1_praca"]
            ws['L' + str(imovel + 1)] = dictionary[imovel]["data_2_praca"]
            ws['M' + str(imovel + 1)] = dictionary[imovel]["valor_2_praca"]
            ws['N' + str(imovel + 1)] = dictionary[imovel]["numero_lote"]
        
        for cell in ws['A']:
            if cell.value != "Link Imóvel":
                cell.font = hyperlink_font
        for cell in ws['J']:
            if cell.value != "Data 1° praça":
                cell.number_format = "DD/MM/YYYY"
        for cell in ws['L']:
            if cell.value != "Data 2° praça":
                cell.number_format = "DD/MM/YYYY"
        dia_atual = str(datetime.datetime.today()).split(".")[0].replace(":", "-")
        planilha_path = "/planilhas/leiloes-" + str(dia_atual) + ".xlsx"
        wb.save("./" + planilha_path)
        return planilha_path