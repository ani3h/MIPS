from Conversion import DecimalToBinaryNum, BinaryToDecimal
from ControlUnit import ControlUnit

Clock = 0
Memory = {}

startAdd = 0x00400000
i = startAdd
with open('fibo_bin.txt', 'r') as machineCode:
    for l in machineCode:
        Memory[i] = str(l[0:8])
        Memory[i+1] = str(l[8:16])
        Memory[i+2] = str(l[16:24])
        Memory[i+3] = str(l[24:32])
        i += 4

endAdd = i


OPcodes = {
    "lw": DecimalToBinaryNum(35, 6), "la": DecimalToBinaryNum(35, 6), "sub": DecimalToBinaryNum(0, 6), "divu": DecimalToBinaryNum(0, 6),
    "mflo": DecimalToBinaryNum(0, 6), "subi": DecimalToBinaryNum(8, 6), "add": DecimalToBinaryNum(0, 6), "slt": DecimalToBinaryNum(0, 6),
    "sra": DecimalToBinaryNum(0, 6), "mul": DecimalToBinaryNum(0, 6), "j": DecimalToBinaryNum(2, 6), "lui": DecimalToBinaryNum(15, 6),
    "addi": DecimalToBinaryNum(8, 6), "sw": DecimalToBinaryNum(43, 6), "beq": DecimalToBinaryNum(4, 6), "div": DecimalToBinaryNum(0, 6),
    "bne": DecimalToBinaryNum(5, 6)}

DataMem = {}

data_startAdd = 268500992
j = data_startAdd
with open('fibo_data.txt', 'r') as dataCode:
    for l in dataCode:
        DataMem[j] = str(l[0:8])
        DataMem[j + 1] = str(l[8:16])
        DataMem[j + 2] = str(l[16:24])
        DataMem[j + 3] = str(l[24:32])
        j += 4


RegMem = [0 for _ in range(32)]


