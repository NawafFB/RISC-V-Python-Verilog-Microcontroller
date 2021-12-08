from myhdl import *

'''
SBA Pulse Width Modulation Module

This module is responsible for sending a pulse modulated signal outside the microcontrller.
@input: data - data coming from the CPU that contains the active and period times.
@input: reset - reset signal
@input: clk - clock that will drive the module.
@input: STB - enable signal
@output: pwmSignal - pulse modulated signal
'''
@block
def SBA_PWM(data, reset, clk, STB, pwmSignal):
    load_comp = Signal(bool(0))
    loadCNT = Signal(bool(0))
    EN_CNT = Signal(bool(0))
    is_zero = Signal(bool(0))

    DP = DataPath(STB, data, clk, load_comp, loadCNT, reset, EN_CNT, pwmSignal, is_zero)
    CU = ControlUnit(is_zero, reset, clk, STB, load_comp, loadCNT, EN_CNT)

    return instances()


@block
def DataPath(STB, data, clk, load_comp, loadCNT, reset, EN_CNT, pwmSignal, is_zero):
    COMP0_out = Signal(intbv(0)[16:])
    COMP1_out = Signal(intbv(0)[16:])
    CNT_out = Signal(intbv(0)[16:])
    period = Signal(intbv(0)[16:])
    active = Signal(intbv(0)[16:])
    load_enable = Signal(bool(0))

    REG1 = REG_16bit(period, load_comp, clk, reset, COMP0_out)
    REG2 = REG_16bit(active, load_comp, clk, reset, COMP1_out)

    CNT = CountDown_REG(period, EN_CNT, loadCNT, clk, reset, CNT_out)

    Zero_comp = Zero_COMP(CNT_out, is_zero)
    ACT_COMP = Active_Comparator(COMP1_out, CNT_out, pwmSignal)

    @always_comb
    def EN():
        load_enable.next = STB[3]

    @always(load_enable.posedge)
    def connect():
        if STB[3]:
            period.next = data[32:16]
            active.next = data[16:]

    return instances()

'''
Control Unit

This module in the PWM is responsible for controlling the flow of data inside the PWM module.
'''
@block
def ControlUnit(is_zero, reset, clk, STB, load_comp, loadCNT, EN_CNT):
    R_edge = Signal(intbv(0)[2:])  # Variable used to avoid debounce of the write enable pin
    D_edge = Signal(bool(0))  # Wire used to connect the D_edge
    state = Signal(intbv(0)[1:])

    # idle 0
    # run  1

    @always(clk.posedge)
    def CU():

        if reset:
            load_comp.next = False
            loadCNT.next = False
            EN_CNT.next = False
            state.next = False
        else:

            load_comp.next = False
            loadCNT.next = False
            EN_CNT.next = False

            if state == 0:  # idle state
                EN_CNT.next = False
                load_comp.next = True
                loadCNT.next = True
                if D_edge :  # and STB[3]
                    state.next = True  # go to run mode
                else:
                    state.next = 0  # stay idle

            elif state == 1:
                EN_CNT.next = True
                if is_zero:
                    loadCNT.next = True
                elif STB[1] == 0 and STB[3] == 1:
                    state.next = False

            else:
                state.next = False

            if D_edge and STB[3]:
                loadCNT.next = True
                load_comp.next = True

    @always(clk.posedge, reset.posedge)
    def input_detect():
        if reset:
            R_edge.next = 0
        else:
            if STB[3]:
                R_edge.next = concat(R_edge[0], STB[1])

    @always_comb
    def cont():
        D_edge.next = not R_edge[1] and R_edge[0]  # this makes sure that the enable signal is read once

    return instances()


@block
def REG_16bit(data_in, load_comp, clk, reset, data_out):
    storage = Signal(intbv(0)[16:])

    @always(clk.posedge, reset.posedge)
    def reg():
        if reset:
            storage.next = False  # reset
        else:
            if load_comp:
                storage.next = data_in

    @always_comb
    def out():
        data_out.next = storage

    return instances()


@block
def Zero_COMP(CNT, zero):
    @always_comb
    def comp():
        if CNT == 1:
            zero.next = 1
        else:
            zero.next = 0

    return instances()

'''
Active Comparator

A comparator that will keep comparing the value of the CountDown_REG and the active value stored in comp1.
'''
@block
def Active_Comparator(comp1, CNT, PWM_out):
    @always_comb
    def comp():
        if CNT < comp1:
            PWM_out.next = 1
        else:
            PWM_out.next = 0

    return instances()

'''
Count Down Register

This module counts down starting from the period time until it reaches zero.
'''
@block
def CountDown_REG(data, EN_CNT, loadCNT, clk, reset, CNT_out):
    value = Signal(modbv(0)[16:])

    @always_comb
    def out():
        CNT_out.next = value

    @always(clk.posedge)  # or load.posedge
    def LD():

        if reset:
            value.next = 0  # reset
        else:
            if loadCNT:
                value.next = data

            elif EN_CNT:
                value.next = value - 1  # decrement the value of the counter by one.

    return instances()


@block
def TestBench():
    period = Signal(intbv(0)[16:])
    active = Signal(intbv(0)[16:])
    start = Signal(bool(0))
    stop = Signal(bool(0))
    clk = Signal(bool(0))
    pwm_output = Signal(bool(0))

    PWM = SBA_PWM(period, active, start, stop, clk, pwm_output)

    @always(delay(5))
    def toggle():
        clk.next = not clk

    @instance
    def T():
        print(now(), "PWM output", pwm_output)
        period.next = 30
        active.next = 15
        yield delay(30)
        start.next = 1

        yield start.posedge
        print(now(), 'started')

    @always(clk.posedge)
    def show():
        print(now(), "PWM output", pwm_output)

    return instances()


# t = TestBench()
# t.run_sim(400)

if __name__ == '__main__':
    data = Signal(intbv(0)[32:])
    STB = Signal(intbv(0)[4:])
    clk = Signal(bool(0))
    reset = Signal(bool(0))
    pwmSignal = Signal(bool(0))
    toVerilog.initial_values = True

    PWM = SBA_PWM(data, reset, clk, STB, pwmSignal)

    PWM.run_sim()
    PWM.convert(hdl='verilog')
