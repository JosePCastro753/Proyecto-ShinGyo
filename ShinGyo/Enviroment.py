"""
Proyecto Shin DMS
@author: Jose Pablo Castro
"""
import random
import numpy as np
import h5py
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
def roundby(x, base=5):
    return int(x) - int(x) % int(base)


def generar():
    tamano_lote = roundby(random.randint(300, 600), 20)
    porcentaje_reproceso = random.uniform(0.1, 0.1)
    porcentaje_scrap = random.uniform(0.05, 0.075)
    tamano_ordenes_total = 0

    velocidad_m1 = random.randrange(15, 25)
    velocidad_m2 = random.randrange(15, 25)
    velocidad_m3 = random.randrange(10, 15)

    i = np.identity(2)
    n = np.array([[0, 1],
                  [porcentaje_reproceso, 0]])

    a = np.array([[0, 0],
                  [porcentaje_scrap, (1 - (porcentaje_scrap + porcentaje_reproceso))]])
    minverse_i_n = np.linalg.inv(np.subtract(i, n))

    markov = minverse_i_n @ a
    markov = markov[1]
    markov = 1 / markov[1]

    tamano_orden_1 = roundby(random.randrange(1200, 4500) * markov, 20)
    tamano_orden_2 = roundby(random.randrange(1200, 4500) * markov, 20)
    tamano_orden_3 = roundby(random.randrange(1200, 4500) * markov, 20)
    tamano_orden_4 = roundby(random.randrange(1200, 4500) * markov, 20)
    tamano_orden_5 = roundby(random.randrange(1200, 4500) * markov, 20)
    emer_1 = roundby(random.randrange(600, 1100), 20)
    emer_2 = roundby(random.randrange(1100, 4500), 20)

    tamano_ordenes = [tamano_orden_1, tamano_orden_2, tamano_orden_3, tamano_orden_4, tamano_orden_5]

    tamano_ordenes = sorted(tamano_ordenes)

    for i in range(len(tamano_ordenes)):
        tamano_ordenes_total += tamano_ordenes[i]

    datos = [tamano_lote, porcentaje_reproceso, porcentaje_scrap,
             markov, velocidad_m1, velocidad_m2, velocidad_m3
             ] + tamano_ordenes + [emer_1, emer_2, tamano_ordenes_total]
    return datos


def decisiones(datos, desicion_urgente_1, desicion_urgente_2, decision_lotes):
    tamano_ordenes = [datos[7], datos[8], datos[9], datos[10], datos[11]]
    tamano_lote = datos[0]
    emer_1 = datos[12]
    emer_2 = datos[13]
    tamano_total = 180
    tamano_total_original = 0
    if desicion_urgente_1 == 1 and desicion_urgente_2 == 0:
        tamano_ordenes.append(emer_1)
        datos.extend([emer_1, 0])
    if desicion_urgente_1 == 0 and desicion_urgente_2 == 1:
        tamano_ordenes.append(emer_2)
        datos.extend([0, emer_2])
    if desicion_urgente_1 == 1 and desicion_urgente_2 == 1:
        tamano_ordenes.extend([emer_1, emer_2])
        datos.extend([emer_1, emer_2])
    for i in range(len(tamano_ordenes)):
        tamano_total_original += tamano_ordenes[i]
    if decision_lotes == 1:
        for i in range(len(tamano_ordenes)):
            tamano_ordenes[i] = tamano_ordenes[i] + (tamano_lote - (tamano_ordenes[i] % tamano_lote))
    for i in range(len(tamano_ordenes)):
        tamano_total += tamano_ordenes[i]

    lotes = [tamano_total, tamano_total_original] + tamano_ordenes

    return lotes


