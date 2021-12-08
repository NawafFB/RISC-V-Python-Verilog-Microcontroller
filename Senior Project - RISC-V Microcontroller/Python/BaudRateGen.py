from lib2to3.pytree import convert

import myhdl as hdl
from myhdl import *

'''
Arithmetic Logic Unit 

@input : clock - clock that drives the baud rate generator
@input : reset - signal toreset the module
@input : baudRateDiv - value of the desired baud rate / 16
@input : enable - enable signal
@output : tick - ticks that will be drive the Tx and Rx modules
'''
@block
def BRG(clock, reset, tick, baudRateDiv, enable):
    baudRateReg = Signal(modbv(0)[32:])  # register to count until it reaches the value of baudRateDiv
    R_edge = Signal(intbv(0)[2:])
    D_edge = Signal(bool(0))

    @always(clock.posedge, reset.posedge)
    def gen():
        if reset:
            baudRateReg.next = True
        else:
            if D_edge:
                baudRateReg.next = True
            elif tick == 1:
                baudRateReg.next = True
            else:
                baudRateReg.next = baudRateReg + 0b1

    @always_comb
    def compare():
        tick.next = (baudRateReg == baudRateDiv)

    @always(clock.posedge)
    def input_detect():
        if reset:
            R_edge.next = 0
        else:
            R_edge.next = concat(R_edge[0], enable)

    @always_comb
    def cont():
        D_edge.next = not R_edge[1] and R_edge[0]  # this makes sure that the enable signal is read once

    return instances()

@block
def test():
    clock = Signal(bool(0))
    reset = Signal(bool(0))
    baudRateDiv = (Signal(intbv(0)[15:]))
    tick = Signal(bool(0))

    @always(delay(5))
    def gen():
        clock.next = not clock

    uart = BRG(clock, reset, baudRateDiv, tick)

    @instance
    def testBench():
        baudRateDiv.next = 5
        yield clock.posedge

    return instances()


if __name__ == '__main__':
    clock = Signal(bool(0))
    reset = Signal(bool(0))
    baudRateDiv = (Signal(intbv(0)[16:]))
    tick = Signal(bool(0))

    tb = BRG(clock, reset, tick, baudRateDiv)
    tb.run_sim()
    toVerilog.initial_values = True
    tb.convert(hdl='verilog')

# tb = test()
# tb.run_sim(1000)
