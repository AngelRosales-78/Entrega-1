import tkinter as tk
from tkinter import ttk, messagebox
import oracledb

DSN = "localhost:1521/xe"
USER = "angel"
PASSWORD = "princhipesa"

def conectar():
    return oracledb.connect(user=USER, password=PASSWORD, dsn=DSN)

def obtener_datos_vista():
    lista = []
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM V_REPORTE_PLANILLA ORDER BY SALARIO DESC")
        for fila in cursor:
            lista.append(fila)
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Error de conexión: {e}")
    return lista

def obtener_auditoria():
    lista = []
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT NOMBRE_EMPLEADO, PUESTO_ANTIGUO, FECHA_DESPIDO, USUARIO_QUE_BORRO FROM AUDITORIA_DESPIDOS ORDER BY ID_AUDIT DESC")
        for fila in cursor:
            lista.append(fila)
        conn.close()
    except Exception as e:
        pass
    return lista

def db_aumentar_sueldo(puesto, porcentaje):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.callproc('SP_AUMENTAR_POR_PUESTO', [puesto, porcentaje])
        conn.close()
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Fallo en Procedure: {e}")
        return False

def db_registrar_empleado(cod, nom, puesto, sal, dept):
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "INSERT INTO EMPLEADOS (CODIGO, NOMBRE, PUESTO, FECHA_ING, SALARIO, COD_DEPT) VALUES (:1, :2, :3, SYSDATE, :4, :5)"
        cursor.execute(sql, [cod, nom, puesto, sal, dept])
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo registrar: {e}")
        return False

def db_simular_trampa():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO EMPLEADOS (CODIGO, NOMBRE, PUESTO, FECHA_ING, SALARIO, COD_DEPT) VALUES (9999, 'TRAMPA', 'TEMPORAL', SYSDATE, 1000, 20)")
        cursor.execute("DELETE FROM EMPLEADOS WHERE CODIGO = 9999")
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Error en simulación: {e}")
        return False

