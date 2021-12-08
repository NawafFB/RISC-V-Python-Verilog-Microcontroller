from myhdl import *

"""
@input: STB : STB[3] signal enables the UART module
@input: we : signal to enable the Tx module
@input: data : data coming from the CPU
@input: TxDone : Tx completion signal
@input: RxDone : Rx completion signal
@input: RxData : data coming from the UART to the CPU
@output: TxData : data[8:] = data sent to the UART Tx module by the controller
@output: baud_rate : data[32:16] = data sent to the UART Tx module by the controller
@output: TxEn : enable signal to the Tx module
@output: RxEn : enable signal to the Rx module
@output: TxFlag
@output: RxFlag
@output: UART_DAT_OUT
"""


@block
def UART_controller(clk, STB, we, data, TxData, RxDone, TxDone, baud_rate, TxEn, RxEn, TxFlag, RxFlag, UART_DAT_OUT, RxData, BRG_En):

    @always(clk.posedge)
    def connection():

        TxFlag.next = TxDone
        RxFlag.next = RxDone
        RxEn.next = True
        UART_DAT_OUT.next = RxData

        if STB[3] == 1:  # UART module enabled
            baud_rate.next = data[32:16]
            TxData.next = data[8:]
            if we:  # write is enabled
                TxEn.next = True
                BRG_En.next = True
            else:
                BRG_En.next = False
        else:
            TxEn.next = False

    return instances()


if __name__ == '__main__':

    RxData = Signal(intbv(0)[8:])  # data received
    TxData = Signal(intbv(0)[8:])  # data to send
    RxDone = Signal(bool(1))
    TxDone = Signal(bool(1))
    we = Signal(bool(1))
    baud_rate = Signal(modbv(0)[16:])
    data = Signal(modbv(0)[32:])
    UART_DAT_OUT = Signal(modbv(0)[32:])
    STB = Signal(modbv(0)[4:])
    TxEn = Signal(bool(1))
    RxEn = Signal(bool(1))
    TxFlag = Signal(bool(1))
    RxFlag = Signal(bool(1))

    tb = UART_controller(STB, we, data, TxData, RxDone, TxDone, baud_rate, TxEn, RxEn, TxFlag, RxFlag, UART_DAT_OUT, RxData)
    toVerilog.initial_values = True
    tb.convert(hdl='verilog')
