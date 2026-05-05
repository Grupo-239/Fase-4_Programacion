import sys
import logs
from gui import iniciar_app
from cliente import SistemaClientes
from servicio import ReservaSala, AlquilerEquipo, Asesoria
from reserva import Reserva

def ejecutar_bateria_pruebas():
    """
    Simulación automatizada de 10 operaciones para validar la lógica de negocio,
    el polimorfismo y el manejo de excepciones del sistema Software FJ.
    """
    print("="*60)
    print("SISTEMA SOFTWARE FJ - SIMULACIÓN DE 10 OPERACIONES")
    print("="*60)
    
    sistema = SistemaClientes()
    clientes_prueba = []

    # --- BLOQUE 1: GESTIÓN DE CLIENTES (3 OPERACIONES) ---
    
    # 1. Registro exitoso de cliente
    try:
        c1 = sistema.registrar_cliente("Jhonnier Ramos", "100200", "jhonnier@unad.edu.co")
        clientes_prueba.append(c1)
        print(f"Op 1: Registro exitoso -> {c1}")
    except Exception as e: print(f"Op 1 Error: {e}")

    # 2. Intento de registro con cédula inválida (Letras)
    try:
        sistema.registrar_cliente("Usuario Error", "ABC123", "test@mail.com")
    except Exception as e:
        print(f"Op 2: Validación de cédula (Correcta) -> {e}")

    # 3. Intento de registro con correo inválido (Sin @)
    try:
        sistema.registrar_cliente("Juan Perez", "300400", "juan_sin_correo")
    except Exception as e:
        print(f"Op 3: Validación de correo (Correcta) -> {e}")


    # --- BLOQUE 2: LÓGICA DE SERVICIOS Y POLIMORFISMO (4 OPERACIONES) ---

    # 4. Creación de servicio de Sala (Cálculo por horas)
    s_sala = ReservaSala(4, 50) # 4 horas a $50
    print(f"Op 4: Servicio Sala creado (Polimorfismo). Costo: ${s_sala.calcular_total()}")

    # 5. Creación de servicio de Equipo (Cálculo por días)
    s_equipo = AlquilerEquipo(2, 100) # 2 días a $100
    print(f"Op 5: Servicio Equipo creado (Polimorfismo). Costo: ${s_equipo.calcular_total()}")

    # 6. Creación de servicio de Asesoría
    s_asesor = Asesoria(1, 120) # 1 hora a $120
    print(f"Op 6: Servicio Asesoría creado. Costo: ${s_asesor.calcular_total()}")

    # 7. Intento de crear servicio con tiempo negativo (Excepción)
    try:
        ReservaSala(-5, 50)
    except Exception as e:
        print(f"Op 7: Validación de tiempo (Correcta) -> {e}")


    # --- BLOQUE 3: GESTIÓN DE RESERVAS Y ESTADOS (3 OPERACIONES) ---

    # 8. Creación de reserva vinculada a cliente
    try:
        reserva_final = Reserva(clientes_prueba[0], s_sala)
        print(f"Op 8: Objeto Reserva vinculado a {clientes_prueba[0].nombre}")
    except Exception as e: print(f"Op 8 Error: {e}")

    # 9. Confirmación de reserva y registro de evento
    try:
        reserva_final.confirmar()
        print(f"Op 9: Estado de reserva actualizado a -> {reserva_final.estado}")
    except Exception as e: print(f"Op 9 Error: {e}")

    # 10. Intento de confirmar reserva sin cliente activo
    try:
        Reserva(None, s_equipo)
    except Exception as e:
        print(f"Op 10: Validación de integridad (Correcta) -> {e}")

    print("\n" + "="*60)
    print("SIMULACIÓN FINALIZADA - REVISE 'sistema.log' PARA DETALLES")
    print("="*60 + "\n")

if __name__ == "__main__":
    # Evitar archivos .pyc para mantener el directorio limpio
    sys.dont_write_bytecode = True

    # Inicializar logs
    logs.registrar_evento("Arranque del sistema para evaluación académica.")

    # Ejecutar las 10 operaciones en consola
    ejecutar_bateria_pruebas()

    # Abrir la interfaz gráfica
    iniciar_app()