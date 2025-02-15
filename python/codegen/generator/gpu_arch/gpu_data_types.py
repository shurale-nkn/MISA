from enum import Enum
from typing import List

from ..base_components import reg_block, reg_type, regVar
#should be 1 symbol len

class const_val():
    def __init__(self, val) -> None:
        self.label = val
        self.val = val
            
    def __str__(self) -> str:
        return f' {self.val}' 


class const():
    def __init__(self, val) -> None:
        self.label = val
        if(type(val) is int):
            if(val <= 64 and val >= -16):
                self.val = val
            else:
                assert False
        elif(type(val) is float):
            if (val in [0.0, 0.5, 1.0, 2.0, 4.0, -0.5, -1.0, -2.0, -4.0, 0.1592, 0.15915494, 0.15915494309189532]):
                self.val = val
            else:
                assert False
        else:
            assert False
    
    def __str__(self) -> str:
        return f' {self.val}'

class iconst():
    def __init__(self, val) -> None:
        self.label = val
        if(type(val) is int):
            if(val <= 64 and val >= -16):
                self.val = val
            else:
                assert False
        else:
            assert False
    
    def __str__(self) -> str:
        return f' {self.val}'

class literal():
    def __init__(self, val) -> None:
        self.label = val
        if(type(val) in [int, float]):
            self.val = val
        else:
            assert False
            
    def __str__(self) -> str:
        return f' {self.val}'        

class imm16_t(const_val):
    def __init__(self, val) -> None:
        if(type(val) is int and (val <= 65535) and (val >= -32768)):
            super().__init__(val=val)
        else:
            assert False
            
    def __str__(self) -> str:
        return f' {self.val}'   

class simm32_t(const_val):
    def __init__(self, val) -> None:
        if(type(val) is int and (val < 1**32) and (val >= -(1**32))):
            super().__init__(val=val)
        else:
            assert False
            
    def __str__(self) -> str:
        return f' {self.val}' 

class simm21_t(const_val):
    def __init__(self, val) -> None:
        if(type(val) is int and (val < 1**20) and (val >= -(1**20) )):
            super().__init__(val=val)
        else:
            assert False
            
    def __str__(self) -> str:
        return f' {self.val}'  

class uimm20_t(const_val):
    def __init__(self, val) -> None:
        if(type(val) is int and (val < 1**20) and (val >= 0)):
            super().__init__(val=val)
        else:
            assert False
            
    def __str__(self) -> str:
        return f' {self.val}' 


class label_t():
    def __init__(self, val:str) -> None:
        self.label = val
        if(type(val) is str):
            self.val = val
        else:
            assert False
            
    def __str__(self) -> str:
        return f' {self.val}' 

    def define(self):
        return f' {self.val}:'


class reg_block_custom_reg(reg_block):
    def __init__(self, label:str, reg_t:reg_type, dwords:int = 1):
        
        assert type(label) is str
        assert type(dwords) is int
        super().__init__(label=label, reg_t=reg_t, position=-1, dwords=dwords)
        self.position = label

    def define(self):
        raise AttributeError( "'custom_reg' object has no attribute 'define'" )

    def set_position(self, position:int):
        raise AttributeError( "'custom_reg' object has no attribute 'set_position'" )
    
    def expr(self, index = 0):
        raise AttributeError( "'custom_reg' object has no attribute 'expr'" )


class block_of_reg_blocks(reg_block):
    def __init__(self, label: str, reg_t: reg_type, reg_blocks:List[reg_block], position: int = 0, dwords: int = 1, reg_align=1):
        super().__init__(label, reg_t, position=position, dwords=dwords, reg_align=reg_align)
        self._reg_blocks = reg_blocks
    
    @classmethod
    def declare(cls, label:str, reg_t:reg_type, reg_blocks:List[reg_block], dwords:int = 1, reg_align=1):
        '''Declaration without definition, only block type, label and size will be defined'''
        return block_of_reg_blocks(label, reg_t, reg_blocks, position=-1, dwords=dwords, reg_align=reg_align)


