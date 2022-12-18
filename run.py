from flask import Flask,render_template, request, redirect
import pymysql

app = Flask(__name__)

# menghubungkan mysql
db = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'akademik'
)

# tampilan home
@app.route('/')
def home():
    return render_template('home.html')

# ================================================================================================== 
# menampilkan data jurusan
@app.route('/jurusan')
def list_jurusan():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tb_jurusan")
    result = cursor.fetchall()

    return render_template('list_jurusan.html', data=result)

# input data jurusan
@app.route('/jurusan/add_jurusan', methods =['GET', 'POST'])
def add_jurusan():
    if request.method == 'POST':
        data            = request.form
        kode_jurusan    = data['kode_jurusan']
        jurusan         = data['jurusan']
        kaprodi         = data['kaprodi']

        cursor = db.cursor()
        query  = f"""INSERT INTO tb_jurusan (
                kode_jurusan, jurusan, kaprodi)
                VALUES ('{kode_jurusan}', '{jurusan}', '{kaprodi}')"""
        
        cursor.execute(query)
        db.commit()

        return redirect('/jurusan', code=302, Response=None)

    return render_template('add_jurusan.html')

#  Update Jurusan
@app.route('/jurusan/edit_jurusan/<kode_jurusan>', methods=['GET', 'POST'])
def edit_jurusan(kode_jurusan):
    if request.method == "GET":

        cursor= db.cursor()
        cursor.execute("""
        SELECT * FROM tb_jurusan
        WHERE kode_jurusan=%s""",(kode_jurusan))
        jurusan = cursor.fetchone()
        cursor.close()

        return render_template('edit_jurusan.html', jurusan=jurusan)
    else:
        if request.method == 'POST':   
            kode_jurusan  = request.values.get('kode_jurusan')    
            jurusan       = request.values.get('jurusan')    
            kaprodi       = request.values.get('kaprodi')    

            query = f"""UPDATE tb_jurusan SET kode_jurusan = '{kode_jurusan}', jurusan = '{jurusan}', kaprodi = '{kaprodi}'
                    WHERE kode_jurusan = '{kode_jurusan}'"""
            cursor = db.cursor()
            cursor.execute(query)
            db.commit()

            return redirect('/jurusan')

    return render_template('list_jurusan.html')

# Delete data jurusan
@app.route('/jurusan/hapus_jurusan/<kode_jurusan>')
def hps_jurusan(kode_jurusan):
    cursor = db.cursor()
    query = f"DELETE FROM tb_jurusan WHERE kode_jurusan='{kode_jurusan}'"
    cursor.execute(query)
    db.commit()

    return redirect('/jurusan', code=302, Response=None)

# =============================================================================================

# menampilkan data mahasiswa
@app.route('/mahasiswa')
def list_mhs():
    cursor = db.cursor()
    query = f"""SELECT tb_mahasiswa.nim, tb_mahasiswa.nama_mahasiswa,tb_jurusan.jurusan, tb_mahasiswa.jenis_kelamin, tb_mahasiswa.tempat_lahir, tb_mahasiswa.tanggal_lahir, tb_mahasiswa.alamat
            FROM tb_mahasiswa, tb_jurusan
            WHERE tb_mahasiswa.kode_jurusan=tb_jurusan.kode_jurusan"""
    cursor.execute(query)
    result = cursor.fetchall()

    return render_template('list_mhs.html', data=result)

