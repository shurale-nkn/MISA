################################################################################
# 
#  MIT License
# 
#  Copyright (c) 2020-2021 Advanced Micro Devices, Inc.
# 
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
# 
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
# 
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
# 
################################################################################
from __future__ import print_function
import sys
from ..codegen import *

class inst_buffer_load_t(object):
    ''' TODO: this implementation always offen '''
    def __init__(self, data_byte):
        self.data_byte = data_byte

    def __call__(self, vdst, vaddr, srsrc, soffset, offset):
        if type(soffset) is int and soffset == 0:
            soffset_str = "0"
        else:
            soffset_str = f"s[{soffset}]"

        if self.data_byte == 1:
            return f"buffer_load_ubyte v[{vdst}], v[{vaddr}], s[{srsrc}:{srsrc}+3], {soffset_str} offen offset:{offset}"
        if self.data_byte == 2:
            return f"buffer_load_short_d16 v[{vdst}], v[{vaddr}], s[{srsrc}:{srsrc}+3], {soffset_str} offen offset:{offset}"
        if self.data_byte == 4:
            return f"buffer_load_dword v[{vdst}], v[{vaddr}], s[{srsrc}:{srsrc}+3], {soffset_str} offen offset:{offset}"
        if self.data_byte == 8:
            return f"buffer_load_dwordx2 v[{vdst}:{vdst}+1], v[{vaddr}], s[{srsrc}:{srsrc}+3], {soffset_str} offen offset:{offset}"
        if self.data_byte == 12:
            return f"buffer_load_dwordx3 v[{vdst}:{vdst}+2], v[{vaddr}], s[{srsrc}:{srsrc}+3], {soffset_str} offen offset:{offset}"
        if self.data_byte == 16:
            return f"buffer_load_dwordx4 v[{vdst}:{vdst}+3], v[{vaddr}], s[{srsrc}:{srsrc}+3], {soffset_str} offen offset:{offset}"
        assert False

class inst_buffer_store_t(object):
    ''' TODO: this implementation always offen '''
    def __init__(self, data_byte):
        self.data_byte = data_byte

    def __call__(self, vdata, vaddr, srsrc, soffset, offset, lo_hi = 0):
        if type(soffset) is int and soffset == 0:
            soffset_str = "0"
        else:
            soffset_str = f"s[{soffset}]"

        if self.data_byte == 1:
            if lo_hi == 0:
                return f"buffer_store_byte v[{vdata}], v[{vaddr}], s[{srsrc}:{srsrc}+3], {soffset_str} offen offset:{offset}"
            else:
                return f"buffer_store_byte_d16_hi v[{vdata}], v[{vaddr}], s[{srsrc}:{srsrc}+3], {soffset_str} offen offset:{offset}"
        if self.data_byte == 2:
            if lo_hi == 0:
                return f"buffer_store_short v[{vdata}], v[{vaddr}], s[{srsrc}:{srsrc}+3], {soffset_str} offen offset:{offset}"
            else:
                return f"buffer_store_short_d16_hi v[{vdata}], v[{vaddr}], s[{srsrc}:{srsrc}+3], {soffset_str} offen offset:{offset}"
        if self.data_byte == 4:
            return f"buffer_store_dword v[{vdata}], v[{vaddr}], s[{srsrc}:{srsrc}+3], {soffset_str} offen offset:{offset}"
        if self.data_byte == 8:
            return f"buffer_store_dwordx2 v[{vdata}:{vdata}+1], v[{vaddr}], s[{srsrc}:{srsrc}+3], {soffset_str} offen offset:{offset}"
        if self.data_byte == 12:
            return f"buffer_store_dwordx3 v[{vdata}:{vdata}+2], v[{vaddr}], s[{srsrc}:{srsrc}+3], {soffset_str} offen offset:{offset}"
        if self.data_byte == 16:
            return f"buffer_store_dwordx4 v[{vdata}:{vdata}+3], v[{vaddr}], s[{srsrc}:{srsrc}+3], {soffset_str} offen offset:{offset}"
        assert False

class inst_buffer_atomic_add_dword_t(object):
    ''' TODO: this implementation always offen '''
    def __init__(self, data_byte, pack=1):
        self.data_byte = data_byte
        self.pack = pack

    def __call__(self, vdata, vaddr, srsrc, soffset, offset, lo_hi=0):
        if type(soffset) is int and soffset == 0:
            soffset_str = "0"
        else:
            soffset_str = f"s[{soffset}]"

        if self.data_byte == 4 and self.pack == 1:
            return f"buffer_atomic_add_f32 v[{vdata}], v[{vaddr}], s[{srsrc}:{srsrc}+3], {soffset_str} offen offset:{offset}"
        if self.data_byte == 4 and self.pack == 2:
            return f"buffer_atomic_pk_add_f16 v[{vdata}], v[{vaddr}], s[{srsrc}:{srsrc}+3], {soffset_str} offen offset:{offset}"
        assert False, f"data_byte:{self.data_byte}, pack:{self.pack}"


# pattern is logic or of below:
GLOBAL_PTN_D0_S = (1 << 0)
GLOBAL_PTN_D0_V = (1 << 1)
GLOBAL_PTN_D0_K = (1 << 2)
GLOBAL_PTN_D1_S = (1 << 0) << 4
GLOBAL_PTN_D1_V = (1 << 1) << 4
GLOBAL_PTN_D1_K = (1 << 2) << 4




class ctrl_2d_global_load_t(object):
    def __init__(self):
        self.length_d0 = 1           # if d0 is 1, it is indeed 1d access
        self.length_d1 = 1
        self.vector_d1 = 1
        self.precision = 'fp32'      # 'fp32', 'fp16', ...
        self.src_order = 0           # 0-d0xd1, 1-d1xd0
        self.dst_order = 0           # 0-d0xd1, 1-d1xd0
        self.use_flag = 0
        self.flag_on_d0 = 0
        self.flag_on_d1 = 0
        self.bfe_flag = 0
        self.precache_ptn = 0        # 0: d0 use sgpr precache, d1 use sgpr precache
                                     # 1: d0 use sgpr precache, d1 use vgpr precache
                                     # 2: d0 use sgpr precache, d1 use immidiate value
                                     # 3: d0 use vgpr precache, d1 use sgpr precache
                                     # 4: d0 use vgpr precache, d1 use vgpr precache
                                     # 5: d0 use vgpr precache, d1 use immidiate value
                                     # 4: .... maybe consider not using precache?
        self.flag_merge_v = 0        # when flag on v_offset, flag and multiple load, or flag per load
        self.dim_conti_flag  = 0        # when dim flag is set, means length d0 is contiguous, and sgpr offset will not be used


