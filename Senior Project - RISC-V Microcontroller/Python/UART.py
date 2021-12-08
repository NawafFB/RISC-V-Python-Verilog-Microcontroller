from myhdl import *
from RX import RX
from TX import TX
from BaudRateGen import BRG

"""
@input: clk
@input: reset
@input: Rx : parallel input data to the UART from the PIN to be received
@input: TxData : parallel input data to the UART from the CPU to transmit
@input: TxEn
@input: RxEn
@output: RxData
@output: Tx
"""


@block
def UART(clk, reset, Rx, RxData, Tx, TxData, RxDone, TxDone, baud_rate, TxEn, RxEn, BRG_En):
    tick = Signal(bool(0))
    Nbits = Signal(intbv(8)[4:])  # size of data to be received/sent

    """ UART modules """

    RX_driver = RX(clk, reset, RxEn, RxData, RxDone, Rx, tick, Nbits)
    TX_driver = TX(clk, reset, TxEn, TxData, TxDone, Tx, tick, Nbits)
    BRG_driver = BRG(clk, reset, tick, baud_rate, BRG_En)

    return instances()


@block
def test():
    clk = Signal(bool(0))
    reset = Signal(bool(0))
    Rx = Signal(bool(1))  # data coming to the UART
    RxData = Signal(intbv(0)[8:])  # data received
    Tx = Signal(bool(1))  # data sent
    TxData = Signal(intbv(0)[8:])  # data to send

    @always(delay(1))
    def clk_driver():
        clk.next = not clk

    uart_driver = UART(clk, reset, Rx, RxData, Tx, TxData)

    @instance
    def run():
        print('start')
        TxData.next = 0b01100110  # start bit
        yield clk.negedge
        Rx.next = 0  # start bit
        yield delay(64)
        Rx.next = 0
        yield delay(64)
        Rx.next = 1
        yield delay(64)
        Rx.next = 1
        yield delay(64)
        Rx.next = 0
        yield delay(64)
        Rx.next = 0
        yield delay(64)
        Rx.next = 1
        yield delay(64)
        Rx.next = 1
        yield delay(64)
        Rx.next = 0
        yield delay(64)
        Rx.next = 1  # stop bit
        yield delay(64)

    return instances()


# tb = test()
# tb.run_sim(10000)

if __name__ == '__main__':
    clk = Signal(bool(0))
    reset = Signal(bool(0))
    Rx = Signal(bool(1))  # data coming to the UART
    RxData = Signal(intbv(0)[8:])  # data received
    Tx = Signal(bool(1))  # data sent
    TxData = Signal(intbv(0)[8:])  # data to send
    RxDone = Signal(bool(1))
    TxDone = Signal(bool(1))
    baud_rate = Signal(modbv(0)[16:])
    TxEn = Signal(bool(1))
    RxEn = Signal(bool(1))

    tb = UART(clk, reset, Rx, RxData, Tx, TxData, RxDone, TxDone, baud_rate, TxEn, RxEn)
    toVerilog.initial_values = True
    tb.convert(hdl='verilog')