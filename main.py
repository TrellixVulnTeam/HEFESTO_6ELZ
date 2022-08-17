from typing import List
import numpy as np
import cmath as cm
import math as m
import copy as cp


class DefaultDictFormat():
    @staticmethod
    def get_dict_struct(nominal, base=None):
        keys = ['nominal', 'base', 'pu']
        struct = {key: None for key in keys}
        struct['nominal'] = nominal
        if base != None:
            struct['base'] = base
        return struct

d = DefaultDictFormat()
# vlt1 = d.get_dict_struct(Voltage(13.2, 'k', 'V', 1))
# zput1 = d.get_dict_struct(Impedance('pu%', 10))

class MagConversion():
    def __init__(self) -> None:
        self.multipliers = {
            'p': pow(10, -12),
            'n': pow(10, -9),
            'u': pow(10, -6),
            'm': pow(10, -3),
            ' ': pow(10, 0),
            'k': pow(10, 3),
            'M': pow(10, 6),
            'G': pow(10, 9),
            'T': pow(10, 12),
            '%': pow(10, -2)
        }


    def get_value(self, eng_notation):
        if isinstance(eng_notation, dict):
            return self.multipliers[eng_notation['nominal'].multiplier] * eng_notation['nominal'].mag
        else:
            return self.multipliers[eng_notation.multiplier] * eng_notation.mag
#print(MagConversion().get_value(power))
# {'nominal': Voltage('k', 13.8, 1), 'base': None, 'pu': None}

    def get_eng_notation(self, value):
        for multiplier, meq in self.multipliers.items():
            if value / meq >= 1 and value / meq < 1000:
                return (multiplier, value / meq)
# print(MagConversion().get_eng_notation(13800))


class Number():
    def __init__(self, mag, multiplier, measurement_unit) -> None:
        self.mag = mag
        self.multiplier = multiplier
        self.measurement_unit = measurement_unit
        

class Power(Number):
    def __init__(self, mag, multiplier, measurement_unit) -> None:
        super().__init__(mag, multiplier, measurement_unit)
# p = Power(25, 'M', 'VA')
# print(f'Power Object: {p.mag} {p.multiplier}{p.measurement_unit}')


class Voltage(Number):
    def __init__(self, mag, multiplier, measurement_unit, bar) -> None:
        super().__init__(mag, multiplier, measurement_unit)
        self.bar = bar

# v = d.get_dict_struct(Voltage(13.2, 'k', 'V', 1))
# print(f'Voltage object: {v}')
# print(f"Nominal Voltage: {v['nominal'].mag}{v['nominal'].multiplier}{v['nominal'].measurement_unit} in bar {v['nominal'].bar}")


class Impedance(Number):
    def __init__(self, mag, multiplier, measurement_unit, characteristic, lenght=None) -> None:
        super().__init__(mag, multiplier, measurement_unit)
        self.characteristic = characteristic
        self.len = lenght
        self.check_format()

    def check_format(self):
        mc = MagConversion()
        if self.measurement_unit == 'ohm/km':
            self.mag *= self.len
            self.measurement_unit = 'ohm'
        elif self.measurement_unit == 'kohm*km':
            if self.mag.imag > 0:
                self.mag = -self.mag * 1000 / self.len
            else:
                self.mag = self.mag * 1000 / self.len
            self.measurement_unit = 'ohm'

# z = d.get_dict_struct(Impedance(10, '%', 'pu', 'series'))
# print(f'Impedance struct: {z}')
# print(f"Impedance object: {z['nominal'].mag}{z['nominal'].multiplier}{z['nominal'].measurement_unit} type {z['nominal'].characteristic}")
# z = d.get_dict_struct(Impedance(100j, ' ', 'ohm', 'series'))
# print(f'Impedance struct: {z}')
# print(f"Impedance object: {z['nominal'].mag}{z['nominal'].multiplier}{z['nominal'].measurement_unit} type {z['nominal'].characteristic}")
# z = d.get_dict_struct(Impedance(1 + 0.4j, ' ', 'ohm/km', 'series', 80))
# print(f'Impedance struct: {z}')
# print(f"Impedance object: {z['nominal'].mag}{z['nominal'].multiplier}{z['nominal'].measurement_unit} type {z['nominal'].characteristic}")
# z = d.get_dict_struct(Impedance(280j, ' ', 'kohm*km', 'shunt', 100))
# print(f'Impedance struct: {z}')
# print(f"Impedance object: {z['nominal'].mag}{z['nominal'].multiplier}{z['nominal'].measurement_unit} type {z['nominal'].characteristic}")


