from myhdl import block, always, instance, instances, always_comb, Signal, intbv, delay, bin, _always_comb, concat

'''
SBA Control Unit Block

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
@output : WE_O : 0=read 1:write
@output : regWrite
@output : branch
@output : ALUsrc
@output : dataSrc
'''


@block
def SBA_CU(opcode, funct3, funct7, ALUop, WE_O, regWrite, branch, ALUsrc, dataSrc, STB_O):
    @always_comb
    def control_system():
        # R-type instructions
        if opcode == 0b0110011:
            branch.next = 0  # no branches
            WE_O.next = 0  # read from element as default
            regWrite.next = 1  # enable writing in file register
            ALUsrc.next = 0  # second operand comes from rs2
            dataSrc.next = 0  # data comes from the ALU
            STB_O.next = 0  # disable everything as default

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
            WE_O.next = 0  # enable reading
            regWrite.next = 1  # enable writing in file register
            ALUsrc.next = 1  # second operand comes from imm
            dataSrc.next = 1  # data comes from the memory
            STB_O.next = concat(funct3, True)

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
            WE_O.next = 0  # enable reading (doesnt matter actually, we want to turn off both read/write)
            regWrite.next = 1  # enable writing in file register
            ALUsrc.next = 1  # second operand comes from imm
            dataSrc.next = 0  # data comes from the ALU
            STB_O.next = 0  # turn off writing/reading to/from peripherals

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
            WE_O.next = 0  # enable reading (doesnt matter actually, we want to turn off both read/write)
            regWrite.next = 0  # disable writing in file register
            ALUsrc.next = 0  # second operand comes from rs2
            dataSrc.next = 0  # data comes from the ALU
            ALUop.next = 0b001110
            STB_O.next = 0

        # S-type instruction
        elif opcode == 0b0100011:

            branch.next = 0  # no branches
            WE_O.next = 1  # enable writing
            regWrite.next = 0  # disable writing in file register
            ALUsrc.next = 1  # second operand comes from imm
            dataSrc.next = 0  # data comes from the ALU
            STB_O.next = concat(funct3, True)  # enable writing

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
            WE_O.next = 0  # enable reading (doesnt matter actually, we want to turn off both read/write)
            regWrite.next = 0  # disable writing in file register
            ALUsrc.next = 0  # second operand comes from rs2
            dataSrc.next = 0  # data comes from the ALU
            STB_O.next = 0

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

            WE_O.next = 0  # enable reading (doesnt matter actually, we want to turn off both read/write)

            # LUI
            if opcode == 0b0110111:
                branch.next = 0  # no branches
                regWrite.next = 1  # enable writing in file register
                ALUsrc.next = 1  # second operand comes from imm
                dataSrc.next = 1  # data comes from the memory
                ALUop.next = 0b100100
                STB_O.next = concat(funct3, True)

            # AUIPC
            elif opcode == 0b0010111:
                branch.next = 1  # there is a branch
                regWrite.next = 0  # disable writing in file register
                ALUsrc.next = 1  # second operand comes from imm
                dataSrc.next = 0  # data comes from the ALU
                ALUop.next = 0b100101
                STB_O.next = 0

        # J-type instructions
        elif opcode == 0b1101111:

            branch.next = 1  # there is a branch
            WE_O.next = 0  # enable reading (doesnt matter actually, we want to turn off both read/write)
            regWrite.next = 1  # enable writing in file register
            ALUsrc.next = 0  # second operand comes from rs2
            dataSrc.next = 0  # data comes from the ALU
            ALUop.next = 0b100110
            STB_O.next = 0

        # bubble instruction
        elif opcode == 0b0000000:
            branch.next = 0  # no branches
            WE_O.next = 0  # enable reading (doesnt matter actually, we want to turn off both read/write)
            regWrite.next = 0  # disable writing in file register
            ALUsrc.next = 0  # second operand comes from rs2
            dataSrc.next = 0  # data comes from the ALU
            STB_O.next = 0

    return instances()