class regAbs(regVar):
    def __init__(self, reg_src:regVar):
        self.__dict__.update(reg_src.__dict__)
    def __str__(self) -> str:
        return f'abs({super().__str__()})'

class regNeg(regVar):
    def __init__(self, reg_src:regVar):
        self.__dict__.update(reg_src.__dict__)
    def __str__(self) -> str:
        return f'neg({super().__str__()})'

def abs(reg:regVar):
    return regAbs

def neg(reg:regVar):
    return regAbs

m0_reg_block = reg_block('m0', reg_type.sgpr, -1, 2)

class  M0_reg(regVar):
    def __init__(self):
        super().__init__(m0_reg_block.label, m0_reg_block, 0, 2)

    def set_lable(self, label:str):
        raise AttributeError( "'m0' object has no attribute 'set_lable'" )

    def define(self):
        raise AttributeError( "'m0' object has no attribute 'define'" )

    def define_as(self, label:str):
        raise AttributeError( "'m0' object has no attribute 'define_as'" )

    def __getitem__(self, key):
        slice_size = 1
        l = 0
        r = 0
        if(type(key) is tuple):
            assert len(key) == 2
            r = key[1]
            l = key[0]
        elif (type(key) is slice):
            r = key.stop
            l = key.start
        else:
            l = key
            r = key
        #send label without reg_type prefix
        slice_size = r - l
        assert(slice_size <= 1 and slice_size >= 0)
        return self

    def __str__(self) -> str:
        return f'{self.label}'

vcc_reg_block = reg_block('vcc', reg_type.sgpr, -1, 2) 

class  VCC_reg(regVar):
    def __init__(self, baseVCC=True):
        super().__init__(vcc_reg_block.label, vcc_reg_block, 0, 2)
        if(baseVCC):
            self.lo = _VCC_LO()
            self.hi = _VCC_HI()
    
    def set_lable(self, label:str):
        raise AttributeError( "'VCC' object has no attribute 'set_lable'" )

    def define(self):
        raise AttributeError( "'VCC' object has no attribute 'define'" )

    def define_as(self, label:str):
        raise AttributeError( "'VCC' object has no attribute 'define_as'" )

    def __getitem__(self, key):
        slice_size = 1
        l = 0
        r = 0
        if(type(key) is tuple):
            assert len(key) == 2
            r = key[1]
            l = key[0]
        elif (type(key) is slice):
            r = key.stop
            l = key.start
        else:
            l = key
            r = key
        #send label without reg_type prefix
        slice_size = r - l
        assert(slice_size <= 1 and slice_size >= 0)
        if(slice_size > 0):
            return self
        else:
            if(l == 0):
                return self.lo
            else:
                return self.hi

    def __str__(self) -> str:
        return f'{self.label}'

class  _VCC_LO(VCC_reg):
    def __init__(self):

        super().__init__(baseVCC=False)
        self.label = 'vcc_lo'
        self.regVar_size = 1

    def __getitem__(self, key):
        l = 0
        r = 0
        if(type(key) is tuple):
            assert len(key) == 2
            r = key[1]
            l = key[0]
        elif (type(key) is slice):
            r = key.stop
            l = key.start
        else:
            l = key
            r = key
        #send label without reg_type prefix
        assert(l == r)
        
        return self
        
class  _VCC_HI(VCC_reg):
    def __init__(self):
        super().__init__(baseVCC=False)
        self.reg_offset = 1
        self.regVar_size = 1
        self.label = 'vcc_hi'
    
    def __getitem__(self, key):
        l = 0
        r = 0
        if(type(key) is tuple):
            assert len(key) == 2
            r = key[1]
            l = key[0]
        elif (type(key) is slice):
            r = key.stop
            l = key.start
        else:
            l = key
            r = key
        #send label without reg_type prefix
        assert(l == r)
        
        return self

EXEC_reg_block = reg_block('exec', reg_type.sgpr, -1, 2) 

