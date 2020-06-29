# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

from tkinter import *
from tkinter import filedialog
from tkinter import ttk



#Base
root = Tk()

#Configurações da Janela
root.title("BalanceUs")
root.configure(bg="#d6eeb9")
root.resizable(0,0)
root.geometry("900x650")

#Bug Fix
global style_check
style_check = True

#Funções


def pegarArquivo(entrada):
   caminho = filedialog.askopenfilename(title="Selecione um Arquivo:", filetypes=(("arquivos excel","*.xlsx"), ("todos os arquivos", "*.*")))
   entrada.delete(0, END)
   entrada.insert(0, caminho)
   return None

def iniciar():
   #Criar Janela de Resultados
   result = Toplevel()
   result.title("BalanceUs")
   result.configure(bg="#d6eeb9")
   result.geometry("900x550")
   result.resizable(0,0)
   global style_check

   #Style
   style = ttk.Style()
   if(style_check is True):
       style.theme_create( "us", parent="alt", settings={
           "TNotebook": {"configure": {"background": "#868987"} },
           "TNotebook.Tab": {
               "configure": {"font": ('Arial', '16'), "background": "#6ab789"} }})

       style.theme_use("us")
       style_check = False

   #Abas
   resultados = ttk.Notebook(result, height=450, width=900)
   resultados.grid(row=0, column=0, columnspan=3)
   tab_unimed = Frame(resultados, bg="#d6eeb9")
   tab_cassi = Frame(resultados, bg="#d6eeb9")
   tab_unimed.grid(row=1, column=0)
   tab_cassi.grid(row=1, column=1)
   resultados.add(tab_unimed, text="Unimed")
   resultados.add(tab_cassi, text="Cassi")

   #Butões
   back_butao = Button(result, text="Voltar", command=result.destroy, bg="#6ab789", font=('Arial', 16), width=12)
   back_butao.grid(row=14, column=0, padx=10, pady=5)
   exit_butao = Button(result, text="Sair", command=root.quit, bg="#6ab789", font=('Arial', 16), width=12)
   exit_butao.grid(row=14, column=2, padx=10, pady=5)

   unimed(tab_unimed)
   cassi(tab_cassi)
   
   return None

def printPaciente(data, nome_paciente, procedimento, valor, medica):
    print("-----------------------------------------")
    print("Data: ", data,"\n")
    print("Nome do Paciente: ", nome_paciente,"\n")
    print("Procedimento: ", procedimento,"\n")
    print("Valor: ", valor,"\n")
    print("Médica: ", medica, "\n")
    print("-----------------------------------------")

def repPacienteM(data, nome_paciente, procedimento, valor, medica):
    rep = ("-----------------------------------------\n")
    rep += ("Data: %s\n" % data)
    rep += ("Nome do Paciente: %s\n" % nome_paciente)
    rep += ("Procedimento: %s\n" % procedimento)
    rep += ("Valor: %s\n" % valor)
    rep += ("Médica: %s\n" % medica)
    rep +=("-----------------------------------------\n")
    return rep

def repPaciente(data, nome_paciente, procedimento, valor):
    rep = ("-----------------------------------------\n")
    rep += ("Data: %s\n" % data)
    rep += ("Nome do Paciente: %s\n" % nome_paciente)
    rep += ("Procedimento: %s\n" % procedimento)
    rep += ("Valor: %s\n" % valor)
    rep +=("-----------------------------------------\n")
    return rep

