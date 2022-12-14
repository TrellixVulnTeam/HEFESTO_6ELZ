""" This module is responsible for getting user input and determine system pu equivalent

:return: Default return of python script.
:rtype: None
"""
from typing import List
# import numpy as np
# import cmath as cm
# import math as m
import copy as cp
import sys


class DefaultDictFormat():
    """This class is responsable for hosting the static method get_dict_struct."""
    @staticmethod
    def get_dict_struct(nominal, base=None):
        """This method returns a dictionary in the following structure: {'nominal': nominal, 'base': None, 'pu': None} when just the nominal parameter is given and the folowing: {'nominal': nominal, 'base': Base, 'pu': None} when the optional parameter is given.

        :param nominal: Object to be used as value under the key 'nominal'.
        :type nominal: Object can be a instance of 1 of these 3: Voltage(), Impedance() or Power().
        :param base: When parameter nominal is an instance of Power() the base is given as the system power base, defaults to None.
        :type base: Power(), optional.
        :return: Dictionary as described in method description .
        :rtype: Dict.
        """
        keys = ['nominal', 'base', 'pu']
        struct = {key: None for key in keys}
        struct['nominal'] = nominal
        if base is not None:
            struct['base'] = base
        return struct


class MagConversion():
    """This class is responsable for converting to and from engineering notation with the methods: get_value() and get_eng_notation().
    """
    def __init__(self) -> None:
        """Constructor method. Atributtes predetermined dictionary to instance variable multipliers.
        """
        self.multipliers = {
            'p': pow(10, -12),
            'n': pow(10, -9),
            'u': pow(10, -6),
            'm': pow(10, -3),
            '': pow(10, 0),
            'k': pow(10, 3),
            'M': pow(10, 6),
            'G': pow(10, 9),
            'T': pow(10, 12),
            '%': pow(10, -2)
        }


    def get_value(self, eng_notation):
        """Returns the corresponding float value given a dict with the key 'nominal' and object in value field with the attribute .multiplier which should correspond with this class instance attribute .multipliers.

        :param eng_notation: Received dict with object of type Voltage(), Impedance() or Power() in the format: {'nominal': object, ...}.
        :type eng_notation: Dict.
        :return: A float corresponding to the given engineering notetion.
        :rtype: float.
        """
        if isinstance(eng_notation, dict):
            return self.multipliers[eng_notation['nominal'].multiplier] * eng_notation['nominal'].mag
        else:
            return self.multipliers[eng_notation.multiplier] * eng_notation.mag

    def get_eng_notation(self, value):
        """Returns the engineering notation of a given value in the form of a tuple where the 1st element is the string representing the multiplier in the notation and the 2nd element the value associated with the multiplier.

        :param value: A float or int to be converted to engineering notation.
        :type value: float, int.
        :return: A tuple containg like (multiplier, value).
        :rtype: (str, float).
        """
        for multiplier, meq in self.multipliers.items():
            if value / meq >= 1 and value / meq < 1000:
                return (multiplier, value / meq)

    def get_inverse_multiplier(self, multiplier):
        
        inv_m_value = pow(self.multipliers[multiplier], -1)
        for key, value in self.multipliers.items():
            if inv_m_value == value:
                return key


class Number():
    """This class purpose is to be inherited by other classes.
    """
    def __init__(self, mag, multiplier, measurement_unit) -> None:
        """Generator method.

        :param mag: Magnitude of a number in engineering notation.
        :type mag: float or int.
        :param multiplier: String representing the multiplier in engineering notation .
        :type multiplier: str.
        :param measurement_unit: String representing the unit of the measurement i.e 'V' for 'volts', 'W' for active power, etc.
        :type measurement_unit: str.
        """
        self.mag = mag
        self.multiplier = multiplier
        self.measurement_unit = measurement_unit
        

class Power(Number):
    """This class represents the eletric characteristic know as power.

    :param Number: Object from which to inherit common characteristics.
    :type Number: Number().
    """
    def __init__(self, mag, multiplier, measurement_unit) -> None:
        """Constructor method. Same parameters as parent class.

        :param mag: Magnitude of power in engineering notation.
        :type mag: float or int.
        :param multiplier: String representing the multiplier in engineering notation.
        :type multiplier: str.
        :param measurement_unit: Power can be specified in 'W' or 'VA'. This parameters specifies which one.
        :type measurement_unit: str.
        """
        self.name = 'Pot??ncia'
        super().__init__(mag, multiplier, measurement_unit)


class Voltage(Number):
    """This class represents the eletric characteristic know as voltage.

    :param Number: Object from which to inherit common characteristics.
    :type Number: Number().
    """
    def __init__(self, mag, multiplier, measurement_unit, bar) -> None:
        """Constructor method. Same parameters as parent class with addition of the parameter bar.

        :param mag: Magnitude of voltage in engineering notation.
        :type mag: float or int.
        :param multiplier: String representing the multiplier in engineering notation .
        :type multiplier: str.
        :param measurement_unit: A voltage is measured in volts which is specified in this parameter.
        :type measurement_unit: str.
        :param bar: Since voltage is measured in a bar this parameter was added. A bar is identified by it's number.
        :type bar: int.
        """
        self.name = 'Tens??o'
        super().__init__(mag, multiplier, measurement_unit)
        self.bar = bar


