import oracledb

oracledb.init_oracle_client(lib_dir=r"C:\oracle")

usuario = "angel"
contrasena = "princhipesa"
dsn = "localhost:1522/xe"

try:
    conexion = oracledb.connect(user=usuario, password=contrasena, dsn=dsn)
    print("Conexión exitosa a Oracle.")

    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM empleados")

    for fila in cursor:
        print(fila)

except oracledb.Error as error:
    print("Error al conectar o consultar:", error)

finally:
    try:
        cursor.close()
        conexion.close()
    except:
        pass