# input data mahasiswa
@app.route('/mahasiswa/add_mhs', methods =['GET', 'POST'])
def add_mhs():
    if request.method == 'POST':
        data            = request.form
        nim             = data['nim']
        nama_mahasiswa  = data['nama_mahasiswa']
        jenis_kelamin   = data['jenis_kelamin']
        tempat_lahir    = data['tempat_lahir']
        tanggal_lahir   = data['tanggal_lahir']
        kode_jurusan    = data['kode_jurusan']
        alamat          = data['alamat']

        cursor = db.cursor()
        query = f"""INSERT INTO tb_mahasiswa (
            nim, kode_jurusan, nama_mahasiswa, jenis_kelamin, tempat_lahir, tanggal_lahir, alamat)
            VALUES ('{nim}', '{kode_jurusan}', '{nama_mahasiswa}', '{jenis_kelamin}', '{tempat_lahir}',
            '{tanggal_lahir}', '{alamat}')"""
        
        cursor.execute(query)
        db.commit()

        return redirect('/mahasiswa', code=302, Response=None)

    return render_template('add_mhs.html')

# Update data mahasiswa
@app.route('/mahasiswa/edit_mhs/<nim>', methods=['GET', 'POST'])
def edit_mhs(nim):
    if request.method == "GET":

        cursor= db.cursor()
        cursor.execute("""
        SELECT * FROM tb_mahasiswa
        WHERE nim=%s""",(nim,))
        mhs = cursor.fetchone()
        cursor.close()

        return render_template('edit_mhs.html', mhs=mhs)
    else:
        if request.method == 'POST':
            nim           = request.values.get('nim')    
            kode_jurusan  = request.values.get('kode_jurusan')    
            nama_mahasiswa= request.values.get('nama_mahasiswa')    
            jenis_kelamin = request.values.get('jenis_kelamin')    
            tempat_lahir  = request.values.get('tempat_lahir')    
            tanggal_lahir = request.values.get('tanggal_lahir')    
            alamat        = request.values.get('alamat')

            query = f"""UPDATE tb_mahasiswa SET nim='{nim}', kode_jurusan = '{kode_jurusan}', nama_mahasiswa = '{nama_mahasiswa}',
            jenis_kelamin = '{jenis_kelamin}',tempat_lahir = '{tempat_lahir}',tanggal_lahir = '{tanggal_lahir}',alamat = '{alamat}'
            WHERE nim = '{nim}'"""
            cursor = db.cursor()
            cursor.execute(query)
            db.commit()
            
        return redirect('/mahasiswa')

    return render_template('mahasiswa.html')

# Delete data mahasiswa
@app.route('/mahasiswa/hapus_mhs/<nim>')
def hps_mhs(nim):
    cursor = db.cursor()
    query = f"DELETE FROM tb_mahasiswa WHERE nim='{nim}'"
    cursor.execute(query)
    db.commit()

    return redirect('/mahasiswa', code=302, Response=None)


# ================================================================
# menampilkan data dosen 
@app.route('/dosen')
def list_dosen():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tb_dosen")
    result = cursor.fetchall()

    return render_template('list_dosen.html', data=result)

# input data dosen
@app.route('/dosen/add_dosen', methods =['GET', 'POST'])
def add_dosen():
    if request.method == 'POST':
        data            = request.form
        nidn            = data['nidn']
        nama_dosen      = data['nama_dosen']
        jenis_kelamin   = data['jenis_kelamin']
        tempat_lahir    = data['tempat_lahir']
        tanggal_lahir   = data['tanggal_lahir']
        alamat          = data['alamat']

        cursor = db.cursor()
        query = f"""INSERT INTO tb_dosen (
            nidn, nama_dosen, jenis_kelamin, tempat_lahir, tanggal_lahir, alamat)
            VALUES ('{nidn}', '{nama_dosen}', '{jenis_kelamin}', '{tempat_lahir}',
            '{tanggal_lahir}', '{alamat}')"""
        
        cursor.execute(query)
        db.commit()

        return redirect('/dosen', code=302, Response=None)

    return render_template('add_dosen.html')

