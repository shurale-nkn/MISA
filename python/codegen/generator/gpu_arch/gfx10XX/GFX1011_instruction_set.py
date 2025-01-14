#generated by instruction_parser.py
from typing import Any, Union
from ..gpu_instruct import inst_base, inst_caller_base, instruction_type
from ..gpu_data_types import *

class dpp16_base_gfx10Ex(inst_base): 
	def __init__(self, INSTRUCTION:str, DST:Union[regVar,None,Any], SRC0:Union[regVar,None,Any], SRC1:Union[regVar,None,Any], MODIFIERS:str): 
		super().__init__(instruction_type.SMEM, INSTRUCTION)
		self.DST = DST 
		self.SRC0 = SRC0 
		self.SRC1 = SRC1 
		self.MODIFIERS = MODIFIERS 
	def __str__(self): 
		args_l = filter(None.__ne__, [self.DST,self.SRC0,self.SRC1]) 
		return f"{self.label} {', '.join(map(str, args_l))} {self.MODIFIERS}" 
class dpp16_instr_caller_gfx10Ex(inst_caller_base): 
	def __init__(self, insturction_container) -> None:
     		super().__init__(insturction_container)
	def v_dot2c_f32_f16_dpp(self, vdst:regVar, vsrc0:regVar, vsrc1:regVar, MODIFIERS:str=''):
		""":param str MODIFIERS: dpp16_ctrl row_mask bank_mask bound_ctrl fi"""
		return self.ic_pb(dpp16_base_gfx10Ex('v_dot2c_f32_f16_dpp', vdst, vsrc0, vsrc1, MODIFIERS))
	def v_dot4c_i32_i8_dpp(self, vdst:regVar, vsrc0:regVar, vsrc1:regVar, MODIFIERS:str=''):
		""":param str MODIFIERS: dpp16_ctrl row_mask bank_mask bound_ctrl fi"""
		return self.ic_pb(dpp16_base_gfx10Ex('v_dot4c_i32_i8_dpp', vdst, vsrc0, vsrc1, MODIFIERS))
class dpp8_base_gfx10Ex(inst_base): 
	def __init__(self, INSTRUCTION:str, DST:Union[regVar,None,Any], SRC0:Union[regVar,None,Any], SRC1:Union[regVar,None,Any], MODIFIERS:str): 
		super().__init__(instruction_type.SMEM, INSTRUCTION)
		self.DST = DST 
		self.SRC0 = SRC0 
		self.SRC1 = SRC1 
		self.MODIFIERS = MODIFIERS 
	def __str__(self): 
		args_l = filter(None.__ne__, [self.DST,self.SRC0,self.SRC1]) 
		return f"{self.label} {', '.join(map(str, args_l))} {self.MODIFIERS}" 
class dpp8_instr_caller_gfx10Ex(inst_caller_base): 
	def __init__(self, insturction_container) -> None:
     		super().__init__(insturction_container)
	def v_dot2c_f32_f16_dpp(self, vdst:regVar, vsrc0:regVar, vsrc1:regVar, MODIFIERS:str=''):
		""":param str MODIFIERS: dpp8_sel fi"""
		return self.ic_pb(dpp8_base_gfx10Ex('v_dot2c_f32_f16_dpp', vdst, vsrc0, vsrc1, MODIFIERS))
	def v_dot4c_i32_i8_dpp(self, vdst:regVar, vsrc0:regVar, vsrc1:regVar, MODIFIERS:str=''):
		""":param str MODIFIERS: dpp8_sel fi"""
		return self.ic_pb(dpp8_base_gfx10Ex('v_dot4c_i32_i8_dpp', vdst, vsrc0, vsrc1, MODIFIERS))
class vop2_base_gfx10Ex(inst_base): 
	def __init__(self, INSTRUCTION:str, DST:Union[regVar,None,Any], SRC0:Union[regVar,None,Any], SRC1:Union[regVar,None,Any]): 
		super().__init__(instruction_type.SMEM, INSTRUCTION)
		self.DST = DST 
		self.SRC0 = SRC0 
		self.SRC1 = SRC1 
	def __str__(self): 
		args_l = filter(None.__ne__, [self.DST,self.SRC0,self.SRC1]) 
		return f"{self.label} {', '.join(map(str, args_l))} " 
