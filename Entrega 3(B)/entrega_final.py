import oracledb

DSN = "localhost:1521/xe"
USER = "angel"
PASSWORD = "princhipesa"

def conectar():
    return oracledb.connect(user=USER, password=PASSWORD, dsn=DSN)

def ver_reporte_vista():
    print("\n--- REPORTE DE PLANILLA (VISTA) ---")
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM V_REPORTE_PLANILLA ORDER BY SALARIO DESC")
        
        print(f"{'NOMBRE':<12} {'PUESTO':<15} {'DEPARTAMENTO':<15} {'SUELDO':<10} {'ANUAL'}")
        print("-" * 65)
        for fila in cursor:
            print(f"{fila[1]:<12} {fila[2]:<15} {fila[3]:<15} {fila[4]:<10} {fila[5]}")
    except oracledb.Error as e:
        print(f"Error al consultar vista: {e}")
    finally:
        cursor.close()
        conn.close()

def ejecutar_aumento(puesto, porcentaje):
    print(f"\n--- EJECUTANDO PROCEDURE: Aumento del {porcentaje}% a {puesto} ---")
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.callproc('SP_AUMENTAR_POR_PUESTO', [puesto, porcentaje])
        print("Proceso completado correctamente en la base de datos.")
    except oracledb.Error as e:
        print(f"Error en el procedimiento: {e}")
    finally:
        cursor.close()
        conn.close()

def crear_empleado_manual():
    print("\n--- REGISTRO DE NUEVO EMPLEADO ---")
    conn = conectar()
    cursor = conn.cursor()
    try:
        cod = int(input("Codigo (ej. 7999): "))
        nom = input("Nombre: ").upper()
        puesto = input("Puesto: ").upper()
        sal = float(input("Salario: "))
        dept = int(input("Codigo Depto (10, 20 o 30): "))
        
        sql = "INSERT INTO EMPLEADOS (CODIGO, NOMBRE, PUESTO, FECHA_ING, SALARIO, COD_DEPT) VALUES (:1, :2, :3, SYSDATE, :4, :5)"
        cursor.execute(sql, [cod, nom, puesto, sal, dept])
        conn.commit()
        print(f"Empleado {nom} registrado exitosamente.")
    except oracledb.Error as e:
        print(f"Error al registrar: {e}")
    finally:
        cursor.close()
        conn.close()

def crear_empleado_trampa():
    conn = conectar()
    cursor = conn.cursor()
    try:
        print("\nCreando empleado de prueba 'TRAMPA'...")
        sql = "INSERT INTO EMPLEADOS (CODIGO, NOMBRE, PUESTO, FECHA_ING, SALARIO, COD_DEPT) VALUES (9999, 'TRAMPA', 'TEMPORAL', SYSDATE, 1000, 20)"
        cursor.execute(sql)
        conn.commit()
        print("Empleado de prueba creado.")
    except oracledb.Error as e:
        print(f"Error (quizas ya existe): {e}")
    finally:
        cursor.close()
        conn.close()

def eliminar_empleado_trampa():
    conn = conectar()
    cursor = conn.cursor()
    try:
        print("Eliminando empleado TRAMPA")
        cursor.execute("DELETE FROM EMPLEADOS WHERE CODIGO = 9999")
        conn.commit()
        print("Empleado eliminado. Verificando auditoria...")
    except oracledb.Error as e:
        print(f"Error al eliminar: {e}")
    finally:
        cursor.close()
        conn.close()

def ver_auditoria():
    conn = conectar()
    cursor = conn.cursor()
    try:
        print(" REGISTROS DE AUDITORIA (TRIGGER)")
        cursor.execute("SELECT NOMBRE_EMPLEADO, PUESTO_ANTIGUO, FECHA_DESPIDO, USUARIO_QUE_BORRO FROM AUDITORIA_DESPIDOS ORDER BY ID_AUDIT DESC")
        print(f"{'EMPLEADO':<15} {'PUESTO':<15} {'FECHA':<15} {'USUARIO'}")
        print("-" * 60)
        for fila in cursor:
            print(f"{fila[0]:<15} {fila[1]:<15} {str(fila[2])[:10]:<15} {fila[3]}")
    except oracledb.Error as e:
        print(f"Error al consultar auditoria: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    while True:
        print("SISTEMA DE GESTION DE RRHH - ENTREGA 3")
        print("1) Ver Reporte General (Vista)")
        print("2) Aumentar Sueldos (Procedure)")
        print("3) Registrar Nuevo Empleado")
        print("4) Prueba de Auditoria (Trigger)")
        print("5) Salir")
        
        opcion = input("\nSeleccione una opcion: ")
        
        if opcion == "1":
            ver_reporte_vista()
        elif opcion == "2":
            p = input("Ingrese Puesto (ej. ANALISTA): ").upper()
            pct = float(input("Porcentaje de aumento (ej. 10): "))
            ejecutar_aumento(p, pct)
        elif opcion == "3":
            crear_empleado_manual()
        elif opcion == "4":
            crear_empleado_trampa()
            input("Presione ENTER para borrarlo y activar el Trigger")
            eliminar_empleado_trampa()
            ver_auditoria()
        elif opcion == "5":
            print("Saliendo del sistema")
            break
        else:
            print("Opcion no valida intente de nuevo")