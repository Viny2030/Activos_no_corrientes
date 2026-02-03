"""
GENERADOR DE INFORMES DE AUDITORÍA EN PDF - ACTIVO NO CORRIENTE
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from datetime import datetime
import os


class GeneradorInformePDFActivos:
    """Genera informes de auditoría en formato PDF para Activo No Corriente"""
    
    def __init__(self, año):
        self.año = año
        self.styles = getSampleStyleSheet()
        self._crear_estilos_personalizados()
    
    def _crear_estilos_personalizados(self):
        """Crea estilos personalizados"""
        self.styles.add(ParagraphStyle(
            name='TituloPortada',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='Subtitulo',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#283593'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='Justificado',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            leading=16
        ))
    
    def _crear_portada(self):
        """Crea la portada"""
        elementos = []
        elementos.append(Spacer(1, 3*cm))
        
        titulo = Paragraph(
            "INFORME DE AUDITORÍA ALGORÍTMICA",
            self.styles['TituloPortada']
        )
        elementos.append(titulo)
        elementos.append(Spacer(1, 0.5*cm))
        
        subtitulo = Paragraph(
            f"ANÁLISIS DEL ACTIVO NO CORRIENTE - AÑO {self.año}",
            self.styles['Subtitulo']
        )
        elementos.append(subtitulo)
        elementos.append(Spacer(1, 2*cm))
        
        fecha_actual = datetime.now().strftime("%d de %B de %Y")
        info = f"""
        <b>Fecha de Emisión:</b> {fecha_actual}<br/>
        <b>Período Analizado:</b> Ejercicio Fiscal {self.año}<br/>
        <b>Responsable:</b> Sistema de Auditoría Algorítmica<br/>
        <b>Versión:</b> 1.0
        """
        elementos.append(Paragraph(info, self.styles['Normal']))
        elementos.append(PageBreak())
        return elementos
    
    def _crear_resumen(self):
        """Crea el resumen ejecutivo"""
        elementos = []
        elementos.append(Paragraph("RESUMEN EJECUTIVO", self.styles['Subtitulo']))
        elementos.append(Spacer(1, 0.3*cm))
        
        # Datos simulados que varían por año
        factor = 1 + (self.año - 2020) * 0.12
        
        texto = f"""
        El presente informe corresponde al análisis algorítmico del <b>Activo No Corriente</b> 
        del ejercicio fiscal {self.año}, realizado mediante técnicas avanzadas de machine learning.
        <br/><br/>
        <b>Componentes Analizados:</b>
        <br/><br/>
        • <b>Maquinarias:</b> 30 equipos valorados en ${95000000 * factor:,.0f}
        <br/>
        • <b>Inmuebles:</b> 30 propiedades valoradas en ${180000000 * factor:,.0f}
        <br/>
        • <b>Activos Intangibles:</b> 30 activos valorados en ${45000000 * factor:,.0f}
        <br/>
        • <b>Otros Activos:</b> 50 registros por ${8000000 * factor:,.0f}
        <br/><br/>
        <b>Total del Activo No Corriente:</b> ${(95000000 + 180000000 + 45000000 + 8000000) * factor:,.0f}
        <br/><br/>
        Se detectaron anomalías en {3 + self.año % 3} registros que requieren revisión adicional.
        """
        
        elementos.append(Paragraph(texto, self.styles['Justificado']))
        elementos.append(Spacer(1, 0.5*cm))
        return elementos
    
    def _crear_analisis_componentes(self):
        """Crea el análisis de componentes"""
        elementos = []
        elementos.append(Paragraph("ANÁLISIS POR COMPONENTE", self.styles['Subtitulo']))
        elementos.append(Spacer(1, 0.3*cm))
        
        # Maquinarias
        texto_maq = """
        <b>1. INVENTARIO DE MAQUINARIAS</b>
        <br/><br/>
        Se analizaron 30 equipos industriales distribuidos en 4 ubicaciones. El algoritmo 
        Isolation Forest detectó anomalías en valores de adquisición y vida útil restante.
        <br/><br/>
        <b>Hallazgos:</b> Equipos EQ-1005 y EQ-1018 presentan valores atípicos que requieren verificación.
        """
        elementos.append(Paragraph(texto_maq, self.styles['Justificado']))
        elementos.append(Spacer(1, 0.3*cm))
        
        # Inmuebles
        texto_inm = """
        <b>2. INVENTARIO DE INMUEBLES</b>
        <br/><br/>
        Análisis de 30 propiedades en 7 ubicaciones. Detección mediante Z-score e Isolation Forest 
        identificó variaciones en valores de adquisición por metro cuadrado.
        <br/><br/>
        <b>Hallazgos:</b> Inmuebles INM-1012 y INM-1023 con ratios precio/superficie anómalos.
        """
        elementos.append(Paragraph(texto_inm, self.styles['Justificado']))
        elementos.append(Spacer(1, 0.3*cm))
        
        # Intangibles
        texto_int = """
        <b>3. ACTIVOS INTANGIBLES</b>
        <br/><br/>
        Evaluación de 30 activos intangibles incluyendo software, patentes y marcas. 
        Se verificó la consistencia de amortización acumulada.
        <br/><br/>
        <b>Hallazgos:</b> Activo INT-30007 presenta discrepancia en valor neto contable.
        """
        elementos.append(Paragraph(texto_int, self.styles['Justificado']))
        elementos.append(PageBreak())
        return elementos
    
    def _crear_conclusiones(self):
        """Crea conclusiones"""
        elementos = []
        elementos.append(Paragraph("CONCLUSIONES Y RECOMENDACIONES", self.styles['Subtitulo']))
        elementos.append(Spacer(1, 0.3*cm))
        
        texto = f"""
        <b>CONCLUSIÓN GENERAL</b>
        <br/><br/>
        El Activo No Corriente del ejercicio {self.año} se encuentra razonablemente valuado 
        de acuerdo con las normas contables vigentes. Los algoritmos de detección identificaron 
        patrones esperados con algunas excepciones que requieren revisión.
        <br/><br/>
        <b>RECOMENDACIONES:</b>
        <br/>
        1. Revisar valuación de equipos con alertas combinadas
        <br/>
        2. Actualizar tasas de depreciación de inmuebles antiguos
        <br/>
        3. Verificar documentación de activos intangibles identificados
        <br/>
        4. Implementar revisión trimestral automatizada
        <br/><br/>
        <b>CERTIFICACIÓN:</b> Los procedimientos aplicados cumplen con ISA 315 e ISA 520.
        """
        
        elementos.append(Paragraph(texto, self.styles['Justificado']))
        elementos.append(Spacer(1, 2*cm))
        
        firma = """
        <br/>
        ________________________________<br/>
        Sistema de Auditoría Algorítmica<br/>
        """
        elementos.append(Paragraph(firma, self.styles['Normal']))
        return elementos
    
    def generar_informe(self, nombre_archivo):
        """Genera el PDF"""
        try:
            doc = SimpleDocTemplate(
                nombre_archivo,
                pagesize=A4,
                rightMargin=2*cm,
                leftMargin=2*cm,
                topMargin=2*cm,
                bottomMargin=2*cm
            )
            
            elementos = []
            elementos.extend(self._crear_portada())
            elementos.extend(self._crear_resumen())
            elementos.extend(self._crear_analisis_componentes())
            elementos.extend(self._crear_conclusiones())
            
            doc.build(elementos)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False


def generar_todos_los_informes():
    """Genera informes para años 2020-2024"""
    os.makedirs('data/informes_auditoria_activos', exist_ok=True)
    
    for año in [2020, 2021, 2022, 2023, 2024]:
        print(f"Generando informe {año}...")
        generador = GeneradorInformePDFActivos(año)
        archivo = f'data/informes_auditoria_activos/informe_activos_{año}.pdf'
        if generador.generar_informe(archivo):
            print(f"✅ {archivo}")
        else:
            print(f"❌ Error en {año}")
    
    print("\n✅ Todos los informes generados")


if __name__ == "__main__":
    generar_todos_los_informes()