class Impedance(Number):
    """This class represents the eletric characteristic know as impedance.

    :param Number: Object from which to inherit common characteristics.
    :type Number: Number().
    """
    def __init__(self, mag, multiplier, measurement_unit, characteristic, lenght=None) -> None:
        """Constructor method. Same parameters as parent class with addition of the parameteres characteristic and length (optional).

        :param mag: Magnitude of impedance in engineering notation.
        :type mag: float or int.
        :param multiplier: String representing the multiplier in engineering notation .
        :type multiplier: str.
        :param measurement_unit: A impedance can be measured in 'ohm', 'ohm/km', 'kohm*km' or '%'. Which one is specified in this parameter.
        :type measurement_unit: str.
        :param characteristic: A impedance can be in series or shunt, which one is specified in this parameter.
        :type characteristic: str.
        :param lenght: When a impedance measurement unit is given in 'ohm/km' or 'kohm*km' a length is needed in order to get the concentraded parameter, defaults to None.
        :type lenght: float or int, optional.
        """
        self.name = 'Imped??ncia'
        super().__init__(mag, multiplier, measurement_unit)
        self.characteristic = characteristic
        self.len = lenght
        self.check_format()

    def check_format(self):
        """This method checks if the Impedance was specified as a distributed parameter, if It has this method converts to a concentrated parameter aproprieate for calculations.
        """
        if self.measurement_unit == 'ohm/km':
            self.mag *= self.len
            self.measurement_unit = 'ohm'
        elif self.measurement_unit == 'kohm*km':
            if self.mag.imag > 0:
                self.mag = -self.mag * 1000 / self.len
            else:
                self.mag = self.mag * 1000 / self.len
            self.measurement_unit = 'ohm'


class Admittance(Number):
    """This class represents the eletric characteristic know as impedance.

    :param Number: Object from which to inherit common characteristics.
    :type Number: Number().
    """
    def __init__(self, mag, multiplier, measurement_unit) -> None:
        """Constructor method. Same parameters as parent class with addition of the parameteres characteristic and length (optional).

        :param mag: Magnitude of impedance in engineering notation.
        :type mag: float or int.
        :param multiplier: String representing the multiplier in engineering notation .
        :type multiplier: str.
        :param measurement_unit: A impedance can be measured in 'ohm', 'ohm/km', 'kohm*km' or '%'. Which one is specified in this parameter.
        :type measurement_unit: str.
        """
        self.name = 'Admit??ncia'
        super().__init__(mag, multiplier, measurement_unit)


class Generators():
    """This class models the eletric component of eletric power systems know as generator.
    """
    instances = []

    def __init__(self, impedance, terminals, power=None, voltage=None) -> None:
        """Constructor method.

        :param impedance: A generator is modeled as having a series impedance. This parameter specifies the impedance chacteristics.
        :type impedance: dict {'nominal': Impedance(), 'base': None, 'pu': None}.
        :param terminals: A generator has a pair of terminals for this representation. This parameter specifies them.
        :type terminals: tuple.
        :param power: A generator has a nominal power, when is of interest this parameter specifies that, defaults to None.
        :type power: Power(), optional.
        :param voltage: A generator has a nominal voltage, when is of interest this parameter specifies that, defaults to None.
        :type voltage: dict {'nominal': Voltage(), 'base': None, 'pu': None}, optional.
        """
        self.name = 'Gerador'
        Generators.instances.append(self)
        self.id = len(Generators.instances)
        self.power = power
        self.voltage = voltage
        self.impedance = impedance
        self.terminals = terminals
        self.admittance = None
        self.set_admittance()
    
    def set_power(self, key, power):
        """This method sets the voltage of the generator. Since the voltage is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the voltage attribute.
        :type key: str.
        :param voltage: Value representing a type of voltage.
        :type voltage: Voltage() or float.
        """
        self.power[key] = power

    def set_voltage(self, key, voltage):
        """This method sets the voltage of the generator. Since the voltage is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the voltage attribute.
        :type key: str.
        :param voltage: Value representing a type of voltage.
        :type voltage: Voltage() or float.
        """
        self.voltage[key] = voltage

    def set_impedance(self, key, impedance):
        """This method sets the impedance of the generator. Since the impedance is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the impedance attribute.
        :type key: str.
        :param voltage: Value representing a type of impedance.
        :type voltage: Impedance() or float.
        """
        self.impedance[key] = impedance
    
    def set_admittance(self):
        """This method sets the admittance of the generator. Since the admittance is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the admittance attribute.
        :type key: str.
        :param voltage: Value representing a type of admittance.
        :type voltage: Admittance() or float.
        """
        d = DefaultDictFormat()
        mc = MagConversion()
        self.admittance = d.get_dict_struct(Admittance(None, None, 'Siemens'))
        self.admittance['nominal'].mag = pow(self.impedance['nominal'].mag, -1)
        self.admittance['nominal'].multiplier = mc.get_inverse_multiplier(self.impedance['nominal'].multiplier)
        

