from flask import Flask,render_template, request,redirect,url_for,flash
from flask_mysqldb import MySQL

app= Flask(__name__)
app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= ''
app.config['MYSQL_DB']= 'bdpython'
app.secret_key= 'mysecretkey'

mysql= MySQL(app)



@app.route('/')
def Index():
    cursor= mysql.connection.cursor();
    cursor.execute('select * from albums')
    consulta= cursor.fetchall()

    return render_template('index.html',albums=consulta)

@app.route('/agregar',methods=['POST'])
def agreAlbum():
    if request.method == 'POST':
        vtitulo = request.form['txt_titulo']
        vartista = request.form['txt_artista']
        vanio = request.form['txt_anio']
        
        cursor= mysql.connection.cursor()
        cursor.execute('insert into albums(titulo,artista,anio) values(%s,%s,%s)', (vtitulo,vartista,vanio) )
        mysql.connection.commit()
        
        flash('Album agregado correctamente')
        return redirect(url_for('Index'))



@app.route('/editar/<id>')
def obtenerAlbum(id):
    cur = mysql.connection.cursor()
    cur.execute('select * from albums where id= %s',(id))
    consulta= cur.fetchall()
    return render_template('editarAlbum.html',album= consulta[0])

@app.route('/actualizar/<id>', methods= ['POST'])
def actualizar_album(id):
    if request.method == 'POST':
        Valbum= request.form['txt_titulo']
        Vartista= request.form['txt_artista']
        Vanio= request.form['txt_anio']
        
        cur = mysql.connection.cursor()
        cur.execute('update albums set titulo= %s, artista= %s, anio=%s where id= %s', (Valbum,Vartista,Vanio, id))
        mysql.connection.commit()
        
        flash('Album Actualizado en la BD')
        return redirect(url_for('Index'))



@app.route('/eliminar/<string:id>')
def elimAlbum(id):
    cur = mysql.connection.cursor()
    cur.execute('delete from albums where id ={0}'.format(id))
    mysql.connection.commit()
    flash('Album eliminado de la BD')
    return redirect(url_for('Index'))
    
    

if __name__ == '__main__':
    app.run(port= 3000,debug= True)