class Machine1:
    def __init__(self, tamano_total, velocity_1):
        self.wip_1 = tamano_total
        self.buffer_mode = 0
        self.velocity_1 = random.normalvariate(velocity_1, 1)
        self.velocidad_acumulada = 0
        self.procesamiento = 0

    def define_buffer_mode(self, buffer_mode):
        self.buffer_mode = buffer_mode

    def procesar(self):
        if self.buffer_mode == 0:
            if self.wip_1 == 0:
                self.velocidad_acumulada = 0
            else:
                self.velocidad_acumulada += self.velocity_1
            if self.velocidad_acumulada >= 20 and self.wip_1 != 0:
                self.velocidad_acumulada -= 20
                self.wip_1 -= 20
                self.procesamiento = 1
            else:
                self.procesamiento = 0
                # 1 es que lo proceso, 0 que no proceso
        if self.buffer_mode == 1:
            self.velocidad_acumulada = 0
            self.procesamiento = 0

        return self.procesamiento

    def entrada_reproceso(self, reproceso):
        if reproceso == 2:
            self.wip_1 += 20

    def get_wip(self):
        return self.wip_1

    def reset(self):
        self.wip_1 = 0
        self.buffer_mode = 0
        self.velocity_1 = 0
        self.velocidad_acumulada = 0


class Machine2:
    def __init__(self, velocity_2, p_reproceso, p_scrap):
        self.wip_2 = 0
        self.velocity_2 = random.normalvariate(velocity_2, 1)
        self.velocidad_acumulada = 0
        self.p_reproceso = p_reproceso
        self.p_scrap = p_scrap
        self.d_reproceso = 0
        self.d_scrap = 0
        self.scrap = 0
        self.aleatorio = 0
        self.procesamiento = 0

    def procesar(self):
        if self.wip_2 == 0:
            self.velocidad_acumulada = 0
        else:
            self.velocidad_acumulada += self.velocity_2
        self.aleatorio = random.randrange(0, 100) / 100
        if self.velocidad_acumulada >= 20 and self.wip_2 != 0:
            self.velocidad_acumulada += -20
            self.wip_2 += -20
            self.d_reproceso = (random.randrange(0, 10) / 100) * self.p_reproceso
            self.d_scrap = (random.randrange(0, 10) / 100) * self.p_scrap
            if self.aleatorio >= self.d_reproceso:
                self.aleatorio = random.randrange(0, 100) / 100
                if self.aleatorio >= self.d_scrap:
                    self.procesamiento = 1
                else:
                    self.procesamiento = 2
            else:
                self.scrap += 20
                self.procesamiento = 0
        else:
            self.procesamiento = 0
            # 1 es que lo proceso, 2 que lo reprocesa, 0 que lo desecha o no procesa
        return self.procesamiento

    def entrada_1(self, procesamiento_1):
        if procesamiento_1 == 1:
            self.wip_2 += 20

    def get_wip(self):
        return self.wip_2

    def get_scrap(self):
        return self.scrap

    def reset(self):
        self.wip_2 = 0
        self.velocity_2 = 0
        self.velocidad_acumulada = 0
        self.p_reproceso = 0
        self.p_scrap = 0
        self.d_reproceso = 0
        self.d_scrap = 0
        self.scrap = 0
        self.aleatorio = 0


class Machine3:
    def __init__(self, velocity_3, buffer_level, drum_level):
        self.wip_3 = 0
        self.velocity_3 = random.normalvariate(velocity_3, 1)
        self.velocidad_acumulada = 0
        self.buffer_level = buffer_level
        self.drum_level = drum_level
        self.buffer_mode = 0
        self.unidades_terminadas = 0
        self.maquina_parada = 0

    def procesar(self):
        if self.wip_3 == 0:
            self.velocidad_acumulada = 0
        else:
            self.velocidad_acumulada += self.velocity_3
        if self.velocidad_acumulada >= 20 and self.wip_3 != 0:
            self.velocidad_acumulada += -20
            self.wip_3 += -20
        else:
            self.maquina_parada += 1

    def entrada_2(self, procesamiento_2):
        if procesamiento_2 == 1:
            self.wip_3 += 20
            self.unidades_terminadas += 20

    def actualizar_buffer_mode(self):
        if self.wip_3 >= self.buffer_level:
            self.buffer_mode = 1
        if self.wip_3 <= self.drum_level:
            self.buffer_mode = 0
        return self.buffer_mode

    def get_wip(self):
        return self.wip_3

    def get_u_terminadas(self):
        return self.unidades_terminadas

    def reset(self):
        self.wip_3 = 0
        self.velocity_3 = 0
        self.velocidad_acumulada = 0
        self.buffer_level = 0
        self.drum_level = 0
        self.buffer_mode = 0
        self.unidades_terminadas = 0


