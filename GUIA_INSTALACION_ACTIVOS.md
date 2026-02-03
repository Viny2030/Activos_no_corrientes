# 🚀 GUÍA DE INSTALACIÓN: ACTIVO NO CORRIENTE

## 📦 ARCHIVOS INCLUIDOS

Has recibido los siguientes archivos:

### 1. Código Principal
- **`Activo_no_corriente_app.py`** - Aplicación Streamlit consolidada

### 2. Dependencias
- **`requirements.txt`** - Librerías necesarias

### 3. Informes PDF (5 archivos)
- `informe_activos_2020.pdf`
- `informe_activos_2021.pdf`
- `informe_activos_2022.pdf`
- `informe_activos_2023.pdf`
- `informe_activos_2024.pdf`

### 4. Generador (OPCIONAL)
- **`generar_informes_activos.py`** - Para regenerar informes

---

## 🎯 COMPONENTES DE LA APLICACIÓN

La aplicación analiza **4 componentes del Activo No Corriente**:

1. **🏭 Inventario de Maquinarias**
   - 30 equipos industriales
   - Detección de anomalías con Isolation Forest
   - Análisis de vida útil y depreciación

2. **🏢 Inventario de Inmuebles**
   - 30 propiedades en 7 ubicaciones
   - Z-score + Isolation Forest
   - Análisis de valor por m²

3. **💡 Activos Intangibles**
   - Software, patentes, marcas, etc.
   - Verificación de amortización
   - 30 activos analizados

4. **📦 Otros Activos No Corrientes**
   - 50 registros de activos diversos
   - Análisis de antigüedad
   - Múltiples monedas

---

## 📁 ESTRUCTURA DEL PROYECTO

Debes crear esta estructura en tu repositorio:

```
tu-proyecto-activos/
├── Activo_no_corriente_app.py   ← Archivo principal
├── requirements.txt              ← Dependencias
└── data/
    └── informes_auditoria_activos/
        ├── informe_activos_2020.pdf
        ├── informe_activos_2021.pdf
        ├── informe_activos_2022.pdf
        ├── informe_activos_2023.pdf
        └── informe_activos_2024.pdf
```

---

## 🔧 INSTALACIÓN EN RENDER

### PASO 1: Crear Repositorio en GitHub

1. **Crea un nuevo repositorio** en GitHub (ejemplo: `activos-no-corrientes`)

2. **Sube los archivos**:
   ```bash
   # En tu terminal local
   git init
   git add .
   git commit -m "Initial commit: Activo No Corriente app"
   git branch -M main
   git remote add origin https://github.com/tu-usuario/activos-no-corrientes.git
   git push -u origin main
   ```

### PASO 2: Crear Carpeta de Informes

**Opción A: Directamente en GitHub**
1. Ve a tu repositorio
2. Click en "Add file" → "Create new file"
3. Nombre: `data/informes_auditoria_activos/.gitkeep`
4. Commit
5. Navega a `data/informes_auditoria_activos/`
6. Click "Add file" → "Upload files"
7. Sube los 5 PDFs
8. Commit

**Opción B: Desde terminal**
```bash
mkdir -p data/informes_auditoria_activos
# Copia los 5 PDFs a esa carpeta
git add data/informes_auditoria_activos/*.pdf
git commit -m "Add audit reports"
git push
```

### PASO 3: Configurar Render