class Transformers():
    """This class models the eletric component of eletric power systems know as transformer.
    """
    instances = []

    def __init__(self, impedance, terminals, power=None, voltage_h=None, voltage_l=None) -> None:
        """Constructor method.

        :param impedance: A transformer is modeled as having a series impedance. This parameter specifies the impedance chacteristics.
        :type impedance: dict {'nominal': Impedance(), 'base': None, 'pu': None}.
        :param terminals: A transformer has a pair of terminals for this representation. This parameter specifies them.
        :type terminals: tuple.
        :param power: A transformer has a nominal power, when is of interest this parameter specifies that, defaults to None.
        :type power: Power(), optional.
        :param voltage_h: A transformer has a high voltage side, when is of interest this parameter specifies that voltage value, defaults to None.
        :type voltage_h: dict {'nominal': Voltage(), 'base': None, 'pu': None}, optional.
        :param voltage_l: A transformer has a low voltage side, when is of interest this parameter specifies that voltage value, defaults to None.
        :type voltage_l: dict {'nominal': Voltage(), 'base': None, 'pu': None}, optional.
        """
        self.name = 'Transformador'
        Transformers.instances.append(self)
        self.id = len(Transformers.instances)
        self.power = power
        self.voltage_h = voltage_h
        self.voltage_l = voltage_l
        self.impedance = impedance
        self.terminals = terminals
        self.admittance = None
        self.set_admittance()
    
    def set_power(self, key, power):
        """This method sets the voltage of the generator. Since the voltage is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the voltage attribute.
        :type key: str.
        :param voltage: Value representing a type of voltage.
        :type voltage: Voltage() or float.
        """
        self.power[key] = power

    def set_voltage_h(self, key, voltage_h):
        """This method sets the voltage of the transformer. Since the voltage is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the voltage attribute.
        :type key: str.
        :param voltage: Value representing a type of voltage.
        :type voltage: Voltage() or float.
        """
        self.voltage_h[key] = voltage_h
    
    def set_voltage_l(self, key, voltage_l):
        """This method sets the voltage of the transformer. Since the voltage is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the voltage attribute.
        :type key: str.
        :param voltage: Value representing a type of voltage.
        :type voltage: Voltage() or float.
        """
        self.voltage_l[key] = voltage_l

    def set_impedance(self, key, impedance):
        """This method sets the impedance of the transformer. Since the impedance is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the impedance attribute.
        :type key: str.
        :param voltage: Value representing a type of impedance.
        :type voltage: Impedance() or float.
        """
        self.impedance[key] = impedance
    
    def set_admittance(self):
        """This method sets the admittance of the generator. Since the admittance is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the admittance attribute.
        :type key: str.
        :param voltage: Value representing a type of admittance.
        :type voltage: Admittance() or float.
        """
        d = DefaultDictFormat()
        mc = MagConversion()
        self.admittance = d.get_dict_struct(Admittance(None, None, 'Siemens'))
        self.admittance['nominal'].mag = pow(self.impedance['nominal'].mag, -1)
        self.admittance['nominal'].multiplier = mc.get_inverse_multiplier(self.impedance['nominal'].multiplier)


class ShortTLines():
    """This class models the eletric component of eletric power systems know as short transmission line.
    """
    instances = []

    def __init__(self, series_impedance, terminals) -> None:
        """Constructor method.

        :param series_impedance: A short transmission line is modeled as having a series impedance. This parameter specifies the impedance chacteristics.
        :type series_impedance: dict {'nominal': Impedance(), 'base': None, 'pu': None}.
        :param terminals:  A short transmission line has a pair of terminals for this representation. This parameter specifies them.
        :type terminals: tuple.
        """
        self.name = 'Linha de Transmiss??o Pequena'
        ShortTLines.instances.append(self)
        self.id = len(ShortTLines.instances)
        self.series_impedance = series_impedance
        self.terminals = terminals
        self.series_admittance = None
        self.set_series_admittance()
    
    def set_series_impedance(self, key, impedance):
        """This method sets the series impedance of the short transmission line. Since the impedance is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the impedance attribute.
        :type key: str.
        :param voltage: Value representing a type of impedance.
        :type voltage: Impedance() or float.
        """
        self.series_impedance[key] = impedance
    
    def set_series_admittance(self):
        """This method sets the admittance of the generator. Since the admittance is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the admittance attribute.
        :type key: str.
        :param voltage: Value representing a type of admittance.
        :type voltage: Admittance() or float.
        """
        d = DefaultDictFormat()
        mc = MagConversion()
        self.series_admittance = d.get_dict_struct(Admittance(None, None, 'Siemens'))
        self.series_admittance['nominal'].mag = pow(self.series_impedance['nominal'].mag, -1)
        self.series_admittance['nominal'].multiplier = mc.get_inverse_multiplier(self.series_impedance['nominal'].multiplier)
        


