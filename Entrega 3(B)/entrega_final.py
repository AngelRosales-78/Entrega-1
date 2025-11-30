import oracledb

DSN = "localhost:1521/xe"
USER = "angel"
PASSWORD = "princhipesa"

def conectar():
    return oracledb.connect(user=USER, password=PASSWORD, dsn=DSN)


def ver_reporte_vista():
    print("\n--- REPORTE GERENCIAL (Usando VISTA de Oracle) ---")
    conn = conectar()
    cursor = conn.cursor()
    try:
        
        cursor.execute("SELECT * FROM V_REPORTE_PLANILLA ORDER BY SALARIO DESC")
        
        print(f"{'NOMBRE':<12} {'PUESTO':<15} {'DEPARTAMENTO':<15} {'SUELDO':<10} {'ANUAL (x12)'}")
        print("-" * 75)
        for fila in cursor:
            print(f"{fila[1]:<12} {fila[2]:<15} {fila[3]:<15} {fila[4]:<10} {fila[5]}")
        print("-" * 75)
    except oracledb.Error as e:
        print(f"[ERROR] {e}")
    finally:
        cursor.close(); conn.close()


def ejecutar_aumento(puesto, porcentaje):
    print(f"\n--- EJECUTANDO PROCEDURE: Aumento del {porcentaje}% a {puesto} ---")
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.callproc('SP_AUMENTAR_POR_PUESTO', [puesto, porcentaje])
        print(" [ÉXITO] Oracle procesó el aumento correctamente.")
    except oracledb.Error as e:
        print(f" [ERROR] Falló el procedimiento: {e}")
    finally:
        cursor.close(); conn.close()


def crear_empleado_prueba():
    conn = conectar()
    cursor = conn.cursor()
    try:
        print("Creando empleado de prueba 'TRAMPA'")
        sql = "INSERT INTO EMPLEADOS (CODIGO, NOMBRE, PUESTO, FECHA_ING, SALARIO, COD_DEPT) VALUES (9999, 'TRAMPA', 'TEMPORAL', SYSDATE, 1000, 20)"
        cursor.execute(sql)
        conn.commit()
        print("Empleado creado.")
    except oracledb.Error as e:
        print(f" El empleado ya existía o hubo error: {e}")
    finally:
        cursor.close(); conn.close()

def eliminar_empleado_prueba():
    conn = conectar()
    cursor = conn.cursor()
    try:
        print("\nEliminando empleado 'TRAMPA'...")
        cursor.execute("DELETE FROM EMPLEADOS WHERE CODIGO = 9999")
        conn.commit()
        print("Empleado eliminado. (El Trigger debió guardar esto en auditoría)")
    except oracledb.Error as e:
        print(f"[ERROR] {e}")
    finally:
        cursor.close(); conn.close()


def ver_auditoria():
    conn = conectar()
    cursor = conn.cursor()
    try:
        print("\n--- TABLA SECRETA DE AUDITORÍA (Resultados del Trigger) ---")
        cursor.execute("SELECT NOMBRE_EMPLEADO, PUESTO_ANTIGUO, FECHA_DESPIDO, USUARIO_QUE_BORRO FROM AUDITORIA_DESPIDOS")
        print(f"{'EMPLEADO BORRADO':<20} {'PUESTO':<15} {'FECHA':<15} {'CULPABLE'}")
        print("-" * 70)
        for fila in cursor:
            print(f"{fila[0]:<20} {fila[1]:<15} {str(fila[2])[:10]:<15} {fila[3]}")
    except oracledb.Error as e:
        print(f"[ERROR] {e}")
    finally:
        cursor.close(); conn.close()


if __name__ == "__main__":
    while True:
        print("\n" + "="*40)
        print("   SISTEMA FINAL RRHH (ENTREGA 3)   ")
        print("="*40)
        print("1. Ver Reporte (VISTA)")
        print("2. Aumentar Sueldos (PROCEDURE)")
        print("3. Probar Trigger (Crear, Borrar y Auditar)")
        print("4. Salir")
        
        opcion = input("\nElige una opción: ")
        
        if opcion == "1":
            ver_reporte_vista()
        elif opcion == "2":
            p = input("Ingrese Puesto (ej. GERENTE, ANALISTA): ").upper()
            pct = float(input("Porcentaje % (ej. 10): "))
            ejecutar_aumento(p, pct)
            print("(Tip: Vuelve a la opción 1 para ver los nuevos sueldos)")
        elif opcion == "3":
            crear_empleado_prueba()
            input("Presiona ENTER para borrarlo y activar el Trigger...")
            eliminar_empleado_prueba()
            ver_auditoria()
        elif opcion == "4":
            print("Cerrando sistema...")
            break
        else:
            print("Opción no válida")