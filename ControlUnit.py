class ControlUnit:

    def __init__(self, Instruction):
        self.Instruction = Instruction
        self.op = self.Instruction[0:6]
        self.ControlSignals = {
            "MemtoReg": 0,
            "MemWrite": 0,
            "branch": 0,
            "aluControl": 0,
            "aluSrc": 0,
            "regDest": 0,
            "regWrite": 0,
            "jump": 0
        }

    def ControlUnitAssign(self, MemtoReg, MemWrite, MemRead, branch, AluCont, aluSrc, Regdst, regWr, jmp):
        self.ControlSignals["MemtoReg"] = MemtoReg
        self.ControlSignals["MemWrite"] = MemWrite
        self.ControlSignals["MemRead"] = MemRead
        self.ControlSignals["branch"] = branch
        self.ControlSignals["aluControl"] = AluCont
        self.ControlSignals["aluSrc"] = aluSrc
        self.ControlSignals["regDest"] = Regdst
        self.ControlSignals["regWrite"] = regWr
        self.ControlSignals["jump"] = jmp

    def ALUControl(self):
        if self.op == "000000":
            funct = self.Instruction[26:32]
            if funct == "100000":
                return "010"
            elif funct == "100010":
                return "011"
            elif funct == "100100":
                return "000"
            elif funct == "100101":
                return "001"
            elif funct == "101010":
                return "100"
            elif funct == "100001":
                return "010"
            elif funct == "000010":
                return "101"
        return "000"