class  EXEC_reg(regVar):
    def __init__(self, baseEXEC=True):
        super().__init__(EXEC_reg_block.label, EXEC_reg_block, 0, 2)
        if(baseEXEC):
            self.lo = _EXEC_LO()
            self.hi = _EXEC_HI()
    
    def set_lable(self, label:str):
        raise AttributeError( "'EXEC' object has no attribute 'set_lable'" )

    def define(self):
        raise AttributeError( "'EXEC' object has no attribute 'define'" )

    def define_as(self, label:str):
        raise AttributeError( "'EXEC' object has no attribute 'define_as'" )

    def __getitem__(self, key):
        slice_size = 1
        l = 0
        r = 0
        if(type(key) is tuple):
            assert len(key) == 2
            r = key[1]
            l = key[0]
        elif (type(key) is slice):
            r = key.stop
            l = key.start
        else:
            l = key
            r = key
        #send label without reg_type prefix
        slice_size = r - l
        assert(slice_size <= 1 and slice_size >= 0)
        if(slice_size > 0):
            return self
        else:
            if(l == 0):
                return self.lo
            else:
                return self.hi

    def __str__(self) -> str:
        return f'{self.label}'

class  _EXEC_LO(EXEC_reg):
    def __init__(self):
        super().__init__(baseEXEC=False)
        self.label = 'exec_lo'
        self.regVar_size = 1
    
    def __getitem__(self, key):
        l = 0
        r = 0
        if(type(key) is tuple):
            assert len(key) == 2
            r = key[1]
            l = key[0]
        elif (type(key) is slice):
            r = key.stop
            l = key.start
        else:
            l = key
            r = key
        #send label without reg_type prefix
        assert(l == r)
        
        return self
        
class  _EXEC_HI(EXEC_reg):
    def __init__(self):

        super().__init__(baseEXEC=False)
        self.regVar_size = 1
        self.reg_offset = 1
        self.label = 'exec_hi'

    
    def __getitem__(self, key):
        l = 0
        r = 0
        if(type(key) is tuple):
            assert len(key) == 2
            r = key[1]
            l = key[0]
        elif (type(key) is slice):
            r = key.stop
            l = key.start
        else:
            l = key
            r = key
        #send label without reg_type prefix
        assert(l == r)
        
        return self

SCC_reg_block = reg_block('scc', reg_type.sgpr, -1, 1)

class SCC_bit(regVar):
    def __init__(self):
        super().__init__(SCC_reg_block.label, SCC_reg_block, 0, 2)
    
    def set_lable(self, label:str):
        raise AttributeError( "'SCC_bit' object has no attribute 'set_lable'" )

    def define(self):
        raise AttributeError( "'SCC_bit' object has no attribute 'define'" )

    def define_as(self, label:str):
        raise AttributeError( "'SCC_bit' object has no attribute 'define_as'" )

    def __getitem__(self, key):
        l = 0
        r = 0
        if(type(key) is tuple):
            assert len(key) == 2
            r = key[1]
            l = key[0]
        elif (type(key) is slice):
            r = key.stop
            l = key.start
        else:
            l = key
            r = key
        #send label without reg_type prefix
        assert(l == r)
        
        return self

    def __str__(self) -> str:
        return f'{self.label}'

class off_reg(const_val):
    def __init__(self):
        super().__init__(val='off')

off = off_reg()    

class null_t(const_val):
    def __init__(self):
        super().__init__(val='null')

class lds_direct_t(const_val):
    def __init__(self):
        super().__init__(val='lds_direct')

class ival_t(const_val):
    def __init__(self, val:str):
        syntax = ['shared_base', 'shared_limit', 'private_base', 'private_limit', 'pops_exiting_wave_id']
        if(val in syntax):
            super().__init__(val=val)

class  TTMP_reg(regVar):
    def __init__(self, TTMP_reg_block, size):
        super().__init__('ttmp', TTMP_reg_block, reg_offset = 0, regVar_size=size)
    
    def set_lable(self, label:str):
        raise AttributeError( "'TTMP_reg' object has no attribute 'set_lable'" )

    def define(self):
        raise AttributeError( "'TTMP_reg' object has no attribute 'define'" )

    def define_as(self, label:str):
        raise AttributeError( "'TTMP_reg' object has no attribute 'define_as'" )

