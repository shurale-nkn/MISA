################################################################################
# 
#  MIT License
# 
#  Copyright (c) 2022 Advanced Micro Devices, Inc.
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
import string

from .hsa_rt import hsa_runtime
from .pal_rt import pal_runtime
from runtime import base_runtime_class

__runtime_extension_available = False
try:
    __import__('imp').find_module('extension.runtime_ext')
    __extension_available = True
    #import extension.lang
except ImportError:
    pass


def get_runtime(name:string, **args) -> base_runtime_class:
    if (name == 'hsa'):
        return hsa_runtime
    elif(name == 'pal'):
        return pal_runtime
    elif(__extension_available):
        from extension import runtime_ext
        ret = runtime_ext.get_runtime(name, **args)
        if (ret != None):
            return  ret
