# wsolver

document: [http://www.fangchengzu.com/document](http://www.fangchengzu.com/document)

### 求解超越方程组（Solve the system of transcendental equations）

```text
from wsolver import *

es = EquationSystem()

# Add variable
es.add_variable('x', -100, 100)
es.add_variable('y', -100, 100)

# Add equation
es.add_equation('x^2 + sin(y) = 1')
es.add_equation('x = ln(y)')

# transform equations
es.transform()

# solve
sr = solve(es, 1000, 1E-7, 1E-12)

if len(sr.get_fuzzy_roots()) > 0:
    print('A system of equations may have an infinite number of real roots. ')
else:
    roots = sr.get_clear_roots()
    for i in range(0, len(roots)):
        print('x=' + str(round(roots[i][0], 6)) + ' ' + 'y=' + str(round(roots[i][1], 6)))
```

**Result**

```text
x=0.224597 y=1.251818
x=-0.733499 y=0.480226
```

* * *

### 求解对数值法不友好的高次方程组（Solve the system of high-degree equations）

```text
from wsolver import *

es = EquationSystem()

# Add variable
es.add_variable('x', -100, 100)

# Add equation
es.add_equation('(x-1)*(x-2)*(x-3)*(x-4)*(x-5)=0')

# transform equations
es.transform()

# solve
sr = solve(es, 1000, 1E-7, 1E-12)

if len(sr.get_fuzzy_roots()) > 0:
    print('A system of equations may have an infinite number of real roots. ')
else:
    roots = sr.get_clear_roots()
    for i in range(0, len(roots)):
        print('x=' + str(round(roots[i][0], 6)))
```

**Result**

```text
x=4.0
x=3.0
x=2.0
x=1.0
x=5.0
```

* * *

### 求解变量数和方程数不一致的方程组（Solve a system of equations where the number of variables does not match the number of equations）

```text
from wsolver import *

es = EquationSystem()

# Add variable
es.add_variable('x', -100, 100)
es.add_variable('y', -100, 100)

# Add equation
es.add_equation('(x-1)^2+(y-2)^2*(y-3)^2=0')

# transform equations
es.transform()

# solve
sr = solve(es, 1000, 1E-8, 1E-14)

if len(sr.get_fuzzy_roots()) > 0:
    print('A system of equations may have an infinite number of real roots. ')
else:
    roots = sr.get_clear_roots()
    for i in range(0, len(roots)):
        print('x=' + str(round(roots[i][0], 6)) + ' ' + 'y=' + str(round(roots[i][1], 6)))
```

**Result**

```text
x=1.0 y=3.0
x=1.0 y=2.0
```

* * *

### 和sympy的效率对比（Efficiency comparison with SymPy）

```text
from wsolver import *
import sympy
import time

x = sympy.Symbol('x')
y = sympy.Symbol('y')

eq1 = x**2 / 2 + y**2 - 1
eq2 = x**2 + y**2 / 2 - 1

start_time = time.perf_counter()
for i in range(0, 1000):
    sympy.solve([eq1, eq2])
end_time = time.perf_counter()
print('sympy: ' + str(end_time - start_time))

#########################

es = EquationSystem()

# Add variable
es.add_variable('x', -100, 100)
es.add_variable('y', -100, 100)

# Add equation
es.add_equation('x^2 / 2 + y^2 - 1 = 0')
es.add_equation('x^2 + y^2 / 2 - 1 = 0')

# transform equations
es.transform()

# solve
start_time = time.perf_counter()
for i in range(0, 1000):
    solve(es, 1000, 1E-7, 1E-12)
end_time = time.perf_counter()
print('wsolver: ' + str(end_time - start_time))
```

**Result**

```text
sympy: 2.632635699934326
wsolver: 0.1961184999672696
```