class macro_igemm_2d_global_load_t(macro_base_t):
    # TODO: if need vectorize further LDS write, need shuffle dst gpr while load
    def __init__(self, mc, ctrl, inline = False):
        assert type(ctrl) is ctrl_2d_global_load_t
        macro_base_t.__init__(self, mc, inline)
        self.ctrl = ctrl
        self.declare_arg("v_dst")
        self.declare_arg("s_ptr")
        self.declare_arg("v_os")
        self.declare_arg("s_stride_d0")
        self.declare_arg("s_stride_d1")
        self.declare_arg("s_tmp2")

    def name(self):
        ctrl = self.ctrl
        if ctrl.precision == "fp32":
            bits_str = 'b32'
        elif ctrl.precision in ("fp16", "bf16"):
            bits_str = 'b16'
        else:
            assert False

        if ctrl.vector_d1 == 4:
            vec_str = 'v4'
        elif ctrl.vector_d1 == 2:
            vec_str = 'v2'
        elif ctrl.vector_d1 == 1:
            vec_str = 'v1'
        else:
            assert False

        #assert ctrl.length_d1 % ctrl.vector_d1 = 0
        #n_d1 = ctrl.length_d1 // ctrl.vector_d1
        return f".v_gld_{ctrl.length_d0}x{ctrl.length_d1}_{bits_str}_{vec_str}"

    def expr(self):
        ctrl = self.ctrl
        assert ctrl.length_d1 % ctrl.vector_d1 == 0
        n_d1 = ctrl.length_d1 // ctrl.vector_d1
        # assert ctrl.precision == 'fp32', "TO BE supported"
        buffer_load_dword = inst_buffer_load_t(ctrl.vector_d1 * amdgpu_precision_data_byte(ctrl.precision))
        #with self._emit_macro_indented('.macro {} v_dst, s_ptr, v_os, s_stride_d0, s_stride_d1, s_tmp2'.format(self.name())):
        if ctrl.src_order == 0 and ctrl.dst_order == 0:
            i_dst = 0
            for i_d0 in range(ctrl.length_d0):
                for i_d1 in range(n_d1):
                    if i_d1 == 0 and i_d0 == 0:
                        self._emit(buffer_load_dword(f"{self.v_dst()}+{i_dst*ctrl.vector_d1}", f"{self.v_os()}", f"{self.s_ptr()}", 0, 0))
                    elif i_d1 == 0 and i_d0 != 0:
                        self._emit(buffer_load_dword(f"{self.v_dst()}+{i_dst*ctrl.vector_d1}", f"{self.v_os()}", f"{self.s_ptr()}", f"{self.s_tmp2()}+1", 0))
                    else:
                        self._emit(buffer_load_dword(f"{self.v_dst()}+{i_dst*ctrl.vector_d1}", f"{self.v_os()}", f"{self.s_ptr()}", f"{self.s_tmp2()}", 0))

                    if i_d1 != (n_d1 - 1):
                        if i_d1 == 0 and i_d0 ==  0:
                            self._emit(f"s_mov_b32 s[{self.s_tmp2()}], s[{self.s_stride_d1()}]")
                        elif i_d1 == 0 and i_d0 !=  0:
                            self._emit(f"s_add_u32 s[{self.s_tmp2()}], s[{self.s_tmp2()}+1], s[{self.s_stride_d1()}]")
                        else:
                            self._emit(f"s_add_u32 s[{self.s_tmp2()}], s[{self.s_tmp2()}], s[{self.s_stride_d1()}]")
                    i_dst = i_dst + 1

                if i_d0 != (ctrl.length_d0 - 1):
                    if i_d0 == 0:
                        self._emit(f"s_mov_b32 s[{self.s_tmp2()}+1], s[{self.s_stride_d0()}]")
                    else:
                        self._emit(f"s_add_u32 s[{self.s_tmp2()}+1], s[{self.s_tmp2()}+1], s[{self.s_stride_d0()}]")
        elif ctrl.src_order == 1 and ctrl.dst_order == 0:
            assert ctrl.vector_d1 == 1, "in such reorder, vector load is meanless"
            for i_d1 in range(ctrl.length_d1):
                for i_d0 in range(ctrl.length_d0):
                    if i_d0 == 0 and i_d1 == 0:
                        self._emit(buffer_load_dword(f"{self.v_dst()}+{i_d0 * ctrl.length_d1 + i_d1}", f"{self.v_os()}", f"{self.s_ptr()}", 0, 0))
                    elif i_d0 == 0 and i_d1 != 0:
                        self._emit(buffer_load_dword(f"{self.v_dst()}+{i_d0 * ctrl.length_d1 + i_d1}", f"{self.v_os()}", f"{self.s_ptr()}", f"{self.s_tmp2()}+1", 0))
                    else:
                        self._emit(buffer_load_dword(f"{self.v_dst()}+{i_d0 * ctrl.length_d1 + i_d1}", f"{self.v_os()}", f"{self.s_ptr()}", f"{self.s_tmp2()}", 0))

                    if i_d0 != (ctrl.length_d0 - 1):
                        if i_d0 == 0 and i_d1 ==  0:
                            self._emit(f"s_mov_b32 s[{self.s_tmp2()}], s[{self.s_stride_d0()}]")
                        elif i_d0 == 0 and i_d1 !=  0:
                            self._emit(f"s_add_u32 s[{self.s_tmp2()}], s[{self.s_tmp2()}+1], s[{self.s_stride_d0()}]")
                        else:
                            self._emit(f"s_add_u32 s[{self.s_tmp2()}], s[{self.s_tmp2()}], s[{self.s_stride_d0()}]")

                if i_d1 != (ctrl.length_d1 - 1):
                    if i_d1 == 0:
                        self._emit(f"s_mov_b32 s[{self.s_tmp2()}+1], s[{self.s_stride_d1()}]")
                    else:
                        self._emit(f"s_add_u32 s[{self.s_tmp2()}+1], s[{self.s_tmp2()}+1], s[{self.s_stride_d1()}]")

        elif ctrl.src_order == 0 and ctrl.dst_order == 1:
            assert False, "un implemented"
        elif ctrl.src_order == 1 and ctrl.dst_order == 1:
            assert False, "un implemented, consider simple swap stride_d0/d1 order should be the same"
        else:
            assert False

    def get_issues(self):
        ctrl = self.ctrl
        n_d1 = ctrl.length_d1 // ctrl.vector_d1
        return  ctrl.length_d0 * n_d1