class MediumTLines():
    """This class models the eletric component of eletric power systems know as medium transmission line.
    """
    instances = []

    def __init__(self, series_impedance, shunt_impedance, terminals) -> None:
        """Constructor method.

        :param series_impedance: A medium transmission line is modeled as having a series impedance. This parameter specifies the impedance chacteristics.
        :type series_impedance: dict {'nominal': Impedance(), 'base': None, 'pu': None}.
        :param shunt_impedance: A medium transmission line is modeled as having a shunt impedance. This parameter specifies the impedance chacteristics.
        :type shunt_impedance: dict {'nominal': Impedance(), 'base': None, 'pu': None}.
        :param terminals:  A medium transmission line has a pair of terminals for this representation. This parameter specifies them.
        :type terminals: tuple.
        """
        self.name = 'Linha de Transmiss??o M??dia'
        MediumTLines.instances.append(self)
        self.id = len(MediumTLines.instances)
        self.series_impedance = series_impedance
        self.shunt_impedance = shunt_impedance
        self.shunt_impedance_per_side = cp.deepcopy(shunt_impedance)
        self.terminals = terminals
        self.correct_shunt_impedance_per_side()
        self.series_admittance = None
        self.set_series_admittance()
        self.shunt_admittance_per_side = None
        self.set_shunt_admittance_per_side()
    
    def correct_shunt_impedance_per_side(self):
        """This method corrects the value of shunt impedance per side.
        """
        self.shunt_impedance_per_side['nominal'].mag = 2 * self.shunt_impedance['nominal'].mag
        self.shunt_impedance_per_side['nominal'].characteristic = 'Shunt/lado'
        
    def set_shunt_impedance_per_side(self, key, impedance):
        """This method sets the shunt impedance per side of the medium transmission line. Since the impedance is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the impedance attribute.
        :type key: str.
        :param voltage: Value representing a type of impedance.
        :type voltage: Impedance() or float.
        """
        self.shunt_impedance_per_side[key] = impedance

    def set_series_impedance(self, key, impedance):
        """This method sets the series impedance of the medium transmission line. Since the impedance is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the impedance attribute.
        :type key: str.
        :param voltage: Value representing a type of impedance.
        :type voltage: Impedance() or float.
        """
        self.series_impedance[key] = impedance
    
    def set_shunt_impedance(self, key, impedance):
        """This method sets the shunt impedance of the medium transmission line. Since the impedance is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the impedance attribute.
        :type key: str.
        :param voltage: Value representing a type of impedance.
        :type voltage: Impedance() or float.
        """
        self.shunt_impedance[key] = impedance
    
    def set_series_admittance(self):
        """This method sets the admittance of the generator. Since the admittance is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the admittance attribute.
        :type key: str.
        :param voltage: Value representing a type of admittance.
        :type voltage: Admittance() or float.
        """
        d = DefaultDictFormat()
        mc = MagConversion()
        self.series_admittance = d.get_dict_struct(Admittance(None, None, 'Siemens'))
        self.series_admittance['nominal'].mag = pow(self.series_impedance['nominal'].mag, -1)
        self.series_admittance['nominal'].multiplier = mc.get_inverse_multiplier(self.series_impedance['nominal'].multiplier)
    
    def set_shunt_admittance_per_side(self):
        """This method sets the admittance of the generator. Since the admittance is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the admittance attribute.
        :type key: str.
        :param voltage: Value representing a type of admittance.
        :type voltage: Admittance() or float.
        """
        d = DefaultDictFormat()
        mc = MagConversion()
        self.shunt_admittance_per_side = d.get_dict_struct(Admittance(None, None, 'Siemens'))
        self.shunt_admittance_per_side['nominal'].mag = pow(self.shunt_admittance_per_side['nominal'].mag, -1)
        self.shunt_admittance_per_side['nominal'].multiplier = mc.get_inverse_multiplier(self.shunt_admittance_per_side['nominal'].multiplier)


class PowerFactor():
    """This class models the eletric characteristic of eletric power know as power factor.
    """
    def __init__(self, pf, characteristic) -> None:
        """Constructor method.

        :param pf: Power factor value ranging between ]0, 1].
        :type pf: float.
        :param characteristic: _description_
        :type characteristic: _type_
        """
        self.name = 'Fator de Pot??ncia'
        self.pf = pf
        self.characteristic = characteristic


class Loads():
    """This class models the eletric component of eletric power systems know as load.
    """
    instances = []

    def __init__(self, terminals, power=None, power_factor=None, impedance = None) -> None:
        """Constructor method.

        :param terminals: A load has a pair of terminals for this representation. This parameter specifies them.
        :type terminals: tuple.
        :param power: A load can be specified by it's power and power factor, this parameter specifies it's power, defaults to None.
        :type power: dict {'nominal': Power(), 'base': None, 'pu': None}, optional.
        :param power_factor: A load can be specified by it's power and power factor, this parameter specifies it's power factor, defaults to None.
        :type power_factor: PowerFactor(), optional.
        :param impedance: A load can be specified by it's impedance, this parameter specifies that, defaults to None.
        :type impedance: dict {'nominal': Impedance(), 'base': None, 'pu': None}, optional.
        """
        self.name = 'Carga'
        Loads.instances.append(self)
        self.id = len(Loads.instances)
        self.power = power
        self.pf = power_factor
        self.terminals = terminals

    def set_power(self, key, power):
        """This method sets the voltage of the generator. Since the voltage is a dict this method receives the key and the value to attribute.

        :param key: Dict key for the voltage attribute.
        :type key: str.
        :param voltage: Value representing a type of voltage.
        :type voltage: Voltage() or float.
        """
        self.power[key] = power