class Generators():
    instances = []
    counter = 0
    def __init__(self, power, voltage, impedance, terminals) -> None:
        Generators.instances.append(self)
        Generators.counter += 1
        self.id = Generators.counter
        self.power = power
        self.voltage = voltage
        self.impedance = impedance
        self.terminals = terminals
    
    def set_voltage(self, key, voltage):
        self.voltage[key] = voltage

    def set_impedance(self, key, impedance):
        self.impedance[key] = impedance


# pg1, tg1 = Power(30, 'M', 'VA'), (0, 1)
# vg1 = d.get_dict_struct(Voltage(15, 'k', 'V', 1))
# zpug1 = d.get_dict_struct(Impedance(8, '%', 'pu', 'series'))
# g1 = Generators(pg1, vg1, zpug1, tg1)

# print(f"Generator object: {g1}")
# print(f"Generator power: {g1.power}")
# print(f"Generator power: {g1.power.mag}{g1.power.multiplier}{g1.power.measurement_unit}")
# print(f"Generator voltage: {g1.voltage}")
# print(f"Generator nominal voltage: {g1.voltage['nominal'].mag}{g1.voltage['nominal'].multiplier}{g1.voltage['nominal'].measurement_unit} in bar {g1.voltage['nominal'].bar}")
# print(f"Generator impedance: {g1.impedance}")
# print(f"Generator nominal impedance: {g1.impedance['nominal'].mag}{g1.impedance['nominal'].multiplier}{g1.impedance['nominal'].measurement_unit} type {g1.impedance['nominal'].characteristic}")


class Transformers():
    instances = []
    counter = 0
    def __init__(self, power, voltage_h, voltage_l, impedance, terminals) -> None:
        Transformers.instances.append(self)
        Transformers.counter += 1
        self.id = Transformers.counter
        self.power = power
        self.voltage_h = voltage_h
        self.voltage_l = voltage_l
        self.impedance = impedance
        self.terminals = terminals
    
    def set_voltage(self, key, voltage):
        self.voltage[key] = voltage

    def set_impedance(self, key, impedance):
        self.impedance[key] = impedance

# pt1, tt1 = Power(50, 'M', 'VA'), (1, 2)
# vht1 = d.get_dict_struct(Voltage(125, 'k', 'V', 2))
# vlt1 = d.get_dict_struct(Voltage(13.8, 'k', 'V', 1))
# zput1 = d.get_dict_struct(Impedance(10, '%', 'pu', 'series'))
# t1 = Transformers(pt1, vht1, vlt1, zput1, tt1)

# print(f"Transformer object: {t1}")
# print(f"Transformer power: {t1.power}")
# print(f"Transformer power: {t1.power.mag}{t1.power.multiplier}{t1.power.measurement_unit}")
# print(f"Transformer high voltage: {t1.voltage_h}")
# print(f"Transformer high nominal voltage: {t1.voltage_h['nominal'].mag}{t1.voltage_h['nominal'].multiplier}{t1.voltage_h['nominal'].measurement_unit} in bar {t1.voltage_h['nominal'].bar}")
# print(f"Transformer low voltage: {t1.voltage_l}")
# print(f"Transformer low nominal voltage: {t1.voltage_l['nominal'].mag}{t1.voltage_l['nominal'].multiplier}{t1.voltage_l['nominal'].measurement_unit} in bar {t1.voltage_l['nominal'].bar}")
# print(f"Transformer impedance: {t1.impedance}")
# print(f"Transformer nominal impedance: {t1.impedance['nominal'].mag}{t1.impedance['nominal'].multiplier}{t1.impedance['nominal'].measurement_unit} type {t1.impedance['nominal'].characteristic}")