class macro_igemm_2d_global_load_precache_soffset_t(macro_base_t):
    # precache soffset means no salu while do loading
    def __init__(self, mc, ctrl, inline = False):
        assert type(ctrl) is ctrl_2d_global_load_t
        macro_base_t.__init__(self, mc, inline)
        self.ctrl = ctrl
        self.declare_arg("v_dst")
        self.declare_arg("s_ptr")
        self.declare_arg("v_os")
        self.declare_arg("s_stride_d0")
        self.declare_arg("s_stride_d1")
        self.declare_arg("s_offset")
        if self.ctrl.use_flag:
            self.declare_arg("v_flag")

    def name(self):
        ctrl = self.ctrl
        if ctrl.precision == "fp32":
            bits_str = 'b32'
        elif ctrl.precision in ("fp16", "bf16"):
            bits_str = 'b16'
        else:
            assert False

        if ctrl.vector_d1 == 4:
            vec_str = 'v4'
        elif ctrl.vector_d1 == 2:
            vec_str = 'v2'
        elif ctrl.vector_d1 == 1:
            vec_str = 'v1'
        else:
            assert False

        return f".v_gld_{ctrl.length_d0}x{ctrl.length_d1}_{bits_str}_{vec_str}_precache_soffset"
    
    def get_2d_index_soffset(self):
        ctrl = self.ctrl
        assert ctrl.length_d1 % ctrl.vector_d1 == 0
        n_d1 = ctrl.length_d1 // ctrl.vector_d1
        soffset_cnt = 0
        index_mapping = list()
        for i_d0 in range(ctrl.length_d0):
            index_mapping_per_d1 = [-1] * n_d1
            for i_d1 in range(n_d1):
                if i_d0 == 0 and i_d1 == 0:
                    continue
                if i_d0 == 0 and i_d1 == 1:
                    continue
                if i_d0 == 1 and i_d1 == 0:
                    continue
                index_mapping_per_d1[i_d1] = soffset_cnt
                soffset_cnt += 1
            index_mapping.append(index_mapping_per_d1)
        return index_mapping

    def get_num_precache_soffset(self):
        ctrl = self.ctrl
        assert ctrl.length_d1 % ctrl.vector_d1 == 0
        n_d1 = ctrl.length_d1 // ctrl.vector_d1
        soffset_cnt = 0
        for i_d0 in range(ctrl.length_d0):
            for i_d1 in range(n_d1):
                if i_d0 == 0 and i_d1 == 0:
                    continue
                if i_d0 == 0 and i_d1 == 1:
                    continue
                if i_d0 == 1 and i_d1 == 0:
                    continue
                soffset_cnt += 1
        return soffset_cnt

    def init_precache_soffset(self, s_stride_d0, s_stride_d1, s_offset, s_tmp):
        ctrl = self.ctrl
        assert ctrl.length_d1 % ctrl.vector_d1 == 0
        n_d1 = ctrl.length_d1 // ctrl.vector_d1
        with self._deferred_context():
            i_soffset = 0
            for i_d0 in range(ctrl.length_d0):
                for i_d1 in range(n_d1):
                    if i_d0 == 0 and i_d1 == 0:
                        continue
                    if i_d0 == 0 and i_d1 == 1:
                        continue
                    if i_d0 == 1 and i_d1 == 0:
                        continue

                    # start to emit init
                    if i_d0 == 0:
                        self._emit(f"s_mul_i32 s[{s_offset}+{i_soffset}], {i_d1}, s[{s_stride_d1}]")
                    elif i_d0 == 1:
                        if i_d1 == 1:
                            self._emit(f"s_add_u32 s[{s_offset}+{i_soffset}], s[{s_stride_d0}], s[{s_stride_d1}]")
                        else:
                            self._emit(f"s_add_u32 s[{s_offset}+{i_soffset}], s[{s_stride_d0}], s[{s_offset}+{i_d1-2}]")
                    else:
                        if i_d1 == 0:
                            self._emit(f"s_mul_i32 s[{s_tmp}], s[{s_stride_d0}], {i_d0}")
                        if i_d1 == 0:
                            self._emit(f"s_mov_b32 s[{s_offset}+{i_soffset}], s[{s_tmp}]")
                        elif i_d1 == 1:
                            self._emit(f"s_add_u32 s[{s_offset}+{i_soffset}], s[{s_tmp}], s[{s_stride_d1}]")
                        else:
                            self._emit(f"s_add_u32 s[{s_offset}+{i_soffset}], s[{s_tmp}], s[{s_offset}+{i_d1-2}]")
                    i_soffset += 1
        return self._get_deferred()

    def expr(self):
        ctrl = self.ctrl
        assert ctrl.length_d1 % ctrl.vector_d1 == 0
        n_d1 = ctrl.length_d1 // ctrl.vector_d1
        # assert ctrl.precision == 'fp32', "TO BE supported"
        buffer_load_dword = inst_buffer_load_t(ctrl.vector_d1 * amdgpu_precision_data_byte(ctrl.precision))
        #with self._emit_macro_indented('.macro {} v_dst, s_ptr, v_os, s_stride_d0, s_stride_d1, s_offset'.format(self.name())):
        # self._emit(f".v_clear_nc \\v_dst, {ctrl.length_d0 * ctrl.length_d1}")
        data_byte = amdgpu_precision_data_byte(ctrl.precision)
        pixel_per_vgpr = 4 // data_byte
        vgpr_per_vector = (ctrl.vector_d1 + pixel_per_vgpr - 1) // pixel_per_vgpr
        if ctrl.src_order == 0 and ctrl.dst_order == 0:
            i_dst = 0
            i_soffset = 0
            for i_d0 in range(ctrl.length_d0):
                for i_d1 in range(n_d1):
                    if ctrl.dim_conti_flag == 0:
                        if ctrl.use_flag and self.v_flag != None:
                            self._emit(f"v_cmpx_le_u32 vcc, 1, v[{self.v_flag(i_dst)}]")
                        if i_d0 == 0 and i_d1 == 0:
                            self._emit(buffer_load_dword(f"{self.v_dst()}+{i_dst*vgpr_per_vector}", f"{self.v_os()}", f"{self.s_ptr()}", 0, 0))
                        elif i_d0 == 0 and i_d1 == 1:
                            self._emit(buffer_load_dword(f"{self.v_dst()}+{i_dst*vgpr_per_vector}", f"{self.v_os()}", f"{self.s_ptr()}", f"{self.s_stride_d1()}", 0))
                        elif i_d0 == 1 and i_d1 == 0:
                            self._emit(buffer_load_dword(f"{self.v_dst()}+{i_dst*vgpr_per_vector}", f"{self.v_os()}", f"{self.s_ptr()}", f"{self.s_stride_d0()}", 0))
                        else:
                            self._emit(buffer_load_dword(f"{self.v_dst()}+{i_dst*vgpr_per_vector}", f"{self.v_os()}", f"{self.s_ptr()}", f"{self.s_offset()}+{i_soffset}", 0))
                            i_soffset += 1
                        if ctrl.use_flag and self.v_flag != None:
                            self._emit(f"s_mov_b64 exec, -1")
                    else:
                        self._emit(buffer_load_dword(f"{self.v_dst()}+{i_dst*vgpr_per_vector}", f"{self.v_os()}", f"{self.s_ptr()}", 0, i_d1 * vgpr_per_vector * 4))
                    i_dst = i_dst + 1

        elif ctrl.src_order == 1 and ctrl.dst_order == 0:
            assert ctrl.vector_d1 == 1, "in such reorder, vector load is meanless"
            index_mapping = self.get_2d_index_soffset()
            for i_d1 in range(ctrl.length_d1):
                for i_d0 in range(ctrl.length_d0):
                    if i_d0 == 0 and i_d1 == 0:
                        self._emit(buffer_load_dword(f"{self.v_dst()}+{i_dst*vgpr_per_vector}", f"{self.v_os()}", f"{self.s_ptr()}", 0, 0))
                    elif i_d0 == 0 and i_d1 == 1:
                        self._emit(buffer_load_dword(f"{self.v_dst()}+{i_dst*vgpr_per_vector}", f"{self.v_os()}", f"{self.s_ptr()}", f"{self.s_stride_d1()}", 0))
                    elif i_d0 == 1 and i_d1 == 0:
                        self._emit(buffer_load_dword(f"{self.v_dst()}+{i_dst*vgpr_per_vector}", f"{self.v_os()}", f"{self.s_ptr()}", f"{self.s_stride_d0()}", 0))
                    else:
                        i_soffset = index_mapping[i_d0][i_d1]
                        assert i_soffset != 1, "impossible"
                        self._emit(buffer_load_dword(f"{self.v_dst()}+{i_dst*vgpr_per_vector}", f"{self.v_os()}", f"{self.s_ptr()}", f"{self.s_offset()}+{i_soffset}", 0))
        elif ctrl.src_order == 0 and ctrl.dst_order == 1:
            assert False, "un implemented"
        elif ctrl.src_order == 1 and ctrl.dst_order == 1:
            assert False, "un implemented, consider simple swap stride_d0/d1 order should be the same"
        else:
            assert False

    def get_issues(self):
        ctrl = self.ctrl
        n_d1 = ctrl.length_d1 // ctrl.vector_d1
        return  ctrl.length_d0 * n_d1

