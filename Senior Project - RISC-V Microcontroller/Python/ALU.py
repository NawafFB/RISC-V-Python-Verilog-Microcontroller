from myhdl import block, Signal, intbv, delay, always_comb, instance, instances, bin, modbv, always, concat

'''
Arithmetic Logic Unit 

@input : PC - Program counter
@input : operand1 - first operand
@input : operand2 - second operand
@input : ALUop - operation
@output : out - result from the arithmetic operation
@output : zero- result from comparison 
'''

@block
def ALU(PC, operand1, operand2, ALUop, out, zero):
    temp = Signal(intbv(0)[64:])

    @always(PC, operand1, operand2, ALUop)
    def multiplication():
        # MUL
        if ALUop == 0b011100:
            temp.next = operand1 * operand2
        # MULH
        elif ALUop == 0b011101:
            temp.next = (operand1 * operand2)
        # MULHSU
        elif ALUop == 0b011110:
            temp.next = (operand1 * operand2[32:])
        # MULHU
        elif ALUop == 0b011111:
            temp.next = (operand1[32:]) * (operand2[32:])
        else:
            temp.next = 0

    @always_comb
    def alu_calculation():
        # LB
        if ALUop == 0b000000:
            out.next = operand1 + operand2
            zero.next = 0b0
        # LH
        elif ALUop == 0b000001:
            out.next = operand1 + operand2
            zero.next = 0b0
        # LW
        elif ALUop == 0b000010:
            out.next = operand1 + operand2
            zero.next = 0b0
        # LBU
        elif ALUop == 0b000011:
            # out.next = operand1[32:] + operand2
            out.next = operand1 + operand2
            zero.next = 0b0
        # LHU
        elif ALUop == 0b000100:
            out.next = operand1 + operand2
            zero.next = 0b0
        # SLLI
        elif ALUop == 0b000101:
            out.next = operand1 << operand2
        # SRLI
        elif ALUop == 0b000110:
            out.next = operand1 >> operand2
            zero.next = 0b0
        # SRAI
        elif ALUop == 0b000111:
            out.next = operand1 >> operand2
            zero.next = 0b0
        # ADDI
        elif ALUop == 0b001000:
            out.next = operand1 + operand2
            zero.next = 0b0
        # XORI
        elif ALUop == 0b001001:
            out.next = operand1 ^ operand2
            zero.next = 0b0
        # ORI
        elif ALUop == 0b001010:
            out.next = operand1 | operand2
            zero.next = 0b0
        # ANDI
        elif ALUop == 0b001011:
            out.next = operand1 & operand2
            zero.next = 0b0
        # SLTI
        elif ALUop == 0b001100:
            if operand1 < operand2:
                out.next = 1
                zero.next = 0b0
            else:
                out.next = 0
                zero.next = 0b0
        # SLTIU
        elif ALUop == 0b001101:
            if concat(False, operand1[31:]) < concat(False, operand2[31:]):
                out.next = 1
                zero.next = 0b0
            else:
                out.next = 0
                zero.next = 0b0
        # JALR
        elif ALUop == 0b001110:
            out.next = operand1 + operand2
            zero.next = 0b1
        # JAL
        elif ALUop == 0b100110:
            out.next = PC + operand2
            zero.next = 0b1
        # SB
        elif ALUop == 0b001111:
            out.next = operand1 + operand2
            zero.next = 0b0
        # SH
        elif ALUop == 0b010000:
            out.next = operand1 + operand2
            zero.next = 0b0
        # SW
        elif ALUop == 0b010001:
            out.next = operand1 + operand2
            zero.next = 0b0
        # SLL
        elif ALUop == 0b010010:
            out.next = operand1 << operand2[32:]
            zero.next = 0b0
        # SRL
        elif ALUop == 0b010011:
            out.next = operand1 >> operand2[32:]
            zero.next = 0b0
        # SRA
        elif ALUop == 0b010100:
            out.next = modbv((operand1 >> operand2[32:]) | (operand1 << (32 - operand2[32:])), min=(-2 ** 32),
                             max=(2 ** 32 - 1))
            zero.next = 0b0
        # ADD
        elif ALUop == 0b010101:
            out.next = operand1 + operand2
            zero.next = 0b0
        # SUB
        elif ALUop == 0b010110:
            out.next = operand1 - operand2
            zero.next = 0b0
        # XOR
        elif ALUop == 0b010111:
            out.next = operand1 ^ operand2
            zero.next = 0b0
        # OR
        elif ALUop == 0b011000:
            out.next = operand1 | operand2
            zero.next = 0b0
        # AND
        elif ALUop == 0b011001:
            out.next = operand1 & operand2
            zero.next = 0b0
        # SLT
        elif ALUop == 0b011010:
            if operand1 < operand2:
                out.next = 1
                zero.next = 0b0
            else:
                out.next = 0
                zero.next = 0b0
        # SLTU
        elif ALUop == 0b011011:
            if concat(False, operand1[31:]) < concat(False, operand2[31:]):
                out.next = 1
                zero.next = 0b0
            else:
                out.next = 0
                zero.next = 0b0
        # MUL
        elif ALUop == 0b011100:
            out.next = temp[32:]
            zero.next = 0b0
        # MULH
        elif ALUop == 0b011101:
            out.next = temp[64:32]
            zero.next = 0b0
        # MULHSU
        elif ALUop == 0b011110:
            out.next = temp[64:32]
            zero.next = 0b0
        # MULHU
        elif ALUop == 0b011111:
            out.next = temp[64:32]
            zero.next = 0b0
        # DIV
        elif ALUop == 0b100000:
            out.next = operand1 // operand2
            zero.next = 0b0
        # DIVU
        elif ALUop == 0b100001:
            out.next = operand1[32:] // operand2[32:]
            zero.next = 0b0
        # REM
        elif ALUop == 0b100010:
            out.next = operand1 % operand2
            zero.next = 0b0
        # REMU
        elif ALUop == 0b100011:
            out.next = operand1[32:] % operand2[32:]
            zero.next = 0b0
        # LUI
        elif ALUop == 0b100100:
            out.next = (operand2 << 12)
            zero.next = 0b0
        # AUIPC
        elif ALUop == 0b100101:
            out.next = PC + (operand2 << 12)
            zero.next = 0b0
        # BEQ
        elif ALUop == 0b100111:
            if operand1 == operand2:
                zero.next = 0b1
                out.next = 0
            else:
                zero.next = 0b0
                out.next = 0
        # BNE
        elif ALUop == 0b101000:
            if operand1 != operand2:
                zero.next = 0b1
                out.next = 0
            else:
                zero.next = 0b0
                out.next = 0
        # BLT
        elif ALUop == 0b101001:
            if operand1 < operand2:
                zero.next = 0b1
                out.next = 0
            else:
                zero.next = 0b0
                out.next = 0
        # BGE
        elif ALUop == 0b101010:
            if operand1 >= operand2:
                zero.next = 0b1
                out.next = 0
            else:
                zero.next = 0b0
                out.next = 0
        # BLTU
        elif ALUop == 0b101011:
            if operand1[32:] < operand2[32:]:
                zero.next = 0b1
                out.next = 0
            else:
                zero.next = 0b0
                out.next = 0
        # BGEU
        elif ALUop >= 0b101100:
            if operand1[32:] == operand2[32:]:
                zero.next = 0b1
                out.next = 0
            else:
                zero.next = 0b0
                out.next = 0

    return instances()


