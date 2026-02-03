# =================================================================
# APLICACIÓN CONSOLIDADA: ACTIVO NO CORRIENTE
# =================================================================
import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from pandas.tseries.offsets import DateOffset
from mpl_toolkits.mplot3d import Axes3D
import streamlit as st
import os
import PyPDF2

# =================================================================
# CONFIGURACIÓN GENERAL
# =================================================================
st.set_page_config(layout="wide", page_title="Análisis de Activo No Corriente")

# =================================================================
# FUNCIONES DE GENERACIÓN DE DATOS - MAQUINARIAS
# =================================================================

@st.cache_data
def generar_datos_maquinarias():
    """Genera datos simulados de inventario de maquinarias."""
    fake = Faker('es_AR')
    random.seed(42)
    np.random.seed(42)
    Faker.seed(42)
    
    num_equipos = 30
    tipos_maquinaria = ["Torno CNC", "Fresadora", "Impresora industrial", "Camión", "Grua hidráulica"]
    ubicaciones = ["Planta A", "Planta B", "Depósito Central", "Taller de Mantenimiento"]
    estados = ["Operativo", "En reparación", "Fuera de servicio", "Pendiente de baja"]

    maquinarias = []
    for i in range(num_equipos):
        tipo = random.choice(tipos_maquinaria)
        fecha_adquisicion = fake.date_between(start_date='-10y', end_date='-1y')
        valor_adquisicion = round(random.uniform(200000, 5000000), 2)
        vida_util_anios = random.randint(5, 15)
        maquinarias.append({
            "id_equipo": f"EQ-{1000 + i}",
            "tipo_equipo": tipo,
            "descripcion": f"{tipo} modelo {fake.bothify(text='???-####')}",
            "ubicacion": random.choice(ubicaciones),
            "estado": random.choices(estados, weights=[0.7, 0.15, 0.1, 0.05])[0],
            "fecha_adquisicion": fecha_adquisicion,
            "valor_adquisicion": valor_adquisicion,
            "vida_util_anios": vida_util_anios,
            "fecha_fin_vida_util": fecha_adquisicion + timedelta(days=vida_util_anios * 365)
        })
    return pd.DataFrame(maquinarias)


# =================================================================
# FUNCIONES DE GENERACIÓN DE DATOS - INMUEBLES
# =================================================================

@st.cache_data
def generar_datos_inmuebles():
    """Genera datos simulados de inventario de inmuebles."""
    fake = Faker('es_AR')
    random.seed(101)
    np.random.seed(101)
    Faker.seed(101)

    num_inmuebles = 30
    tipos_inmuebles = ["Oficina", "Depósito", "Terreno", "Planta industrial",
                      "Local comercial", "Edificio", "Galpón", "Centro logístico"]
    estados_inmueble = ["Operativo", "Arrendado", "Mantenimiento", "Disponible", "Inactivo"]
    ubicaciones = ["CABA", "Gran Buenos Aires", "Córdoba", "Mendoza", "Rosario", "Neuquén", "Salta"]

    inmuebles = []
    for i in range(num_inmuebles):
        tipo = random.choice(tipos_inmuebles)
        direccion = fake.address().replace("\n", ", ")
        ciudad = random.choice(ubicaciones)
        estado = random.choices(estados_inmueble, weights=[0.5, 0.2, 0.1, 0.1, 0.1])[0]
        fecha_adquisicion = fake.date_between(start_date='-25y', end_date='-2y')
        valor_adquisicion = round(random.uniform(100000.0, 15000000.0), 2)
        superficie_m2 = round(random.uniform(100.0, 5000.0), 2)
        
        inmuebles.append({
            "id_inmueble": f"INM-{1000 + i}",
            "tipo_inmueble": tipo,
            "direccion": direccion,
            "ubicacion": ciudad,
            "estado": estado,
            "fecha_adquisicion": fecha_adquisicion,
            "valor_adquisicion": valor_adquisicion,
            "superficie_m2": superficie_m2
        })
    return pd.DataFrame(inmuebles)


# =================================================================
# FUNCIONES DE GENERACIÓN DE DATOS - ACTIVOS INTANGIBLES
# =================================================================