class Bars():
    """This class models the eletric element of eletric power systems know as bar.
    """
    def __init__(self) -> None:
        """Constructor method.
        """
        self.name = 'Barra'
        self.id = None
        self.adjacent = []
        self.isVisited = False
        self.voltage = None

    def set_id(self, id) -> None:
        """This method sets the instance attribute id with given parameter.

        :param id: Identifier for the bar.
        :type id: int.
        """
        self.id = id

    def get_bars(self, components) -> List:
        """This method returns a list to be iterated over when instatiating the bars.

        :param components: A list of the given eletric components .
        :type components: [Generators(), Transformers(), ShortTLines(), MediumTLines(), Loads()] or any combination of these objects.
        :return: A list of integers from 0 up to the higher terminal.
        :rtype: List.
        """
        t_list = [terminals for component in components for terminals in component.terminals]
        max_terminal = sorted(t_list)[-1]
        bar_list = [i for i in range(max_terminal + 1)]
        return bar_list

    def set_adjacent(self, components) -> None:
        """This method sets a list of adjacent bars to each bar.

        :param components: A list of the given eletric components .
        :type components: [Generators(), Transformers(), ShortTLines(), MediumTLines(), Loads()] or any combination of these objects.
        """
        for component in components:
            if self.id in component.terminals:
                if self.id != component.terminals[0]:
                    self.adjacent.append(component.terminals[0])
                else:
                     self.adjacent.append(component.terminals[1])

    def set_isVisited(self, isVisited) -> None:
        """This method sets the isVisited attribute of the caller instance to true.

        :param isVisited: This parameter is used as part of algorithm to go through all the bars.
        :type isVisited: bool
        """
        self.isVisited = isVisited
    
    def set_voltage(self, voltage) -> None:
        """This method sets the bar voltage attribute.

        :param voltage: Voltage value to be set. 
        :type voltage: float
        """
        self.voltage = MagConversion().get_value(voltage)

    def set_voltages(self, components, bars) -> None:
        """This method works recursively in order to visit all bars and set their base voltage.

        :param components: A list of the given eletric components .
        :type components: [Generators(), Transformers(), ShortTLines(), MediumTLines(), Loads()] or any combination of these objects.
        :param bars: A list with all the instances of Bars().
        :type bars: [Bar(1st instance), Bars(2nd instance), ...].
        :return: Since this is a recursive method it returns itself ultil reaches a base case.
        :rtype: itself
        """
        aux = self 
        while(aux != None):
            aux.isVisited = True
            for adjacent in aux.adjacent:
                if adjacent != 0: # N??o fazer nada para barra 0; 
                    if aux.voltage == None:
                        aux.voltage = aux.calcVoltage(components, bars)
                    if not bars[adjacent].isVisited:
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
        """This method returns the calculation of the bar voltage given the first known voltage connected to the bar.

        :param components: A list of the given eletric components .
        :type components: [Generators(), Transformers(), ShortTLines(), MediumTLines(), Loads()] or any combination of these objects.
        :param bars: A list with all the instances of Bars().
        :type bars: [Bar(1st instance), Bars(2nd instance), ...].
        :return: A float representing the bar base voltage.
        :rtype: float.
        """
        current_bar = self
        knowVoltageBar = current_bar.findFirstKnowVoltageBar(bars)
        terminals = (current_bar.id, knowVoltageBar.id)
        selected_component = None
        for component in components:
            if terminals[0] in component.terminals and terminals[1] in component.terminals:
                selected_component = component
                break
        if isinstance(selected_component, Transformers):
            transformer = selected_component
            voltage_h = (MagConversion().get_value(transformer.voltage_h), transformer.voltage_h['nominal'].bar)
            voltage_l = (MagConversion().get_value(transformer.voltage_l), transformer.voltage_l['nominal'].bar)
            transf_relation = voltage_h[0] / voltage_l[0]
            if current_bar.id == voltage_h[1]:
                current_bar.voltage = knowVoltageBar.voltage * transf_relation
            else:
                current_bar.voltage = knowVoltageBar.voltage / transf_relation
        elif isinstance(selected_component, ShortTLines) or isinstance(selected_component, MediumTLines):
            current_bar.voltage = knowVoltageBar.voltage
        return current_bar.voltage

    def findFirstKnowVoltageBar(self, bars):
        """This method returns the first known voltage of a adjacent bar of the current bar.

        :param bars: A list with all the instances of Bars().
        :type bars: [Bar(1st instance), Bars(2nd instance), ...].
        :return: Returns the voltage of the first adjacente bar with a known voltage.
        :rtype: float.
        """
        for adjacent in self.adjacent:
            if bars[adjacent].id != 0 and bars[adjacent].voltage != None:
                return bars[adjacent]