'''
ALU test bench
the next block will test the previous 
block by changing the operation code
coming from the ALUop unit and also
changing the operands and then printing
the results

'''


@block
def alu_test():
    pc = Signal(intbv(0, min=0, max=2 * 21))
    operand1 = Signal(intbv(0))
    operand2 = Signal(intbv(0, min=(-2 ** 31), max=2 ** 31))
    ALUop, zero = [Signal(intbv(0)) for i in range(2)]
    out = Signal(modbv(0, min=(-2 ** 31), max=2 ** 31))

    alu_1 = ALU(pc, operand1, operand2, ALUop, out, zero)

    @instance
    def stimulus():
        # random
        # operand1.next = 1
        # print('1> ', bin(operand1, 32), bin(operand2, 32), bin(out, 32))
        # yield delay(10)
        # print('2> ', bin(operand1, 32), bin(operand2, 32), bin(out, 32))
        # operand1.next = -1
        # yield delay(10)
        # print('3> ', bin(operand1, 32), bin(operand2, 32), bin(out, 32))

        # ADD
        operand1.next = 1
        operand2.next = 2
        ALUop.next = 0b010101
        print('before> ', bin(operand1, 32), bin(operand2, 32), bin(out, 32))
        yield delay(10)
        print('after> ', bin(operand1, 32), bin(operand2, 32), bin(out, 32))
        print()

        # ADDI instruction
        operand1.next = 0
        operand2.next = 5
        ALUop.next = 0b001000
        print('before> ', bin(operand1, 32), bin(operand2, 32), bin(out, 32))
        yield delay(10)
        print('after> ', bin(operand1, 32), bin(operand2, 32), bin(out, 32))
        print()

        # SRA instruction
        operand1.next = 15
        operand2.next = 2
        ALUop.next = 0b010100
        print('before> ', bin(operand1, 32), bin(operand2, 32), bin(out, 32))
        yield delay(10)
        print('after> ', bin(operand1, 32), bin(operand2, 32), bin(out, 32))
        print()

        # MUL instruction
        operand1.next = 50
        operand2.next = 40
        ALUop.next = 0b011100
        print('before> ', bin(operand1, 32), bin(operand2, 32), bin(out, 32))
        yield delay(10)
        print('after> ', bin(operand1, 32), bin(operand2, 32), bin(out, 32))
        print()

        # SUB instruction
        operand1.next = 20
        operand2.next = 30
        ALUop.next = 0b010110  # sub instruction
        print('before> ', bin(operand1, 32), bin(operand2, 32), bin(out, 32))
        yield delay(10)
        print('after> ', bin(operand1, 32), bin(operand2, 32), bin(out, 32))

    return instances()


if __name__ == '__main__':
    pc = Signal(intbv(0, min=0, max=2 ** 32))
    zero = Signal(bool(0))
    operand11 = Signal(intbv(0, min=(-2 ** 31), max=2 ** 31))
    operand21 = Signal(intbv(0, min=(-2 ** 31), max=2 ** 31))
    ALUop = Signal(intbv(0, min=0, max=2 ** 6))
    out1 = Signal(modbv(0, min=(-2 ** 31), max=2 ** 31))

    alu_1 = ALU(pc, operand11, operand21, ALUop, out1, zero)
    alu_1.run_sim()
    alu_1.convert(hdl='verilog')

# tb = alu_test()
# tb.run_sim(1000)
