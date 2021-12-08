from myhdl import *

"""
@input: Clk - clock to drive the Tx module
@input: Tick - Tick coming from the BRG
@input: Rst_n - reset signal
@input: TxEn : signal to enable the module
@input: NBits : number of bits to send
@input: TxData : parallel input data from the CPU to transmit
@output: Tx - bits transmitted
@output: TxDone - completion flag
"""

@block
def TX(Clk, Rst_n, TxEn, TxData, TxDone, Tx, Tick, NBits):
    # local variables
    state = Signal(bool(0))  # 1 = read, 0 = idle
    next_state = Signal(bool(0))
    write_enable = Signal(bool(0))
    start_bit = Signal(bool(1))
    stop_bit = Signal(bool(0))
    Bit = Signal(intbv(0)[5:])
    counter = Signal(modbv(0)[4:])
    in_data = Signal(intbv(0)[8:])
    R_edge = Signal(intbv(0)[2:])  # Variable used to avoid debounce of the write enable pin
    D_edge = Signal(bool(0))  # Wire used to connect the D_edge

    """ Rst_n module """

    @always(Clk.posedge, Rst_n.posedge)
    def reset_module():
        if Rst_n:
            state.next = False  # go back to the idle state
        else:
            state.next = next_state  # go to the next state

    """ next step decision """

    @always(state, D_edge, TxData, TxDone)
    def next_state_module():
        if state == 0:  # idle state
            if D_edge:
                next_state.next = True
            else:
                next_state.next = False

        elif state == 1:  # writing state
            if TxDone:  # done writing
                next_state.next = False  # stay at idle
            else:
                next_state.next = True  # start writing

        else:
            next_state.next = False  # idle by default

    """ enable writing or not """

    @always(state)
    def write_enable_func():
        if state == 1:
            write_enable.next = True
        else:
            write_enable.next = False

    """ write data to Tx pin """

    @always(Tick.posedge)
    def Tx_output():
        if not write_enable:
            if TxEn:
                TxDone.next = False
            start_bit.next = True
            stop_bit.next = False

        elif write_enable:
            counter.next = counter + 1  # add 1 to tick counter

            if start_bit and not stop_bit:  # before we send the data, we need to send the start bit
                # print(now(), '*** TX 1: start bit value:', Tx, '***')
                Tx.next = False  # output the start bit (low signal)
                in_data.next = TxData  # save the data in the in_data register to send it out of the UART bit by bit

            if counter == 15 and start_bit:  # check if we're at the middle of the first bit (after the start bit)
                # print(now(), '*** TX 1: start bit value:', bin(Tx), '***')
                start_bit.next = False  # we are past the start bit, disable it.
                in_data.next = concat(False, in_data[8:1])  # shift the in_data register to the right once
                Tx.next = in_data[0]  # output the first bit saved in the in_data register

            if counter == 15 and not start_bit and Bit < NBits - 1:  # loop through the remaining 7 bits
                # print(now(), '*** TX 2: bit value:', bin(Tx), '***')
                in_data.next = concat(False, in_data[8:1])  # shift the in_data register to the right once
                Bit.next = Bit + 1  # increment the number of the current bit (move to the next bit)
                Tx.next = in_data[0]
                start_bit.next = False  # we are past the start bit, keep disabling it.
                counter.next = False  # Rst_n the counter

            if counter == 15 and Bit == NBits - 1 and not stop_bit:  # we reached the end, raise the stop bit
                # print(now(), '*** TX 3: last bit value:', bin(Tx), '***')
                Tx.next = True  # raise the stop bit
                counter.next = False  # Rst_n the counter
                stop_bit.next = True  # enable the stop bit

            if counter == 15 and Bit == NBits - 1 and stop_bit:  # we sent a full byte
                # print(now(), '*** TX 4: stop bit value:', bin(Tx), '***')
                Bit.next = False  # Rst_n the bits counter
                TxDone.next = True  # raise the done flag
                counter.next = False  # Rst_n the counter

    """ detect the enable signal """

    @always(Clk.posedge, Rst_n.posedge)
    def input_detect():
        if Rst_n:
            R_edge.next = 0
        else:
            R_edge.next = concat(R_edge[0], TxEn)

    @always_comb
    def cont():
        D_edge.next = not R_edge[1] and R_edge[0]  # this makes sure that the enable signal is read once

    return instances()


if __name__ == '__main__':
    Clk = Signal(bool(0))
    Rst_n = Signal(bool(0))
    TxEn = Signal(bool(0))
    TxData = Signal(intbv(0)[8:])
    TxDone = Signal(bool(0))
    Tx = Signal(bool(0))
    Tick = Signal(bool(0))
    NBits = Signal(intbv(0)[4:])

    tb = TX(Clk, Rst_n, TxEn, TxData, TxDone, Tx, Tick, NBits)
    toVerilog.initial_values = True
    tb.convert(hdl='verilog')