class PuConvesions():
    """This class is responsable for converting all power system inputed components to pu.
    """
    instances = []

    def __init__(self, sys_power, sys_voltage) -> None:
        """Constructor method.

        :param base_power: The inputed power base of the system in float format.
        :type base_power: float.
        """
        self.name = 'Classe Convers??o PU'
        PuConvesions.instances.append(self)
        self.id = len(PuConvesions.instances)
        self.sys_power = sys_power
        self.sys_voltage = sys_voltage

    def generator_to_pu(self, bars, components):
        """This method converts the generator nominal voltage and impedance to pu.

        :param bars: A list with all the instances of Bars().
        :type bars: [Bar(1st instance), Bars(2nd instance), ...].
        :param components: A list of the given eletric components .
        :type components: [Generators(), Transformers(), ShortTLines(), MediumTLines(), Loads()] or any combination of these objects.
        """
        generators = [component for component in components if isinstance(component, Generators)]
        mc = MagConversion()
        for gen in generators: 
            base_p = mc.get_value(self.sys_power)
            gen_npower = mc.get_value(gen.power)
            for bar in bars:
                if bar.id == gen.terminals[1] and bar.id != 0:
                    # Converting power to pu
                    gen.set_power('base', base_p)
                    gen.set_power('pu', gen_npower / base_p)
                    # Converting voltage to pu
                    gen_nvoltage = mc.get_value(gen.voltage['nominal'])
                    gen.set_voltage('base', bar.voltage)
                    gen.set_voltage('pu', gen_nvoltage / bar.voltage)
                    # Converting impedance to pu
                    gen_nimpedance = mc.get_value(gen.impedance['nominal'])
                    gen.set_impedance('base', pow(gen_nvoltage, 2) / gen_npower)
                    gen.set_impedance('pu', gen_nimpedance * gen.impedance['base'] * (base_p / pow(bar.voltage, 2)))
                    # Setting Admitance
            Print.print_components(gen)

    def transformer_to_pu(self, bars, components):
        """This method converts the transformer nominal impedance to pu.

        :param bars: A list with all the instances of Bars().
        :type bars: [Bar(1st instance), Bars(2nd instance), ...].
        :param components: A list of the given eletric components .
        :type components: [Generators(), Transformers(), ShortTLines(), MediumTLines(), Loads()] or any combination of these objects.
        """
        transformers = [component for component in components if isinstance(component, Transformers)]
        mc = MagConversion()
        for tran in transformers: 
            # Getting power values
            base_p = mc.get_value(self.sys_power)
            tran_npower = mc.get_value(tran.power)
            # Converting power to pu
            tran.set_power('base', base_p)
            tran.set_power('pu', tran_npower / base_p)
            # Getting transformer nominal values
            tran_nhv = mc.get_value(tran.voltage_h['nominal'])
            tran_nlv = mc.get_value(tran.voltage_l['nominal'])  
            tran_nz = mc.get_value(tran.impedance['nominal'])  
            # Setting high and low voltage bars
            bar_h = tran.voltage_h['nominal'].bar
            bar_l = tran.voltage_l['nominal'].bar
            # Setting high and low voltages basys
            h_voltage_base = bars[bar_h].voltage
            l_voltage_base = bars[bar_l].voltage
            for bar in bars:
                # Match current trasformer terminal with bar
                if bar.id in tran.terminals:
                    # Converting voltage high to pu
                    tran.set_voltage_h('base', h_voltage_base)
                    tran.set_voltage_h('pu', tran_nhv / h_voltage_base)
                    # Converting voltage low to pu
                    tran.set_voltage_l('base', l_voltage_base)
                    tran.set_voltage_l('pu', tran_nlv / l_voltage_base)
                    # Converting impedance to pu
                    tran.set_impedance('base', pow(tran_nhv, 2) / tran_npower)
                    tran.set_impedance('pu', tran_nz * tran.impedance['base'] * (base_p / pow(h_voltage_base, 2)))
            Print.print_components(tran)
            
    def tlines_to_pu(self, bars, components):
        """This method converts the transmission lines nominal impedance to pu.

        :param bars: A list with all the instances of Bars().
        :type bars: [Bar(1st instance), Bars(2nd instance), ...].
        :param components: A list of the given eletric components .
        :type components: [Generators(), Transformers(), ShortTLines(), MediumTLines(), Loads()] or any combination of these objects.
        """
        tlines = [component for component in components if isinstance(component, ShortTLines) or isinstance(component, MediumTLines)]
        mc = MagConversion()
        # Getting power base values
        base_p = mc.get_value(self.sys_power)
        
        for line in tlines:
            for bar in bars:
                # Match current bar with transmission line in question
                if bar.id in line.terminals:
                    # Getting voltage and impedance base values
                    base_v = bar.voltage
                    # Setting base impedance
                    base_z = pow(base_v, 2) / base_p
                    ######################################################################## Converting impedance to pu
                    # Get nominal series impedance value
                    line_sz = mc.get_value(line.series_impedance['nominal'])
                    print(f'line_sz = {line_sz}', file=sys.stderr)
                    # Setting base series impedance
                    line.set_series_impedance('base', base_z)
                    # Setting pu series impedance
                    line.set_series_impedance('pu', line_sz / line.series_impedance['base'])

                    if isinstance(line, MediumTLines):
                        # Get nominal shunt and shunt per side impedance values
                        line_shz = mc.get_value(line.shunt_impedance['nominal'])
                        line_shzps = mc.get_value(line.shunt_impedance_per_side['nominal'])
                        # Set shunt and shunt per side base impedance values
                        line.set_shunt_impedance('base', base_z)
                        line.set_shunt_impedance_per_side('base', base_z)
                        # Set shunt and shunt per side pu impedance values
                        line.set_shunt_impedance('pu', line_shz / line.shunt_impedance['base'])
                        line.set_shunt_impedance_per_side('pu', line_shzps / line.shunt_impedance_per_side['base'])
            Print.print_components(line)

    def loads_to_pu(self, bars, components):
        """This method converts the loads nominal power to pu.

        :param bars: A list with all the instances of Bars().
        :type bars: [Bar(1st instance), Bars(2nd instance), ...].
        :param components: A list of the given eletric components .
        :type components: [Generators(), Transformers(), ShortTLines(), MediumTLines(), Loads()] or any combination of these objects.
        """
        loads = [component for component in components if isinstance(component, Loads)]
        mc = MagConversion()
        
        for load in loads:
            load_power = mc.get_value(load.power['nominal'])
            load_base_power = mc.get_value(self.sys_power)
            load.set_power('base', load_base_power)
            load.set_power('pu', load_power / load_base_power)

            Print.print_components(load)
            

class Print():
    """This class hosts the print methods.
    """
    @staticmethod
    def print_components(instance):
        """this stactic method prints all pertinent information about a given power system component

        :param instance: A power system component such as any instance of the following classes: Generators(), Transformers(), ShortTLines(), MediumTLines() or Loads().
        :type instance: Generators(), Transformers(), ShortTLines(), MediumTLines() or Loads().
        """
        mc = MagConversion()
        print(f"{str(instance)[10:-30]}[{instance.id}]")
        for attr, value in instance.__dict__.items():
            if 'impedance' in attr:
                print(f"{attr} = {str(value)[:12]}{mc.get_value(value['nominal'])}{str(value)[61:]}")
            if 'voltage' in attr:
                print(f"{attr} = {str(value)[:12]}{mc.get_value(value['nominal'])}{str(value)[59:]}")
            if 'power' in attr:
                print(f"{attr} = {str(value)[:12]}{mc.get_value(value['nominal'])}{str(value)[57:]}")