def unimed(tab_unimed):

    #Lê os Excel e cria Database
    unimed_database = pd.read_excel(unimed_entrada.get())
    valeria_database = pd.read_excel(valeria_entrada.get())
    geruza_database = pd.read_excel(geruza_entrada.get())
    laurise_database = pd.read_excel(laurise_entrada.get())

    #Variáveis Valéria
    quantidade_exames_valeria = 0 
    valor_filmes_valeria = 0.0
    total_arrecadado_valeria = 0.0
    #------------------------------
    #Variavéis Geruza
    quantidade_exames_geruza = 0 
    valor_filmes_geruza = 0.0
    total_arrecadado_geruza = 0.0
    #-------------------------------
    #Variaveis Laurise
    quantidade_exames_laurise = 0 
    valor_filmes_laurise = 0.0
    total_arrecadado_laurise = 0.0
    #-------------------------------
    #Variáveis Erros
    erros = []
    erros_encontrados = ""
    #-------------------------------

    pacientes_confirmados = open("PacientesConfirmados-Unimed.txt", "w+")
    pacientes_confirmados.write("Lista de Pacientes Confirmados - Unimed\n")
    pacientes_error = open("PacientesError-Unimed","w+")
    pacientes_error.write("Lista de Pacientes com Erros - Unimed\n")

    #para cada procedimento em unimed
    for x in range(0, len(unimed_database)):
       
        #Pega os dados de cada procedimento
        data = unimed_database.iloc[x, 0]
        nome_paciente = unimed_database.iloc[x, 1]
        procedimento = unimed_database.iloc[x, 2]
        valor = unimed_database.iloc[x, 3]

        #Filmes
        if(procedimento == 'Filme'):

            paciente_existe_valeria = valeria_database.loc[(valeria_database["Nome do Paciente"]==nome_paciente)]
       
            paciente_existe_geruza = geruza_database.loc[(geruza_database["Nome do Paciente"]==nome_paciente)]
       
            paciente_existe_laurise = laurise_database.loc[(laurise_database["Nome do Paciente"]==nome_paciente)]

            #Filme Valéria
            if(len(paciente_existe_valeria) != 0):
               valor_filmes_valeria += valor

            #Filme Geruza
            elif(len(paciente_existe_geruza) != 0):
                valor_filmes_geruza += valor

            #Filme Laurise
            elif(len(paciente_existe_laurise) != 0):
                valor_filmes_laurise += valor

            #Error Filme
            else:
                erros.append("%s - %s - %s - %s \n" % (data, nome_paciente,procedimento,valor))
                pacientes_error.write(repPaciente(data, nome_paciente, procedimento, valor))
       # Exames
        else:
            paciente_valeria = valeria_database.loc[
                (valeria_database["Data"]==data) &
                (valeria_database["Nome do Paciente"]==nome_paciente) &
                (valeria_database["Procedimento"] == procedimento) &
                (valeria_database["Valor"] == valor )]

            paciente_geruza = geruza_database.loc[
                (geruza_database["Data"]==data) &
                (geruza_database["Nome do Paciente"]==nome_paciente) &
                (geruza_database["Procedimento"] == procedimento) &
                (geruza_database["Valor"] == valor )]

            paciente_laurise = laurise_database.loc[
                (laurise_database["Data"]==data) &
                (laurise_database["Nome do Paciente"]==nome_paciente) &
                (laurise_database["Procedimento"] == procedimento) &
                (laurise_database["Valor"] == valor )]

            #Exames Valéria
            if(len(paciente_valeria)!=0):
                quantidade_exames_valeria += 1
                total_arrecadado_valeria += valor
                printPaciente(data, nome_paciente, procedimento, valor, "Valéria")
                pacientes_confirmados.write(repPacienteM(data, nome_paciente, procedimento, valor, "Valéria"))

            #Exames Geruza
            if(len(paciente_geruza)!=0):
                quantidade_exames_geruza += 1
                total_arrecadado_geruza += valor
                printPaciente(data, nome_paciente, procedimento, valor, "Geruza")
                pacientes_confirmados.write(repPacienteM(data, nome_paciente, procedimento, valor, "Geruza"))

            #Exames Laurise
            if(len(paciente_laurise)!=0):
                quantidade_exames_laurise += 1
                total_arrecadado_laurise += valor
                printPaciente(data, nome_paciente, procedimento, valor, "Laurise")
                pacientes_confirmados.write(repPacienteM(data, nome_paciente, procedimento, valor, "Laurise"))

            #Error Exames
            if(len(paciente_valeria) == 0 and len(paciente_geruza) == 0 and len(paciente_laurise) == 0):
                erros.append("%s - %s - %s - %s \n" % (data, nome_paciente,procedimento,valor))
                pacientes_error.write(repPaciente(data, nome_paciente, procedimento, valor))

    for y in range(0, len(erros)):
        erros_encontrados += erros[y]

    pacientes_confirmados.close()
    pacientes_error.close()

    #Colocando no Result

    #Resultados Unimed Valéria
    unimed_valeria = LabelFrame(tab_unimed, text="Dra.Valéria:",font=('Arial', 18), bg="#d6eeb9")
    quantidade_exames_valeria_texto = Label(unimed_valeria, text="Quantidade de Exames Realizados: %.2f" % quantidade_exames_valeria, bg="#d6eeb9", font=('Arial', 18))
    valor_filmes_valeria_texto = Label(unimed_valeria, text="Valor Arrecadado em Filme: %.2f" % valor_filmes_valeria, bg="#d6eeb9", font=('Arial', 18))
    total_arrecadado_valeria_texto = Label(unimed_valeria, text="Total Arrecadado: %.2f" % total_arrecadado_valeria, bg="#d6eeb9", font=('Arial', 18))
    
    unimed_valeria.grid(row=2, column=0, sticky=W+E)
    quantidade_exames_valeria_texto.grid(row=3, column=0, padx=10, sticky=W)
    valor_filmes_valeria_texto.grid(row=4, column=0, padx=10, sticky=W)
    total_arrecadado_valeria_texto.grid(row=5, column=0, padx=10, sticky=W)

    #Resultados Unimed Geruza
    unimed_geruza = LabelFrame(tab_unimed, text="Dra.Geruza:",font=('Arial', 18), bg="#d6eeb9")
    quantidade_exames_geruza_texto = Label(unimed_geruza, text="Quantidade de Exames Realizados: %.2f" % quantidade_exames_geruza, bg="#d6eeb9", font=('Arial', 18))
    valor_filmes_geruza_texto = Label(unimed_geruza, text="Valor Arrecadado em Filme: %.2f" % valor_filmes_geruza, bg="#d6eeb9", font=('Arial', 18))
    total_arrecadado_geruza_texto = Label(unimed_geruza, text="Total Arrecadado: %.2f" % total_arrecadado_geruza, bg="#d6eeb9", font=('Arial', 18))
    
    unimed_geruza.grid(row=6, column=0, sticky=W+E)
    quantidade_exames_geruza_texto.grid(row=7, column=0, padx=10, sticky=W)
    valor_filmes_geruza_texto.grid(row=8, column=0, padx=10, sticky=W)
    total_arrecadado_geruza_texto.grid(row=9, column=0, padx=10, sticky=W)

    #Resultados Unimed Laurise
    unimed_laurise = LabelFrame(tab_unimed, text="Dra.Laurise:",font=('Arial', 18), bg="#d6eeb9")
    quantidade_exames_laurise_texto = Label(unimed_laurise, text="Quantidade de Exames Realizados: %.2f" % quantidade_exames_laurise, bg="#d6eeb9", font=('Arial', 18))
    valor_filmes_laurise_texto = Label(unimed_laurise, text="Valor Arrecadado em Filme: %.2f" % valor_filmes_laurise, bg="#d6eeb9", font=('Arial', 18))
    total_arrecadado_laurise_texto = Label(unimed_laurise, text="Total Arrecadado: %.2f" % total_arrecadado_laurise, bg="#d6eeb9", font=('Arial', 18))
    
    unimed_laurise.grid(row=10, column=0, sticky=W+E)
    quantidade_exames_laurise_texto.grid(row=11, column=0, padx=10, sticky=W)
    valor_filmes_laurise_texto.grid(row=12, column=0, padx=10, sticky=W)
    total_arrecadado_laurise_texto.grid(row=13, column=0, padx=10, sticky=W)