class macro_igemm_2d_global_load_precache_voffset_t(macro_base_t):
    '''
    not support src/dst order
    '''
    def __init__(self, mc, ctrl, inline = False):
        assert type(ctrl) is ctrl_2d_global_load_t
        macro_base_t.__init__(self, mc, inline)
        self.ctrl = ctrl
        self.declare_arg("v_dst")
        self.declare_arg("s_ptr")
        self.declare_arg("s_os")
        self.declare_arg("v_os")
        if self.ctrl.use_flag:
            self.declare_arg("v_flag")
        if self.ctrl.bfe_flag:
            self.declare_arg("v_tmp")

    def name(self):
        ctrl = self.ctrl
        if ctrl.precision == "fp32":
            bits_str = 'b32'
        elif ctrl.precision in ("fp16", "bf16"):
            bits_str = 'b16'
        else:
            assert False

        if ctrl.vector_d1 == 4:
            vec_str = 'v4'
        elif ctrl.vector_d1 == 2:
            vec_str = 'v2'
        elif ctrl.vector_d1 == 1:
            vec_str = 'v1'
        else:
            assert False

        return f".v_gld_{ctrl.length_d0}x{ctrl.length_d1}_{bits_str}_{vec_str}_precache_voffset"

    def expr(self):
        ctrl = self.ctrl
        assert ctrl.length_d1 % ctrl.vector_d1 == 0
        n_d1 = ctrl.length_d1 // ctrl.vector_d1
        # assert ctrl.precision == 'fp32', "TO BE supported"
        buffer_load_dword = inst_buffer_load_t(ctrl.vector_d1 * amdgpu_precision_data_byte(ctrl.precision))
        pixel_per_vgpr = 4 // amdgpu_precision_data_byte(ctrl.precision)
        vgpr_per_vector = (ctrl.vector_d1 + pixel_per_vgpr - 1) // pixel_per_vgpr
        i_cnt = 0
        for i_d0 in range(ctrl.length_d0):
            for i_d1 in range(n_d1):
                if ctrl.use_flag and self.v_flag != None:
                    if ctrl.bfe_flag:
                        self._emit(f"v_bfe_u32 v[{self.v_tmp()}], v[{self.v_flag()}], {i_cnt}, 1")
                        self._emit(f"v_cmpx_le_u32 vcc, 1, v[{self.v_tmp()}]")
                    else:
                        self._emit(f"v_cmpx_le_u32 vcc, 1, v[{self.v_flag(i_cnt)}]")
                self._emit(buffer_load_dword(f"{self.v_dst()}+{i_cnt*vgpr_per_vector}", f"{self.v_os(i_cnt)}", f"{self.s_ptr()}", f"{self.s_os()}", 0))
                if ctrl.use_flag and self.v_flag != None:
                    self._emit(f"s_mov_b64 exec, -1")
                i_cnt += 1

    def get_issues(self):
        ctrl = self.ctrl
        n_d1 = ctrl.length_d1 // ctrl.vector_d1
        return  ctrl.length_d0 * n_d1

