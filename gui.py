import tkinter as tk 
from cliente import SistemaClientes
from servicio import ReservaSala, AlquilerEquipo, Asesoria
from reserva import Reserva
from logs import registrar_error, registrar_evento


# VARIABLES GLOBALES DEL SISTEMA


# Instancia principal que gestiona todos los clientes
sistema = SistemaClientes()

# Guarda el cliente que tiene la sesión activa (login)
usuario_actual = None

# Lista general de todas las reservas del sistema
reservas = []

# Referencia al componente visual (Listbox) donde se mostrarán las reservas
lista_reservas = None



# CLIENTES (REGISTRO Y SESIÓN)


def registrar():
    """
    Registra un nuevo cliente en el sistema.
    Toma los datos desde la interfaz gráfica.
    """
    global usuario_actual
    try:
        cliente = sistema.registrar_cliente(
            e_nombre.get(),   # input nombre
            e_cedula.get(),   # input cédula
            e_correo.get()    # input correo
        )

        salida.insert(tk.END, f"Registrado: {cliente}\n")
        registrar_evento("Cliente registrado")

    except Exception as e:
        # Captura cualquier error (validaciones, duplicados, etc.)
        registrar_error(str(e))
        salida.insert(tk.END, f"Error: {e}\n")


def login():
    """
    Inicia sesión con un cliente ya registrado.
    Busca por cédula.
    """
    global usuario_actual
    try:
        usuario_actual = sistema.buscar_cliente(e_cedula.get())

        salida.insert(tk.END, f"Sesión iniciada: {usuario_actual}\n")
        registrar_evento("Login exitoso")

        # Actualiza la lista de reservas del usuario logueado
        actualizar_lista()

    except Exception as e:
        registrar_error(str(e))
        salida.insert(tk.END, f"Error: {e}\n")


def logout():
    """
    Cierra la sesión del usuario actual.
    """
    global usuario_actual
    if usuario_actual:
        salida.insert(tk.END, f"Sesión cerrada: {usuario_actual}\n")
        usuario_actual = None

        # Limpia la lista visual de reservas
        actualizar_lista()
    else:
        salida.insert(tk.END, "No hay sesión activa\n")



# SERVICIOS Y RESERVAS


def crear_reserva():
    """
    Crea una reserva según el tipo de servicio seleccionado.
    Valida que haya un usuario logueado.
    """
    try:
        if not usuario_actual:
            raise Exception("Debe iniciar sesión")

        tipo = servicio_var.get()

        # --- RESERVA DE SALA ---
        if tipo == "Sala":
            horas = e_horas.get()  # ← SIN int()
            servicio = ReservaSala(horas, 50)

        # --- ALQUILER DE EQUIPOS ---
        elif tipo == "Equipo":
            dias = e_dias.get()  # ← SIN int()
            tipo_equipo = equipo_var.get()

            precios = {
                "Laptop": 100,
                "Tablet": 70,
                "Periferico": 40
            }

            servicio = AlquilerEquipo(dias, precios[tipo_equipo])

        # --- ASESORÍA ---
        else:
            horas = e_horas.get()  # ← SIN int()
            servicio = Asesoria(horas, 120)

        # Crear reserva
        r = Reserva(usuario_actual, servicio)
        reservas.append(r)

        salida.insert(tk.END, f"Reserva creada: {r} | Costo: {r.costo()}\n")

        actualizar_lista()

    except Exception as e:
        registrar_error(str(e))
        salida.insert(tk.END, f"Error: {e}\n")


def confirmar_reserva():
    """
    Confirma la última reserva del usuario actual.
    """
    try:
        if not usuario_actual:
            raise Exception("Debe iniciar sesión")

        # Filtrar reservas SOLO del usuario actual
        reservas_usuario = [r for r in reservas if r.cliente == usuario_actual]

        if not reservas_usuario:
            raise Exception("No tiene reservas")

        # Se trabaja con la última reserva creada
        reservas_usuario[-1].confirmar()

        salida.insert(tk.END, "Reserva confirmada\n")
        actualizar_lista()

    except Exception as e:
        registrar_error(str(e))
        salida.insert(tk.END, f"Error: {e}\n")


