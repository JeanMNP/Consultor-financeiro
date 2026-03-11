import dearpygui.dearpygui as dpg
import math
import csv

# Função para exportar CSV
import csv

def exportar_csv(resultado):
    salario = dpg.get_value("salario")
    comida = dpg.get_value("comida")
    despesas = dpg.get_value("despesas")
    contas = dpg.get_value("contas")
    emergencia = dpg.get_value("emergencia")
    lazer = dpg.get_value("lazer")
    fluxo_caixa = max(salario - (comida+despesas+contas+emergencia+lazer), 0)

    # Cria/abre arquivo CSV e adiciona linha
    with open("relatorio_financeiro.csv", mode="a", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=";")
        # Cabeçalho só se arquivo estiver vazio
        if file.tell() == 0:
            writer.writerow(["Salário","Comida","Despesas","Contas","Emergência","Lazer","Fluxo Caixa","Resultado"])
        writer.writerow([
            f"R$ {salario:.2f}",
            f"R$ {comida:.2f}",
            f"R$ {despesas:.2f}",
            f"R$ {contas:.2f}",
            f"R$ {emergencia:.2f}",
            f"R$ {lazer:.2f}",
            f"R$ {fluxo_caixa:.2f}",
            resultado
        ])


# Função que pergunta se quer exportar
def confirmar_exportacao(resultado):
    with dpg.window(label="Exportar CSV?", modal=True, width=300, height=150, pos=(500,300), tag="janela_exportacao"):
        dpg.add_text("Deseja exportar este resultado para CSV?")
        dpg.add_button(label="Sim", callback=lambda: [exportar_csv(resultado), dpg.delete_item("janela_exportacao")])
        dpg.add_button(label="Não", callback=lambda: dpg.delete_item("janela_exportacao"))


# Funções de cálculo
def pagar_dividas(salario, gastos, divida, taxa_juros):
    if salario <= 0:
        return "Defina um salário maior que zero para calcular."
    fluxo_caixa = salario - gastos
    if fluxo_caixa <= 0:
        return "Não há fluxo de caixa disponível."
    if divida <= 0:
        return "Nenhuma dívida informada."
    if taxa_juros > 0:
        try:
            meses = math.ceil(math.log((divida * taxa_juros / fluxo_caixa) + 1, 1 + taxa_juros))
        except ValueError:
            return "Não é possível quitar sua dívida."
        valor_cjuro = fluxo_caixa * ((1 + taxa_juros)**meses - 1) / taxa_juros
        return f"Tempo estimado: {meses} meses\nValor pago com juros: R$ {valor_cjuro:.2f}"
    else:
        meses = math.ceil(divida / fluxo_caixa)
        return f"Tempo estimado: {meses} meses"

def reduzir_gastos(salario, gastos):
    if salario <= 0:
        return "Defina um salário maior que zero para calcular."
    percentual = (gastos / salario) * 100
    if percentual <= 50:
        return f"Gasto Percentual: {percentual:.1f}%.\nÓtimo!"
    elif percentual <= 70:
        economia = gastos * 0.1
        return f"Gasto Percentual: {percentual:.1f}%.\nSugestão: reduzir R$ {economia:.2f}."
    else:
        excesso = gastos - (0.7 * salario)
        return f"Gasto Percentual: {percentual:.1f}%.\nPrecisa cortar R$ {excesso:.2f}"

def planejar_poupanca(salario, gastos, taxa_juros, meta, prazo):
    if salario <= 0:
        return "Defina um salário maior que zero para calcular."
    if prazo <= 0:
        return "Informe um prazo válido (maior que zero)."
    fluxo_caixa = salario - gastos
    if fluxo_caixa <= 0:
        return "Não há fluxo de caixa disponível."
    if meta <= 0:
        return "Informe uma meta de poupança válida."
    valor_acumulado = fluxo_caixa * ((1 + taxa_juros)**prazo - 1) / taxa_juros if taxa_juros > 0 else fluxo_caixa * prazo
    return f"Meta: R$ {meta:.2f}\nPrazo: {prazo} meses\nValor acumulado: R$ {valor_acumulado:.2f}"

# Atualiza gráfico de pizza
def atualizar_graficos(sender, app_data):
    salario = dpg.get_value("salario")
    comida = dpg.get_value("comida")
    despesas = dpg.get_value("despesas")
    contas = dpg.get_value("contas")
    emergencia = dpg.get_value("emergencia")
    lazer = dpg.get_value("lazer")

    gastos = comida + despesas + contas + emergencia + lazer
    fluxo_caixa = max(salario - gastos, 0)

    valores = [comida, despesas, contas, emergencia, lazer, fluxo_caixa]
    labels = ["Comida","Despesas","Contas","Emergência","Lazer","Fluxo Caixa"]

    dpg.configure_item("pie_series", values=valores, labels=labels)

    dpg.set_value("resultado_texto", f"Salário: R$ {salario:.2f}\nGastos totais: R$ {gastos:.2f}\nFluxo de caixa: R$ {fluxo_caixa:.2f}")