class macro_igemm_2d_global_load_precache_vs_offset_t(macro_base_t):
    # precache voffset for d0 dimension
    # precache soffset for d1 dimension
    # hence v_flag is along d0 dimension
    def __init__(self, mc, ctrl, inline = False):
        assert type(ctrl) is ctrl_2d_global_load_t
        macro_base_t.__init__(self, mc, inline)
        self.ctrl = ctrl
        self.declare_arg("v_dst")
        self.declare_arg("s_ptr")
        self.declare_arg("v_os")
        self.declare_arg("s_stride_d0") # can be None
        self.declare_arg("s_stride_d1")
        self.declare_arg("s_offset")
        if self.ctrl.use_flag:
            self.declare_arg("v_flag")
        if self.ctrl.bfe_flag:
            self.declare_arg("v_tmp")

    def name(self):
        ctrl = self.ctrl
        if ctrl.precision == "fp32":
            bits_str = 'b32'
        elif ctrl.precision in ("fp16", "bf16"):
            bits_str = 'b16'
        else:
            assert False

        if ctrl.vector_d1 == 4:
            vec_str = 'v4'
        elif ctrl.vector_d1 == 2:
            vec_str = 'v2'
        elif ctrl.vector_d1 == 1:
            vec_str = 'v1'
        else:
            assert False

        return f".v_gld_{ctrl.length_d0}x{ctrl.length_d1}_{bits_str}_{vec_str}_precache_vs_offset"

    def expr(self):
        ctrl = self.ctrl
        assert ctrl.length_d1 % ctrl.vector_d1 == 0
        n_d1 = ctrl.length_d1 // ctrl.vector_d1
        # assert ctrl.precision == 'fp32', "TO BE supported"
        buffer_load_dword = inst_buffer_load_t(ctrl.vector_d1 * amdgpu_precision_data_byte(ctrl.precision))
        pixel_per_vgpr = 4 // amdgpu_precision_data_byte(ctrl.precision)
        vgpr_per_vector = (ctrl.vector_d1 + pixel_per_vgpr - 1) // pixel_per_vgpr

        if ctrl.src_order == 0 and ctrl.dst_order == 0:
            i_dst = 0
            for i_d0 in range(ctrl.length_d0):
                for i_d1 in range(n_d1):
                    if ctrl.use_flag and self.v_flag != None:
                        self._emit(f"v_cmpx_le_u32 vcc, 1, v[{self.v_flag(i_d0)}]")
                    current_s_offset = 0 if i_d1 == 0 else (self.s_stride_d1() if i_d1 == 1 else self.s_offset(i_d1 - 2))
                    self._emit(buffer_load_dword(f"{self.v_dst()}+{i_dst*vgpr_per_vector}", f"{self.v_os(i_d0)}", f"{self.s_ptr()}", current_s_offset, 0))
                    if ctrl.use_flag and self.v_flag != None:
                        self._emit(f"s_mov_b64 exec, -1")
                    i_dst = i_dst + 1

        else:
            assert False

    def get_issues(self):
        ctrl = self.ctrl
        n_d1 = ctrl.length_d1 // ctrl.vector_d1
        return  ctrl.length_d0 * n_d1

class macro_igemm_2d_global_load_precache_sv_offset_t(macro_base_t):
    # precache soffset for d0 dimension
    # precache voffset for d1 dimension
    # hence v_flag is along d1 dimension
    def __init__(self, mc, ctrl, inline = False):
        assert type(ctrl) is ctrl_2d_global_load_t
        macro_base_t.__init__(self, mc, inline)
        self.ctrl = ctrl
        self.declare_arg("v_dst")
        self.declare_arg("s_ptr")
        self.declare_arg("v_os")
        self.declare_arg("s_stride_d0") # can be None
        self.declare_arg("s_stride_d1")
        self.declare_arg("s_offset")
        if self.ctrl.use_flag:
            self.declare_arg("v_flag")
        if self.ctrl.bfe_flag:
            self.declare_arg("v_tmp")

    def name(self):
        ctrl = self.ctrl
        if ctrl.precision == "fp32":
            bits_str = 'b32'
        elif ctrl.precision in ("fp16", "bf16"):
            bits_str = 'b16'
        else:
            assert False

        if ctrl.vector_d1 == 4:
            vec_str = 'v4'
        elif ctrl.vector_d1 == 2:
            vec_str = 'v2'
        elif ctrl.vector_d1 == 1:
            vec_str = 'v1'
        else:
            assert False

        return f".v_gld_{ctrl.length_d0}x{ctrl.length_d1}_{bits_str}_{vec_str}_precache_sv_offset"

    def expr(self):
        ctrl = self.ctrl
        assert ctrl.length_d1 % ctrl.vector_d1 == 0
        n_d1 = ctrl.length_d1 // ctrl.vector_d1
        # assert ctrl.precision == 'fp32', "TO BE supported"
        buffer_load_dword = inst_buffer_load_t(ctrl.vector_d1 * amdgpu_precision_data_byte(ctrl.precision))
        pixel_per_vgpr = 4 // amdgpu_precision_data_byte(ctrl.precision)
        vgpr_per_vector = (ctrl.vector_d1 + pixel_per_vgpr - 1) // pixel_per_vgpr

        if ctrl.src_order == 0 and ctrl.dst_order == 0:
            i_dst = 0
            if ctrl.flag_merge_v and n_d1 == 1:
                # v is along d1 dimension, hence only possible when n_d1 is 1
                if ctrl.use_flag and self.v_flag != None:
                    self._emit(f"v_cmpx_le_u32 vcc, 1, v[{self.v_flag()}]")
                for i_d0 in range(ctrl.length_d0):
                    for i_d1 in range(1):
                        current_s_offset = 0 if i_d0 == 0 else (self.s_stride_d1() if i_d0 == 1 else self.s_offset(i_d0 - 2))
                        self._emit(buffer_load_dword(f"{self.v_dst()}+{i_dst*vgpr_per_vector}", f"{self.v_os(i_d1)}", f"{self.s_ptr()}", current_s_offset, 0))
                        i_dst = i_dst + 1
                if ctrl.use_flag and self.v_flag != None:
                    self._emit(f"s_mov_b64 exec, -1")
            else:
                for i_d0 in range(ctrl.length_d0):
                    for i_d1 in range(n_d1):
                        if ctrl.use_flag and self.v_flag != None:
                            self._emit(f"v_cmpx_le_u32 vcc, 1, v[{self.v_flag(i_d1)}]")
                        current_s_offset = 0 if i_d0 == 0 else (self.s_stride_d1() if i_d0 == 1 else self.s_offset(i_d0 - 2))
                        self._emit(buffer_load_dword(f"{self.v_dst()}+{i_dst*vgpr_per_vector}", f"{self.v_os(i_d1)}", f"{self.s_ptr()}", current_s_offset, 0))
                        if ctrl.use_flag and self.v_flag != None:
                            self._emit(f"s_mov_b64 exec, -1")
                        i_dst = i_dst + 1

        else:
            assert False

    def get_issues(self):
        ctrl = self.ctrl
        n_d1 = ctrl.length_d1 // ctrl.vector_d1
        return  ctrl.length_d0 * n_d1