def cancelar_reserva():
    """
    Cancela la última reserva del usuario actual.
    """
    try:
        if not usuario_actual:
            raise Exception("Debe iniciar sesión")

        reservas_usuario = [r for r in reservas if r.cliente == usuario_actual]

        if not reservas_usuario:
            raise Exception("No tiene reservas")

        reservas_usuario[-1].cancelar()

        salida.insert(tk.END, "Reserva cancelada\n")
        actualizar_lista()

    except Exception as e:
        registrar_error(str(e))
        salida.insert(tk.END, f"Error: {e}\n")



# ACTUALIZACIÓN DE INTERFAZ (LISTA DE RESERVAS)


def actualizar_lista():
    """
    Refresca el Listbox mostrando solo las reservas
    del usuario actualmente logueado.
    """
    if not lista_reservas:
        return

    # Limpiar lista visual
    lista_reservas.delete(0, tk.END)

    # Recorrer reservas del sistema
    for r in reservas:
        if r.cliente == usuario_actual:

            # Determinar tiempo según tipo de servicio
            if r.servicio.nombre == "Sala":
                tiempo = f"{r.servicio.horas}h"
            elif r.servicio.nombre == "Equipo":
                tiempo = f"{r.servicio.dias} días"
            else:
                tiempo = f"{r.servicio.horas}h"

            # Formato de visualización
            texto = f"{r.cliente} | {r.servicio.nombre} | {tiempo} | {r.estado} | ${r.costo()}"

            lista_reservas.insert(tk.END, texto)


# INTERFAZ GRÁFICA (GUI)


def iniciar_app():

    global e_nombre, e_cedula, e_correo, salida
    global e_horas, e_dias, servicio_var, equipo_var
    global lista_reservas

    # Ventana principal
    v = tk.Tk()
    v.title("Sistema FJ")

    # --- DATOS CLIENTE ---
    tk.Label(v, text="Nombre").pack()
    e_nombre = tk.Entry(v)
    e_nombre.pack()

    tk.Label(v, text="Cédula").pack()
    e_cedula = tk.Entry(v)
    e_cedula.pack()

    tk.Label(v, text="Correo").pack()
    e_correo = tk.Entry(v)
    e_correo.pack()

    tk.Button(v, text="Registrar", command=registrar).pack()
    tk.Button(v, text="Login", command=login).pack()
    tk.Button(v, text="Logout", command=logout).pack()

    # --- SERVICIOS ---
    servicio_var = tk.StringVar(value="Sala")

    tk.Label(v, text="Servicio").pack()
    tk.OptionMenu(v, servicio_var, "Sala", "Equipo", "Asesoria").pack()

    tk.Label(v, text="Horas").pack()
    e_horas = tk.Entry(v)
    e_horas.pack()

    tk.Label(v, text="Días (solo equipo)").pack()
    e_dias = tk.Entry(v)
    e_dias.pack()

    equipo_var = tk.StringVar(value="Laptop")
    tk.OptionMenu(v, equipo_var, "Laptop", "Tablet", "Periferico").pack()

    tk.Button(v, text="Crear Reserva", command=crear_reserva).pack()
    tk.Button(v, text="Confirmar última reserva", command=confirmar_reserva).pack()
    tk.Button(v, text="Cancelar última reserva", command=cancelar_reserva).pack()

    # --- LISTA DE RESERVAS ---
    tk.Label(v, text="Reservas del usuario").pack()

    lista_reservas = tk.Listbox(v, width=90)
    lista_reservas.pack()

    tk.Button(v, text="Actualizar lista", command=actualizar_lista).pack()

    # --- SALIDA (LOG VISUAL) ---
    salida = tk.Text(v, height=15)
    salida.pack()

    # Ejecutar aplicación
    v.mainloop()
