from myhdl import *
from mux import *
from ALU import ALU
from File_Register import file_register
from decoder import decoder
from SBA_CU import SBA_CU
from imm_gen import imm_generator
from adder import adder
from BranchAdder import braAdder
from AND import AND
from ROM import ROM
from PC import PC

'''
-the cpu works fine, the only thing that needs to be modified is the initialization of the ROM.
we need to add this code at to the verilog converted file:

initial begin
$readmemh("bank0.mif", ROM0_Memory_block0_MemoryBank0_memory);
$readmemh("bank1.mif", ROM0_Memory_block0_MemoryBank1_memory);
$readmemh("bank2.mif", ROM0_Memory_block0_MemoryBank2_memory);
$readmemh("bank3.mif", ROM0_Memory_block0_MemoryBank3_memory);
end

-Also, we need to delete the "zero initialization" for all banks.

@input: clk
@input: data_in
@output: WE_O
@output: STB_O
@output: addr_out
@output: data_out
'''


@block
def SBA_CPU(clk, data_in, WE_O, STB_O, addr_out, data_out):
    # pc output signals
    current_pc = Signal(intbv(0)[32:])

    # ROM output signals
    instruction = Signal(intbv(0)[32:])

    #   decoder output signals
    opcode = Signal(intbv(0)[7:])
    rdaddress = Signal(intbv(0)[5:])
    rs1address = Signal(intbv(0)[5:])
    rs2address = Signal(intbv(0)[5:])
    imm = Signal(intbv(0)[20:])
    funct3 = Signal(intbv(0)[3:])
    funct7 = Signal(intbv(0)[7:])

    #   alu output signals
    result = Signal(intbv(0)[32:])
    zero = Signal(bool(0))

    #   register file output signals
    rs1out = Signal(intbv(0)[32:])
    rs2out = Signal(intbv(0)[32:])

    # control unit output signals
    ALUop = Signal(intbv(0)[6:])
    regWrite = Signal(bool(0))
    branch = Signal(bool(0))
    ALUsrc = Signal(bool(0))
    dataSrc = Signal(bool(0))

    # imm rs2out mux output signals
    operand2 = Signal(intbv(0)[32:])

    #   pc mux signals
    next_pc = Signal(intbv(0)[32:])

    #   write back mux
    write_back_data = Signal(intbv(0)[32:])

    #   two adders signals
    branch_adder_result = Signal(intbv(0)[32:])
    pc_adder_result = Signal(intbv(0)[32:])

    #   immediate generator output signals
    imm_extended = Signal(intbv(0)[32:])

    #   and gat result
    branch_taken = Signal(bool(0))

    # empty signals
    empty = Signal(bool(0))

    pc_driver = PC(clk, next_pc, current_pc)
    ROM_driver = ROM(empty, empty, current_pc, instruction)
    decoder_driver = decoder(instruction, opcode, rdaddress, rs1address, rs2address, imm, funct3, funct7)
    file_register_driver = file_register(clk, regWrite, write_back_data, rs1address, rs2address, rdaddress, rs1out,
                                         rs2out)
    control_unit = SBA_CU(opcode, funct3, funct7, ALUop, WE_O, regWrite, branch, ALUsrc, dataSrc, STB_O)
    alu = ALU(current_pc, rs1out, operand2, ALUop, result, zero)

    imm_gen = imm_generator(opcode, imm, imm_extended)
    branch_adder = braAdder(current_pc, imm_extended, branch_adder_result)
    pc_adder = adder(current_pc, 4, pc_adder_result)
    and_gate = AND(branch, zero, branch_taken)

    imm_rs2_mux = mux(ALUsrc, rs2out, imm_extended, operand2)
    write_back_mux = mux(dataSrc, result, data_in, write_back_data)
    pc_mux = mux(branch_taken, pc_adder_result, branch_adder_result, next_pc)

    # cpu output signals
    @always_comb
    def connect():
        data_out.next = rs2out
        addr_out.next = result

    return instances()


@block
def tb():
    clk = Signal(bool(0))
    data_in = Signal(intbv(0)[32:])
    instruction = Signal(intbv(0)[32:])
    STB_O = Signal(intbv(0)[4:])
    WE_O = Signal(bool(0))
    addr_out = Signal(intbv(0)[32:])
    data_out = Signal(intbv(0)[32:])

    SBA_CPU_driver = SBA_CPU(clk, data_in, instruction, WE_O, STB_O, addr_out, data_out)

    @always(delay(5))
    def clock_driver():
        clk.next = not clk

    @instance
    def run():
        instruction.next = 0b00011111010000000000000010010011
        print("time: %s\ndata in: %s\ninstruction: %s\nwe: %s\nstb: %s\naddress out: %s\ndata out: %s\n" % (
            now(), data_in, instruction, WE_O, STB_O, addr_out, data_out))
        yield clk.negedge

        instruction.next = 0b00111110100000000000000100010011
        print("time: %s\ndata in: %s\ninstruction: %s\nwe: %s\nstb: %s\naddress out: %s\ndata out: %s\n" % (
            now(), str(data_in), str(instruction), str(WE_O), str(STB_O), str(addr_out), str(data_out)))
        yield clk.negedge

        instruction.next = 0b00000000001000001010000000100011
        print("time: %s\ndata in: %s\ninstruction: %s\nwe: %s\nstb: %s\naddress out: %s\ndata out: %s\n" % (
            now(), str(data_in), str(instruction), str(WE_O), str(STB_O), str(addr_out), str(data_out)))
        yield clk.negedge

        instruction.next = 0b00000000000000001010000110000011
        print("time: %s\ndata in: %s\ninstruction: %s\nwe: %s\nstb: %s\naddress out: %s\ndata out: %s\n" % (
            now(), str(data_in), str(instruction), str(WE_O), str(STB_O), str(addr_out), str(data_out)))
        yield clk.negedge

        instruction.next = 0b0
        print("time: %s\ndata in: %s\ninstruction: %s\nwe: %s\nstb: %s\naddress out: %s\ndata out: %s\n" % (
            now(), str(data_in), str(instruction), str(WE_O), str(STB_O), str(addr_out), str(data_out)))
        yield clk.negedge

    return instances()


# test = tb()
# test.run_sim(50)

if __name__ == '__main__':
    clk = Signal(bool(0))
    data_in = Signal(intbv(0)[32:0])
    WE_O = Signal(bool(0))
    STB_O = Signal(intbv(0)[4:0])
    addr_out = Signal(intbv(0)[32:0])
    data_out = Signal(intbv(0)[32:0])

    cpu = SBA_CPU(clk, data_in, WE_O, STB_O, addr_out, data_out)
    toVerilog.initial_values = True
    toVerilog.timescale = "0"
    cpu.run_sim()
    cpu.convert(hdl='verilog')