class macro_igemm_2d_global_load_precache_offset_t(macro_base_t):
    def __init__(self, mc, ctrl, inline = False):
        assert type(ctrl) is ctrl_2d_global_load_t
        macro_base_t.__init__(self, mc, inline)
        self.ctrl = ctrl
        self.declare_arg("v_dst")
        self.declare_arg("s_ptr")
        self.declare_arg("v_os")
        self.declare_arg("s_os")    # can be None, the soffset parsed to buffer_load/store
                                    # used when d0, d1 not sgpr, to privide an optional sstride to buffer_load/store
                                    # TODO: remove this since duplicated idea

        # following can be none, used when at least one of d0, d1 is sgpr
        self.declare_arg("s_stride_d0")
        self.declare_arg("s_stride_d1")
        self.declare_arg("s_offset")

        self.declare_arg("v_flag")
        self.declare_arg("v_tmp")   # used when bfe_flag=1

        self.declare_arg("k_gld_d0_stride")
        self.declare_arg("k_gld_d1_stride")

    def name(self):
        ctrl = self.ctrl
        if ctrl.precision == "fp32":
            bits_str = 'b32'
        elif ctrl.precision in ("fp16", "bf16"):
            bits_str = 'b16'
        else:
            assert False

        if ctrl.vector_d1 == 4:
            vec_str = 'v4'
        elif ctrl.vector_d1 == 2:
            vec_str = 'v2'
        elif ctrl.vector_d1 == 1:
            vec_str = 'v1'
        else:
            assert False

        return f".v_gld_{ctrl.length_d0}x{ctrl.length_d1}_{bits_str}_{vec_str}_precache_{ctrl.precache_ptn}"

    def init_precache_soffset(self, s_stride_d0, s_stride_d1, s_offset, s_tmp):
        ctrl = self.ctrl
        assert ctrl.precache_ptn & GLOBAL_PTN_D0_S and ctrl.precache_ptn & GLOBAL_PTN_D1_S
        assert ctrl.length_d1 % ctrl.vector_d1 == 0
        n_d1 = ctrl.length_d1 // ctrl.vector_d1
        with self._deferred_context():
            i_soffset = 0
            for i_d0 in range(ctrl.length_d0):
                for i_d1 in range(n_d1):
                    if i_d0 == 0 and i_d1 == 0:
                        continue
                    if i_d0 == 0 and i_d1 == 1:
                        continue
                    if i_d0 == 1 and i_d1 == 0:
                        continue

                    # start to emit init
                    if i_d0 == 0:
                        self._emit(f"s_mul_i32 s[{s_offset}+{i_soffset}], {i_d1}, s[{s_stride_d1}]")
                    elif i_d0 == 1:
                        if i_d1 == 1:
                            self._emit(f"s_add_u32 s[{s_offset}+{i_soffset}], s[{s_stride_d0}], s[{s_stride_d1}]")
                        else:
                            self._emit(f"s_add_u32 s[{s_offset}+{i_soffset}], s[{s_stride_d0}], s[{s_offset}+{i_d1-2}]")
                    else:
                        if i_d1 == 0:
                            self._emit(f"s_mul_i32 s[{s_tmp}], s[{s_stride_d0}], {i_d0}")
                        if i_d1 == 0:
                            self._emit(f"s_mov_b32 s[{s_offset}+{i_soffset}], s[{s_tmp}]")
                        elif i_d1 == 1:
                            self._emit(f"s_add_u32 s[{s_offset}+{i_soffset}], s[{s_tmp}], s[{s_stride_d1}]")
                        else:
                            self._emit(f"s_add_u32 s[{s_offset}+{i_soffset}], s[{s_tmp}], s[{s_offset}+{i_d1-2}]")
                    i_soffset += 1
        return self._get_deferred()

    def get_num_precache_soffset(self):
        ctrl = self.ctrl
        assert ctrl.length_d1 % ctrl.vector_d1 == 0
        n_d1 = ctrl.length_d1 // ctrl.vector_d1
        soffset_cnt = 0
        for i_d0 in range(ctrl.length_d0):
            for i_d1 in range(n_d1):
                if i_d0 == 0 and i_d1 == 0:
                    continue
                if i_d0 == 0 and i_d1 == 1:
                    continue
                if i_d0 == 1 and i_d1 == 0:
                    continue
                soffset_cnt += 1
        return soffset_cnt

    def expr(self):
        ctrl = self.ctrl
        assert ctrl.length_d1 % ctrl.vector_d1 == 0
        n_d1 = ctrl.length_d1 // ctrl.vector_d1
        # assert ctrl.precision == 'fp32', "TO BE supported"
        buffer_load_dword = inst_buffer_load_t(ctrl.vector_d1 * amdgpu_precision_data_byte(ctrl.precision))
        pixel_per_vgpr = 4 // amdgpu_precision_data_byte(ctrl.precision)
        vgpr_per_vector = (ctrl.vector_d1 + pixel_per_vgpr - 1) // pixel_per_vgpr

        def gen_soffset_sequence():
            if ctrl.precache_ptn & GLOBAL_PTN_D0_S and ctrl.precache_ptn & GLOBAL_PTN_D1_S:
                ssequence = list()
                s_offset_cnt = 0
                for x0 in range(ctrl.length_d0):
                    for x1 in range(n_d1):
                        if x0 == 0:
                            if x1 == 0:
                                ssequence.append(0)
                            elif x1 == 1:
                                ssequence.append(self.s_stride_d1())
                            else:
                                ssequence.append(self.s_offset(s_offset_cnt))
                                s_offset_cnt = s_offset_cnt + 1
                        else:
                            if x0 == 1 and x1 == 0:
                                ssequence.append(self.s_stride_d0())
                            else:
                                ssequence.append(self.s_offset(s_offset_cnt))
                                s_offset_cnt = s_offset_cnt + 1
                return ssequence
            else:
                return None

        ssequence = gen_soffset_sequence()

        def get_soffset(i_d0, i_d1):
            # TODO: global_load/store not have sgpr offset
            current_s_offset = 0
            if ctrl.precache_ptn & GLOBAL_PTN_D0_S and not ctrl.precache_ptn & GLOBAL_PTN_D1_S:
                current_s_offset = 0 if i_d0 == 0 else (self.s_stride_d0() if i_d0 == 1 else self.s_offset(i_d0 - 2))
            elif not ctrl.precache_ptn & GLOBAL_PTN_D0_S and ctrl.precache_ptn & GLOBAL_PTN_D1_S:
                current_s_offset = 0 if i_d1 == 0 else (self.s_stride_d1() if i_d1 == 1 else self.s_offset(i_d1 - 2))
            elif ctrl.precache_ptn & GLOBAL_PTN_D0_S and ctrl.precache_ptn & GLOBAL_PTN_D1_S:
                current_s_offset = ssequence[i_d0 * n_d1 + i_d1]
            else:
                current_s_offset = 0 if self.s_os is None else self.s_os()

            return current_s_offset

        def get_voffset(i_d0, i_d1):
            if ctrl.precache_ptn & GLOBAL_PTN_D0_V and ctrl.precache_ptn & GLOBAL_PTN_D1_V:
                assert False, "it is meaningless to have both d0/d1 vgpr offset, maybe reconsider algorithm"
            if ctrl.precache_ptn & GLOBAL_PTN_D0_V:
                return self.v_os(i_d0)
            if ctrl.precache_ptn & GLOBAL_PTN_D1_V:
                return self.v_os(i_d1)
            return self.v_os()  # single offset value

        def get_ioffset(i_d0, i_d1):
            if ctrl.precache_ptn & GLOBAL_PTN_D0_K and ctrl.precache_ptn & GLOBAL_PTN_D1_K:
                assert False, "not supported yet. may not need"
            if ctrl.precache_ptn & GLOBAL_PTN_D0_K:
                return 0 if i_d0 == 0 else f'{i_d0} * {self.k_gld_d0_stride()}'
            if ctrl.precache_ptn & GLOBAL_PTN_D1_K:
                return 0 if i_d1 == 0 else f'{i_d1} * {self.k_gld_d1_stride()}'
            else:
                return 0

        def try_exec_flag_start(idx):
            #if ctrl.use_flag and self.v_flag != None:
            if self.v_flag != None:
                self._emit(f"v_cmpx_le_u32 vcc, 1, v[{self.v_flag(idx)}]")

        def try_exec_flag_finish():
            #if ctrl.use_flag and self.v_flag != None:
            if self.v_flag != None:
                self._emit(f"s_mov_b64 exec, -1")

        assert not (ctrl.precache_ptn & GLOBAL_PTN_D0_V and ctrl.precache_ptn & GLOBAL_PTN_D1_V)
        assert not (ctrl.precache_ptn & GLOBAL_PTN_D0_K and ctrl.precache_ptn & GLOBAL_PTN_D1_K)

        exec_slot_d0_up = ctrl.flag_on_d1 and ((ctrl.precache_ptn & GLOBAL_PTN_D1_V) and (ctrl.flag_merge_v and n_d1 == 1)) or \
                                ((ctrl.precache_ptn & GLOBAL_PTN_D0_S or ctrl.precache_ptn & GLOBAL_PTN_D0_K) and \
                                (ctrl.precache_ptn & GLOBAL_PTN_D1_S or ctrl.precache_ptn & GLOBAL_PTN_D1_K) and ctrl.flag_merge_v)
        exec_slot_d0_d1 = ctrl.flag_on_d0
        exec_slot_d1_dw = ctrl.flag_on_d1 and not exec_slot_d0_up

        assert not (exec_slot_d0_up and exec_slot_d0_d1 and exec_slot_d1_dw), "should not happen"

        if ctrl.dst_order == 1:
            assert ctrl.vector_d1 == 1, "currently can't have vector d1 when reorder"

        if ctrl.src_order == 0:
            if exec_slot_d0_up:
                try_exec_flag_start(0)
            i_dst = 0
            for i_d0 in range(ctrl.length_d0):
                if exec_slot_d0_d1:
                    try_exec_flag_start(i_d0)
                for i_d1 in range(n_d1):
                    if exec_slot_d1_dw:
                        try_exec_flag_start(i_d1)
                    # print(f"get_ioffset(i_d0, i_d1):{get_ioffset(i_d0, i_d1)}")
                    dst_idx = i_dst * vgpr_per_vector if ctrl.dst_order == 0 else i_d1 * ctrl.length_d0 + i_d0
                    self._emit(buffer_load_dword(f"{self.v_dst(dst_idx)}", f"{get_voffset(i_d0, i_d1)}", f"{self.s_ptr()}", get_soffset(i_d0, i_d1), get_ioffset(i_d0, i_d1)))
                    i_dst = i_dst + 1
                    if exec_slot_d1_dw:
                        try_exec_flag_finish()
                if exec_slot_d0_d1:
                    try_exec_flag_finish()
            if exec_slot_d0_up:
                try_exec_flag_finish()

        else:
            assert False

    def get_issues(self):
        ctrl = self.ctrl
        n_d1 = ctrl.length_d1 // ctrl.vector_d1
        return  ctrl.length_d0 * n_d1




