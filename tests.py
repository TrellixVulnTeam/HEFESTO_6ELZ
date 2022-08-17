class Impedance():
    def __init__(self, symbol, mag, lenght=None) -> None:
        self.symbol = symbol
        self.mag = mag
        self.len = lenght
        self.check_format()
  
    def check_format(self):
        if self.symbol == 'series':
            self.mag *= self.len
        elif self.symbol == 'shunt':
            self.mag /= self.len

# z = Impedance('ohm', 10 + 30j)
z = Impedance('series', 0.25 + 0.625j, 80)
# Impedance('shunt', 25000 - 68000j)
# Impedance('pu', 0.25 + 0.625j)
print(z.mag)
