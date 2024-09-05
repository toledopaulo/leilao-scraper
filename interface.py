import customtkinter
import main
import threading

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")  

app = customtkinter.CTk()
app.wm_title("Leiloeiro")
app.geometry("500x300")

def iniciar():
  main.run_frazao_leiloes()
  # main.run_caixa_leiloes_v2()
  # main.run_megaleiloes()
  # main.gerar_planilha()


button = customtkinter.CTkButton(master=app, text="Iniciar raspagem de dados", command=lambda: threading.Thread(target=iniciar).start())
button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
bem_vindo_label = customtkinter.CTkLabel(
    master=app,
    text="Bem vindo, [usuário]",  # Texto da Label
    font=("Arial", 16, "bold"),  # Fonte Arial, tamanho 16, negrito
    fg_color="transparent",
    text_color="white"
)
tutorial_label = customtkinter.CTkLabel(
    master=app,
    text="Para obter os dados, clique no botão abaixo.",  # Texto da Label
    font=("Arial", 16, "bold"),  # Fonte Arial, tamanho 16, negrito
    fg_color="transparent",
    text_color="white"
)
# Posicionar a Label no topo da página
bem_vindo_label.pack(pady=20)  # Define uma margem superior
tutorial_label.pack(pady=40)

app.mainloop()