class vop2_instr_caller_gfx10Ex(inst_caller_base): 
	def __init__(self, insturction_container) -> None:
     		super().__init__(insturction_container)
	def v_dot2c_f32_f16(self, vdst:regVar, src0:regVar, vsrc1:regVar):
		return self.ic_pb(vop2_base_gfx10Ex('v_dot2c_f32_f16', vdst, src0, vsrc1))
	def v_dot4c_i32_i8(self, vdst:regVar, src0:regVar, vsrc1:regVar):
		return self.ic_pb(vop2_base_gfx10Ex('v_dot4c_i32_i8', vdst, src0, vsrc1))
class vop3p_base_gfx10Ex(inst_base): 
	def __init__(self, INSTRUCTION:str, DST:Union[regVar,None,Any], SRC0:Union[regVar,None,Any], SRC1:Union[regVar,None,Any], SRC2:Union[regVar,None,Any], MODIFIERS:str): 
		super().__init__(instruction_type.SMEM, INSTRUCTION)
		self.DST = DST 
		self.SRC0 = SRC0 
		self.SRC1 = SRC1 
		self.SRC2 = SRC2 
		self.MODIFIERS = MODIFIERS 
	def __str__(self): 
		args_l = filter(None.__ne__, [self.DST,self.SRC0,self.SRC1,self.SRC2]) 
		return f"{self.label} {', '.join(map(str, args_l))} {self.MODIFIERS}" 
class vop3p_instr_caller_gfx10Ex(inst_caller_base): 
	def __init__(self, insturction_container) -> None:
     		super().__init__(insturction_container)
	def v_dot2_f32_f16(self, vdst:regVar, src0:regVar, src1:regVar, src2:regVar, MODIFIERS:str=''):
		""":param str MODIFIERS: neg_lo neg_hi clamp"""
		return self.ic_pb(vop3p_base_gfx10Ex('v_dot2_f32_f16', vdst, src0, src1, src2, MODIFIERS))
	def v_dot2_i32_i16(self, vdst:regVar, src0:regVar, src1:regVar, src2:regVar, MODIFIERS:str=''):
		""":param str MODIFIERS: clamp"""
		return self.ic_pb(vop3p_base_gfx10Ex('v_dot2_i32_i16', vdst, src0, src1, src2, MODIFIERS))
	def v_dot2_u32_u16(self, vdst:regVar, src0:regVar, src1:regVar, src2:regVar, MODIFIERS:str=''):
		""":param str MODIFIERS: clamp"""
		return self.ic_pb(vop3p_base_gfx10Ex('v_dot2_u32_u16', vdst, src0, src1, src2, MODIFIERS))
	def v_dot4_i32_i8(self, vdst:regVar, src0:regVar, src1:regVar, src2:regVar, MODIFIERS:str=''):
		""":param str MODIFIERS: clamp"""
		return self.ic_pb(vop3p_base_gfx10Ex('v_dot4_i32_i8', vdst, src0, src1, src2, MODIFIERS))
	def v_dot4_u32_u8(self, vdst:regVar, src0:regVar, src1:regVar, src2:regVar, MODIFIERS:str=''):
		""":param str MODIFIERS: clamp"""
		return self.ic_pb(vop3p_base_gfx10Ex('v_dot4_u32_u8', vdst, src0, src1, src2, MODIFIERS))
	def v_dot8_i32_i4(self, vdst:regVar, src0:regVar, src1:regVar, src2:regVar, MODIFIERS:str=''):
		""":param str MODIFIERS: clamp"""
		return self.ic_pb(vop3p_base_gfx10Ex('v_dot8_i32_i4', vdst, src0, src1, src2, MODIFIERS))
	def v_dot8_u32_u4(self, vdst:regVar, src0:regVar, src1:regVar, src2:regVar, MODIFIERS:str=''):
		""":param str MODIFIERS: clamp"""
		return self.ic_pb(vop3p_base_gfx10Ex('v_dot8_u32_u4', vdst, src0, src1, src2, MODIFIERS))