def cassi(tab_cassi):
    
    #Lê os Excel e cria Database
    cassi_database = pd.read_excel(cassi_entrada.get())
    valeria_database = pd.read_excel(valeria_entrada.get())
    geruza_database = pd.read_excel(geruza_entrada.get())
    laurise_database = pd.read_excel(laurise_entrada.get())

    #Variáveis Valéria
    quantidade_exames_valeria = 0 
    valor_filmes_valeria = 0.0
    total_arrecadado_valeria = 0.0
    #------------------------------
    #Variavéis Geruza
    quantidade_exames_geruza = 0 
    valor_filmes_geruza = 0.0
    total_arrecadado_geruza = 0.0
    #-------------------------------
    #Variaveis Laurise
    quantidade_exames_laurise = 0 
    valor_filmes_laurise = 0.0
    total_arrecadado_laurise = 0.0
    #-------------------------------
    #Variáveis Erros
    erros = []
    erros_encontrados = ""
    #-------------------------------

    pacientes_confirmados = open("PacientesConfirmados-Cassi.txt", "w+")
    pacientes_confirmados.write("Lista de Pacientes Confirmados - Cassi\n")
    pacientes_error = open("PacientesError-Cassi","w+")
    pacientes_error.write("Lista de Pacientes com Erros - \n")


