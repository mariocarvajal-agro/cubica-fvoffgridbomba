import streamlit as st
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# Función para calcular rieles
def calcular_riel_montaje(n_paneles, ancho_panel, largo_riel):
    riel_montaje = (n_paneles * ancho_panel) + ((n_paneles + 1) * 0.025)
    sobrante = riel_montaje % largo_riel
    riel_adicional = 1 if sobrante * 2 < largo_riel / 2 else 2
    total_rieles = int((riel_montaje // largo_riel) * 2 + riel_adicional)
    return total_rieles, riel_montaje

# Función para generar lista
def generar_lista_compra(p):
    n_riel_montaje, riel_montaje = calcular_riel_montaje(p["N_panel"], p["ancho_panel"], p["l_rielmontaje"])
    cable_solar = riel_montaje + p["dis_caseta_panel"] + 3
    cable_verde = 5 + 2
    trozo_20 = p["N_panel"] + 3
    tor_hex = trozo_20 * 2
    abraza_met20 = cable_verde / 0.5
    diametro_cable = p["dia_cable_solar"]

    return {
        "Paneles solares": p["N_panel"],
        "Rieles de montaje (4.2 m)": n_riel_montaje,
        "Abrazaderas intermedias": (p["N_panel"] * 2) - 2,
        "Abrazaderas finales": 4,
        "Soportes tipo L": p["Arco_estructura"] * 2,
        "Par de Conectores MC4": 2,
        f"Cable solar negro ø {diametro_cable} (m)": round(cable_solar),
        f"Cable solar rojo ø {diametro_cable} (m)": round(cable_solar - riel_montaje),
        "Amarras plásticas de 15 cms app": round(riel_montaje),
        f"Prensas estopa para cable solar N° {diametro_cable}": 2,
        "Tablero exterior 5 circuitos": 1,
        "Porta fusibles": 2,
        "Fusibles 15A CC": 2,
        "Prensa para barra de puesta a tierra": p["sis_puesta_tierra"],
        "Barra copper de 1.5 m": p["sis_puesta_tierra"],
        "Cámara de registro 160mm": p["sis_puesta_tierra"],
        f"Cable verde ø {diametro_cable} puesta a tierra (m)": cable_verde,
        "Tubo metálico corrugado 20 mm (m)": cable_verde,
        "Abrazaderas metálicas cady 20 mm": int(abraza_met20 * 0.5),
        "Terminal de tubo metálico flexible de 20 mm": p["sis_puesta_tierra"] * 2,
        "Cable 20 cms con terminal de ojo": trozo_20,
        "Tornillos hexagonales punta de lenteja cortos": tor_hex,
        "Bolsa chica de hidrocal": p["sis_puesta_tierra"],
        "Señalética logo grande": 1,
        "Señalética tablero FV": 1,
        "Señalética cámara registro": p["sis_puesta_tierra"],
        "Señalética tablero": 1,
        "Señalética paneles": p["N_panel"],
        "Bomba de riego": 1,
        "Cable RVK de 4*2.5 (m)": 7,
        "Amarra plástica chica para abrazadera concéntrica": 6,
        "Tornillos tipo lenteja": 6,
        "Prensas estopa para cordón RVK": 2,
        "Tablero 12 módulos": 1,
        "Automático de 20A bipolo": 1,
        "Diferencial de 25A": 1,
        "Metalcom Omega (3m)": 1,
        "Canalización EMT 25 mm (m)": p["dis_caseta_panel"] + 3,
        "Curvas EMT 25 mm": 6,
        "Coplas EMT 25 mm": round((p["dis_caseta_panel"] + 3) / 2) + 1,
        "Tubo PVC 90 mm cortado a 30 cm": round((p["dis_caseta_panel"] + 3) / 2) + 2,
        "Saco de H2O o árido y cemento": round((p["dis_caseta_panel"] + 3) / 2 * 0.1),
        "Caja metálica distribución 100x100 mm": 1,
        "Terminales tubería EMT de 25 mm": 2,
        "Gromix": 1,
        "Abrazaderas tipo Caddy 25 mm": 4,
        "Tornillos tipo lenteja": 4
    }

# Función para exportar PDF
def exportar_pdf(df, filename="lista_compra.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    title = Paragraph("📋 Lista de Compra para Instalación FV", styles["Title"])
    elements.append(title)

    data = [["Elemento", "Cantidad"]] + df.values.tolist()
    table = Table(data, colWidths=[300, 100])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))
    elements.append(table)
    doc.build(elements)

# Interfaz Streamlit
st.title("🔧 Cubicación FV Offgrid – Bomba de Riego")

# Formulario
params = {
    "N_panel": st.number_input("🔢 Número de paneles solares", min_value=1, value=13),
    "ancho_panel": st.number_input("📏 Ancho de cada panel (m)", value=1.14),
    "l_rielmontaje": st.number_input("📐 Largo del riel de montaje (m)", value=4.2),
    "Arco_estructura": st.number_input("🧱 Número de arcos de estructura", value=5),
    "dia_cable_solar": st.number_input("🔌 Diámetro del cable solar (mm)", value=6),
    "dis_caseta_panel": st.number_input("📍 Distancia entre caseta y paneles (m)", value=10),
    "cap_fusible": st.number_input("⚡ Capacidad del fusible (A)", value=15),
    "sis_puesta_tierra": st.number_input("🌎 Sistemas de puesta a tierra", value=2)
}

if st.button("📊 Generar lista de compra"):
    lista = generar_lista_compra(params)
    df = pd.DataFrame(list(lista.items()), columns=["Elemento", "Cantidad"])
    st.dataframe(df)

    exportar_pdf(df)
    with open("lista_compra.pdf", "rb") as f:
        st.download_button("📥 Descargar PDF", f, file_name="lista_compra.pdf")
