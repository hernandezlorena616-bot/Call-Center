import simpy
import random

# Parámetros
TIEMPO_SIMULACION = 30
NUMERO_AGENTES = 2

clientes_llaman = 0
clientes_atendidos = 0

def atender_cliente(env, nombre, agentes):
    global clientes_atendidos

    print(f"[{env.now}] {nombre} está llamando.")

    with agentes.request() as solicitud:
        yield solicitud

        print(f"[{env.now}] {nombre} está siendo atendido.")

        tiempo = random.randint(2, 5)
        yield env.timeout(tiempo)

        clientes_atendidos += 1
        print(f"[{env.now}] {nombre} fue atendido.")

def generar_llamadas(env, agentes):
    global clientes_llaman

    numero = 1

    while True:
        espera = random.randint(1, 4)
        yield env.timeout(espera)

        clientes_llaman += 1
        env.process(
            atender_cliente(env, f"Cliente {numero}", agentes)
        )

        numero += 1

# Crear entorno
env = simpy.Environment()

# Crear agentes
agentes = simpy.Resource(env, capacity=NUMERO_AGENTES)

# Iniciar llamadas
env.process(generar_llamadas(env, agentes))

# Ejecutar simulación
env.run(until=TIEMPO_SIMULACION)

# Resumen
print("\n===== RESUMEN =====")
print("Tiempo de llamadas:", TIEMPO_SIMULACION)
print("Número de clientes que llamaron:", clientes_llaman)
print("Número de clientes atendidos:", clientes_atendidos)
