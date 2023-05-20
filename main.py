import random
from math import log
import time,timeit

class LGC:
    def __init__(self, x_n):
        self.x_n = x_n
    def lgc_rand(self):
        a = 1685
        c = 8263
        m = 2 ** 32
        self.x_n = (a * self.x_n + c) % m
        return self.x_n / m

class Middle:
    def __init__(self):
        self.r0 = int(time.time()) % 10_000
        self.r1 = int(time.time()) % 10_000
        self.b = 17

    def middle_products(self):
        r = (self.r0 * self.r1 * self.b) % 10_000
        self.r0 = self.r1
        self.r1 = r
        self.r0 += 13
        self.r1 += 11
        self.b += 7
        return float('0.' + str(r))

sizes = [100, 500, 1000, 2500, 5000, 10000, 50000, 80000, 200000, 500000]
time_middle, time_LGC, time_standard = [], [], []
samples_middle = {}
samples_LGC = {}

for i in sizes:
    first = Middle()
    samples_middle[i] = []
    for _ in range(i):
        samples_middle[i].append(first.middle_products())

#print(samples_middle)
print("Middle")
print("Cреднее, отклонение и коэффициент вариации:")
char_middle = {}

for i in sizes:
    char_middle[i] = [sum(samples_middle[i]) / i] #среднее
    tmp = 0
    for j in range(i):
        tmp += (samples_middle[i][j] - char_middle[i][0]) ** 2
    tmp /= i
    char_middle[i].append(tmp ** (1 / 2)) #отклонение
    char_middle[i].append(100 * char_middle[i][1] / char_middle[i][0]) #коэффициент вариации
    print(f'size = {i}, {char_middle[i]}')

for i in sizes:
    if char_middle[i][2] > 33:
        print(f'Выборка объёмом {i} не является однородной')
    else:
        print(f'Выборка объёмом {i} является однородной')

Xi_theor = {}
Xi_theor[7] = [2.2, 10.6]
Xi_theor[9] = [3.5, 13.4]
Xi_theor[10] = [4.2, 14.7]
Xi_theor[12] = [5.6, 17.3]
Xi_theor[13] = [6.3, 18.5]
Xi_theor[14] = [7.0, 19.8]
Xi_theor[16] = [8.5, 22.3]
Xi_theor[17] = [9.3, 23.5]
Xi_theor[18] = [10.1, 24.8]
Xi_theor[19] = [10.9, 26.0]

Xi_middle = {}
for i in sizes:
    intervals = int(1 + 3.322 * log(i, 10))
    Xi_middle[intervals] = 0
    p = 1 / intervals
    intervals_el = []
    position = 0
    for _ in range(intervals):
        tmp = 0
        for el in samples_middle[i]:
            if position <= el <= (position + p):
                tmp += 1
        intervals_el.append(tmp)
        position += p
    for j in intervals_el:
        Xi_middle[intervals] += j**2 / p
    Xi_middle[intervals] /= i
    Xi_middle[intervals] -= i
    print(f'intervals = {intervals}, size = {i}, Xi_middle = {Xi_middle[intervals]}')
    if Xi_theor[intervals][0] <= Xi_middle[intervals] <= Xi_theor[intervals][1]:
        print('Гипотеза о случайности равномерного генератора выполняется')
    else:
        print('Гипотеза о случайности равномерного генератора не выполняется')





for i in sizes:
    first = LGC(int(str(random.random())[2:]))
    samples_LGC[i] = []
    for _ in range(i):
        samples_LGC[i].append(first.lgc_rand())

#print(samples_LGC)
print("LGC")
print("Cреднее, отклонение и коэффициент вариации:")
char_LGC = {}

for i in sizes:
    char_LGC[i] = [sum(samples_LGC[i]) / i]
    temp = 0
    for j in range(i):
        temp += (samples_LGC[i][j] - char_LGC[i][0]) ** 2
    temp /= i
    char_LGC[i].append(temp ** (1 / 2))
    char_LGC[i].append(100 * char_LGC[i][1] / char_LGC[i][0])
    print(f'size = {i}, {char_LGC[i]}')

for i in sizes:
    if char_LGC[i][2] > 33:
        print(f'Выборка объёмом {i} не является однородной')
    else:
        print(f'Выборка объёмом {i} является однородной')

Xi_LGC = {}
for i in sizes:
    intervals = int(1 + 3.322 * log(i, 10))
    Xi_LGC[intervals] = 0
    p = 1 / intervals
    intervals_el = []
    position = 0
    for _ in range(intervals):
        tmp = 0
        for el in samples_LGC[i]:
            if position <= el <= (position + p):
                tmp += 1
        intervals_el.append(tmp)
        position += p
    for j in intervals_el:
        Xi_LGC[intervals] += j**2 / p
    Xi_LGC[intervals] /= i
    Xi_LGC[intervals] -= i
    print(f'intervals = {intervals}, size = {i}, Xi_LGC = {Xi_LGC[intervals]}')
    if Xi_theor[intervals][0] <= Xi_LGC[intervals] <= Xi_theor[intervals][1]:
        print('Гипотеза о случайности равномерного генератора выполняется')
    else:
        print('Гипотеза о случайности равномерного генератора не выполняется')

# for i in [1000, 10000, 50000, 100000, 250000, 500000, 1000000]:
#     starttime = timeit.default_timer()
#     first = Middle()
#     for _ in range(i):
#         print(first.middle_products())
#     end = timeit.default_timer() - starttime
#     time_middle.append(end)
# print(time_middle)
#[0.009223399974871427, 0.11045229999581352, 0.4959580000140704, 1.0644196000066586, 2.5630081999697722, 5.19092379999347, 10.215828599990346]

# for i in [1000, 10000, 50000, 100000, 250000, 500000, 1000000]:
#     starttime = timeit.default_timer()
#     first = LGC(int(str(random.random())[2:]))
#     for _ in range(i):
#         print(first.lgc_rand())
#     end = timeit.default_timer() - starttime
#     time_LGC.append(end)
# print(time_LGC)
#[0.013452799990773201, 0.13707180001074448, 0.7825376999680884, 1.0878946000011638, 2.4748314999742433, 5.026430999976583, 10.040267299977131]


# for i in [1000, 10000, 50000, 100000, 250000, 500000, 1000000]:
#     starttime = timeit.default_timer()
#     for _ in range(i):
#         print(random.random())
#     end = timeit.default_timer() - starttime
#     time_standard.append(end)
# print(time_standard)
#[0.014810800028499216, 0.11393560003489256, 0.4374256000155583, 0.909968200023286, 2.3429057000321336, 4.706860799982678, 8.98348369996529]