# Funções dos botões
def calcular_divida():
    salario = dpg.get_value("salario")
    gastos = sum([dpg.get_value("comida"), dpg.get_value("despesas"), dpg.get_value("contas"), dpg.get_value("emergencia"), dpg.get_value("lazer")])
    divida = dpg.get_value("divida")
    taxa = dpg.get_value("taxa")/100
    resultado = pagar_dividas(salario, gastos, divida, taxa)
    dpg.set_value("resultado_texto", resultado)
    confirmar_exportacao(resultado)

def calcular_gastos():
    salario = dpg.get_value("salario")
    gastos = sum([dpg.get_value("comida"), dpg.get_value("despesas"), dpg.get_value("contas"), dpg.get_value("emergencia"), dpg.get_value("lazer")])
    resultado = reduzir_gastos(salario, gastos)
    dpg.set_value("resultado_texto", resultado)
    confirmar_exportacao(resultado)

def calcular_poupanca():
    salario = dpg.get_value("salario")
    gastos = sum([dpg.get_value("comida"), dpg.get_value("despesas"), dpg.get_value("contas"), dpg.get_value("emergencia"), dpg.get_value("lazer")])
    taxa = dpg.get_value("taxa")/100
    meta = dpg.get_value("meta")
    prazo = dpg.get_value("prazo")
    resultado = planejar_poupanca(salario, gastos, taxa, meta, prazo)
    dpg.set_value("resultado_texto", resultado)
    confirmar_exportacao(resultado)

def ajustar_janela(sender, app_data):
    largura = dpg.get_viewport_width()
    altura = dpg.get_viewport_height()
    dpg.set_item_width("janela_principal", largura)
    dpg.set_item_height("janela_principal", altura)

# --- Interface ---
dpg.create_context()

with dpg.window(label="Consultor Financeiro",  tag="janela_principal"):


     dpg.add_input_float(label="Salário", tag="salario", default_value=0.00, format="R$ %.2f", callback=atualizar_graficos)
     dpg.add_input_float(label="Comida", tag="comida", default_value=0.00, format="R$ %.2f", callback=atualizar_graficos)
     dpg.add_input_float(label="Despesas", tag="despesas", default_value=0.00, format="R$ %.2f", callback=atualizar_graficos)
     dpg.add_input_float(label="Contas", tag="contas", default_value=0.00, format="R$ %.2f", callback=atualizar_graficos)
     dpg.add_input_float(label="Emergência", tag="emergencia", default_value=0.00, format="R$ %.2f", callback=atualizar_graficos)
     dpg.add_input_float(label="Lazer", tag="lazer", default_value=0.00, format="R$ %.2f", callback=atualizar_graficos)


     dpg.add_separator()

    # Gráfico de Pizza
     with dpg.plot(label="Gráfico de gastos", height=400, width=500):
      dpg.add_plot_axis(dpg.mvXAxis, label="x")
      dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")
      dpg.add_pie_series(0.5, 0.5, 0.8,   
                       [0,0,0,0,0,0],
                       ["Comida","Despesas","Contas","Emergência","Lazer","Fluxo Caixa"],
                       parent="y_axis",
                       tag="pie_series")


     dpg.add_separator()

     # Campos extras para dívida/poupança
     dpg.add_input_float(label="Dívida", tag="divida", default_value=0.00, format="R$ %.2f")
     dpg.add_input_float(label="Taxa de juros (%)", tag="taxa", default_value=0.00, format="%.2f%")  # aqui não precisa de R$, pois é porcentagem
     dpg.add_input_float(label="Meta Poupança", tag="meta", default_value=0.00, format="R$ %.2f")
     dpg.add_input_int(label="Prazo (meses)", tag="prazo", default_value=0)

     dpg.add_separator()

    # Botões
     dpg.add_button(label="Pagar Dívidas", callback=calcular_divida)
     dpg.add_button(label="Reduzir Gastos", callback=calcular_gastos)
     dpg.add_button(label="Criar Poupança", callback=calcular_poupanca)

     dpg.add_text("", tag="resultado_texto")


dpg.create_viewport(title="Consultor Financeiro", width=1200, height=800)
# Ativar callback quando viewport mudar
dpg.set_viewport_resize_callback(ajustar_janela)

# --- Centralizar janela ---
screen_width = dpg.get_viewport_client_width()
screen_height = dpg.get_viewport_client_height()

window_width = 1200
window_height = 800

pos_x = int((screen_width - window_width) / 2)
pos_y = int((screen_height - window_height) / 2)

dpg.set_viewport_pos([pos_x, pos_y])
# ---------------------------

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