class ShortTLines():
    instances = []
    counter = 0
    def __init__(self, series_impedance, terminals) -> None:
        ShortTLines.instances.append(self)
        ShortTLines.counter += 1
        self.id = ShortTLines.counter
        self.z_series = series_impedance
        self.terminals = terminals
    
    def set_series_impedance(self, key, impedance):
        self.z_series[key] = impedance

# zl1, tl1 = d.get_dict_struct(Impedance(100j, ' ', 'ohm', 'series')), (2, 3)
# l1 = ShortTLines(zl1, tl1)

# print(f"Short Line nominal impedance: {l1.z_series['nominal'].mag}{l1.z_series['nominal'].multiplier}{l1.z_series['nominal'].measurement_unit} type {l1.z_series['nominal'].characteristic}")


class MediumTLines():
    instances = []
    counter = 0
    def __init__(self, series_impedance, shunt_impedance, terminals) -> None:
        MediumTLines.instances.append(self)
        MediumTLines.counter += 1
        self.id = MediumTLines.counter
        self.z_series = series_impedance
        self.z_shunt = shunt_impedance
        self.z_shunt_per_side = cp.deepcopy(shunt_impedance)
        self.terminals = terminals
        self.initialize_shunt_impedance_per_side()
    
    def initialize_shunt_impedance_per_side(self):
        self.z_shunt_per_side['nominal'].mag = 2 * self.z_shunt['nominal'].mag
        
    def set_shunt_impedance_per_side(self, key, impedance):
        self.z_shunt_per_side[key] = impedance

    def set_series_impedance(self, key, impedance):
        self.z_series[key] = impedance
    
    def set_shunt_impedance(self, key, impedance):
        self.z_shunt[key] = impedance

# zsml1, tml1 = d.get_dict_struct(Impedance(100j, ' ', 'ohm', 'series')), (2, 3)
# zshml1 = d.get_dict_struct(Impedance(-5000j, ' ', 'ohm', 'shunt'))
# l1 = MediumTLines(zsml1, zshml1, tml1)

# print(f"Medium Line series nominal impedance: {l1.z_series['nominal'].mag}{l1.z_series['nominal'].multiplier}{l1.z_series['nominal'].measurement_unit} type {l1.z_series['nominal'].characteristic}")
# print(f"Medium Line shunt nominal impedance: {l1.z_shunt['nominal'].mag}{l1.z_shunt['nominal'].multiplier}{l1.z_shunt['nominal'].measurement_unit} type {l1.z_shunt['nominal'].characteristic}")


class PowerFactor():
    def __init__(self, pf, characteristic) -> None:
        self.pf = pf
        self.characteristic = characteristic

class Loads():
    instances = []
    
    counter = 0
    def __init__(self, power, power_factor, terminals, impedance = None) -> None:
        Loads.instances.append(self)
        Loads.counter += 1
        self.id = Loads.counter
        self.power = power
        self.pf = power_factor
        self.terminals = terminals
        self.impedance = impedance
        
    def set_impedance(self, impedance):
        self.impedance = impedance
# pld1, pfld1, tld1 = Power(35, 'M', 'VA'), PowerFactor(0.98, 'atrasado'), (1, 2)
# ld1 = Loads(pld1, pfld1, tld1)

# print(f"Load object: {ld1}")
# print(f"Load power: {ld1.power}")
# print(f"Load power: {ld1.power.mag}{ld1.power.multiplier}{ld1.power.measurement_unit} with a power factor of {ld1.pf.pf} {ld1.pf.characteristic}")



