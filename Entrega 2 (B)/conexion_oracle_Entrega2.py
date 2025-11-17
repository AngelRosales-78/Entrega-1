import oracledb
oracledb.init_oracle_client(lib_dir=r"C:\oracle")
DSN = "localhost:1522/xe"
USER = "angel"
PASSWORD = "princhipesa"

def conectar():
    return oracledb.connect(user=USER, password=PASSWORD, dsn=DSN)

def crear_empleado(codigo, nombre, puesto, salario, dept):
    conn = conectar()
    cursor = conn.cursor()
    try:
        sql = """
            INSERT INTO EMPLEADOS (CODIGO, NOMBRE, PUESTO, FECHA_ING, SALARIO, COD_DEPT) 
            VALUES (:1, :2, :3, SYSDATE, :4, :5)
        """
        cursor.execute(sql, [codigo, nombre, puesto, salario, dept])
        conn.commit()
        print(f"[ÉXITO] Empleado '{nombre}' insertado correctamente.")
    except oracledb.Error as e:
        conn.rollback() 
        print(f"[ERROR] No se pudo insertar: {e}")
    finally:
        cursor.close()
        conn.close()

def leer_empleados():
    conn = conectar()
    cursor = conn.cursor()
    try:
        sql = """
            SELECT e.CODIGO, e.NOMBRE, e.PUESTO, e.SALARIO, d.DNOMBRE 
            FROM EMPLEADOS e 
            JOIN DEPARTAMENTOS d ON e.COD_DEPT = d.COD_DEPT
            ORDER BY e.CODIGO
        """
        cursor.execute(sql)
        print("\n" + "="*70)
        print(f"{'COD':<5} {'NOMBRE':<12} {'PUESTO':<15} {'SALARIO':<10} {'DEPARTAMENTO'}")
        print("-" * 70)
        for fila in cursor:
            print(f"{fila[0]:<5} {fila[1]:<12} {fila[2]:<15} {fila[3]:<10} {fila[4]}")
        print("="*70 + "\n")
    except oracledb.Error as e:
        print(f"[ERROR] Consulta fallida: {e}")
    finally:
        cursor.close()
        conn.close()

def actualizar_salario(codigo, nuevo_salario):
    conn = conectar()
    cursor = conn.cursor()
    try:
        sql = "UPDATE EMPLEADOS SET SALARIO = :1 WHERE CODIGO = :2"
        cursor.execute(sql, [nuevo_salario, codigo])
        conn.commit() # Confirmar transacción
        print(f"[ÉXITO] Salario del empleado {codigo} actualizado a {nuevo_salario}.")
    except oracledb.Error as e:
        conn.rollback()
        print(f"[ERROR] Actualización fallida: {e}")
    finally:
        cursor.close()
        conn.close()

def eliminar_empleado(codigo):
    conn = conectar()
    cursor = conn.cursor()
    try:
        sql = "DELETE FROM EMPLEADOS WHERE CODIGO = :1"
        cursor.execute(sql, [codigo])
        conn.commit() # Confirmar transacción
        print(f"[ÉXITO] Empleado {codigo} eliminado del sistema.")
    except oracledb.Error as e:
        conn.rollback()
        print(f"[ERROR] Eliminación fallida: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("--- INICIANDO DEMOSTRACIÓN DEL SISTEMA CRUD ---")

    print("1. Creando registro de prueba...")
    crear_empleado(9999, 'TEST_USER', 'DESARROLLADOR', 2500, 20)

    print("2. Listando empleados...")
    leer_empleados()

    print("3. Actualizando salario...")
    actualizar_salario(9999, 4500)

    input("Presiona ENTER para eliminar el registro y finalizar...")
    eliminar_empleado(9999)
    
    print("FIN DE LA DEMOSTRACIÓN")