@st.cache_data
def generar_datos_intangibles():
    """Genera datos simulados de activos intangibles."""
    np.random.seed(789)
    random.seed(789)
    fake = Faker('es_AR')
    Faker.seed(789)

    num_activos_intangibles = 30
    tipos_activo_intangible = ['Software Licencia', 'Patente', 'Marca Registrada', 'Derechos de Autor',
                               'Fondo de Comercio', 'Lista de Clientes', 'Tecnología no Patentada']
    vida_util_rangos = {'Software Licencia': (3, 7), 'Patente': (10, 20), 'Marca Registrada': (5, 15),
                        'Derechos de Autor': (5, 10), 'Fondo de Comercio': (5, 10), 'Lista de Clientes': (2, 5),
                        'Tecnología no Patentada': (3, 8)}
    empresas_propietarias = [
        {'empresa_id': 3000 + i, 'nombre_empresa': fake.company(), 'cuit': fake.unique.bothify(text='30-########-#')}
        for i in range(10)]

    activos_intangibles = []
    for i in range(num_activos_intangibles):
        propietaria = random.choice(empresas_propietarias)
        tipo = random.choice(tipos_activo_intangible)
        fecha_adquisicion = fake.date_between(start_date='-10y', end_date='-30d')
        min_vida, max_vida = vida_util_rangos.get(tipo, (5, 10))
        vida_util_anios = random.randint(min_vida, max_vida)
        costo_adquisicion = round(random.uniform(50000, 2000000), 2)
        
        today = datetime.now().date()
        days_since_acquisition = (today - fecha_adquisicion).days
        amortizacion_anual = costo_adquisicion / vida_util_anios
        amortizacion_acumulada_simulada = round(amortizacion_anual * (days_since_acquisition / 365.25), 2)
        amortizacion_acumulada_simulada = min(amortizacion_acumulada_simulada, costo_adquisicion)
        valor_neto_contable_simulado = round(costo_adquisicion - amortizacion_acumulada_simulada, 2)
        
        if valor_neto_contable_simulado <= 0.01:
            estado = 'Totalmente Amortizado'
        else:
            estado = 'Activo'
        if random.random() < 0.05 and estado == 'Activo':
            estado = 'Vendido'
            
        activos_intangibles.append({
            'activo_id': f'INT-{30000 + i}',
            'empresa_id': propietaria['empresa_id'],
            'tipo_activo_intangible': tipo,
            'fecha_adquisicion': fecha_adquisicion,
            'costo_adquisicion': costo_adquisicion,
            'vida_util_anios': vida_util_anios,
            'amortizacion_acumulada_simulada': amortizacion_acumulada_simulada,
            'valor_neto_contable_simulado': valor_neto_contable_simulado,
            'estado_activo': estado,
            'nombre_empresa_propietaria': propietaria['nombre_empresa'],
            'cuit_empresa_propietaria': propietaria['cuit']
        })

    return pd.DataFrame(activos_intangibles)


# =================================================================
# FUNCIONES DE GENERACIÓN DE DATOS - OTROS ACTIVOS
# =================================================================

@st.cache_data
def generar_datos_otros_activos():
    """Genera datos simulados de otros activos no corrientes."""
    np.random.seed(901)
    random.seed(901)
    fake = Faker('es_AR')
    Faker.seed(901)

    num_registros = 50
    tipos_activo = ['Valores a cobrar LP', 'Inversiones a Largo Plazo', 
                    'Activos por Impuestos Diferidos', 'Cuentas por Cobrar LP']
    monedas = ['ARS', 'USD', 'EUR']

    activos = []
    for i in range(num_registros):
        activos.append({
            'id_activo': f'OA-{1000 + i}',
            'tipo_activo': random.choice(tipos_activo),
            'monto': round(random.uniform(10000, 250000), 2),
            'moneda': random.choice(monedas),
            'fecha_registro': fake.date_between(start_date='-120d', end_date='today'),
            'descripcion': f'Activo {random.choice(tipos_activo)}'
        })
    return pd.DataFrame(activos)


# =================================================================
# FUNCIONES DE AUDITORÍA - MAQUINARIAS
# =================================================================

