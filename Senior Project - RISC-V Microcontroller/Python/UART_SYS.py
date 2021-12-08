from myhdl import *
from UART import UART
from UART_controller import UART_controller

"""
@input: clk
@input: reset
@input: we : write enable signal
@input: STB : enables the module
@input: address : selects the output mode. 
@input: data_in : data going to the UART (from data output bus)
@input: Rx : data coming from the port
@output: data_out : data going to the CPU (to data input bus)
@output: Tx : data going to the port
"""


@block
def SBA_UART_SYS(clk, reset, data_in, we, STB, address, data_out, Tx, Rx):
    baud_rate = Signal(intbv(0)[16:])
    TxData = Signal(intbv(0)[8:])
    UART_DAT_OUT = Signal(intbv(0)[8:])
    RxData = Signal(intbv(0)[8:])
    TxEn = Signal(bool(0))
    RxEn = Signal(bool(0))
    TxDone = Signal(bool(0))
    RxDone = Signal(bool(0))
    TxFlag = Signal(bool(0))
    RxFlag = Signal(bool(0))
    BRG_En = Signal(bool(0))

    controller = UART_controller(clk, STB, we, data_in, TxData, RxDone, TxDone, baud_rate, TxEn, RxEn, TxFlag, RxFlag, UART_DAT_OUT,
                    RxData, BRG_En)
    uart = UART(clk, reset, Rx, RxData, Tx, TxData, RxDone, TxDone, baud_rate, TxEn, RxEn, BRG_En)

    @always_comb
    def connection():
        if STB == 0b1000:
            data_out.next = UART_DAT_OUT
        elif STB == 0b1001:
            data_out.next = RxFlag
        elif STB == 0b1010:
            data_out.next = TxFlag

    return instances()


if __name__ == '__main__':
    clk = Signal(bool(0))
    reset = Signal(bool(0))
    we = Signal(bool(0))
    STB = Signal(intbv(0)[4:])
    address = Signal(intbv(0)[32:])
    data_in = Signal(intbv(0)[32:])
    data_out = Signal(intbv(0)[32:])
    Tx = Signal(bool(0))
    Rx = Signal(bool(0))

    tb = SBA_UART_SYS(clk, reset, data_in, we, STB, address, data_out, Tx, Rx)
    toVerilog.initial_values = True
    tb.convert(hdl='verilog')