class Bars():
    def __init__(self) -> None:
        self.id = None
        self.adjacent = []
        self.isVisited = False
        self.voltage = None

    def set_id(self, id) -> None:
        self.id = id

    def get_bars(self, components) -> List:
        t_list = [terminals for component in components for terminals in component.terminals]
        max_terminal = sorted(t_list)[-1]
        t_list = [i for i in range(max_terminal + 1)]
        return t_list

    def set_adjacent(self, components) -> None:
        for component in components:
            if self.id in component.terminals:
                if self.id != component.terminals[0]:
                    self.adjacent.append(component.terminals[0])
                else:
                     self.adjacent.append(component.terminals[1])

    def set_isVisited(self, isVisited) -> None:
        self.isVisited = isVisited
    
    def set_voltage(self, voltage) -> None:
        self.voltage = MagConversion().get_value(voltage)
    # components = lista dos objetos componentes = [gerador, transformador 1, linha 1, transformador 2]
    # bars = lista dos objetos barra = [barra 0, barra 1, barra 2, barra 3, barra 4]
    def set_voltages(self, components, bars) -> None:
        # 1ª CHAMADA set_voltages(): aux = head = barra 1
        # 2ª CHAMADA set_voltages(): aux = barra 2
        # 3ª CHAMADA set_voltages(): 
        aux = self 
        while(aux != None): # Roda infinito
            # 1ª CHAMADA set_voltages(): seta head como visitado
            # 2ª CHAMADA set_voltages(): seta barra 2 como visitado
            # 3ª CHAMADA set_voltages(): 
            aux.isVisited = True
            # 1ª CHAMADA set_voltages(): Para as barras 0 e 2
            # 2ª CHAMADA set_voltages(): Para as barras 1 e 3
            # 3ª CHAMADA set_voltages(): 
            for adjacent in aux.adjacent:
                if adjacent != 0: # Não fazer nada para barra 0; 
                    # 1ª CHAMADA set_voltages(): Se a tensão na head for None > False
                    # 2ª CHAMADA set_voltages(): Se a tensão na barra 3 for None > True
                    # 3ª CHAMADA set_voltages(): 
                    if aux.voltage == None:
                        # 1ª CHAMADA set_voltages(): Não entra aqui
                        # 2ª CHAMADA set_voltages(): Calcula tensão na barra 3
                        # 3ª CHAMADA set_voltages(): 
                        aux.voltage = aux.calcVoltage(components, bars)
                    # 1ª CHAMADA set_voltages(): Barra 2 não visitada > True
                    # 2ª CHAMADA set_voltages(): 
                    if not bars[adjacent].isVisited:
                        # 1ª CHAMADA set_voltages(): Chama o próprio método partir da instância da barra 2; começo da 2ª CHAMADA
                        # 2ª CHAMADA set_voltages(): 
                        return bars[adjacent].set_voltages(components, bars)
            # Verifying process end
            visited = [bar.isVisited for bar in bars if bar.id != 0]
            if False in visited:
                for i, visited in enumerate(visited):
                    if visited == False:
                        aux = bars[i + 1]
                        break
            else:
                break
            
    def calcVoltage(self, components, bars):
        # 2ª CHAMADA set_voltages(): atribui a barra em análise à variável current_bar para legibilidade
        # 3ª CHAMADA set_voltages(): IDEM
        current_bar = self
        # 2ª CHAMADA set_voltages(): self = barra 2; self.findFirstKnowVoltageBar(bars) retornará a barra 1: HEAD
        # 3ª CHAMADA set_voltages(): 
        knowVoltageBar = current_bar.findFirstKnowVoltageBar(bars)
        # 2ª CHAMADA set_voltages(): (2, 1) = (Id barra 2, Id barra 1)
        # 3ª CHAMADA set_voltages(): (3, 2) = 
        terminals = (current_bar.id, knowVoltageBar.id)
        selected_component = None
        # 2ª CHAMADA set_voltages(): Busca dentro dos componentes aquele cujos terminais coincidem com os da análise
        # 3ª CHAMADA set_voltages(): IDEM
        for component in components:
            if terminals[0] in component.terminals and terminals[1] in component.terminals:
                selected_component = component
                break
        if isinstance(selected_component, Transformers):
            transformer = selected_component
            # 2ª CHAMADA set_voltages(): criam-se as tuplas (tensão, Id da barra) para fins de cálculo e legibilidade
            # 3ª CHAMADA set_voltages(): IDEM
            voltage_h = (MagConversion().get_value(transformer.voltage_h), transformer.voltage_h['nominal'].bar)
            voltage_l = (MagConversion().get_value(transformer.voltage_l), transformer.voltage_l['nominal'].bar)
            # 2ª CHAMADA set_voltages(): Cálculo da tensão na barra 2
            # 3ª CHAMADA set_voltages(): Cálculo da tensão na barra 3
            transf_relation = voltage_h[0] / voltage_l[0]
            if current_bar.id == voltage_h[1]:
                current_bar.voltage = knowVoltageBar.voltage * transf_relation
            else:
                current_bar.voltage = knowVoltageBar.voltage / transf_relation
        elif isinstance(selected_component, ShortTLines) or isinstance(selected_component, MediumTLines):
            current_bar.voltage = knowVoltageBar.voltage
        # 2ª CHAMADA set_voltages(): retorna tensão na barra 2
        # 3ª CHAMADA set_voltages(): retorna tensão na barra 3
        return current_bar.voltage

    def findFirstKnowVoltageBar(self, bars):
        for adjacent in self.adjacent:
            if bars[adjacent].id != 0 and bars[adjacent].voltage != None: # Não fazer nada para barra 0; 
                return bars[adjacent]


