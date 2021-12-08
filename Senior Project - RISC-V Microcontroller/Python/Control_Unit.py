from myhdl import block, always, instance, instances, always_comb, Signal, intbv, delay, bin, _always_comb

'''control unit block
this module will be in control of the 
whole system, it receives an opcode, funct3
and funct7 to distribute signals for the cpu
components.
 
@input : reset
@input : clk
@input : opcode
@input : funct3
@input : funct7
@output : ALUop
@output : memRead
@output : memWrite
@output : regWrite
@output : branch
@output : ALUsrc
@output : dataSrc
'''


@block
def control(opcode, funct3, funct7, ALUop, memRead, memWrite, regWrite, branch, ALUsrc, dataSrc):
    @always_comb
    def control_system():
        # R-type instructions
        if opcode == 0b0110011:
            branch.next = 0  # no branches
            memRead.next = 0  # disable reading from memory
            memWrite.next = 0  # disable writing in memory
            regWrite.next = 1  # enable writing in file register
            ALUsrc.next = 0  # second operand comes from rs2
            dataSrc.next = 0  # data comes from the ALU

            # ADD
            if (funct3 == 0b000) and (funct7 == 0b0000000):
                ALUop.next = 0b010101
            # SUB
            elif (funct3 == 0b000) and (funct7 == 0b0100000):
                ALUop.next = 0b010110
            # SLL
            elif (funct3 == 0b001) and (funct7 == 0b0000000):
                ALUop.next = 0b010010
            # SLT
            elif (funct3 == 0b010) and (funct7 == 0b0000000):
                ALUop.next = 0b011010
            # SLTU
            elif (funct3 == 0b011) and (funct7 == 0b0000000):
                ALUop.next = 0b011011
            # XOR
            elif (funct3 == 0b100) and (funct7 == 0b0000000):
                ALUop.next = 0b010111
            # SRL
            elif (funct3 == 0b101) and (funct7 == 0b0000000):
                ALUop.next = 0b010011
            # SRA
            elif (funct3 == 0b101) and (funct7 == 0b0100000):
                ALUop.next = 0b010100
            # OR
            elif (funct3 == 0b110) and (funct7 == 0b0000000):
                ALUop.next = 0b011000
            # AND
            elif (funct3 == 0b111) and (funct7 == 0b0000000):
                ALUop.next = 0b011001
            # MUL
            elif (funct3 == 0b000) and (funct7 == 0b0000001):
                ALUop.next = 0b011100
            # MULH
            elif (funct3 == 0b001) and (funct7 == 0b0000001):
                ALUop.next = 0b011101
            # MULHSU
            elif (funct3 == 0b010) and (funct7 == 0b0000001):
                ALUop.next = 0b011110
            # MULSU
            elif (funct3 == 0b011) and (funct7 == 0b0000001):
                ALUop.next = 0b011111
            # DIV
            elif (funct3 == 0b100) and (funct7 == 0b0000001):
                ALUop.next = 0b100000
            # DIVU
            elif (funct3 == 0b101) and (funct7 == 0b0000001):
                ALUop.next = 0b100001
            # REM
            elif (funct3 == 0b110) and (funct7 == 0b0000001):
                ALUop.next = 0b100010
            # REMU
            elif (funct3 == 0b111) and (funct7 == 0b0000001):
                ALUop.next = 0b100011

        # I-type load instructions
        elif opcode == 0b0000011:

            branch.next = 0  # no branches
            memRead.next = 1  # enable reading from memory
            memWrite.next = 0  # disable writing in memory
            regWrite.next = 1  # enable writing in file register
            ALUsrc.next = 1  # second operand comes from imm
            dataSrc.next = 1  # data comes from the memory

            # LB
            if funct3 == 0b000:
                ALUop.next = 0b000000
            # LH
            elif funct3 == 0b001:
                ALUop.next = 0b000001
            # LW
            elif funct3 == 0b010:
                ALUop.next = 0b000010
            # LBU
            elif funct3 == 0b100:
                ALUop.next = 0b000011
            # LHU
            elif funct3 == 0b101:
                ALUop.next = 0b000100

        # I-type arithmetic instructions
        elif opcode == 0b0010011:

            branch.next = 0  # no branches
            memRead.next = 0  # disable reading from memory
            memWrite.next = 0  # disable writing in memory
            regWrite.next = 1  # enable writing in file register
            ALUsrc.next = 1  # second operand comes from imm
            dataSrc.next = 0  # data comes from the ALU

            # ADDI
            if funct3 == 0b000:
                ALUop.next = 0b001000
            # SLLI
            elif funct3 == 0b001:
                ALUop.next = 0b000101
            # SLTI
            elif funct3 == 0b010:
                ALUop.next = 0b001100
            # SLTIU
            elif funct3 == 0b011:
                ALUop.next = 0b001101
            # XORI
            elif funct3 == 0b100:
                ALUop.next = 0b001001
            elif funct3 == 0b101:
                # SRLI
                if funct7 == 0b0000000:
                    ALUop.next = 0b000110
                # SRAI
                elif funct7 == 0b0100000:
                    ALUop.next = 0b000111
            # ORI
            elif funct3 == 0b110:
                ALUop.next = 0b001010
            # ANDI
            elif funct3 == 0b111:
                ALUop.next = 0b001011

        # I-type jump instruction
        elif opcode == 0b1100111:

            branch.next = 1  # there is a branch
            memRead.next = 0  # disable reading from memory
            memWrite.next = 0  # disable writing in memory
            regWrite.next = 0  # disable writing in file register
            ALUsrc.next = 0  # second operand comes from rs2
            dataSrc.next = 0  # data comes from the ALU

            ALUop.next = 0b001110

        # S-type instruction
        elif opcode == 0b0100011:

            branch.next = 0  # no branches
            memRead.next = 0  # disable reading from memory
            memWrite.next = 1  # enable writing in memory
            regWrite.next = 0  # disable writing in file register
            ALUsrc.next = 1  # second operand comes from imm
            dataSrc.next = 0  # data comes from the ALU

            # SB
            if funct3 == 0b000:
                ALUop.next = 0b001111
            # SH
            elif funct3 == 0b001:
                ALUop.next = 0b010000
            # SW
            elif funct3 == 0b010:
                ALUop.next = 0b010001

        # B-type instructions
        elif opcode == 0b1100011:

            branch.next = 1  # there is a branch
            memRead.next = 0  # disable reading from memory
            memWrite.next = 0  # disable writing in memory
            regWrite.next = 0  # disable writing in file register
            ALUsrc.next = 0  # second operand comes from rs2
            dataSrc.next = 0  # data comes from the ALU

            # BEQ
            if funct3 == 0b000:
                ALUop.next = 0b100111
            # BNE
            elif funct3 == 0b001:
                ALUop.next = 0b101000
            # BLT
            elif funct3 == 0b100:
                ALUop.next = 0b101001
            # BGE
            elif funct3 == 0b101:
                ALUop.next = 0b101010
            # BLTU
            elif funct3 == 0b110:
                ALUop.next = 0b101011
            # BGEU
            elif funct3 == 0b111:
                ALUop.next = 0b101100

        # U-type instructions
        elif (opcode == 0b0110111) or (opcode == 0b0010111):

            memWrite.next = 0  # disable writing in memory

            # LUI
            if opcode == 0b0110111:
                branch.next = 0  # no branches
                memRead.next = 1  # enable reading from memory
                regWrite.next = 1  # enable writing in file register
                ALUsrc.next = 1  # second operand comes from imm
                dataSrc.next = 1  # data comes from the memory

                ALUop.next = 0b100100

            # AUIPC
            elif opcode == 0b0010111:
                branch.next = 1  # there is a branch
                memRead.next = 0  # disable reading from memory
                regWrite.next = 0  # disable writing in file register
                ALUsrc.next = 1  # second operand comes from imm
                dataSrc.next = 0  # data comes from the ALU

                ALUop.next = 0b100101

        # J-type instructions
        elif opcode == 0b1101111:

            branch.next = 1  # there is a branch
            memRead.next = 0  # disable reading from memory
            memWrite.next = 0  # disable writing in memory
            regWrite.next = 1  # enable writing in file register
            ALUsrc.next = 0  # second operand comes from rs2
            dataSrc.next = 0  # data comes from the ALU

            ALUop.next = 0b100110

        # bubble instruction
        elif opcode == 0b0000000:
            branch.next = 0  # no branches
            memRead.next = 0  # disable reading from memory
            memWrite.next = 0  # disable writing in memory
            regWrite.next = 0  # disable writing in file register
            ALUsrc.next = 0  # second operand comes from rs2
            dataSrc.next = 0  # data comes from the ALU

    return instances()