class macro_igemm_write_4d_strided_t(macro_base_t):
    '''
    TODO: this is always not inline
    '''
    def name(self):
        return '.v_write4d_strided'
    def __init__(self, mc, inline = False):
        macro_base_t.__init__(self, mc, inline)

    def __call__(self, v_src, s_p_dst, v_dst_os, s_dst_diff1d, s_dst_diff2d, s_dst_diff3d, s_dst_diff4d,
                s_dst_os_4, t_dim_1d, t_dim_2d, t_dim_3d, t_dim_4d, vec_1d = 1):
        return '{} {},{},{},{},{},{},{},{},{},{},{},{}'.format(self.name(),
            v_src, s_p_dst, v_dst_os, s_dst_diff1d, s_dst_diff2d, s_dst_diff3d, s_dst_diff4d,
            s_dst_os_4, t_dim_1d, t_dim_2d, t_dim_3d, t_dim_4d, vec_1d)
    def emit(self):
        def emit_write1d_strided():
            self._emit('; write 1d tensor to global with stride')
            with self._emit_macro_indented('.macro .v_write1d_strided v_src, s_p_buf_dst, v_dst_os, s_dst_diff, s_dst_os, t_dim_1d, vec_1d=1'):
                self._emit('.itr_1d = 0')
                self._emit('.if \\t_dim_1d % \\vec_1d != 0')
                self._emit('    .error "\\t_dim_1d can not evenly divided by \\vec_1d"')
                self._emit('    .end')
                self._emit('.endif')
                self._emit('.t_dim_1d_v = \\t_dim_1d / \\vec_1d')
                self._emit('.rept .t_dim_1d_v')
                self._inc_indent()
                self._emit('.if \\vec_1d == 1')
                self._emit('buffer_store_dword v[\\v_src+.itr_1d], v[\\v_dst_os], s[\\s_p_buf_dst:\\s_p_buf_dst+3], s[\\s_dst_os] offen')
                self._emit('.elseif  \\vec_1d == 2')
                self._emit('buffer_store_dwordx2 v[\\v_src+.itr_1d:\\v_src+.itr_1d+1], v[\\v_dst_os], s[\\s_p_buf_dst:\\s_p_buf_dst+3], s[\\s_dst_os] offen')
                self._emit('.elseif \\vec_1d == 4')
                self._emit('buffer_store_dwordx4 v[\\v_src+.itr_1d:\\v_src+.itr_1d+3], v[\\v_dst_os], s[\\s_p_buf_dst:\\s_p_buf_dst+3], s[\\s_dst_os] offen')
                self._emit('.endif')
                self._emit('.if .itr_1d != .t_dim_1d_v - 1')
                self._inc_indent()
                self._emit('s_add_u32 s[\\s_dst_os], s[\\s_dst_os], s[\\s_dst_diff]')
                self._dec_indent()
                self._emit('.endif')
                self._emit('.itr_1d = .itr_1d + \\vec_1d')
                self._dec_indent()
                self._emit('.endr')

        def emit_write2d_strided():
            self._emit('; write 2d tensor to global with stride')
            with self._emit_macro_indented('.macro .v_write2d_strided v_src, s_p_dst, v_dst_os, s_dst_diff1d, s_dst_diff2d, s_dst_os_2, t_dim_1d, t_dim_2d, vec_1d=1'):
                self._emit('.itr_2d = 0')
                self._emit('.rept \\t_dim_2d')
                self._emit('.v_write1d_strided (\\v_src + .itr_2d * \\t_dim_1d), \\s_p_dst, \\v_dst_os, \\s_dst_diff1d, \\s_dst_os_2, \\t_dim_1d')
                self._emit('.if .itr_2d != \\t_dim_2d - 1')
                self._inc_indent()
                self._emit('s_add_u32 s[\\s_dst_os_2+1], s[\\s_dst_os_2+1], s[\\s_dst_diff2d]')
                self._emit('s_mov_b32 s[\\s_dst_os_2], s[\\s_dst_os_2+1]')
                self._dec_indent()
                self._emit('.endif')
                self._emit('.itr_2d = .itr_2d + 1')
                self._emit('.endr')

        def emit_write3d_strided():
            self._emit('; write 3d tensor to global with stride')
            with self._emit_macro_indented('.macro .v_write3d_strided v_src, s_p_dst, v_dst_os, s_dst_diff1d, s_dst_diff2d, s_dst_diff3d, s_dst_os_3, t_dim_1d, t_dim_2d, t_dim_3d, vec_1d=1'):
                self._emit('.itr_3d = 0')
                self._emit('.rept \\t_dim_3d')
                self._emit('.v_write2d_strided (\\v_src+ .itr_3d * \\t_dim_1d * \\t_dim_2d), \\s_p_dst, \\v_dst_os, \\s_dst_diff1d, \\s_dst_diff2d, \\s_dst_os_3, \\t_dim_1d, \\t_dim_2d')
                self._emit('.if .itr_3d != \\t_dim_3d - 1')
                self._inc_indent()
                self._emit('s_add_u32 s[\\s_dst_os_3+2], s[\\s_dst_os_3+2], s[\\s_dst_diff3d]')
                self._emit('s_mov_b32 s[\\s_dst_os_3+1], s[\\s_dst_os_3+2]')
                self._emit('s_mov_b32 s[\\s_dst_os_3], s[\\s_dst_os_3+1]')
                self._dec_indent()
                self._emit('.endif')
                self._emit('.itr_3d = .itr_3d + 1')
                self._emit('.endr')

        def emit_write4d_strided():
            self._emit('; write 4d tensor to global with stride')
            with self._emit_macro_indented('.macro .v_write4d_strided v_src, s_p_dst, v_dst_os, s_dst_diff1d, s_dst_diff2d, s_dst_diff3d, s_dst_diff4d, s_dst_os_4, t_dim_1d, t_dim_2d, t_dim_3d, t_dim_4d, vec_1d=1'):
                self._emit('.itr_4d = 0')
                self._emit('.rept \\t_dim_4d')
                self._emit('.v_write3d_strided (\\v_src+ .itr_4d * \\t_dim_1d * \\t_dim_2d * \\t_dim_3d), \\s_p_dst, \\v_dst_os, \\s_dst_diff1d, \\s_dst_diff2d, \\s_dst_diff3d, \\s_dst_os_4, \\t_dim_1d, \\t_dim_2d, \\t_dim_3d')
                self._emit('.if .itr_4d != \\t_dim_4d - 1')
                self._inc_indent()
                self._emit('s_add_u32 s[\\s_dst_os_4+3], s[\\s_dst_os_4+3], s[\\s_dst_diff4d]')
                self._emit('s_mov_b32 s[\\s_dst_os_4+2], s[\\s_dst_os_4+3]')
                self._emit('s_mov_b32 s[\\s_dst_os_4+1], s[\\s_dst_os_4+2]')
                self._emit('s_mov_b32 s[\\s_dst_os_4], s[\\s_dst_os_4+1]')
                self._dec_indent()
                self._emit('.endif')
                self._emit('.itr_4d = .itr_4d + 1')
                self._emit('.endr')
        
        emit_write1d_strided()
        emit_write2d_strided()
        emit_write3d_strided()
        emit_write4d_strided()

    def get_issues(self):
        # write out is ignored
        return 0
