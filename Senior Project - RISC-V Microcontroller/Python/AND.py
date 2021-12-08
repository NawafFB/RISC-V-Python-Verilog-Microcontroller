from myhdl import *

'''
simple logical AND gate

@input : val1 - first value
@input : val2 - second value
@output : result - result from AND gate
'''
@block
def AND(val1, val2, result):
    @always_comb
    def add():
        result.next = val1 and val2

    return instances()


if __name__ == '__main__':
    val1 = Signal(bool(0))
    val2 = Signal(bool(0))
    result = Signal(bool(0))

    AND_sim = AND(val1, val2, result)
    AND_sim.run_sim()
    AND_sim.convert(hdl='verilog')