class Processor:
    def __init__(self, PC, Memory, DataMem, RegMem):
        self.PC = PC
        self.Mem = Memory
        self.dataMem = DataMem
        self.regMem = RegMem

    def IF(self, Instruction):
        global Clock
        Clock += 1
        return Instruction[0:6]

    def ID(self, opcode, control, Instruction):
        global Clock
        Clock += 1

        if (opcode == "000000"):
            rs = BinaryToDecimal(Instruction[6:11])
            rt = BinaryToDecimal(Instruction[11:16])
            rd = BinaryToDecimal(Instruction[16:21])

            funct = control.ALUControl()
            control.ControlUnitAssign(0, 0, 0, 0, funct, 0, 1, 1, 0)

            return [rs, rt, rd]

        elif (opcode == "000010"):
            control.ControlUnitAssign(1, 0, 0, 0, "0", 0, 0, 0, 1)
            return [Instruction[6:32]]

        else:
            rs = BinaryToDecimal(Instruction[6:11])
            rt = BinaryToDecimal(Instruction[11:16])
            imm = BinaryToDecimal(Instruction[16:32])

            MemToReg = 0
            MemWrite = 0
            MemRead = 0
            Branch = 0
            AluCount = "010"
            AluSRC = 1
            RegDest = 1
            RegWire = 1

            if (opcode == OPcodes["lw"]):
                MemToReg = 1
                MemWrite = 0
                MemRead = 1
                Branch = 0
                AluCount = "010"
                AluSRC = 1
                RegDest = 0
                RegWire = 1

            if (opcode == OPcodes["lui"]):
                MemToReg = 0
                MemWrite = 0
                MemRead = 0
                Branch = 0
                AluCount = "100"
                AluSRC = 1
                RegDest = 0
                RegWire = 1

            elif (opcode == OPcodes["sw"]):
                MemToReg = 0
                MemWrite = 1
                MemRead = 0
                Branch = 0
                AluCount = "010"
                AluSRC = 1
                RegDest = 1
                RegWire = 0

            elif (opcode == OPcodes["addi"]):
                MemToReg = 0
                MemWrite = 0
                MemRead = 0
                Branch = 0
                AluCount = "010"
                AluSRC = 1
                RegDest = 1
                RegWire = 1

            elif (opcode == OPcodes["beq"]):
                MemToReg = 0
                MemWrite = 0
                MemRead = 0
                Branch = 1
                AluCount = "011"
                AluSRC = 0
                RegDest = 1
                RegWire = 0

            elif (opcode == OPcodes["bne"]):
                MemToReg = 0
                MemWrite = 0
                Branch = 1
                AluCount = "011"
                AluSRC = 0
                RegDest = 1
                RegWire = 0

            control.ControlUnitAssign(
                MemToReg, MemWrite, MemRead, Branch, AluCount, AluSRC, RegDest, RegWire, 0)
            return [rs, rt, imm]

    def EX(self, sorceA, sorceB, controller, imm):
        global Clock
        Clock += 1

        AluControl = controller.ControlSignals["aluControl"]
        branch = controller.ControlSignals["branch"]
        src = controller.ControlSignals["aluSrc"]

        if (branch):
            if (AluControl == "111" or AluControl == "110"):
                if (sorceA > sorceB):
                    return imm + 1
                else:
                    return 1
            if (AluControl == "011"):
                return sorceA - sorceB

        if (not src):
            if (AluControl == "010"):
                return sorceA + sorceB

            elif (AluControl == "011"):
                if (controller.op == OPcodes["bne"]):
                    if (sorceA - sorceB == 0):
                        return 1
                    else:
                        return 0
                return sorceA - sorceB

            elif (AluControl == "001"):
                return sorceA | sorceB

            elif (AluControl == "111"):
                return sorceA > sorceB

            elif (AluControl == "0001"):
                return sorceA % sorceB

            elif (AluControl == "110"):
                return sorceA <= 0

            elif (AluControl == "101"):
                return sorceA * sorceB

            elif (AluControl == "100"):
                if (sorceA < sorceB):
                    return 1
                else:
                    return 0

        elif (src):
            if (AluControl == "010"):
                return sorceA + imm

            elif (AluControl == "011"):
                return sorceA - imm

            elif (AluControl == "001"):
                return sorceA | imm

            elif (AluControl == "111"):
                return sorceA > imm

            elif (AluControl == "101"):
                return sorceA * sorceB

            elif (AluControl == "100"):
                return imm * pow(2, 16)

    def memory(self, controller, AluRes, reg):
        global Clock
        Clock += 1

        MemWrite = controller.ControlSignals["MemWrite"]
        MemRead = controller.ControlSignals["MemRead"]
        if (MemRead):
            print("Reading from Data Memory")
            read = ""
            read += DataMem[AluRes] + DataMem[AluRes +
                                              1] + DataMem[AluRes + 2] + DataMem[AluRes + 3]
            return read

        if (MemWrite):
            print("Writing to Data Memory")
            x = DecimalToBinaryNum(self.regMem[reg], 32)
            DataMem[AluRes] = x[0:8]
            DataMem[AluRes + 1] = x[8:16]
            DataMem[AluRes + 2] = x[16:24]
            DataMem[AluRes + 3] = x[24:32]

        return 0

    def writeBack(self, controller, dataAlures, memdata, reg):
        global Clock
        Clock += 1

        MemToReg = controller.ControlSignals["MemtoReg"]
        jmp = controller.ControlSignals["jump"]
        branch = controller.ControlSignals["branch"]

        if (jmp or branch):
            return
        if (MemToReg):
            self.regMem[reg] = BinaryToDecimal(memdata)
        else:
            self.regMem[reg] = dataAlures


PC = startAdd
while (PC in Memory.keys()):
    processor = Processor(PC, Memory, DataMem, RegMem)

    instruction = ""
    instruction += Memory[PC]
    instruction += Memory[PC+1]
    instruction += Memory[PC+2]
    instruction += Memory[PC+3]
    op_code = processor.IF(instruction)

    if (op_code == OPcodes["j"]):
        jump = "0000" + instruction[7:] + "00"
        PC = BinaryToDecimal(jump)
    else:
        controller = ControlUnit(instruction)
        dat = processor.ID(op_code, controller, instruction)

        alu_res = processor.EX(
            RegMem[dat[0]], RegMem[dat[1]], controller, dat[2])

        if (alu_res == 0 and instruction[0:6] == "000100"):
            PC += 4 * dat[2]
            print("Branching, New PC:", PC)
        elif (alu_res != 0 and instruction[0:6] == "000101"):
            PC += 4 * dat[2]
            print("Branching, New PC:", PC)
        else:
            if (op_code == "000000"):
                memRes = processor.memory(controller, alu_res, dat[2])
            else:
                memRes = processor.memory(controller, alu_res, dat[1])
            print("RegMem:", RegMem)
            print("PC:", PC)
            print()
            if (op_code == "000000"):
                processor.writeBack(controller, alu_res, memRes, dat[2])
            else:
                processor.writeBack(controller, alu_res, memRes, dat[1])

        PC += 4


print("-------------------------------------------------------------------------------------------------------------------------")
print("Clock Cycles: ", Clock)
print()

print("Result is stored in DataMem(location: 268501007), Answer =",
      BinaryToDecimal(DataMem[268501007]))
print()