class PuConvesions():
    def __init__(self, base_power) -> None:
        self.base_p = base_power

    def generator_to_pu(self, bars, components):
        # Grab generators and put them on a list
        generators = [component for component in components if isinstance(component, Generators)]
        mc = MagConversion()
        for gen in generators: 
            gen_npower = mc.get_value(gen.power)
            for bar in bars:
                if bar.id == gen.terminals[1] and bar.id != 0:
                    gen_nvoltage = mc.get_value(gen.voltage['nominal'])
                    gen.set_voltage('base', bar.voltage)
                    gen.set_voltage('pu', gen_nvoltage / bar.voltage)

                    gen_nimpedance = mc.get_value(gen.impedance['nominal'])
                    gen.set_impedance('base', pow(gen_nvoltage, 2) / gen_npower)
                    gen.set_impedance('pu', gen_nimpedance * gen.impedance['base'] * self.base_p / pow(bar.voltage, 2))
            pdict = ''
            for key, value in gen.voltage.items():
                if key == 'nominal':
                    pdict = f'Generator[{gen.id}] voltage => {key}: {value.mag}{value.multiplier}{value.measurement_unit}'
                elif key == 'base':
                    pdict += f', {key}: {value} V'
                else:
                    pdict += f', {key}: {value} pu'
            print(pdict)

            for key, value in gen.impedance.items():
                if key == 'nominal':
                    pdict = f'Generator[{gen.id}] impedance => {key}: {value.mag} %'
                elif key == 'base':
                    pdict += f', {key}: {value} ohm'
                else:
                    pdict += f', {key}: {value} pu'
            print(pdict)

    def transformer_to_pu(self, bars, components):
        # Grab transformers and put them on a list
        transformers = [component for component in components if isinstance(component, Transformers)]
        mc = MagConversion()
        for tran in transformers: 
            # Grab transformer power in type float
            tran_npower = mc.get_value(tran.power)
            pdict = ''
            for bar in bars:
                # Match current trasformer terminal with bar
                if bar.id == tran.terminals[0]:
                    # Match bar to any transformer terminal to grab correct voltage for calculations
                    if bar.id == tran.voltage_h['nominal'].bar:
                        tran_nv = mc.get_value(tran.voltage_h['nominal'])
                    else:
                        tran_nv = mc.get_value(tran.voltage_l['nominal'])
                    tran_nimpedance = mc.get_value(tran.impedance['nominal'])
                    tran.set_impedance('base', pow(tran_nv, 2) / tran_npower)
                    tran.set_impedance('pu', tran_nimpedance * tran.impedance['base'] * self.base_p / pow(bar.voltage, 2))
            pdict = ''
            for key, value in tran.impedance.items():
                if key == 'nominal':
                    pdict = f'Transformer[{tran.id}] impedance => {key}: {value.mag} %'
                elif key == 'base':
                    pdict += f', {key}: {value} ohm'
                else:
                    pdict += f', {key}: {value} pu'
            print(pdict)

    def tlines_to_pu(self, bars, components):
        tlines = [component for component in components if isinstance(component, ShortTLines) or isinstance(component, MediumTLines)]
        mc = MagConversion()
        for line in tlines:
            for bar in bars:
                if bar.id in line.terminals:
                    line.set_series_impedance('base', pow(bar.voltage, 2) / self.base_p)
                    line_series_impedance = line.z_series['nominal'].mag
                    if isinstance(line, MediumTLines):
                        line_shunt_impedance = line.z_shunt['nominal'].mag
                        line.set_shunt_impedance('base', line.z_series['base'])
                        line.set_shunt_impedance('pu', line_shunt_impedance / line.z_series['base'])
                        line_shunt_impedance_per_side = line.z_shunt_per_side['nominal'].mag
                        line.set_shunt_impedance_per_side('base', line.z_series['base'])
                        line.set_shunt_impedance_per_side('pu', line_shunt_impedance_per_side / line.z_series['base'])
                    line.set_series_impedance('pu', line_series_impedance / line.z_series['base'])
            pdict = ''
            for key, value in line.z_series.items():
                if key == 'nominal':
                    pdict = f'Line[{line.id}] series impedance => {key}: {value.mag} ohm'
                elif key == 'base':
                    pdict += f', {key}: {value} ohm'
                else:
                    pdict += f', {key}: {value} pu'
            print(pdict)
            for key, value in line.z_shunt.items():
                if key == 'nominal':
                    pdict = f'Line[{line.id}] shunt impedance => {key}: {value.mag} ohm'
                elif key == 'base':
                    pdict += f', {key}: {value} ohm'
                else:
                    pdict += f', {key}: {value} pu'
            print(pdict)
            for key, value in line.z_shunt_per_side.items():
                if key == 'nominal':
                    pdict = f'Line[{line.id}] shunt impedance per side => {key}: {value.mag} ohm'
                elif key == 'base':
                    pdict += f', {key}: {value} ohm'
                else:
                    pdict += f', {key}: {value} pu'
            print(pdict)

    def loads_to_pu(self, bars, components):
        loads = [component for component in components if isinstance(component, Loads)]
        mc = MagConversion()
        base_voltage = None
        for load in loads:
            load_base_power = mc.get_value(load.power['base'])
            if load.power['nominal'].measurement_unit == 'VA':
                load_apparent_power = mc.get_value(load.power['nominal'])
                load.power['pu'] = load_apparent_power / load_base_power
            elif load.power['nominal'].measurement_unit == 'W':
                load_active_power = mc.get_value(load.power['nominal'])
                load.power['pu'] = load_active_power / load_base_power
            load_base_power = mc.get_value(load.power['base'])
            
            pdict = ''
            for key, value in load.power.items():
                if key == 'nominal':
                    pdict = f'Load[{load.id}] power => {key}: {value.mag} {value.multiplier}{value.measurement_unit}'
                elif key == 'base':
                    pdict += f', {key}: {value.mag} {value.multiplier}{value.measurement_unit}'
                else:
                    pdict += f', {key}: {value} pu'
            print(pdict)


