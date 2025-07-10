"""
Utilidades para análisis y visualización de datos del sistema de monitoreo
Este script se ejecuta en PC para analizar los datos guardados del ESP32
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os

class DataAnalyzer:
    """Analizador de datos del sistema de monitoreo"""
    
    def __init__(self, data_file="Datalogger.txt"):
        self.data_file = data_file
        self.columns = [
            'year', 'month', 'day', 'hour', 'minute', 'second',
            'dht22_temp', 'dht22_humidity', 'multisensor_temp', 
            'multisensor_humidity', 'pm25', 'co2', 'voc'
        ]
    
    def load_data(self):
        """Carga los datos desde el archivo CSV"""
        try:
            # Cargar datos
            df = pd.read_csv(self.data_file, names=self.columns, header=None)
            
            # Crear timestamp
            df['timestamp'] = pd.to_datetime(df[['year', 'month', 'day', 'hour', 'minute', 'second']])
            
            # Limpiar datos inválidos
            df = df.replace([0, None], pd.NA)
            
            print(f"Datos cargados: {len(df)} registros")
            print(f"Rango de fechas: {df['timestamp'].min()} a {df['timestamp'].max()}")
            
            return df
            
        except Exception as e:
            print(f"Error al cargar datos: {e}")
            return None
    
    def plot_temperature_comparison(self, df, hours=24):
        """Gráfico comparativo de temperaturas"""
        # Filtrar últimas horas
        latest_time = df['timestamp'].max()
        start_time = latest_time - pd.Timedelta(hours=hours)
        recent_df = df[df['timestamp'] >= start_time].copy()
        
        plt.figure(figsize=(12, 6))
        plt.plot(recent_df['timestamp'], recent_df['dht22_temp'], 
                label='DHT22', marker='o', markersize=3)
        plt.plot(recent_df['timestamp'], recent_df['multisensor_temp'], 
                label='Multisensor', marker='s', markersize=3)
        
        plt.title(f'Comparación de Temperaturas - Últimas {hours} horas')
        plt.xlabel('Tiempo')
        plt.ylabel('Temperatura (°C)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return plt.gcf()
    
    def plot_air_quality(self, df, hours=24):
        """Gráfico de calidad del aire"""
        latest_time = df['timestamp'].max()
        start_time = latest_time - pd.Timedelta(hours=hours)
        recent_df = df[df['timestamp'] >= start_time].copy()
        
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
        
        # CO2
        ax1.plot(recent_df['timestamp'], recent_df['co2'], 'r-', marker='o', markersize=2)
        ax1.set_title('Concentración de CO2')
        ax1.set_ylabel('CO2 (ppm)')
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=1000, color='orange', linestyle='--', label='Límite recomendado')
        ax1.legend()
        
        # PM2.5
        ax2.plot(recent_df['timestamp'], recent_df['pm25'], 'brown', marker='s', markersize=2)
        ax2.set_title('Partículas PM2.5')
        ax2.set_ylabel('PM2.5 (μg/m³)')
        ax2.grid(True, alpha=0.3)
        ax2.axhline(y=25, color='red', linestyle='--', label='Límite OMS (24h)')
        ax2.legend()
        
        # VOC
        ax3.plot(recent_df['timestamp'], recent_df['voc'], 'green', marker='^', markersize=2)
        ax3.set_title('Compuestos Orgánicos Volátiles (VOC)')
        ax3.set_ylabel('VOC')
        ax3.set_xlabel('Tiempo')
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def generate_daily_report(self, df, date=None):
        """Genera un reporte diario"""
        if date is None:
            date = df['timestamp'].dt.date.max()
        
        daily_df = df[df['timestamp'].dt.date == date].copy()
        
        if daily_df.empty:
            print(f"No hay datos para la fecha {date}")
            return
        
        report = f"""
=== REPORTE DIARIO - {date} ===

Registros totales: {len(daily_df)}
Período: {daily_df['timestamp'].min().strftime('%H:%M')} - {daily_df['timestamp'].max().strftime('%H:%M')}

TEMPERATURA:
- DHT22: Promedio {daily_df['dht22_temp'].mean():.1f}°C (min: {daily_df['dht22_temp'].min():.1f}°C, max: {daily_df['dht22_temp'].max():.1f}°C)
- Multisensor: Promedio {daily_df['multisensor_temp'].mean():.1f}°C (min: {daily_df['multisensor_temp'].min():.1f}°C, max: {daily_df['multisensor_temp'].max():.1f}°C)

HUMEDAD:
- DHT22: Promedio {daily_df['dht22_humidity'].mean():.1f}% (min: {daily_df['dht22_humidity'].min():.1f}%, max: {daily_df['dht22_humidity'].max():.1f}%)
- Multisensor: Promedio {daily_df['multisensor_humidity'].mean():.1f}% (min: {daily_df['multisensor_humidity'].min():.1f}%, max: {daily_df['multisensor_humidity'].max():.1f}%)

CALIDAD DEL AIRE:
- CO2: Promedio {daily_df['co2'].mean():.0f} ppm (min: {daily_df['co2'].min():.0f}, max: {daily_df['co2'].max():.0f})
- PM2.5: Promedio {daily_df['pm25'].mean():.1f} μg/m³ (min: {daily_df['pm25'].min():.1f}, max: {daily_df['pm25'].max():.1f})
- VOC: Promedio {daily_df['voc'].mean():.2f} (min: {daily_df['voc'].min():.2f}, max: {daily_df['voc'].max():.2f})

ALERTAS:
"""
        
        # Verificar alertas
        if daily_df['co2'].max() > 1000:
            report += f"⚠️  CO2 elevado: Máximo {daily_df['co2'].max():.0f} ppm\n"
        
        if daily_df['pm25'].max() > 25:
            report += f"⚠️  PM2.5 elevado: Máximo {daily_df['pm25'].max():.1f} μg/m³\n"
        
        if daily_df['dht22_temp'].max() > 30:
            report += f"🌡️  Temperatura alta: Máximo {daily_df['dht22_temp'].max():.1f}°C\n"
        
        print(report)
        
        # Guardar reporte
        with open(f'reporte_{date}.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report

def main():
    """Función principal para análisis de datos"""
    analyzer = DataAnalyzer()
    
    # Verificar si existe el archivo
    if not os.path.exists(analyzer.data_file):
        print(f"Archivo {analyzer.data_file} no encontrado.")
        print("Coloca el archivo de datos del ESP32 en este directorio.")
        return
    
    # Cargar datos
    df = analyzer.load_data()
    if df is None:
        return
    
    # Generar gráficos
    print("Generando gráfico de temperaturas...")
    temp_fig = analyzer.plot_temperature_comparison(df, hours=24)
    temp_fig.savefig('temperaturas_24h.png', dpi=300, bbox_inches='tight')
    plt.close(temp_fig)
    
    print("Generando gráfico de calidad del aire...")
    air_fig = analyzer.plot_air_quality(df, hours=24)
    air_fig.savefig('calidad_aire_24h.png', dpi=300, bbox_inches='tight')
    plt.close(air_fig)
    
    # Generar reporte diario
    print("Generando reporte diario...")
    analyzer.generate_daily_report(df)
    
    print("\n✅ Análisis completado!")
    print("Archivos generados:")
    print("- temperaturas_24h.png")
    print("- calidad_aire_24h.png")
    print("- reporte_[fecha].txt")

if __name__ == "__main__":
    main()
