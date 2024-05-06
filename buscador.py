import pandas as pd
import pytz
from datetime import datetime

direccion = "/home/pi/FlaskApp/registro/REGISTRO DE TARJETAS.xlsx"
#direccion = r'/home/pi/google-drive/REGISTRO DE TARJETAS.xlsx'
zona_horaria_ecuador = pytz.timezone('America/Guayaquil')

def obtener_fecha():
    return datetime.now(zona_horaria_ecuador).strftime("%Y-%m-%d")#("%d/%m/%Y")

def identificador(ip):
    #la ip llamada super_usuario tiene acceso a la lectura general
    lista_usuarios = {    
        'super_usuario': '192.168.1.51',
        'super_usuario2': '192.168.1.61',
        'JORGE FUENTES': '192.168.1.52', 
        'ARIEL MORETA': '192.168.1.54',
        'MAISSA CASTANEDA': '192.168.1.53',
        'KAREN CASTILLO': '192.168.1.57',
        'ADRIAN VERA': '192.168.1.56',
        'JEREMY CRUEL': '192.168.1.55',
        'MARIA SANTANA': '192.168.1.58',
        'test': '192.168.100.333'
        }
    
    for usuario, identificador in lista_usuarios.items():
        if ip == identificador:
            return usuario
    return False
    

#### escritura en excel ####

def escritura_excel(sector, semana, codigo, diagnostico,ibom, proyecto, observacion, usuario):

    fecha = obtener_fecha()
    try:
        df = pd.read_excel(direccion)
    except Exception as e:
        return f'Error al leer el archivo Excel: {str(e)}'

    if not df.empty and (df['CODIGO'] == codigo).any():
        return 'REPORTE DUPLICADO!!!'

    if df.empty:
        df = pd.DataFrame(columns=['REGISTRO', 'SECTOR','SEMANA', 'CODIGO', 'DIAGNOSTICO','COMPONENTES', 'PROYECTO', 'OBSERVACION', 'RESPONSABLE'])
    nueva_fila = {'REGISTRO': fecha, 'SECTOR': sector,'SEMANA':semana, 'CODIGO': codigo, 'DIAGNOSTICO': diagnostico,'COMPONENTES': ibom, 'PROYECTO': proyecto, 'OBSERVACION': observacion, 'RESPONSABLE': usuario}
    df = df.append(nueva_fila, ignore_index=True)

    try:
        df.to_excel(direccion, sheet_name='registro', index=False)
    except Exception as e:
        return f'Error al escribir en el archivo Excel: {str(e)}'
    
    return 'REPORTE EXITOSO'
    
### modificar registros ####

def modificar_registros(codigo, cambios, user):

    fecha = obtener_fecha()
    try:
        
        df = pd.read_excel(direccion)
        
        
        indice = df.index[df['CODIGO'] == codigo]
        
        
        if len(indice) == 0:
            return None
        
        
        indice = indice[0]
        
        if df.loc[indice, 'OBSERVACION'] in ['Reparada', 'Repuesto','Chatarra']:
            return False
        df.loc[indice, 'REGISTRO'] = fecha
        df.loc[indice, 'OBSERVACION'] = cambios
        df.loc[indice, 'RESPONSABLE'] = user
        
        
        df.to_excel(direccion, sheet_name='registro', index=False)
        
        return 'REPORTE EXITOSO'
    
    except Exception as e:
        return f'Error al modificar los registros: {str(e)}'
        
### eliminar registros guardados ####

def eliminar_registros(codigo):
    fecha = obtener_fecha()
    
    if not codigo:
        return 'ESCRIBIR CODIGO EN CELDA'

    try:
        df = pd.read_excel(direccion)
    except Exception as e:
        return f'Error al leer el archivo Excel: {str(e)}'

    if codigo not in df['CODIGO'].values:
        return 'CODIGO INEXISTENTE'

    if fecha not in df['REGISTRO'].values:
        return 'CODIGO FUERA DE RANGO'

    #df = df[(df['REGISTRO'] != fecha) | (df['CODIGO'] != codigo)]

    try:
        df = df[(df['REGISTRO'] != fecha) | (df['CODIGO'] != codigo)]
        if df.empty:
          return 'CODIGO FUERA DE RANGO'
          
        df.to_excel(direccion, sheet_name='registro', index=False)
        return 'REPORTE ELIMINADO!!'
    except Exception as e:
        return f'Error al escribir en el archivo Excel: {str(e)}'

### filtrar registros para visualizarlos ####

def filtrar_registros(codigo, name):
    if not codigo:
        return False, None
    
    data = pd.read_excel(direccion)
  
    if codigo:
        data_filtrado = data[data['CODIGO'] == codigo]
        if data_filtrado.empty:
            data_filtrado = data[(data['REGISTRO'] == codigo) & (data['RESPONSABLE'] == name)]
    else:
        data_filtrado = data[(data['REGISTRO'] == codigo) & (data['RESPONSABLE'] == name)]
        
    proyectos = ['ASP', 'AMA', 'ROBOTILSA']
    observaciones = ['Reparada', 'Repuesto', 'Chatarra']
    
    conteo = {}
    
    for proyecto in proyectos:
        conteo_proyecto = {}
        for observacion in observaciones:
            count = data_filtrado[(data_filtrado['OBSERVACION'] == observacion) & (data_filtrado['PROYECTO'] == proyecto)].shape[0]
            conteo_proyecto[observacion] = count
        conteo[proyecto] = conteo_proyecto
    
    if data_filtrado.empty:
        return None, conteo
    
    conteo_df = pd.DataFrame(conteo)
    

    
    return data_filtrado, conteo_df


#### modificar registros #### no  se usa xd 

def enviar_registros(codigo,sector, cambios):

    fecha = obtener_fecha()
    try:
        
        df = pd.read_excel(direccion)
               
        indice = df.index[df['CODIGO'] == codigo]
        

        if len(indice) == 0:
            return None
        
        indice = indice[0]
        
        if df.loc[indice, 'ESTADO'] in ['ENVIO']:
            return 'Registro consta como ENVIADO A CAMARONERA'
            
        df.loc[indice, 'REGISTRO'] = fecha
        df.loc[indice, 'SECTOR'] = sector
        df.loc[indice, 'ESTADO'] = cambios
        
        df.to_excel(direccion, sheet_name='registro', index=False)
        
        return 'Registros guardados exitosamente.'
    
    except Exception as e:
        return f'Error al modificar los registros: {str(e)}'