class FormToObj():
    component_list = []

    @staticmethod
    def pu_conv_sb(form):
        d = DefaultDictFormat()
        power_sb = Power(complex(form.power_mag.data), form.power_mult.data, form.power_measure.data)
        voltage_sb = d.get_dict_struct(Voltage(complex(form.voltage_mag.data), form.voltage_mult.data, form.voltage_measure.data, form.bar.data))
        pu_conv = PuConvesions(power_sb, voltage_sb) 
        FormToObj.component_list.append(pu_conv)
        
        # print(f'/puconversions.py -> pu_conv_sb -> FormToObj.component_list = {FormToObj.component_list}', file=sys.stderr)
        return FormToObj.component_list
        
    @staticmethod
    def generator(form):
        d = DefaultDictFormat()
        pg = d.get_dict_struct(Power(complex(form.power_mag.data), form.power_mult.data, form.power_measure.data))
        tg = (0, form.t1.data)
        vg = d.get_dict_struct(Voltage(complex(form.voltage_mag.data), form.voltage_mult.data, form.voltage_measure.data, form.t1.data))
        zpug = d.get_dict_struct(Impedance(complex(form.impedance_mag.data), form.impedance_mult.data, form.impedance_measure.data, 'S??rie'))
        g = Generators(zpug, tg, pg, vg)
        FormToObj.component_list.append(g)
        # print(f'/puconversions.py -> generator -> FormToObj.component_list = {FormToObj.component_list}', file=sys.stderr)
        return FormToObj.component_list

    @staticmethod
    def transformer(form):
        d = DefaultDictFormat()
        pt = d.get_dict_struct(Power(complex(form.power_mag.data), form.power_mult.data, form.power_measure.data))
        tt = (form.t0.data, form.t1.data)
        vht = d.get_dict_struct(Voltage(complex(form.high_voltage_mag.data), form.high_voltage_mult.data, form.high_voltage_measure.data, form.t0.data))
        vlt = d.get_dict_struct(Voltage(complex(form.low_voltage_mag.data), form.low_voltage_mult.data, form.low_voltage_measure.data, form.t1.data))
        zput = d.get_dict_struct(Impedance(complex(form.impedance_mag.data), form.impedance_mult.data, form.impedance_measure.data, 'S??rie'))
        t = Transformers(zput, tt, pt, vht, vlt)
        FormToObj.component_list.append(t)
        # print(f'/puconversions.py -> transformer -> FormToObj.component_list = {FormToObj.component_list}', file=sys.stderr)
        return FormToObj.component_list

    @staticmethod
    def short_tline(form):
        d = DefaultDictFormat()
        tstl = (form.t0.data, form.t1.data)
        if form.lenght.data:
            zsstl = d.get_dict_struct(Impedance(complex(form.series_impedance_mag.data), form.series_impedance_mult.data, form.series_impedance_measure.data, 'S??rie', float(form.lenght.data)))
        else:
            zsstl = d.get_dict_struct(Impedance(complex(form.series_impedance_mag.data), form.series_impedance_mult.data, form.series_impedance_measure.data, 'S??rie'))
        stl = ShortTLines(zsstl, tstl)
        FormToObj.component_list.append(stl)
        # print(f'/puconversions.py -> short_tline -> FormToObj.component_list = {FormToObj.component_list}', file=sys.stderr)
        return FormToObj.component_list

    @staticmethod
    def medium_tline(form):
        d = DefaultDictFormat()
        tmtl = (form.t0.data, form.t1.data)
        if form.lenght.data:
            zsmtl = d.get_dict_struct(Impedance(complex(form.series_impedance_mag.data), form.series_impedance_mult.data, form.series_impedance_measure.data, 'S??rie', float(form.lenght.data)))
            zshmtl = d.get_dict_struct(Impedance(complex(form.shunt_impedance_mag.data), form.shunt_impedance_mult.data, form.shunt_impedance_measure.data, 'Shunt', float(form.lenght.data)))
        else:
            zsmtl = d.get_dict_struct(Impedance(complex(form.series_impedance_mag.data), form.series_impedance_mult.data, form.series_impedance_measure.data, 'S??rie'))
            zshmtl = d.get_dict_struct(Impedance(complex(form.shunt_impedance_mag.data), form.shunt_impedance_mult.data, form.shunt_impedance_measure.data, 'Shunt'))
        mtl = MediumTLines(zsmtl, zshmtl, tmtl)
        FormToObj.component_list.append(mtl)
        # print(f'/puconversions.py -> medium_tline -> FormToObj.component_list = {FormToObj.component_list}', file=sys.stderr)
        return FormToObj.component_list

    @staticmethod
    def load(form):
        d = DefaultDictFormat()
        pld = d.get_dict_struct(Power(complex(form.power_mag.data), form.power_mult.data, form.power_measure.data))
        tld = (0, form.t1.data)
        pfld = PowerFactor(form.power_factor_mag.data, form.power_factor_characteristic.data)
        ld = Loads(tld, pld, pfld)
        FormToObj.component_list.append(ld)
        # print(f'/puconversions.py -> load -> FormToObj.component_list = {FormToObj.component_list}', file=sys.stderr)
        return FormToObj.component_list

    @staticmethod
    def get_components():
        return FormToObj.component_list
    
    @staticmethod
    def del_components():
        FormToObj.component_list = []
        return FormToObj.component_list