class Scenario():
    def __init__(self):
        self.rewards = None
        self.reward_meter_urgentes_1 = 0
        self.reward_completar_lotes = 0
        self.falta_unidades = 0
        self.maquina_3_parada = 0
        self.unidades_sobra = 0
        self.scrap = 0
        self.u_terminadas = 0
        self.wip1 = 0
        self.wip2 = 0
        self.wip3 = 0
        self.mach_2_p = 0
        self.mach_1_p = 0
        self.reward_acumulada = 0
        self.datos_ordenes = None
        self.machine1 = None
        self.machine2 = None
        self.machine3 = None
        self.desicion_urgente_1 = None
        self.desicion_urgente_2 = None
        self.decision_lotes = None
        self.decision_buffer = None
        self.decision_drum = None
        self.generacion = generar()
        self.tiempo = 0
        self.buff_m = 0
        self.buff_acumulado = 0
        self.n_agents = 5
        self.possible_agents = ["completar_lotes",
                                "meter_urgentes_1",
                                "meter_urgentes_2",
                                "establecer_buffer",
                                "establecer_drum"]

    def reset(self):
        self.machine1 = None
        self.machine2 = None
        self.machine3 = None
        self.reward_acumulada = 0
        self.desicion_urgente_1 = None
        self.desicion_urgente_2 = None
        self.decision_lotes = None
        self.decision_buffer = None
        self.decision_drum = None
        self.generacion = generar()
        self.buff_m = 0
        self.buff_acumulado = 0
        lista = [self.generacion[0],
                 self.generacion[1],
                 self.generacion[2],
                 self.generacion[4],
                 self.generacion[5],
                 self.generacion[6],
                 self.generacion[12],
                 self.generacion[13],
                 self.generacion[14]]
        return lista

    def step(self, decision_lotes, desicion_urgente_1, desicion_urgente_2, decision_buffer, decision_drum):
        self.tiempo = 0
        self.decision_lotes = float(decision_lotes)
        if self.decision_lotes >= 1:
            self.decision_lotes = 1
        elif self.decision_lotes < 1:
            self.decision_lotes = 0
        self.desicion_urgente_1 = float(desicion_urgente_1)
        if self.desicion_urgente_1 >= 1:
            self.desicion_urgente_1 = 1
        elif self.desicion_urgente_1 < 1:
            self.desicion_urgente_1 = 0
        self.desicion_urgente_2 = float(desicion_urgente_2)
        if self.desicion_urgente_2 >= 1 :
            self.desicion_urgente_2 = 1
        elif self.desicion_urgente_2 < 1 :
            self.desicion_urgente_2 = 0
        self.decision_buffer = round(float(decision_buffer))
        self.decision_drum = round(float(decision_drum))

        # INICIALIZACION
        self.datos_ordenes = decisiones(self.generacion, self.desicion_urgente_1, self.desicion_urgente_2, self.decision_lotes)
        self.wip1 = self.datos_ordenes[0]
        self.machine1 = Machine1(self.datos_ordenes[0], self.generacion[4])
        self.machine2 = Machine2(self.generacion[5], self.generacion[1], self.generacion[2])
        self.machine3 = Machine3(self.generacion[6], self.decision_buffer, self.decision_drum)
        # SIMULACION
        while self.wip1 != 0:
            self.mach_1_p = self.machine1.procesar()
            self.machine2.entrada_1(self.mach_1_p)
            self.mach_2_p = self.machine2.procesar()
            self.machine1.entrada_reproceso(self.mach_2_p)
            self.machine3.entrada_2(self.mach_2_p)
            self.machine3.procesar()
            self.buff_m = self.machine3.actualizar_buffer_mode()
            self.machine1.define_buffer_mode(self.buff_m)
            self.wip1 = self.machine1.wip_1
            self.wip2 = self.machine2.wip_2
            self.wip3 = self.machine3.wip_3
            self.tiempo += 1
        self.buff_acumulado += self.buff_m
        self.u_terminadas = self.machine3.unidades_terminadas
        self.scrap = self.machine2.scrap
        self.unidades_sobra = self.u_terminadas - self.datos_ordenes[1]
        self.maquina_3_parada = self.machine3.maquina_parada
        if self.unidades_sobra <= 0:
            self.falta_unidades = 1
        else:
            self.falta_unidades = 0

        # establece las recompensas
        self.reward_completar_lotes = self.decision_lotes * 2000 - self.falta_unidades * 6000 - self.unidades_sobra - self.tiempo * 1.2 - self.scrap
        self.reward_meter_urgentes_1 = self.desicion_urgente_1 * 1000 - self.falta_unidades * 6000 - self.unidades_sobra - self.tiempo * 1.2 - self.scrap
        self.reward_meter_urgentes_2 = self.desicion_urgente_2 * 1000 - self.falta_unidades * 6000 - self.unidades_sobra - self.tiempo * 1.2 - self.scrap
        self.reward_establecer_buffer = (0 - self.decision_buffer) - self.falta_unidades * 6000 - self.unidades_sobra - self.maquina_3_parada * 10 - self.tiempo * 1.2 - self.scrap
        self.reward_establecer_drum = self.decision_drum - self.falta_unidades * 6000 - self.unidades_sobra - self.maquina_3_parada * 10 - self.tiempo * 1.2 - self.scrap

        self.reward_acumulada = self.reward_completar_lotes + self.reward_meter_urgentes_1 + self.reward_meter_urgentes_2 + self.reward_establecer_buffer + self.reward_establecer_drum
        return self.reward_acumulada

    def info(self):
        escenario = "tamano_lote " + str(self.generacion[0]) + " porcentaje_reproceso " + str(
            self.generacion[1]) + " porcentaje_scrap " + str(self.generacion[2]) + " markov " + str(
            self.generacion[3]) + " velocidad_m1 " + str(self.generacion[4]) + " velocidad_m2 " + str(
            self.generacion[5]) + " velocidad_m3 " + str(self.generacion[6]) + " tamano_ordene_1 " + str(
            self.generacion[7]) + " tamano_ordene_2 " + str(self.generacion[8]) + " tamano_ordene_3 " + str(
            self.generacion[9]) + " tamano_ordene_4 " + str(self.generacion[10]) + " tamano_ordene_5 " + str(
            self.generacion[11]) + " tamano_emer_1 " + str(self.generacion[12]) + " tamano_emer_2 " + str(
            self.generacion[13])

        decisiones_tomadas = "completar_lotes " + str(self.decision_lotes) + " meter_urgentes_1 " + str(
            self.desicion_urgente_1) + " meter_urgentes_2  " + str(
            self.desicion_urgente_2) + " establecer_buffer" + str(self.decision_buffer) + " establecer_drum " + str(
            self.decision_drum)

        resultados = "u_terminadas " + str(self.u_terminadas) + " scrap " + str(self.scrap) + " tiempo " + str(
                self.tiempo) + " unidades_sobra " + str(self.unidades_sobra) + " maquina_3_parada " + str(
                self.maquina_3_parada)

        info = [escenario, decisiones_tomadas, resultados]
        return info