# Update data Dosen
@app.route('/dosen/edit_dosen/<nidn>', methods=['GET', 'POST'])
def edit_dosen(nidn):
    if request.method == "GET":

        cursor= db.cursor()
        cursor.execute("""
        SELECT * FROM tb_dosen
        WHERE nidn=%s""",(nidn,))
        data = cursor.fetchone()
        cursor.close()

        return render_template('edit_dosen.html', dosen=data)
    else:
        if request.method == 'POST':
            nidn          = request.values.get('nidn')    
            nama_dosen    = request.values.get('nama_dosen')    
            jenis_kelamin = request.values.get('jenis_kelamin')    
            tempat_lahir  = request.values.get('tempat_lahir')    
            tanggal_lahir = request.values.get('tanggal_lahir')    
            alamat        = request.values.get('alamat')

            query = f"""UPDATE tb_dosen SET nidn='{nidn}', nama_dosen = '{nama_dosen}',
            jenis_kelamin = '{jenis_kelamin}',tempat_lahir = '{tempat_lahir}',tanggal_lahir = '{tanggal_lahir}',alamat = '{alamat}'
            WHERE nidn = '{nidn}'"""
            cursor = db.cursor()
            cursor.execute(query)
            db.commit()
            
        return redirect('/dosen')

    return render_template('list_dosen.html')

# Delete data dosen
@app.route('/dosen/hapus_dosen/<nidn>')
def hps_dosen(nidn):
    cursor = db.cursor()
    query = f"DELETE FROM tb_dosen WHERE nidn='{nidn}'"
    cursor.execute(query)
    db.commit()

    return redirect('/dosen', code=302, Response=None)

#==========================================================================
# menampilkan data mata kuliah
@app.route('/matkul')
def list_makul():
    cursor = db.cursor()
    query  = f"""SELECT tb_mata_kuliah.kode_mata_kuliah, tb_mata_kuliah.mata_kuliah, tb_dosen.nama_dosen, tb_mata_kuliah.sks
            FROM tb_mata_kuliah, tb_dosen
            WHERE tb_mata_kuliah.nidn=tb_dosen.nidn"""
    # cursor.execute("SELECT * FROM tb_mata_kuliah")
    cursor.execute(query)
    result = cursor.fetchall()

    return render_template('list_matkul.html', data=result)

# input data mata kuliah
@app.route('/matkul/add_matkul', methods =['GET', 'POST'])
def add_matkul():
    if request.method == 'POST':
        data             = request.form
        kode_mata_kuliah = data['kode_mata_kuliah']
        nidn             = data['nidn']
        mata_kuliah      = data['mata_kuliah']
        sks              = data['sks']

        cursor = db.cursor()
        query  = f"""INSERT INTO tb_mata_kuliah (
                kode_mata_kuliah, nidn, mata_kuliah,sks)
                VALUES ('{kode_mata_kuliah}', '{nidn}', '{mata_kuliah}', '{sks}')"""
        
        cursor.execute(query)
        db.commit()

        return redirect('/matkul', code=302, Response=None)

    return render_template('add_matkul.html')

#  Update mata kuliah
@app.route('/matkul/edit_matkul/<kode_mata_kuliah>', methods=['GET', 'POST'])
def edit_matkul(kode_mata_kuliah):
    if request.method == "GET":

        cursor= db.cursor()
        cursor.execute("""
        SELECT * FROM tb_mata_kuliah
        WHERE kode_mata_kuliah=%s""",(kode_mata_kuliah))
        matkul = cursor.fetchone()
        cursor.close()

        return render_template('edit_matkul.html', matkul=matkul)
    else:
        if request.method == 'POST':   
            kode_mata_kuliah  = request.values.get('kode_mata_kuliah')    
            nidn              = request.values.get('nidn')    
            mata_kuliah       = request.values.get('mata_kuliah')    
            sks               = request.values.get('sks')    

            query = f"""UPDATE tb_mata_kuliah SET kode_mata_kuliah = '{kode_mata_kuliah}', nidn = '{nidn}', mata_kuliah = '{mata_kuliah}', sks = '{sks}'
                    WHERE kode_mata_kuliah = '{kode_mata_kuliah}'"""
            cursor = db.cursor()
            cursor.execute(query)
            db.commit()

            return redirect('/matkul')

    return render_template('list_matkul.html')