class Validation():
    @staticmethod
    def validate_system_connections(component_list):
        continuity_check = False
        used = []
        unused = []
        for component in component_list:
            if not isinstance(component, PuConvesions):
                if isinstance(component, Generators) and 1 in component.terminals:
                    used.append(component.terminals)
                else:
                    unused.append(component.terminals)
        terminal_pair_count = len(unused) + len(used)
        for used_pair in used:
            for used_pair_terminal in used_pair:
                if used_pair_terminal != 0:
                    for unused_pair in unused:
                        if used_pair_terminal in unused_pair:
                            used.append(unused_pair)
                            unused.remove(unused_pair)
                            break
            if len(used) == terminal_pair_count:
                continuity_check = True
                break
        return continuity_check


class Run():
    @staticmethod
    def prep_bars(components):
        # Instantiating bars
        bars = [Bars() for i in Bars().get_bars(components)]
        # Setting bars Id's
        for i in range(len(bars)): bars[i].set_id(i)
        # Setting adjacent bars
        for bar in bars: bar.set_adjacent(components)
        return bars
    
    @staticmethod
    def set_base_voltages(bars, conv, components):
        # Defining groung and head bar
        ground_bar = bars[0]
        ground_bar.set_voltage(Voltage(0, 'k', 'V', 0))
        head = bars[conv.sys_voltage['nominal'].bar]
        bars[head.id].set_voltage(conv.sys_voltage['nominal'])
        head.set_voltages(components, bars)


def run(components):
    """The main functions execute the method calls in order to get the script output.
    """
    # try:
    # Get Pu Conversion class
    conv = components[0]
    # Get system components only
    components = components[1:]
    # Setting Id and adjacent bars
    bars = Run().prep_bars(components)
    # Setting system base voltages
    Run().set_base_voltages(bars, conv, components)

    # Converting system components to pu
    conv.generator_to_pu(bars, components)
    conv.transformer_to_pu(bars, components)
    conv.tlines_to_pu(bars, components)
    conv.loads_to_pu(bars, components)

    # Grouping results to return
    components.insert(0, conv)

    # for component in components:
    #     print(f"{component.name}", file=sys.stderr)
    #     for attr, value in component.__dict__.items():
    #         if 'power' in attr:
    #             print(f"attr, value  = {attr, value}", file=sys.stderr)
    #         if 'voltage' in attr:
    #             print(f"attr, value  = {attr, value}", file=sys.stderr)
    #         if 'impedance' in attr:
    #             print(f"attr, value  = {attr, value}", file=sys.stderr)


    return components










    # except:
    #     return None


# def run():
    """The main functions execute the method calls in order to get the script output.
    """
    # d = DefaultDictFormat()
    # # System basis
    # base_values = [
    #     Power(100, 'M', 'VA'),
    #     Voltage(13.8, 'k', 'V', 1)
    # ]
    # # Generators
    # pg1, tg1 = d.get_dict_struct(Power(60, 'M', 'VA')), (0, 1)
    # vg1 = d.get_dict_struct(Voltage(13.2, 'k', 'V', 1))
    # zpug1 = d.get_dict_struct(Impedance(30, '%', 'pu', 'series'))
    # g1 = Generators(zpug1, tg1, pg1, vg1)

    # # Transformers
    # pt1, tt1 = d.get_dict_struct(Power(50, 'M', 'VA')), (2, 1) 
    # vht1 = d.get_dict_struct(Voltage(132, 'k', 'V', 2))
    # vlt1 = d.get_dict_struct(Voltage(13.2, 'k', 'V', 1))
    # zput1 = d.get_dict_struct(Impedance(5, '%', 'pu', 'series'))
    # t1 = Transformers(zput1, tt1, pt1, vht1, vlt1)
    # pt2, tt2 = d.get_dict_struct(Power(50, 'M', 'VA')), (3, 4)
    # vht2 = d.get_dict_struct(Voltage(135, 'k', 'V', 3))
    # vlt2 = d.get_dict_struct(Voltage(13.2, 'k', 'V', 4))
    # zput2 = d.get_dict_struct(Impedance(6, '%', 'pu', 'series'))
    # t2 = Transformers(zput2, tt2, pt2, vht2, vlt2)

    # # Medium Lines
    # zsl1 = d.get_dict_struct(Impedance(0.4j, ' ', 'ohm/km', 'series', 97))
    # zshl = d.get_dict_struct(Impedance(280j, ' ', 'kohm*km', 'shunt', 97))
    # tl1 = (2, 3)
    # l1 = MediumTLines(zsl1, zshl, tl1)
    # zsl2 = d.get_dict_struct(Impedance(1.05 + 0.4j, ' ', 'ohm/km', 'series', 150)) 
    # zshl2 = d.get_dict_struct(Impedance(280j, ' ', 'kohm*km', 'shunt', 150)) 
    # tl2 = (1, 5)
    # l2 = MediumTLines(zsl2, zshl2, tl2)

    # # Loads
    # pld1 = d.get_dict_struct(Power(35, 'M', 'VA'), base_values[0])
    # pfld1, tld1 = PowerFactor(0.98, 'adiantado'), (4, 0)
    # ld1 = Loads(tld1, pld1, pfld1)
    # pld2 = d.get_dict_struct(Power(2, 'M', 'W'), base_values[0])
    # pfld2, tld2 = PowerFactor(0.85, 'atrasado'), (5, 0)
    # ld2 = Loads(tld2, pld2, pfld2)

    # # print(f'components = {components}', file=sys.stderr)


        # components = [g1, t1, l1, t2, ld1, l2, ld2]
        # head = bars[base_values[1].bar]
        # bars[head.id].set_voltage(base_values[1])
        # Calculating base voltages

        # for bar in bars: print(f"bar[{bar.id}].voltage = {bar.voltage}")

        # Pu Conversion
        # conv = PuConvesions(base_values[0], base_values[1])

# run()