1. **Ve a** https://dashboard.render.com/
2. **Click en** "New +" → "Web Service"
3. **Conecta tu repositorio** de GitHub
4. **Configuración:**
   - **Name:** `activos-no-corrientes`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run Activo_no_corriente_app.py --server.port=$PORT --server.address=0.0.0.0`
5. **Click en** "Create Web Service"

### PASO 4: Esperar Despliegue

- ⏱️ Tiempo estimado: 5-8 minutos
- 📊 Monitorea los logs en tiempo real
- ✅ Cuando veas "Your service is live 🎉" está listo

---

## ✅ VERIFICACIÓN POST-DESPLIEGUE

Una vez desplegado, tu aplicación debe tener:

### 6 Pestañas Funcionales:

1. **🏭 Maquinarias**
   - Métricas: Total Equipos, Anomalías IA, Alertas
   - Gráficos: Valor por tipo, Conteo por ubicación

2. **🏢 Inmuebles**
   - Métricas: Total Inmuebles, Anomalías
   - Gráficos: Valor por tipo, Superficie vs Valor

3. **💡 Activos Intangibles**
   - Métricas: Total Activos, Discrepancias
   - Gráficos: Distribución por tipo

4. **📦 Otros Activos**
   - Métricas: Total Registros, Monto Total
   - Gráficos: Distribución por tipo y moneda

5. **📊 Resumen Consolidado**
   - Métricas de todos los componentes
   - Gráfico comparativo
   - Total del Activo No Corriente

6. **📄 Informes de Auditoría**
   - Selector de años (2020-2024)
   - Descarga de PDFs
   - Vista de contenido

---

## 🎨 CARACTERÍSTICAS PRINCIPALES

### Detección de Anomalías
- ✅ **Isolation Forest** - ML para detectar outliers
- ✅ **Z-score** - Análisis estadístico
- ✅ **Alertas combinadas** - Múltiples métricas

### Visualizaciones
- ✅ Gráficos de barras con seaborn
- ✅ Histogramas de distribución
- ✅ Scatter plots 3D (maquinarias)
- ✅ Gráficos apilados por ubicación

### Informes PDF
- ✅ 5 informes profesionales (2020-2024)
- ✅ Portada con metadatos
- ✅ Resumen ejecutivo
- ✅ Análisis por componente
- ✅ Conclusiones y recomendaciones

---

## 📊 DATOS SIMULADOS

La aplicación genera datos **realistas** pero **ficticios**:

- **Maquinarias:** 30 equipos (Tornos, Fresadoras, Grúas, etc.)
- **Inmuebles:** 30 propiedades en Argentina
- **Intangibles:** 30 activos (Software, Patentes, Marcas)
- **Otros:** 50 registros en ARS, USD, EUR

Cada ejecución usa **seeds fijas** para reproducibilidad.

---

## 🔍 TROUBLESHOOTING

### Error: Module not found

**Solución:** Verifica que `requirements.txt` incluya todas las librerías:
```
streamlit
pandas
numpy
matplotlib
seaborn
scikit-learn
scipy
faker
reportlab>=3.6.0
PyPDF2
```

### Error: No se encuentran informes

**Causa:** Los PDFs no están en `data/informes_auditoria_activos/`

**Solución:**
1. Verifica la estructura de carpetas en GitHub
2. Asegúrate de que los 5 PDFs estén subidos
3. Verifica los nombres de archivos

### Error: Build failed

**Causa:** Problemas con dependencias

**Solución:**
1. Revisa los logs de Render
2. Verifica que `requirements.txt` esté en la raíz
3. Limpia caché: "Clear build cache & deploy"

---

## 💡 MEJORAS FUTURAS

Puedes extender la aplicación con:

- **Conexión a base de datos real**
- **Exportar reportes a Excel**
- **Dashboard interactivo con Plotly**
- **Alertas por email**
- **Integración con ERP**
- **Análisis de tendencias históricas**

---

## 📞 COMANDOS ÚTILES

```bash
# Ejecutar localmente
streamlit run Activo_no_corriente_app.py

# Regenerar informes
python generar_informes_activos.py

# Verificar dependencias
pip install -r requirements.txt

# Ver logs de Render
# (desde el dashboard)
```

---

## 🎊 ¡LISTO!

Tu aplicación de Activo No Corriente está completa con:
- ✅ 6 pestañas funcionales
- ✅ Detección de anomalías con IA
- ✅ Visualizaciones profesionales
- ✅ 5 informes PDF de auditoría
- ✅ Lista para producción en Render

---

**Versión:** 1.0.0  
**Fecha:** Febrero 2026  
**Compatibilidad:** Python 3.8+, Streamlit 1.30+