# Delete data mata kuliah
@app.route('/matkul/hapus_matkul/<kode_mata_kuliah>')
def hps_matkul(kode_mata_kuliah):
    cursor = db.cursor()
    query = f"DELETE FROM tb_mata_kuliah WHERE kode_mata_kuliah='{kode_mata_kuliah}'"
    cursor.execute(query)
    db.commit()

    return redirect('/matkul', code=302, Response=None)


# ======================================================================================
# menampilkan data nilai
@app.route('/nilai')
def list_nilai():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tb_nilai")
    result = cursor.fetchall()

    return render_template('list_nilai.html', data=result)

# input data nilai
@app.route('/nilai/add_nilai', methods =['GET', 'POST'])
def add_nilai():
    if request.method == 'POST':
        data            = request.form
        nim             = data['nim']
        kode_mata_kuliah= data['kode_mata_kuliah']
        absen           = data['absen']
        tugas           = data['tugas']
        uts             = data['uts']
        uas             = data['uas']

        cursor = db.cursor()
        query = f"""INSERT INTO tb_nilai (
            nim, kode_mata_kuliah, absen, tugas, uts, uas)
            VALUES ('{nim}', '{kode_mata_kuliah}', '{absen}', '{tugas}',
            '{uts}', '{uas}')"""
        
        cursor.execute(query)
        db.commit()

        return redirect('/nilai', code=302, Response=None)

    return render_template('add_nilai.html')

#  Update data nilai
@app.route('/nilai/edit_nilai/<id_nilai>', methods=['GET', 'POST'])
def edit_nilai(id_nilai):
    if request.method == "GET":

        cursor= db.cursor()
        cursor.execute("""
        SELECT * FROM tb_nilai
        WHERE id_nilai=%s""",(id_nilai))
        nilai = cursor.fetchone()
        cursor.close()

        return render_template('edit_nilai.html', nilai=nilai)
    else:
        if request.method == 'POST':   
            id_nilai         = request.values.get('id_nilai')    
            nim              = request.values.get('nim')    
            kode_mata_kuliah = request.values.get('kode_mata_kuliah')    
            absen            = request.values.get('absen')    
            tugas            = request.values.get('tugas')    
            uts              = request.values.get('uts')    
            uas              = request.values.get('uas')    

            query = f"""UPDATE tb_nilai SET id_nilai = '{id_nilai}', nim = '{nim}', kode_mata_kuliah = '{kode_mata_kuliah}', 
                    absen = '{absen}', tugas = '{tugas}', uts = '{uts}', uas = '{uas}'
                    WHERE id_nilai = '{id_nilai}'"""
            cursor = db.cursor()
            cursor.execute(query)
            db.commit()

            return redirect('/nilai')

    return render_template('list_nilai.html')

# Delete data mata kuliah
@app.route('/nilai/hapus_nilai/<id_nilai>')
def hps_nilai(id_nilai):
    cursor = db.cursor()
    query = f"DELETE FROM tb_nilai WHERE id_nilai='{id_nilai}'"
    cursor.execute(query)
    db.commit()

    return redirect('/nilai', code=302, Response=None)

# ========================================================================================
#  Menampilkan data KHS
@app.route('/khs')
def list_khs():
    cursor = db.cursor()
    query  = f"""SELECT
                tb_nilai.id_nilai, 
                tb_mahasiswa.nim, tb_mahasiswa.nama_mahasiswa,
                tb_mata_kuliah.mata_kuliah, tb_mata_kuliah.sks,
                tb_nilai.absen, tb_nilai.tugas, tb_nilai.uts, tb_nilai.uas,
                (0.1*tb_nilai.absen)+(0.2*tb_nilai.tugas)+(0.3*tb_nilai.uts)+(0.4*tb_nilai.uas) as total
                FROM (select * from tb_nilai where nim = 204855041) as tb_nilai
                join tb_mahasiswa on (tb_mahasiswa.nim = tb_nilai.nim)
                join tb_mata_kuliah on (tb_mata_kuliah.kode_mata_kuliah = tb_nilai.kode_mata_kuliah)
                join tb_dosen on (tb_dosen.nidn = tb_mata_kuliah.nidn)
                join tb_jurusan on (tb_jurusan.kode_jurusan = tb_mahasiswa.kode_jurusan)
            """

    cursor.execute(query)
    result = cursor.fetchall()
    # cursor.close()

    return render_template('khs.html', khs=result)