def auditar_maquinarias(df):
    """Aplica auditoría a maquinarias."""
    df['fecha_adquisicion'] = pd.to_datetime(df['fecha_adquisicion'])
    df['fecha_fin_vida_util'] = pd.to_datetime(df['fecha_fin_vida_util'])
    fecha_actual = datetime.now()
    df['edad_anios'] = ((fecha_actual - df['fecha_adquisicion']).dt.days / 365.25).round(2)
    df['vida_util_restante_anios'] = ((df['fecha_fin_vida_util'] - fecha_actual).dt.days / 365.25).round(2)
    df.loc[df['vida_util_restante_anios'] < 0, 'vida_util_restante_anios'] = 0
    df['valor_adquisicion_zscore'] = zscore(df['valor_adquisicion'])

    umbral_z = 2.5
    features = df[['valor_adquisicion', 'edad_anios', 'vida_util_restante_anios']].copy()
    iso = IsolationForest(random_state=42, contamination=0.1)
    df['is_anomaly_ia'] = iso.fit_predict(features)

    df['alerta_combinada'] = df.apply(lambda row: 'Z-score alto y Anomalía IA' if (
                abs(row['valor_adquisicion_zscore']) > umbral_z and row['is_anomaly_ia'] == -1) else (
        'Z-score alto' if abs(row['valor_adquisicion_zscore']) > umbral_z else (
            'Anomalía IA' if row['is_anomaly_ia'] == -1 else 'Sin alerta')), axis=1)

    return df


# =================================================================
# FUNCIONES DE AUDITORÍA - INMUEBLES
# =================================================================

def auditar_inmuebles(df):
    """Aplica auditoría a inmuebles."""
    df['fecha_adquisicion'] = pd.to_datetime(df['fecha_adquisicion'], errors='coerce')
    df['fecha_adquisicion'].fillna(pd.to_datetime('2020-01-01'), inplace=True)

    if 'fecha_fin_vida_util' not in df.columns:
        df['fecha_fin_vida_util'] = df.apply(
            lambda row: row['fecha_adquisicion'] + DateOffset(years=np.random.randint(50, 100)), axis=1)
    else:
        df['fecha_fin_vida_util'] = pd.to_datetime(df['fecha_fin_vida_util'], errors='coerce')
        df['fecha_fin_vida_util'].fillna(df['fecha_adquisicion'] + DateOffset(years=75), inplace=True)

    fecha_actual_referencia = datetime.now()
    df['edad_anios'] = ((fecha_actual_referencia - df['fecha_adquisicion']).dt.days / 365.25).round(2)
    df['vida_util_restante_anios'] = ((df['fecha_fin_vida_util'] - fecha_actual_referencia).dt.days / 365.25).round(2)
    df.loc[df['vida_util_restante_anios'] < 0, 'vida_util_restante_anios'] = 0

    df['valor_adquisicion_zscore'] = zscore(df['valor_adquisicion'])
    umbral_zscore = 3
    df['is_anomaly_zscore'] = np.where(
        (df['valor_adquisicion_zscore'] > umbral_zscore) | (df['valor_adquisicion_zscore'] < -umbral_zscore), -1, 1)

    features_for_anomaly_detection = df[
        ['valor_adquisicion', 'edad_anios', 'vida_util_restante_anios', 'superficie_m2']].copy()
    features_for_anomaly_detection.replace([np.inf, -np.inf], np.nan, inplace=True)
    features_for_anomaly_detection.fillna(features_for_anomaly_detection.median(), inplace=True)

    iso_forest = IsolationForest(random_state=42, contamination=0.1)
    df['is_anomaly_ia'] = iso_forest.fit_predict(features_for_anomaly_detection)

    df['resultado_auditoria'] = 'Normal'
    df.loc[
        (df['is_anomaly_zscore'] == -1) & (df['is_anomaly_ia'] == -1), 'resultado_auditoria'] = 'Anomalía Z-score e IA'
    df.loc[(df['is_anomaly_zscore'] == -1) & (df['is_anomaly_ia'] != -1), 'resultado_auditoria'] = 'Anomalía Z-score'
    df.loc[(df['is_anomaly_zscore'] != -1) & (df['is_anomaly_ia'] == -1), 'resultado_auditoria'] = 'Anomalía IA'

    return df


# =================================================================
# FUNCIONES DE AUDITORÍA - ACTIVOS INTANGIBLES
# =================================================================