#----------------------------------------------------------------------------------------------------------------------------------------------
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#----------------------------------------------------------------------------------------------------------------------------------------------

#Frames
convenios = LabelFrame(root, text="Convênios:", font=('Arial', 18), bg="#d6eeb9")
medicos = LabelFrame(root, text="Médicas:", font=('Arial', 18), bg="#d6eeb9")

#Textos
#Textos Convênios
intro_texto = Label(root, text="BalanceUs - Análise de Contas", bg="#d6eeb9", font=('Arial', 20), anchor='center')
unimed_texto = Label(convenios, text="Unimed:", bg="#d6eeb9", font=('Arial', 18))
cassi_texto = Label(convenios, text="Cassi:", bg="#d6eeb9", font=('Arial', 18))
caixa_texto = Label(convenios, text="Caixa:", bg="#d6eeb9", font=('Arial', 18))
embrapa_texto = Label(convenios, text="Embrapa:", bg="#d6eeb9", font=('Arial', 18))
afrafep_texto = Label(convenios, text="Afrafep:", bg="#d6eeb9", font=('Arial', 18))
#Textos Medicos
valeria_texto = Label(medicos, text="Valéria:", bg="#d6eeb9", font=('Arial', 18))
geruza_texto = Label(medicos, text="Geruza:", bg="#d6eeb9", font=('Arial', 18))
laurise_texto = Label(medicos, text="Laurise:", bg="#d6eeb9", font=('Arial', 18))

#Entradas
#Entradas Convênios
unimed_entrada = Entry(convenios, width=50, borderwidth=2,font=('Arial', 16))
unimed_entrada.insert(0, "Selecione o excel da Unimed...")
cassi_entrada = Entry(convenios, width=50, borderwidth=2,font=('Arial', 16))
cassi_entrada.insert(0, "Selecione o excel da Cassi...")
caixa_entrada = Entry(convenios, width=50, borderwidth=2,font=('Arial', 16))
caixa_entrada.insert(0, "Selecione o excel da Caixa...")
embrapa_entrada = Entry(convenios, width=50, borderwidth=2,font=('Arial', 16))
embrapa_entrada.insert(0, "Selecione o excel da Embrapa...")
afrafep_entrada = Entry(convenios, width=50, borderwidth=2,font=('Arial', 16))
afrafep_entrada.insert(0, "Selecione o excel da Afrafep...")
#Entradas Medicos
valeria_entrada = Entry(medicos, width=50, borderwidth=2,font=('Arial', 16))
valeria_entrada.insert(0, "Selecione o excel do Med de Valéria...")
geruza_entrada = Entry(medicos, width=50, borderwidth=2,font=('Arial', 16))
geruza_entrada.insert(0, "Selecione o excel do Med de Geruza...")
laurise_entrada = Entry(medicos, width=50, borderwidth=2,font=('Arial', 16))
laurise_entrada.insert(0, "Selecione o excel do Med de Laurise...")


