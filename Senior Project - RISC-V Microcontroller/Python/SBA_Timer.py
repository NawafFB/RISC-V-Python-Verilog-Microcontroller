from myhdl import *

"""
@input: STB - signal to enable the timer
@input: base - base value of the timer
@input: clk - clock to drive the timer
@input: reset - reset signal
@output: flag - timer flag signal
"""

@block
def SBA_TIMER(STB, base, clk, reset, flag):
    state = Signal(bool(0))
    count_enable = Signal(bool(0))
    counter = Signal(modbv(0)[8:])
    next_state = Signal(bool(0))
    base_reg = Signal(modbv(0)[8:])
    enable = Signal(bool(0))
    start = Signal(bool(0))
    stop = Signal(bool(0))

    @always_comb
    def connect():
        enable.next = STB[3]
        start.next = STB[1]
        stop.next = STB[0]

    @always(clk.posedge, reset.posedge)
    def state_machine():
        if reset:
            state.next = False  # idle
        else:
            state.next = next_state

    @always(flag.posedge, enable.posedge, start.posedge, stop.posedge)
    def next_state_machine():
        if state == 0:
            if enable == 1:
                next_state.next = True
                base_reg.next = base
            else:
                next_state.next = False
        elif state == 1:
            if stop == 1:
                next_state.next = False
            elif flag == 1:
                next_state.next = False
            else:
                next_state.next = True
        else:
            next_state.next = False

    @always(state)
    def enable_machine():
        if state == 1:
            count_enable.next = True
        else:
            count_enable.next = False

    @always(clk.posedge, reset.posedge)
    def timer():
        if reset:
            flag.next = False
            counter.next = False
        else:
            if not count_enable:
                counter.next = base_reg
                if next_state:
                    flag.next = False
            if count_enable:
                counter.next = counter + 1
                if counter == 0b11111111:
                    flag.next = True
                    counter.next = False

    return instances()


if __name__ == '__main__':
    base = Signal(intbv(0)[8:])
    STB = Signal(intbv(0)[4:])
    clk = Signal(bool(0))
    reset = Signal(bool(0))
    flag = Signal(bool(0))
    toVerilog.initial_values = True

    PWM = SBA_TIMER(STB, base, clk, reset, flag)

    PWM.run_sim()
    PWM.convert(hdl='verilog')