def auditar_intangibles(df):
    """Aplica auditoría a activos intangibles."""
    df['fecha_adquisicion'] = pd.to_datetime(df['fecha_adquisicion'])
    numeric_cols = ['costo_adquisicion', 'vida_util_anios', 'amortizacion_acumulada_simulada',
                    'valor_neto_contable_simulado']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df.fillna(0, inplace=True)

    df['valor_neto_calculado'] = df['costo_adquisicion'] - df['amortizacion_acumulada_simulada']
    df['discrepancia_vnc'] = df['valor_neto_calculado'] - df['valor_neto_contable_simulado']

    fecha_auditoria = datetime.now()
    df['amortizacion_anual_calculada'] = df['costo_adquisicion'] / df['vida_util_anios']
    df['amortizacion_anual_calculada'] = df['amortizacion_anual_calculada'].replace([np.inf, -np.inf], np.nan)
    df['amortizacion_anual_calculada'] = df['amortizacion_anual_calculada'].fillna(0)

    df['anios_transcurridos'] = (fecha_auditoria - df['fecha_adquisicion']).dt.days / 365.25
    df['amortizacion_acumulada_esperada'] = df.apply(
        lambda row: min(row['costo_adquisicion'], row['amortizacion_anual_calculada'] * row['anios_transcurridos']),
        axis=1)
    df['discrepancia_amortizacion'] = df['amortizacion_acumulada_esperada'] - df['amortizacion_acumulada_simulada']
    df['antiguedad_anios'] = (fecha_auditoria - df['fecha_adquisicion']).dt.days / 365.25

    return df


# =================================================================
# FUNCIONES DE AUDITORÍA - OTROS ACTIVOS
# =================================================================

def auditar_otros_activos(df):
    """Aplica auditoría a otros activos."""
    df['fecha_registro'] = pd.to_datetime(df['fecha_registro'])
    df['monto'] = pd.to_numeric(df['monto'], errors='coerce').fillna(0)

    fecha_auditoria = datetime.now()
    df['dias_desde_registro'] = (fecha_auditoria - df['fecha_registro']).dt.days

    return df


# =================================================================
# FUNCIONES DE ANÁLISIS Y VISUALIZACIÓN - MAQUINARIAS
# =================================================================

def analizar_maquinarias(df):
    """Análisis completo de maquinarias."""
    st.subheader("📊 Análisis de Maquinarias")

    # Métricas clave
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Equipos", len(df))
    with col2:
        anomalias_ia_count = len(df[df['is_anomaly_ia'] == -1])
        st.metric("Anomalías por IA", anomalias_ia_count)
    with col3:
        alertas_combinadas_count = len(df[df['alerta_combinada'] != 'Sin alerta'])
        st.metric("Alertas Combinadas", alertas_combinadas_count)

    # Visualizaciones
    st.markdown("---")
    st.subheader("📈 Visualizaciones")

    col_viz1, col_viz2 = st.columns(2)
    with col_viz1:
        # Gráfico 1: Valor Total por Tipo
        valor_total_tipo = df.groupby('tipo_equipo')['valor_adquisicion'].sum().sort_values(ascending=False)
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.barplot(x=valor_total_tipo.index, y=valor_total_tipo.values, hue=valor_total_tipo.index, 
                   palette='viridis', ax=ax1, legend=False)
        ax1.set_title('Valor Total de Adquisición por Tipo de Equipo')
        ax1.set_xlabel('')
        ax1.set_ylabel('Valor Total ($)')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig1)
        plt.close(fig1)

    with col_viz2:
        # Gráfico 2: Conteo por Ubicación y Estado
        conteo = df.groupby(['ubicacion', 'estado']).size().unstack(fill_value=0)
        fig2, ax2 = plt.subplots(figsize=(10, 7))
        conteo.plot(kind='bar', stacked=True, colormap='Paired', ax=ax2)
        ax2.set_title('Conteo de Equipos por Ubicación y Estado')
        ax2.set_xlabel('Ubicación')
        ax2.set_ylabel('Número de Equipos')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig2)
        plt.close(fig2)


# =================================================================
# FUNCIONES DE ANÁLISIS Y VISUALIZACIÓN - INMUEBLES
# =================================================================

def analizar_inmuebles(df):
    """Análisis completo de inmuebles."""
    st.subheader("📊 Análisis de Inmuebles")

    # Métricas clave
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de Inmuebles", len(df))
    with col2:
        anomalias_count = len(df[df['resultado_auditoria'] != 'Normal'])
        st.metric("Anomalías Detectadas", anomalias_count)

    # Visualizaciones
    st.markdown("---")
    st.subheader("📈 Visualizaciones")

    # Gráfico 1: Valor Total por Tipo
    valor_total_por_tipo = df.groupby('tipo_inmueble')['valor_adquisicion'].sum().sort_values(ascending=False)
    fig1, ax1 = plt.subplots(figsize=(12, 7))
    sns.barplot(x=valor_total_por_tipo.index, y=valor_total_por_tipo.values, hue=valor_total_por_tipo.index,
               palette='viridis', ax=ax1, legend=False)
    ax1.set_title('Valor Total de Adquisición por Tipo de Inmueble')
    ax1.set_xlabel('Tipo de Inmueble')
    ax1.set_ylabel('Valor Total de Adquisición')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig1)
    plt.close(fig1)