class LoadConvertions():
    @staticmethod
    def power_to_impedance(loads, bars, voltage=None):
        for load in loads:
            d = DefaultDictFormat()
            # .get_dict_struct()
            mc = MagConversion()
            power = None
            load_impedance = None
            conj = None
            if load.power['nominal'].measurement_unit == 'VA':
                for bar in bars:
                    if bar.id in load.terminals and bar.id != 0:
                        voltage_load = bar.voltage
                        if load.pf.characteristic == 'atrasado':
                            power = cm.polar(cm.rect(mc.get_value(load.power), m.acos(load.pf.pf)))
                        elif load.pf.characteristic == 'adiantado':
                            power = cm.polar(cm.rect(mc.get_value(load.power), -m.acos(load.pf.pf)))
                        conj = cm.rect(power[0], power[1]).conjugate()
                        load_impedance = pow(voltage_load, 2) / conj
                        load.set_impedance(d.get_dict_struct(Impedance(load_impedance, ' ', 'ohm', 'series')))
                print(f"Load impedance:")
                print(f"{load.impedance}")
                print(f"{load.impedance['nominal'].mag}{load.impedance['nominal'].multiplier}{load.impedance['nominal'].measurement_unit} type {load.impedance['nominal'].characteristic}")
            # elif load.power['nominal'].measurement_unit == 'W':
            #     break


