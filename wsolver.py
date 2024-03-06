from ctypes import *

# document: http://www.fangchengzu.com/document

solver_lib = cdll.LoadLibrary('lib/x64/solver.dll')

solver_lib.NewEquationSystem.argtypes = []
solver_lib.NewEquationSystem.restype = c_void_p

solver_lib.FreeEquationSystem.argtypes = [c_void_p]
solver_lib.FreeEquationSystem.restype = None

solver_lib.AddVariable.argtypes = [c_void_p, c_char_p, c_double, c_double]
solver_lib.AddVariable.restype = c_bool

solver_lib.AddEquation.argtypes = [c_void_p, c_char_p, c_char_p]
solver_lib.AddEquation.restype = c_bool

solver_lib.TransformEquationSystem.argtypes = [c_void_p]
solver_lib.TransformEquationSystem.restype = None

solver_lib.SolveEquationSystem.argtypes = [c_void_p, c_int, c_double, c_double]
solver_lib.SolveEquationSystem.restype = c_void_p

solver_lib.FreeSolverResult.argtypes = [c_void_p]
solver_lib.FreeSolverResult.restype = None

solver_lib.GetClearRootCount.argtypes = [c_void_p]
solver_lib.GetClearRootCount.restype = c_int

solver_lib.GetClearRoots.argtypes = [c_void_p, c_void_p, c_int]
solver_lib.GetClearRoots.restype = None

solver_lib.GetFuzzyRootCount.argtypes = [c_void_p]
solver_lib.GetFuzzyRootCount.restype = c_int

solver_lib.GetFuzzyRoots.argtypes = [c_void_p, c_void_p, c_int]
solver_lib.GetFuzzyRoots.restype = None

solver_lib.GetLastErrorCode.argtypes = []
solver_lib.GetLastErrorCode.restype = c_int


class EquationSystem:
    def __init__(self):
        self.lib = solver_lib
        self.handle = self.lib.NewEquationSystem()
        self.variable_count = 0

    def __del__(self):
        if self.handle is not None:
            self.lib.FreeEquationSystem(self.handle)

    def add_variable(self, name, lower, upper):
        p_name = create_string_buffer(name.encode('utf-8'))
        if not self.lib.AddVariable(self.handle, p_name, lower, upper):
            print('Error code: ' + str(self.lib.GetLastErrorCode()))
            raise
        self.variable_count += 1

    def add_equation(self, expression):
        expressions = expression.split('=')
        if len(expressions) == 2:
            left = create_string_buffer(expressions[0].encode('utf-8'))
            right = create_string_buffer(expressions[1].encode('utf-8'))
        else:
            left = create_string_buffer(expression.encode('utf-8'))
            right = create_string_buffer(b'')
        if not self.lib.AddEquation(self.handle, left, right):
            print('Error code: ' + str(self.lib.GetLastErrorCode()))
            raise

    def transform(self):
        self.lib.TransformEquationSystem(self.handle)


class SolverResult:
    def __init__(self, variable_count, handle):
        self.lib = solver_lib
        self.variable_count = variable_count
        self.handle = handle

    def __del__(self):
        if self.handle is not None:
            self.lib.FreeSolverResult(self.handle)

    def get_clear_roots(self):
        root_count = self.lib.GetClearRootCount(self.handle)
        c_root = (c_double * (root_count * self.variable_count))()
        self.lib.GetClearRoots(self.handle, c_root, root_count)
        root = []
        k = 0
        for i in range(0, root_count):
            ri = []
            for j in range(0, self.variable_count):
                ri.append(c_root[k])
                k += 1
            root.append(ri)
        return root

    def get_fuzzy_roots(self):
        root_count = self.lib.GetFuzzyRootCount(self.handle)
        c_root = (c_double * (root_count * self.variable_count * 2))()
        self.lib.GetFuzzyRoots(self.handle, c_root, root_count)
        root = []
        k = 0
        for i in range(0, root_count):
            ri = []
            for j in range(0, self.variable_count):
                v = [c_root[k], c_root[k + 1]]
                ri.append(v)
                k += 2
            root.append(ri)
        return root


def solve(equation_system: EquationSystem, max_fuzzy_count, variable_epsilon, equation_epsilon) -> SolverResult:
    result_handle = solver_lib.SolveEquationSystem(
        equation_system.handle, max_fuzzy_count, variable_epsilon, equation_epsilon)
    return SolverResult(equation_system.variable_count, result_handle)