# =================================================================
# FUNCIONES DE ANÁLISIS Y VISUALIZACIÓN - INTANGIBLES
# =================================================================

def analizar_intangibles(df):
    """Análisis completo de activos intangibles."""
    st.subheader("📊 Análisis de Activos Intangibles")

    # Métricas clave
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de Activos", len(df))
    with col2:
        inconsistencias_vnc = df[df['discrepancia_vnc'].abs() > 0.01]
        st.metric("Discrepancias en VNC", len(inconsistencias_vnc))

    # Visualizaciones
    st.markdown("---")
    st.subheader("📈 Visualizaciones")

    fig, ax = plt.subplots(figsize=(12, 7))
    df['tipo_activo_intangible'].value_counts().plot(
        kind='bar', 
        color=sns.color_palette("viridis", len(df['tipo_activo_intangible'].unique())),
        ax=ax
    )
    ax.set_title('Distribución de Tipos de Activos Intangibles')
    ax.set_ylabel('Cantidad')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
    plt.close(fig)


# =================================================================
# FUNCIONES DE ANÁLISIS Y VISUALIZACIÓN - OTROS ACTIVOS
# =================================================================

def analizar_otros_activos(df):
    """Análisis completo de otros activos."""
    st.subheader("📊 Análisis de Otros Activos")

    # Métricas clave
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Registros", len(df))
    with col2:
        monto_total = df['monto'].sum()
        st.metric("Monto Total ($)", f"{monto_total:,.2f}")
    with col3:
        registros_antiguos = df[df['dias_desde_registro'] > 90]
        st.metric("Registros > 90 días", len(registros_antiguos))

    # Visualizaciones
    st.markdown("---")
    st.subheader("📈 Visualizaciones")

    fig, ax = plt.subplots(figsize=(12, 7))
    df['tipo_activo'].value_counts().plot(
        kind='bar', 
        color=sns.color_palette("viridis", len(df['tipo_activo'].unique())),
        ax=ax
    )
    ax.set_title('Distribución de Tipos de Activos')
    ax.set_ylabel('Cantidad')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
    plt.close(fig)


# =================================================================
# FUNCIONES PARA INFORMES DE AUDITORÍA
# =================================================================