# DefaultDictFormat()
d = DefaultDictFormat()
# System basis
base_values = [
    Power(100, 'M', 'VA'),
    Voltage(13.8, 'k', 'V', 1)
]
# Generators
pg1, tg1 = Power(60, 'M', 'VA'), (0, 1)
vg1 = d.get_dict_struct(Voltage(13.2, 'k', 'V', 1))
zpug1 = d.get_dict_struct(Impedance(30, '%', 'pu', 'series'))
g1 = Generators(pg1, vg1, zpug1, tg1)

# Transformers
pt1, tt1 = Power(50, 'M', 'VA'), (1, 2) 
vht1 = d.get_dict_struct(Voltage(132, 'k', 'V', 2))
vlt1 = d.get_dict_struct(Voltage(13.2, 'k', 'V', 1))
zput1 = d.get_dict_struct(Impedance(5, '%', 'pu', 'series'))
t1 = Transformers(pt1, vht1, vlt1, zput1, tt1)
pt2, tt2 = Power(50, 'M', 'VA'), (3, 4)
vht2 = d.get_dict_struct(Voltage(135, 'k', 'V', 3))
vlt2 = d.get_dict_struct(Voltage(13.2, 'k', 'V', 4))
zput2 = d.get_dict_struct(Impedance(6, '%', 'pu', 'series'))
t2 = Transformers(pt2, vht2, vlt2, zput2, tt2)

# Medium Lines
zsl1 = d.get_dict_struct(Impedance(0.4j, ' ', 'ohm/km', 'series', 97))
zshl = d.get_dict_struct(Impedance(280j, ' ', 'kohm*km', 'shunt', 97))
tl1 = (2, 3)
l1 = MediumTLines(zsl1, zshl, tl1)
zsl2 = d.get_dict_struct(Impedance(1.05 + 0.4j, ' ', 'ohm/km', 'series', 150)) 
zshl2 = d.get_dict_struct(Impedance(280j, ' ', 'kohm*km', 'shunt', 150)) 
tl2 = (1, 5)
l2 = MediumTLines(zsl2, zshl2, tl2)

# Loads
pld1 = d.get_dict_struct(Power(35, 'M', 'VA'), base_values[0])
pfld1, tld1 = PowerFactor(0.98, 'adiantado'), (4, 0)
ld1 = Loads(pld1, pfld1, tld1)
pld2 = d.get_dict_struct(Power(2, 'M', 'W'), base_values[0])
pfld2, tld2 = PowerFactor(0.85, 'atrasado'), (5, 0)
ld2 = Loads(pld2, pfld2, tld2)


component_classes = [Generators, Transformers, ShortTLines, MediumTLines, Loads]
components = []
for component_class in component_classes:
        # print(f"{str(component_class)[17:-2]}")
        for instance in component_class.instances:
            # print(f"{instance.id} : {instance}")
            components.append(instance)

# for component in components: print(f"{component}")
# Instantiating bars
bars = [Bars() for i in Bars().get_bars(components)]
# Setting bars Id's
for i in range(len(bars)): bars[i].set_id(i)
# Setting adjacent bars
for bar in bars: bar.set_adjacent(components)
# Defining groung and head bar
ground_bar = bars[0]
ground_bar.set_voltage(Voltage(0, 'k', 'V', 0))
head = bars[base_values[1].bar]
bars[head.id].set_voltage(base_values[1])
# Calculating base voltages
head.set_voltages(components, bars)
for bar in bars: print(f'Vb{bar.id}: {bar.voltage} V')

# Pu Conversion
conv = PuConvesions(MagConversion().get_value(base_values[0]))

conv.generator_to_pu(bars, components)
conv.transformer_to_pu(bars, components)
conv.tlines_to_pu(bars, components)
conv.loads_to_pu(bars, components)

# Load Conversion
# loads = [load for load in components if isinstance(load, Loads)]
# ldconv = LoadConvertions()
# ldconv.power_to_impedance(loads, bars)