#Butões
#Butões Convênios
unimed_butao= Button(convenios, text="Selecionar", command=lambda: pegarArquivo(unimed_entrada), bg="#6ab789", font=('Arial', 16), width=8)
cassi_butao= Button(convenios, text="Selecionar", command=lambda: pegarArquivo(cassi_entrada), bg="#6ab789", font=('Arial', 16), width=8)
caixa_butao= Button(convenios, text="Selecionar", command=lambda: pegarArquivo(caixa_entrada), bg="#6ab789", font=('Arial', 16), width=8)
embrapa_butao= Button(convenios, text="Selecionar", command=lambda: pegarArquivo(embrapa_entrada), bg="#6ab789", font=('Arial', 16), width=8)
afrafep_butao= Button(convenios, text="Selecionar", command=lambda: pegarArquivo(afrafep_entrada), bg="#6ab789", font=('Arial', 16), width=8)
#Butões Medicos
valeria_butao= Button(medicos, text="Selecionar", command=lambda: pegarArquivo(valeria_entrada), bg="#6ab789", font=('Arial', 16), width=8)
geruza_butao= Button(medicos, text="Selecionar", command=lambda: pegarArquivo(geruza_entrada), bg="#6ab789", font=('Arial', 16), width=8)
laurise_butao= Button(medicos, text="Selecionar", command=lambda: pegarArquivo(laurise_entrada), bg="#6ab789", font=('Arial', 16), width=8)
sair_butao = Button(root, text="Sair", command=root.quit, bg="#6ab789", font=('Arial', 16), width=12)
iniciar_butao = Button(root, text="Iniciar", command=iniciar, bg="#6ab789", font=('Arial', 16), width=12)



#Grid
intro_texto.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

convenios.grid(row=1, column=0,columnspan=3, padx=10, pady=10, ipadx=5, ipady=5)
#GRiD Unimed
unimed_texto.grid(row=2, column=0, padx=10, pady=5, sticky="w")
unimed_entrada.grid(row=2, column=1, padx=10, pady=5)
unimed_butao.grid(row=2, column=2, padx=10, pady=5)
#GRiD Cassi
cassi_texto.grid(row=3, column=0, padx=10, pady=5, sticky="w")
cassi_entrada.grid(row=3, column=1, padx=10, pady=5)
cassi_butao.grid(row=3, column=2, padx=10, pady=5)
#GRiD Caixa
caixa_texto.grid(row=4, column=0, padx=10, pady=5, sticky="w")
caixa_entrada.grid(row=4, column=1, padx=10, pady=5)
caixa_butao.grid(row=4, column=2, padx=10, pady=5)
#GRiD Embrapa
embrapa_texto.grid(row=5, column=0, padx=10, pady=5, sticky="w")
embrapa_entrada.grid(row=5, column=1, padx=10, pady=5)
embrapa_butao.grid(row=5, column=2, padx=10, pady=5)
#GRiD Afrafep
afrafep_texto.grid(row=6, column=0, padx=10, pady=5, sticky="w")
afrafep_entrada.grid(row=6, column=1, padx=10, pady=5)
afrafep_butao.grid(row=6, column=2, padx=10, pady=5)

medicos.grid(row=6, column=0,columnspan=3, padx=10, pady=10, ipadx=5, ipady=5)
#GRiD Valeria
valeria_texto.grid(row=8, column=0, padx=10, pady=5)
valeria_entrada.grid(row=8, column=1, padx=10, pady=5)
valeria_butao.grid(row=8, column=2, padx=10, pady=5)
#GRiD Geruza
geruza_texto.grid(row=9, column=0, padx=10, pady=5)
geruza_entrada.grid(row=9, column=1, padx=10, pady=5)
geruza_butao.grid(row=9, column=2, padx=10, pady=5)
#GRiD Laurise
laurise_texto.grid(row=10, column=0, padx=10, pady=5)
laurise_entrada.grid(row=10, column=1, padx=10, pady=5)
laurise_butao.grid(row=10, column=2, padx=10, pady=5)
#GRiD Butões
sair_butao.grid(row=11, column=0, padx=10, pady=10)
iniciar_butao.grid(row=11, column=2, padx=10, pady=10)



#GUI Rodando
root.mainloop()