def extraer_texto_pdf(ruta_archivo):
    """Extrae texto de un archivo PDF"""
    try:
        with open(ruta_archivo, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            texto = ""
            for page in pdf_reader.pages:
                texto += page.extract_text() + "\n"
            return texto
    except Exception as e:
        return f"Error al leer el PDF: {str(e)}"


def mostrar_informes_auditoria():
    """Muestra los informes de auditoría disponibles"""
    st.header("📄 Informes de Auditoría")
    st.markdown("""
        Informes profesionales de auditoría del Activo No Corriente.
    """)
    
    # Ruta de los informes
    ruta_informes = "data/informes_auditoria_activos"
    
    # Verificar si existe el directorio
    if not os.path.exists(ruta_informes):
        st.warning(f"⚠️ No se encontró el directorio de informes: {ruta_informes}")
        st.info("Los informes se generarán automáticamente cuando se configure el sistema.")
        return
    
    # Buscar archivos PDF
    archivos_pdf = sorted([f for f in os.listdir(ruta_informes) if f.endswith('.pdf')])
    
    if not archivos_pdf:
        st.warning("⚠️ No se encontraron informes de auditoría en el directorio.")
        return
    
    st.success(f"✅ Se encontraron {len(archivos_pdf)} informes de auditoría")
    st.markdown("---")
    
    # Selector de informe
    informe_seleccionado = st.selectbox(
        "📂 Seleccione un informe:",
        archivos_pdf,
        format_func=lambda x: x.replace('_', ' ').replace('.pdf', '').title()
    )
    
    if informe_seleccionado:
        ruta_completa = os.path.join(ruta_informes, informe_seleccionado)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader(f"📋 {informe_seleccionado.replace('_', ' ').replace('.pdf', '').title()}")
        
        with col2:
            with open(ruta_completa, 'rb') as file:
                st.download_button(
                    label="⬇️ Descargar PDF",
                    data=file.read(),
                    file_name=informe_seleccionado,
                    mime="application/pdf"
                )


# =================================================================
# APLICACIÓN PRINCIPAL
# =================================================================

def main():
    # Título principal
    st.title("📋 Análisis Consolidado de Activo No Corriente")
    st.markdown("""
        Esta aplicación consolida el análisis de todos los componentes del **Activo No Corriente**, 
        incluyendo detección de anomalías mediante inteligencia artificial.
    """)
    st.markdown("---")

    # Crear pestañas
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏭 Maquinarias", 
        "🏢 Inmuebles", 
        "💡 Activos Intangibles",
        "📦 Otros Activos",
        "📊 Resumen Consolidado",
        "📄 Informes de Auditoría"
    ])

    # Generar datos
    with st.spinner("Generando datos..."):
        df_maquinarias = generar_datos_maquinarias()
        df_inmuebles = generar_datos_inmuebles()
        df_intangibles = generar_datos_intangibles()
        df_otros_activos = generar_datos_otros_activos()
        
        df_maquinarias = auditar_maquinarias(df_maquinarias)
        df_inmuebles = auditar_inmuebles(df_inmuebles)
        df_intangibles = auditar_intangibles(df_intangibles)
        df_otros_activos = auditar_otros_activos(df_otros_activos)

    # Pestaña 1: Maquinarias
    with tab1:
        st.header("🏭 Inventario de Maquinarias")
        analizar_maquinarias(df_maquinarias)

    # Pestaña 2: Inmuebles
    with tab2:
        st.header("🏢 Inventario de Inmuebles")
        analizar_inmuebles(df_inmuebles)

    # Pestaña 3: Activos Intangibles
    with tab3:
        st.header("💡 Activos Intangibles")
        analizar_intangibles(df_intangibles)

    # Pestaña 4: Otros Activos
    with tab4:
        st.header("📦 Otros Activos No Corrientes")
        analizar_otros_activos(df_otros_activos)

    # Pestaña 5: Resumen Consolidado
    with tab5:
        st.header("📊 Resumen Consolidado del Activo No Corriente")
        st.markdown("---")

        # Métricas consolidadas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.subheader("🏭 Maquinarias")
            st.metric("Total Equipos", len(df_maquinarias))
            st.metric("Valor Total", f"${df_maquinarias['valor_adquisicion'].sum():,.0f}")
        
        with col2:
            st.subheader("🏢 Inmuebles")
            st.metric("Total Inmuebles", len(df_inmuebles))
            st.metric("Valor Total", f"${df_inmuebles['valor_adquisicion'].sum():,.0f}")
        
        with col3:
            st.subheader("💡 Intangibles")
            st.metric("Total Activos", len(df_intangibles))
            st.metric("Valor Total", f"${df_intangibles['costo_adquisicion'].sum():,.0f}")
        
        with col4:
            st.subheader("📦 Otros Activos")
            st.metric("Total Registros", len(df_otros_activos))
            st.metric("Monto Total", f"${df_otros_activos['monto'].sum():,.0f}")

        st.markdown("---")

        # Total consolidado
        total_activo_nc = (
            df_maquinarias['valor_adquisicion'].sum() +
            df_inmuebles['valor_adquisicion'].sum() +
            df_intangibles['costo_adquisicion'].sum() +
            df_otros_activos['monto'].sum()
        )
        st.subheader("💰 TOTAL ACTIVO NO CORRIENTE")
        st.metric("Valor Total Estimado", f"${total_activo_nc:,.2f}")

        st.markdown("---")

        # Gráfico comparativo
        st.subheader("📊 Comparación de Componentes")
        fig, ax = plt.subplots(figsize=(10, 6))
        componentes = ["Maquinarias", "Inmuebles", "Intangibles", "Otros Activos"]
        valores = [
            df_maquinarias['valor_adquisicion'].sum(),
            df_inmuebles['valor_adquisicion'].sum(),
            df_intangibles['costo_adquisicion'].sum(),
            df_otros_activos['monto'].sum()
        ]
        colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
        ax.bar(componentes, valores, color=colors)
        ax.set_ylabel("Monto Total (ARS)", fontsize=12)
        ax.set_title("Composición del Activo No Corriente", fontsize=16)
        for i, v in enumerate(valores):
            ax.text(i, v, f"${v:,.0f}", ha="center", va="bottom", fontsize=10)
        st.pyplot(fig)
        plt.close(fig)

    # Pestaña 6: Informes de Auditoría
    with tab6:
        mostrar_informes_auditoria()


if __name__ == "__main__":
    main()
