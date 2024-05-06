from flask import Flask, render_template, request
import buscador as bus

app = Flask(__name__)

#obtiene las ip's que se conectan al router

def usuarios():
    ip_user = request.remote_addr
    usuario = bus.identificador(ip_user)
    return usuario

def escritura_excel():
    # obtener datos del formulario
    usuario = usuarios()
    semana = (request.form.get('semana'))
    sector = request.form.get('sector')
    codigo = request.form.get('codigo')
    diagnostico = request.form.get('diagnostico')
    ibom = request.form.get('ibom')
    proyecto = request.form.get('proyecto')
    observacion = request.form.get('observacion')

    if not (sector and semana and codigo and diagnostico and ibom and proyecto and observacion):
        return 'COMPLETAR CAMPOS RESPECTIVOS'

    try:     
        sector = sector.upper().strip()
        codigo = codigo.upper().strip()
        ibom = ibom.upper().strip()
        
        write = bus.escritura_excel(sector, semana, codigo, diagnostico,ibom, proyecto, observacion, usuario)
        
        return write

    except ValueError as e:
        
        pass
    return 'Error al procesar la solicitud'

### lecturar registros ###

def lectura_excel():
    user = usuarios()
    codigo = request.form.get('code')
    name = request.form.get('name', user)
    name = True if name == 'GENERAL' else name
    resultado, conteo = bus.filtrar_registros(codigo, name)
    if resultado is None:
        return None, None
    return resultado , conteo
    
###### envio de informes por ws ###### 

def membrete():
    user = usuarios()
    fecha = request.form.get('code')
    responsable = f'{fecha} - {user}'
    return responsable
    
    
###### templates ###### 

@app.route('/', methods=['GET', 'POST'])
def index():
    registro = usuarios()
    if registro == 'super_usuario':
        return render_template('super_index.html')
    elif registro == 'super_usuario2':
        return render_template('super_index.html')
    elif registro is False:
        return render_template('final.html', registro = 'SIN ACCESO :/')
    else:
        return render_template('index.html', registro = registro)

@app.route('/reporte', methods=['POST'])
def reporte_diario():
    return render_template('final.html', registro = escritura_excel())
    
    
@app.route('/eliminar', methods=['POST'])
def eliminar():
    codigo = request.form['delete']
    return render_template('final.html', registro = bus.eliminar_registros(codigo))    

       
@app.route('/lecturas', methods=['POST'])
def lectura():
    
    registro, conteo = lectura_excel()
    responsable = membrete()
    if registro is False:
        return render_template('final.html', registro='COMPLETAR CAMPOS RESPECTIVOS')
    elif registro is None:
        return render_template('final.html', registro='CODIGO INEXISTENTE', responsable = responsable)
    else:
        return render_template('dataframe.html', table=registro.to_html(classes='table table-striped',index = False), resumen=conteo.to_html(classes='table table-striped'), responsable = responsable)#index = False

        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
    
    
    
    
    
    
    
    
    
    








'''    
@app.route('/modificar', methods=['POST'])
def modificacion():
    user = usuarios()
    codigo = request.form['code_modificacion']
    cambios = request.form['modificacion']
    registro = bus.modificar_registros(codigo,cambios,user)
    if registro is False:
        return render_template('final.html', registro = 'REPORTE DUPLICADO!!')
    if registro is None:
        return render_template('final.html', registro = 'CODIGO INEXISTENTE!!')
    else:
        return render_template('final.html', registro = registro)'''
    
    