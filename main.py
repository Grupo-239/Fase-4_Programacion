from gui import iniciar_app
from cliente import SistemaClientes
from servicio import ReservaSala, AlquilerEquipo, Asesoria
from reserva import Reserva
import logs

def simular_operaciones():
    """Simulación automática de operaciones para cumplir con el requisito"""
    print("--- Ejecutando Simulación Automática (Consola) ---")
    sistema = SistemaClientes()
    
    try:
        # 1. Registro válido
        c1 = sistema.registrar_cliente("Jhonnier Ramos", "12345", "jhon@unad.edu.co")
        # 2. Registro inválido (Cédula no numérica - lanzará error)
        try: sistema.registrar_cliente("Error", "ABC", "mail@mail.com")
        except Exception as e: print(f"Error esperado 2: {e}")
        
        # 3. Creación de servicios
        s1 = ReservaSala(5, 50)
        s2 = AlquilerEquipo(3, 100)
        
        # 4. Reservas
        r1 = Reserva(c1, s1)
        r2 = Reserva(c1, s2)
        
        # 5. Confirmación y 6. Cancelación
        r1.confirmar()
        r2.cancelar()
        
        print("Simulación inicial completada con éxito.")
    except Exception as e:
        print(f"Error en simulación: {e}")
    print("-" * 40)

if __name__ == "__main__":
    # 1. Iniciar registro de logs
    logs.registrar_evento("Iniciando aplicación Software FJ")
    
    # 2. Correr simulación rápida
    simular_operaciones()
    
    # 3. Lanzar la interfaz gráfica
    iniciar_app()