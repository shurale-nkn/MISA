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
# pylint: disable=maybe-no-member

from re import S
from ..codegen import *
from .utility import *
from .dotx_mapping import *
from .dotx import *

class dotx_core_loop_expr(mc_base_t):
    def __init__(self, mc, name, func=None) -> None:
        mc_base_t.__init__(self, mc)
        self.func = func
        self.name = name
        self.args = ()
        
    def expr_set_args(self, *args):
        self.args = args
        
    def expr_ir(self):
        return self.name
    
    def expr_asm_codes(self):
        if isinstance(self.func, str):
            return self.func
        else:
            return self.func(*self.args)
    
    def emit_expr_asm_codes(self):
        self._emit(self.expr_asm_codes())

class dotx_core_loop_node():
    def __init__(self, name, first=None, second=None) -> None:
        self.name = name
        self.first = first
        self.second = second
        
    def get_first_node(self):
        return self.first
    
    def get_second_node(self):
        return self.second
    
    def set_first_node(self, first):
        self.first = first
        
    def set_second_node(self, second):
        self.second = second
    
def print_ir(node):
    if isinstance(node, dotx_core_loop_expr):
        print(node.expr_ir())
        return
    else:
        print_ir(node.first)
        print_ir(node.second)
        return
      
class dotx_core_loop_for_loop(dotx_core_loop_node):
    def __init__(self, mc, name, loop_var="", loop_begin=None, loop_step=None, loop_end=None, loop_check=None, loop_label=None) -> None:
        super().__init__(name)
        self.loop_var = loop_var
        self.loop_begin = loop_begin
        self.loop_step = loop_step
        self.loop_end = loop_end
        self.loop_check = loop_check
        self.loop_label = loop_label
        self.name = name
        self.mc = mc
        
    def form_loop_jump_check(self):
        if self.second.name != "loop_jump_check":
            assert False, "please provide a loop jump check node"
        
        loop_jump_check_node = self.second
        mc = self.mc
        if self.loop_check == "gt":
            expr = dotx_core_loop_expr(mc, "loop expr", f"s_sub_i32 s[{self.loop_var()}], s[{self.loop_var()}], {self.loop_step}")
            cond = dotx_core_loop_expr(mc, "condition", f"s_cmp_gt_i32 s[{self.loop_var()}], {self.loop_end}")
        else:
            assert False, "not support condition"
            
        jump_branch = dotx_core_loop_expr(mc, "branch", f"s_cbranch_scc1 {self.loop_label}")
        loop_jump_check_node.first = expr
        loop_jump_check_node.second = dotx_core_loop_node("branch jump", cond, jump_branch)
        
    def form_loop_body(self):
        pass
        

