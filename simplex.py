import math

def Func(point):
    return point[0] ** 2 + point[0] * point[1] + point[1] ** 2 - 3 * point[0] - 6 * point[1]


#уменьшение в 2 раза растояния от каждой точки до наилучшей точки
def ChangeDistancePoint(x, fmin_index, n):
    x_fmin = x[fmin_index]

    for i in range(n):
        if i != fmin_index:
            x[i] = [
                math.fabs(x[i][0] + x_fmin[0]) / 2,
                math.fabs(x[i][1] + x_fmin[1]) / 2
            ]

    return x


#растяжение / сжатие (в зависимости от coef)
def TensileCompress(coef, point, tc):
    return [
        coef * point[0] + (1 - coef) * tc[0],
        coef * point[1] + (1 - coef) * tc[1]
    ]

###
# tensile_coef - коэффициент растяжения
# compress_coef - коэффициент сжатия
###

def Simplex(err, tensile_coef, compress_coef):
    n = 2
    pn = (math.sqrt(n + 1) + n - 1) / (n * math.sqrt(2))
    gn = (math.sqrt(n + 1) - 1) / (n * math.sqrt(2))
    res = None
    
    x = [
        [0, 0],
        [pn, gn],
        [gn, pn]
    ]

    while True:
        #значения функций в точках 'х'
        f_x = [Func(x[0]), Func(x[1]), Func(x[2])]

        #индексы наихудшей и наилучшей точек в массиве 'х'
        fmax_index = f_x.index(max(f_x))
        fmin_index = f_x.index(min(f_x))

        #центр тяжести
        tc = [
            (sum([x[0][0], x[1][0], x[2][0]]) - x[fmax_index][0]) / n,
            (sum([x[0][1], x[1][1], x[2][1]]) - x[fmax_index][1]) / n
        ]

        #отражение
        to = [
            tc[0] + (tc[0] - x[fmax_index][0]),
            tc[1] + (tc[1] - x[fmax_index][1])
        ]

        f_to = Func(to)
        
        #растяжение
        if f_to < f_x[fmin_index]:
            tr = TensileCompress(tensile_coef, to, tc)

            if Func(tr) < f_x[fmin_index]:
                x[fmax_index] = tr
            elif Func(tr) > f_x[fmin_index]:
                x[fmax_index] = to
        #сжатие
        else:
            if f_to > f_x[fmax_index]:
                xc = TensileCompress(compress_coef, x[fmax_index], tc)
            elif f_to < f_x[fmax_index]:
                xc = TensileCompress(compress_coef, to, tc)

            if Func(xc) < f_x[fmax_index]:
                x[fmax_index] = xc
            elif Func(xc) > f_x[fmax_index]:
                # уменьшение размерности симплекса
                x = ChangeDistancePoint(x, fmin_index, n)

        #рассчет отклонения
        f_sum_midl = sum(f_x) / (n + 1)
        tmp = 0

        for i in range(n):
            tmp += (f_x[i] - f_sum_midl) ** 2

        new_err = math.sqrt(tmp / (n + 1))

        if new_err <= err:
            res = x[fmin_index]
            break
        
    #'res' - наилучшая точка, 'f' - значение ф-ии в этой точке
    return {'point': res, 'f': Func(res)}