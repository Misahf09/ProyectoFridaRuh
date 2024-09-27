import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import openai
# Cargar el dataset
url = "https://raw.githubusercontent.com/Misahf09/ProyectoFridaRuh/refs/heads/main/DatosCorregidosProyecto.csv"
data = pd.read_csv(url)

# Calcular los ratios
data['Liquidez_Corriente'] = data['Current_Assets'] / data['Current_Liabilities']
data['Deuda_a_Patrimonio'] = (data['Short_Term_Debt'] + data['Long_Term_Debt']) / data['Equity']
data['Cobertura_Gastos_Financieros'] = data['Total_Revenue'] / data['Financial_Expenses']

# Configuración de Streamlit
st.title("Dashboard Financiero Interactivo")

# Mostrar las primeras filas del dataset
if st.checkbox("Mostrar datos originales"):
    st.subheader("Datos Originales")
    st.write(data.head())

# Seleccionar ratio a analizar
ratio = st.selectbox("Selecciona un ratio a visualizar", 
                     ['Liquidez_Corriente', 'Deuda_a_Patrimonio', 'Cobertura_Gastos_Financieros'])

# Selección de la industria y tamaño de la empresa
industries = data['Industry'].unique()
selected_industry = st.selectbox("Selecciona una industria", industries)

sizes = data['Company_Size'].unique()
selected_size = st.selectbox("Selecciona el tamaño de la empresa", sizes)

# Filtrar los datos según las selecciones
filtered_data = data[(data['Industry'] == selected_industry) & (data['Company_Size'] == selected_size)]

# Visualización del ratio seleccionado
st.subheader(f"Análisis de {ratio}")
fig, ax = plt.subplots()
sns.boxplot(x='Company_Size', y=ratio, data=filtered_data, ax=ax)
ax.set_title(f"{ratio} por Tamaño de Empresa en la Industria: {selected_industry}")
st.pyplot(fig)

# Comparación entre industrias
st.subheader(f"Comparación del {ratio} entre Industrias")
fig, ax = plt.subplots()
sns.boxplot(x='Industry', y=ratio, data=data, ax=ax)
ax.set_title(f"{ratio} Comparado entre Diferentes Industrias")
st.pyplot(fig)

# Opcional: Más análisis o visualizaciones aquí

# Footer
st.write("Este dashboard fue creado utilizando Streamlit y datos de un proyecto.")


# Instanciar el cliente de OpenAI
openai_api_key = st.secrets["OPENAI_API_KEY"]

client = openai.OpenAI(api_key=openai_api_key)

def obtener_respuesta(prompt):
  response = client.chat.completions.create(
      model="gpt-4o-mini",  # Ajusta el modelo según lo que necesites
      messages=[
          {"role": "system", "content": """
          Eres un financiero que trabaja en una casa de bolsa, eres experto en el área de solvencia,
          entonces vas a responder todo desde la perspectiva de la aseguradora. Contesta siempre en español
          en un máximo de 100 palabras.
          """}, #Solo podemos personalizar la parte de content
          {"role": "user", "content": prompt}
      ]
  )
  output = response.choices[0].message.content
  return output

prompt_user= st.text_area("Ingresa tu pregunta: ")

# Obtener la respuesta del modelo
output_modelo = obtener_respuesta(prompt_user)

# Mostrar la respuesta del modelo
st.write(output_modelo)