class dotx_core_loop_graph():
    def __init__(self, ctrl, mc=None):
        self.ctrl = ctrl
        self.base_node = None
        self.mc = mc
        
    def add_node_comment(self, node, str_comment):
        comment_expr = dotx_core_loop_expr(self.mc, "comments", str_comment)
        new_node = dotx_core_loop_node("with_comments: "+node.name)
        new_node.first = comment_expr
        new_node.second = node
        return new_node
        
    def creat_base_graph(self):
        
        label_fma_body = 'L_{}_fma_body'.format(self.ctrl.label_prefix)
        label_fma_finishing = 'L_{}_fma_finishing'.format(self.ctrl.label_prefix)
        label_fma_end = 'L_{}_end'.format(self.ctrl.label_prefix)
        
        f_gld_a = self.ctrl.global_load_a_functor
        f_gld_b = self.ctrl.global_load_b_functor
        f_sst_a = self.ctrl.shared_store_a_functor
        f_sst_b = self.ctrl.shared_store_b_functor

        f_sld_a = self.ctrl.shared_load_a_functor
        f_sld_b = self.ctrl.shared_load_b_functor

        f_move_slice_window_a = self.ctrl.move_slice_window_a_functor
        f_move_slice_window_b = self.ctrl.move_slice_window_b_functor

        v_a = self.ctrl.v_a
        v_b = self.ctrl.v_b
        v_c = self.ctrl.v_c

        v_gld_a = self.ctrl.v_gld_a
        v_gld_b = self.ctrl.v_gld_b

        v_sst_a_os = self.ctrl.v_sst_a_os
        v_sld_a_os = self.ctrl.v_sld_a_os
        v_sst_b_os = self.ctrl.v_sst_b_os
        v_sld_b_os = self.ctrl.v_sld_b_os

        s_kitr = self.ctrl.s_kitr
        s_knum = self.ctrl.s_knum
        dotx_m = self.ctrl.dotx_m
        
        data_byte = amdgpu_precision_data_byte(amdgpu_string_to_precision(self.ctrl.precision))

        lds_width_m_per_read = data_byte * (dotx_m.macro_tile_m // dotx_m.lanegroup_repeat_m) * self.ctrl.lds_k_pack
        lds_width_n_per_read = data_byte * (dotx_m.macro_tile_n // dotx_m.lanegroup_repeat_n) * self.ctrl.lds_k_pack
        lds_width_m = data_byte * dotx_m.macro_tile_m * self.ctrl.lds_k_pack
        lds_width_n = data_byte * dotx_m.macro_tile_n * self.ctrl.lds_k_pack
        lds_single_size = self.ctrl.lds_single_size
        local_prefetch_num = self.ctrl.local_prefetch_num

        # used as offset:x number. may some 
        lds_base_m = 0
        lds_base_n = 0
        unroll_k = self.ctrl.unroll_k // self.ctrl.lds_k_pack
        k_per_inst = dotx_m.lanegroup_k_per_thread()

        pad_m = self.ctrl.lds_pad_m
        pad_n = self.ctrl.lds_pad_n

        thread_m = dotx_m.lanegroup_repeat_m
        thread_n = dotx_m.lanegroup_repeat_n * 8
        local_buffer_m = self.ctrl.lds_k_pack // dotx_m.inst_dotx.k
        local_buffer_n = self.ctrl.lds_k_pack // dotx_m.inst_dotx.k
        thread_sub_n = local_buffer_n
        thread_sub_m = local_buffer_m
        
        v_dotx_k = macro_dotx_mxnxk_t(self.mc, 1, 1, self.ctrl.lds_k_pack, 1, self.ctrl.precision)
        
        base_node = dotx_core_loop_node("core_loop")
        node_clear_c = dotx_core_loop_expr(self.mc, ".clear_c", f".v_clear_nc {v_c()}, {thread_m * thread_n}")
        
        base_for_loop = dotx_core_loop_for_loop(self.mc, "core_loop", s_kitr, s_knum, unroll_k, 0, "gt", label_fma_body)
        
        loop_begin_check = dotx_core_loop_expr(self.mc, "loop_begin_check")
        loop_body = dotx_core_loop_node("loop_body")
        loop_jump_check = dotx_core_loop_node("loop_jump_check")
        
        base_for_loop.first = dotx_core_loop_node("loop body with label", dotx_core_loop_expr(self.mc, "loop label", label_fma_body+':'), loop_body)
        base_for_loop.second = loop_jump_check
        
        base_for_loop.form_loop_jump_check()
        
        gld_a = dotx_core_loop_expr(self.mc, "gld_a", f_gld_a)
        gld_b = dotx_core_loop_expr(self.mc, "gld_b", f_gld_b)
        sld_a = dotx_core_loop_expr(self.mc, "sld_a", f_sld_a)
        sld_a.expr_set_args(v_a(), v_sld_a_os(), lds_base_m)
        sld_b = dotx_core_loop_expr(self.mc, "sld_b", f_sld_b)
        sld_b.expr_set_args(v_b(), v_sld_b_os(), lds_base_n)
        sst_a = dotx_core_loop_node("sst a node", 
                                    dotx_core_loop_expr(self.mc, "wait a global load", f"s_waitcnt vmcnt({f_gld_b.get_issues()})"), 
                                    dotx_core_loop_expr(self.mc, "sst_a", f_sst_a))
        sst_b = dotx_core_loop_node("sst b node", 
                                    dotx_core_loop_expr(self.mc, "wait b global load", f"s_waitcnt vmcnt(0)"), 
                                    dotx_core_loop_expr(self.mc, "sst_b", f_sst_b))
        
        dotx = dotx_core_loop_expr(self.mc, "dotx", v_dotx_k)
        dotx.expr_set_args(v_c(), v_a(), v_b())
        
        
        base_node.first = node_clear_c
        node_before_loop = dotx_core_loop_node("node before core loop", sst_a, sst_b)
        base_node.second = dotx_core_loop_node("node core loop", node_before_loop, base_for_loop)
        
        loop_body.first = gld_a
        loop_body.second = dotx_core_loop_node("body0")
        loop_body.second.first = gld_b
        loop_body.second.second = dotx_core_loop_node("body1")
        loop_body.second.second.first = sst_a
        loop_body.second.second.second = dotx_core_loop_node("body2")
        loop_body.second.second.second.first = sst_b
        loop_body.second.second.second.second = dotx_core_loop_node("body3")
        loop_body.second.second.second.second.first = sld_a
        loop_body.second.second.second.second.second = dotx_core_loop_node("body4")
        loop_body.second.second.second.second.second.first = sld_b
        loop_body.second.second.second.second.second.second = dotx
        
        base_node = self.add_node_comment(base_node, f"; start FMA loop, {thread_m}x{thread_n}")
        
        self.base_node = base_node
         
if __name__ == "__main__":
    asm_target = os.path.join('out', 'core_loop_test.s')
    emitter = mc_emit_to_file_t(asm_target)
    arch = amdgpu_arch_config_t({
        'arch'          :   'gfx1030',
        'data_type'     :   AMDGPU_PRECISION_FP32,
        'code_object'   :   'cov3'})

    # create mc
    mc = mc_asm_printer_t(emitter, arch)
    mc_set_current(mc)
    
    core_loop_graph = dotx_core_loop_graph(mc, None)
    core_loop_graph.creat_base_graph()
    print_ir(core_loop_graph.base_node)
    
        