@block
def test():
    opcode, funct3, funct7, ALUop, memRead, memWrite, regWrite, branch, ALUsrc, dataSrc = [Signal(intbv(0)) for i in
                                                                                           range(10)]
    reset, clk = [Signal(bool(0)) for i in range(2)]

    drive = control(reset, clk, opcode, funct3, funct7, ALUop, memRead, memWrite, regWrite, branch, ALUsrc, dataSrc)

    @always(delay(5))
    def driver():
        clk.next = not clk

    @instance
    def run():
        # R-TYPE
        opcode.next = 0b0110011
        funct3.next = 0b0
        funct7.next = 0b0
        yield clk.posedge
        print('opcode: %s | funct3: %d | funct7: %d | ALUop: %d | memRead: %d | \nmemWrite: %d | regWrite: %d '
              '| branch: %d | ALUsrc: %d | dataSrc: %d' % (bin(opcode, 7), funct3, funct7, ALUop, memRead, memWrite,
                                                           regWrite, branch, ALUsrc, dataSrc))
        # I-TYPE (LOAD)
        opcode.next = 0b0000011
        funct3.next = 0b0
        funct7.next = 0b0
        yield clk.posedge
        print('\nopcode: %s | funct3: %d | funct7: %d | ALUop: %d | memRead: %d | \nmemWrite: %d | regWrite: %d '
              '| branch: %d | ALUsrc: %d | dataSrc: %d' % (bin(opcode, 7), funct3, funct7, ALUop, memRead, memWrite,
                                                           regWrite, branch, ALUsrc, dataSrc))
        yield clk.posedge
        print('\nopcode: %s | funct3: %d | funct7: %d | ALUop: %d | memRead: %d | \nmemWrite: %d | regWrite: %d '
              '| branch: %d | ALUsrc: %d | dataSrc: %d' % (bin(opcode, 7), funct3, funct7, ALUop, memRead, memWrite,
                                                           regWrite, branch, ALUsrc, dataSrc))

    return instances()


#
# tb = test()
# tb.run_sim(30)
#
if __name__ == '__main__':
    memWrite = Signal(bool(0))
    memRead = Signal(bool(0))
    regWrite = Signal(bool(0))
    ALUsrc = Signal(bool(0))
    branch = Signal(bool(0))
    dataSrc = Signal(bool(0))
    opcode = Signal(intbv(0, min=0, max=2 ** 7))
    funct3 = Signal(intbv(0, min=0, max=2 ** 3))
    funct7 = Signal(intbv(0, min=0, max=2 ** 7))
    ALUop = Signal(intbv(0, min=0, max=2 ** 6))

    tb = control(opcode, funct3, funct7, ALUop, memRead, memWrite, regWrite, branch, ALUsrc, dataSrc)
    tb.run_sim()
    tb.convert(hdl='verilog')