@app.route('/khs/print')
def print():
    cursor = db.cursor()
    query  = f"""SELECT
                tb_nilai.id_nilai, 
                tb_mahasiswa.nim, tb_mahasiswa.nama_mahasiswa,
                tb_mata_kuliah.mata_kuliah, tb_mata_kuliah.sks,
                tb_nilai.absen, tb_nilai.tugas, tb_nilai.uts, tb_nilai.uas,
                (0.1*tb_nilai.absen)+(0.2*tb_nilai.tugas)+(0.3*tb_nilai.uts)+(0.4*tb_nilai.uas) as total
                FROM (select * from tb_nilai where nim = 204855040) as tb_nilai
                join tb_mahasiswa on (tb_mahasiswa.nim = tb_nilai.nim)
                join tb_mata_kuliah on (tb_mata_kuliah.kode_mata_kuliah = tb_nilai.kode_mata_kuliah)
                join tb_dosen on (tb_dosen.nidn = tb_mata_kuliah.nidn)
                join tb_jurusan on (tb_jurusan.kode_jurusan = tb_mahasiswa.kode_jurusan)"""

    cursor.execute(query)
    result = cursor.fetchall()
    # cursor.close()
    return render_template('print.html', khs=result)


#  Menampilkan data KHS
@app.route('/test', methods=["GET", "POST"] )
def tset():
    if request.method == 'GET': 
        cursor = db.cursor()
        cari= (f"SELECT nim,nama_mahasiswa FROM tb_mahasiswa")
        cursor.execute(cari)
        result = cursor.fetchall()

        return render_template('test.html',cari=result)

    else:
        nim = request.form ['nim']
        cursor = db.cursor()
        cursor.execute(f"""
        SELECT tb_mahasiswa.nim,tb_mahasiswa.nama_mahasiswa,tb_jurusan.jurusan, 
        tb_mata_kuliah.sks,tb_mata_kuliah.mata_kuliah,tb_dosen.nama_dosen,tb_nilai.absen,
        tb_nilai.tugas,tb_nilai.uts,tb_nilai.uas,
        (0.1*tb_nilai.absen)+(0.2*tb_nilai.tugas)+(0.3*tb_nilai.uts)+(0.4*tb_nilai.uas) as total 
        FROM (select * from tb_nilai where nim = {nim} ) as tb_nilai
        join tb_mahasiswa on (tb_mahasiswa.nim = tb_nilai.nim)
        join tb_mata_kuliah on (tb_mata_kuliah.kode_mata_kuliah = tb_nilai.kode_mata_kuliah)
        join tb_dosen on (tb_dosen.nidn = tb_mata_kuliah.nidn)
        join tb_jurusan on (tb_jurusan.kode_jurusan = tb_mahasiswa.kode_jurusan);
        """)
        khs = cursor.fetchall()
        
        cursor.execute(f"SELECT * FROM tb_mahasiswa WHERE nim={nim}")
        mhs=cursor.fetchone()
        cursor.execute(f"SELECT nim,nama_mahasiswa FROM tb_mahasiswa")
        mh=cursor.fetchall() 

        # print(mh)
        # print(mhs)
        # print(khs)

        context = {
             'cari' : mh,
             'data' : khs,
             'mhs' :mhs
        }
        return render_template('test.html', data=context)

    
if __name__ == '__main__':
    app.run(debug=True)