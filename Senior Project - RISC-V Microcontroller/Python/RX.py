from myhdl import *

'''
@input: clk
@input: reset
@input: RxEn : enable the module
@input: Nbits : number of bits hold in the RX module
@input: Rx : data coming from the RX pin 
@input: tick : clock coming from the baud rate generator
@output: RxData : received data (going to the data bus)
@output: RxDone : completion flag
'''


@block
def RX(clk, reset, RxEn, RxData, RxDone, Rx, tick, Nbits):
    # local variables
    state = Signal(intbv(0)[2:])  # 1 = read, 0 = idle
    next_state = Signal(intbv(0)[2:])
    read_enable = Signal(bool(0))
    start_bit = Signal(bool(1))
    Bit = Signal(intbv(0)[5:])
    counter = Signal(modbv(0)[4:])
    Read_data = Signal(intbv(0)[8:])

    """ reset module """

    @always(clk.posedge, reset.posedge)
    def reset_module():
        if reset:
            state.next = False  # go back to the idle state
        else:
            state.next = next_state  # go to the next state

    """ next step decision """

    @always(state, Rx, RxEn, RxDone)
    def next_state_module():
        # print(now(), 'current state:', state, 'Rx:', Rx, 'RxEn:', RxEn)
        if state == 0:  # idle state
            if (not Rx) and RxEn:  # the Rx module is enabled
                next_state.next = True  # start reading
            else:
                next_state.next = False  # stay at the idle state
        elif state == 1:  # read state
            if RxDone:
                # print('--- RX module done reading, the output value is:', RxData, '---')
                next_state.next = False  # stop reading
            else:
                next_state.next = True  # keep reading
        else:
            next_state.next = False  # idle state by default

    """ RxEn read or not """

    @always(state, RxDone)
    def enable_read_func():
        if state == 1:  # read state
            read_enable.next = True  # RxEn reading
        else:  # idle state and default
            read_enable.next = False  # disable reading

    """ read input data """

    @always(tick.posedge)
    def read_data_func():
        # print('in read input data!')
        if read_enable:
            # print('read is enabled, increment the counter, counter value:', counter)
            # print(now(), 'tick counter:', counter, 'the current value of Rx is:', Rx)
            RxDone.next = False  # not RxDone reading
            counter.next = counter + 1

            if counter == 8 and start_bit:  # we're at the middle of the start bit
                # print(now(), '*** RX 1: start bit value:', Rx, '***')
                start_bit.next = False
                counter.next = False

            if counter == 15 and not start_bit and Bit < Nbits:  # at the middle of bit number n
                # print(now(), '*** RX 2: received value:', Rx, '***')
                Bit.next = Bit + 1
                Read_data.next = concat(Rx, Read_data[8:1])
                counter.next = False

            if counter == 15 and Bit == Nbits and Rx:  # at the middle of the stop bit
                # print(now(), '*** RX 3: stop bit value:', Rx, '***')
                Bit.next = False
                RxDone.next = True
                counter.next = False
                start_bit.next = True

        # if counter == 15 and Bit == Nbits and not Rx:
        #     # print('stop bit no received !!! counter will reset')
        #     counter.next = False

    """ output assign """

    @always(clk.posedge)
    def assign_output():
        if Nbits == 8:
            RxData.next = Read_data[8:0]
        if Nbits == 7:
            RxData.next = concat(False, Read_data[8:1])
        if Nbits == 6:
            RxData.next = concat(False, False, Read_data[8:2])

    return instances()


if __name__ == '__main__':
    clk = Signal(bool(0))
    reset = Signal(bool(0))
    RxEn = Signal(bool(0))
    RxData = Signal(intbv(0)[8:])
    RxDone = Signal(bool(0))
    Rx = Signal(bool(0))
    tick = Signal(bool(0))
    Nbits = Signal(intbv(0)[4:])

    tb = RX(clk, reset, RxEn, RxData, RxDone, Rx, tick, Nbits)
    toVerilog.initial_values = True
    tb.convert(hdl='verilog')