@block
def test():
    opcode, funct3, funct7, ALUop, WE_O, regWrite, branch, ALUsrc, dataSrc = [Signal(intbv(0)) for i in
                                                                              range(9)]
    STB_O = Signal(intbv(0)[4:])

    drive = SBA_CU(opcode, funct3, funct7, ALUop, WE_O, regWrite, branch, ALUsrc, dataSrc, STB_O)

    @instance
    def run():
        # R-TYPE
        opcode.next = 0b0110011
        funct3.next = 0b0
        funct7.next = 0b0
        yield delay(5)
        print('\nopcode: %s | funct3: %s | funct7: %s | ALUop: %s |\nregWrite: %d '
              '| branch: %d | ALUsrc: %d | dataSrc: %d |\nWE_O: %s | STB_O: %s' % (
                  bin(opcode, 7), bin(funct3, 3), bin(funct7, 7), bin(ALUop, 6),
                  regWrite, branch, ALUsrc, dataSrc, bin(WE_O, 1), bin(STB_O, 4)))
        # I-TYPE (LOAD)
        opcode.next = 0b0000011
        funct3.next = 0b010
        funct7.next = 0b0
        yield delay(5)
        print('\nopcode: %s | funct3: %s | funct7: %s | ALUop: %s |\nregWrite: %d '
              '| branch: %d | ALUsrc: %d | dataSrc: %d |\nWE_O: %s | STB_O: %s' % (
                  bin(opcode, 7), bin(funct3, 3), bin(funct7, 7), bin(ALUop, 6),
                  regWrite, branch, ALUsrc, dataSrc, bin(WE_O, 1), bin(STB_O, 4)))

        opcode.next = 0b0100011  # store
        funct3.next = 0b010  # store word
        funct7.next = 0
        yield delay(5)
        print('\nopcode: %s | funct3: %s | funct7: %s | ALUop: %s |\nregWrite: %d '
              '| branch: %d | ALUsrc: %d | dataSrc: %d |\nWE_O: %s | STB_O: %s' % (
                  bin(opcode, 7), bin(funct3, 3), bin(funct7, 7), bin(ALUop, 6),
                  regWrite, branch, ALUsrc, dataSrc, bin(WE_O, 1), bin(STB_O, 4)))

        opcode.next = 0b0110111  # LUI
        funct3.next = 0b001  # store word
        funct7.next = 0
        yield delay(5)
        print('\nopcode: %s | funct3: %s | funct7: %s | ALUop: %s |\nregWrite: %d '
              '| branch: %d | ALUsrc: %d | dataSrc: %d |\nWE_O: %s | STB_O: %s' % (
                  bin(opcode, 7), bin(funct3, 3), bin(funct7, 7), bin(ALUop, 6),
                  regWrite, branch, ALUsrc, dataSrc, bin(WE_O, 1), bin(STB_O, 4)))

        opcode.next = 0b0010111  # AUIPC
        funct3.next = 0b010  # store word
        funct7.next = 0
        yield delay(5)
        print('\nopcode: %s | funct3: %s | funct7: %s | ALUop: %s |\nregWrite: %d '
              '| branch: %d | ALUsrc: %d | dataSrc: %d |\nWE_O: %s | STB_O: %s' % (
                  bin(opcode, 7), bin(funct3, 3), bin(funct7, 7), bin(ALUop, 6),
                  regWrite, branch, ALUsrc, dataSrc, bin(WE_O, 1), bin(STB_O, 4)))

    return instances()


# tb = test()
# tb.run_sim(50)

if __name__ == '__main__':

    opcode = Signal(intbv(0, min=0, max=2 ** 7))
    funct3 = Signal(intbv(0, min=0, max=2 ** 3))
    funct7 = Signal(intbv(0, min=0, max=2 ** 7))
    ALUop = Signal(intbv(0, min=0, max=2 ** 6))
    WE_O = Signal(bool(0))
    regWrite = Signal(bool(0))
    branch = Signal(bool(0))
    ALUsrc = Signal(bool(0))
    dataSrc = Signal(bool(0))
    STB_O = Signal(intbv(0)[4:])

    tb = SBA_CU(opcode, funct3, funct7, ALUop, WE_O, regWrite, branch, ALUsrc, dataSrc, STB_O)
    tb.run_sim()
    tb.convert(hdl='verilog')