class AplicacionRRHH:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión RRHH")
        self.root.geometry("900x600")
        
        style = ttk.Style()
        style.theme_use('clam')

        tab_control = ttk.Notebook(root)
        
        self.tab1 = ttk.Frame(tab_control)
        self.tab2 = ttk.Frame(tab_control)
        self.tab3 = ttk.Frame(tab_control)
        
        tab_control.add(self.tab1, text='Reporte General')
        tab_control.add(self.tab2, text='Gestion de Personal')
        tab_control.add(self.tab3, text='Auditoria')
        
        tab_control.pack(expand=1, fill="both")
        
        self.crear_tab_reporte()
        self.crear_tab_gestion()
        self.crear_tab_auditoria()

    def crear_tab_reporte(self):
        frame_top = ttk.Frame(self.tab1)
        frame_top.pack(pady=10)
        btn = ttk.Button(frame_top, text="Actualizar Tabla", command=self.cargar_tabla_reporte)
        btn.pack()

        cols = ('NOMBRE', 'PUESTO', 'DEPTO', 'SUELDO', 'ANUAL')
        self.tree_reporte = ttk.Treeview(self.tab1, columns=cols, show='headings')
        
        for col in cols:
            self.tree_reporte.heading(col, text=col)
            self.tree_reporte.column(col, width=150)
            
        self.tree_reporte.pack(expand=True, fill='both', padx=10, pady=10)
        self.cargar_tabla_reporte()

    def cargar_tabla_reporte(self):
        for i in self.tree_reporte.get_children():
            self.tree_reporte.delete(i)
        datos = obtener_datos_vista()
        for fila in datos:
            valores = (fila[1], fila[2], fila[3], f"S/. {fila[4]}", f"S/. {fila[5]}")
            self.tree_reporte.insert("", "end", values=valores)

    def crear_tab_gestion(self):
        frame_aumento = ttk.LabelFrame(self.tab2, text="Aumento de Sueldo")
        frame_aumento.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(frame_aumento, text="Puesto:").grid(row=0, column=0, padx=5, pady=5)
        self.txt_puesto_aum = ttk.Entry(frame_aumento)
        self.txt_puesto_aum.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_aumento, text="Porcentaje %:").grid(row=0, column=2, padx=5, pady=5)
        self.txt_pct_aum = ttk.Entry(frame_aumento, width=10)
        self.txt_pct_aum.grid(row=0, column=3, padx=5, pady=5)
        
        btn_aum = ttk.Button(frame_aumento, text="Aplicar Aumento", command=self.accion_aumento)
        btn_aum.grid(row=0, column=4, padx=20, pady=5)

        frame_reg = ttk.LabelFrame(self.tab2, text="Registrar Nuevo Empleado")
        frame_reg.pack(fill="both", expand=True, padx=20, pady=10)

        ttk.Label(frame_reg, text="Codigo:").grid(row=0, column=0, padx=5, pady=5)
        self.ent_cod = ttk.Entry(frame_reg); self.ent_cod.grid(row=0, column=1)

        ttk.Label(frame_reg, text="Nombre:").grid(row=1, column=0, padx=5, pady=5)
        self.ent_nom = ttk.Entry(frame_reg); self.ent_nom.grid(row=1, column=1)

        ttk.Label(frame_reg, text="Puesto:").grid(row=2, column=0, padx=5, pady=5)
        self.ent_puesto = ttk.Entry(frame_reg); self.ent_puesto.grid(row=2, column=1)

        ttk.Label(frame_reg, text="Salario:").grid(row=3, column=0, padx=5, pady=5)
        self.ent_sal = ttk.Entry(frame_reg); self.ent_sal.grid(row=3, column=1)

        ttk.Label(frame_reg, text="Cod Depto (10, 20, 30):").grid(row=4, column=0, padx=5, pady=5)
        self.ent_dept = ttk.Entry(frame_reg); self.ent_dept.grid(row=4, column=1)

        btn_reg = ttk.Button(frame_reg, text="Guardar Registro", command=self.accion_registro)
        btn_reg.grid(row=5, column=1, pady=20)

    def accion_aumento(self):
        puesto = self.txt_puesto_aum.get().upper()
        try:
            pct = float(self.txt_pct_aum.get())
            if db_aumentar_sueldo(puesto, pct):
                messagebox.showinfo("Correcto", "Aumento aplicado correctamente.")
                self.cargar_tabla_reporte()
        except ValueError:
            messagebox.showerror("Error", "Ingrese un numero valido.")

    def accion_registro(self):
        try:
            c = int(self.ent_cod.get())
            n = self.ent_nom.get().upper()
            p = self.ent_puesto.get().upper()
            s = float(self.ent_sal.get())
            d = int(self.ent_dept.get())
            if db_registrar_empleado(c, n, p, s, d):
                messagebox.showinfo("Correcto", "Empleado registrado.")
                self.ent_cod.delete(0, 'end'); self.ent_nom.delete(0, 'end')
                self.cargar_tabla_reporte()
        except ValueError:
            messagebox.showerror("Error", "Revise los datos ingresados.")

    def crear_tab_auditoria(self):
        frame_top = ttk.Frame(self.tab3)
        frame_top.pack(pady=10)
        
        btn_sim = ttk.Button(frame_top, text="Simular Eliminacion (Probar Trigger)", command=self.accion_simulacion)
        btn_sim.pack(side="left", padx=10)
        
        btn_ref = ttk.Button(frame_top, text="Refrescar Lista", command=self.cargar_tabla_auditoria)
        btn_ref.pack(side="left", padx=10)

        cols = ('EMPLEADO ELIMINADO', 'PUESTO ANTERIOR', 'FECHA', 'USUARIO')
        self.tree_audit = ttk.Treeview(self.tab3, columns=cols, show='headings')
        
        for col in cols:
            self.tree_audit.heading(col, text=col)
            self.tree_audit.column(col, width=180)
            
        self.tree_audit.pack(expand=True, fill='both', padx=10, pady=10)
        self.cargar_tabla_auditoria()

    def accion_simulacion(self):
        if db_simular_trampa():
            messagebox.showwarning("Alerta", "Se elimino un empleado de prueba. Verifique la auditoria.")
            self.cargar_tabla_auditoria()

    def cargar_tabla_auditoria(self):
        for i in self.tree_audit.get_children():
            self.tree_audit.delete(i)
        datos = obtener_auditoria()
        for fila in datos:
            valores = (fila[0], fila[1], str(fila[2]), fila[3])
            self.tree_audit.insert("", "end", values=valores)

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionRRHH(root)
    root.mainloop()