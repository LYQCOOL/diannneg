# _*_ encoding:utf-8 _*_
import copy
import json
def datas(da):
    Iab = [[[0.0, 1.2], [1.2, 3.0], [3.0, 4.5], [4.5, 7.0], [7.0, 10.0]],
           [[0.0, 0.05], [0.05, 0.1], [0.1, 0.15], [0.15, 0.2], [0.2, 0.4]],
           [[0.0, 1.0], [1.0, 2.0], [2.0, 3.0], [3.0, 5.0], [5.0, 8.0]],
           [[0.0, 0.5], [0.5, 1.0], [1.0, 1.5], [1.5, 2.0], [2.0, 4.0]],
           [[0.0, 0.2], [0.2, 0.5], [0.5, 0.8], [0.8, 1.0], [1.0, 2.0]],
           [[1.0, 0.9], [0.9, 0.8], [0.8, 0.5], [0.5, 0.1], [0.1, 0.0]],
           [[0.0, 0.5], [0.5, 1.0], [1.0, 1.5], [1.5, 2.0], [2.0, 4.0]]
           ]
    Icd = copy.deepcopy(Iab)
    for i in range(7):
        for j in range(5):
            if j == 0:
                Icd[i][j] = [Iab[i][j][0], Iab[i][j + 1][1]]

            if j == 4:
                Icd[i][j] = [Iab[i][j - 1][0], Iab[i][j][1]]
            else:
                Icd[i][j] = [Iab[i][j - 1][0], Iab[i][j + 1][1]]

    M = copy.deepcopy(Iab)
    for i in range(7):
        for j in range(5):
            M[i][j] = (float((4 - j)) / 4.0) * (Iab[i][j][0]) + float(j / 4.0) * (Iab[i][j][1])

    U = [[], [], [], [], [], [], []]
    for i in da:
        for j in i:
            for t in range(5):
                if j > M[da.index(i)][t]:
                    if j >= t and j <= Iab[da.index(i)][t][1]:
                        new_da = 0.5 * (1.0 + ((j - Iab[da.index(i)][t][1]) / (t - Iab[da.index(i)][t][1])))
                        U[da.index(i)].append(new_da)
                    elif j > Iab[da.index(i)][t][1] and j <= Icd[da.index(i)][t][1]:
                        new_da = 0.5 * (
                        1.0 + ((j - Iab[da.index(i)][t][1]) / (Icd[da.index(i)][t][1] - Iab[da.index(i)][t][1])))
                        U[da.index(i)].append(new_da)
                    else:
                        U[da.index(i)].append(0.0)
                elif j < t:
                    if j >= Icd[da.index(i)][t][0] and j <= Iab[da.index(i)][t][0]:
                        new_da = 0.5 * (
                        1.0 - ((j - Iab[da.index(i)][t][0]) / (Icd[da.index(i)][t][0] - Iab[da.index(i)][t][0])))
                        U[da.index(i)].append(new_da)
                    elif j > Iab[da.index(i)][t][0] and j <= t:
                        new_da = 0.5 * (1.0 + ((j - Iab[da.index(i)][t][0]) / (t - Iab[da.index(i)][t][0])))
                        U[da.index(i)].append(new_da)
                    else:
                        U[da.index(i)].append(0.0)
                else:
                    U[da.index(i)].append(0.0)
    Max_Min = [[[], []], [[], []], [[], []], [[], []], [[], []], [[], []], [[], []]]
    for row in U:
        for t in range(len(row) / 7):
            Max_Min[U.index(row)][0].append(max(row[t * 5:(t + 1) * 5]))
            Max_Min[U.index(row)][1].append(min(row[t * 5:(t + 1) * 5]))
    w = [0.2058, 0.2650, 0.1008, 0.1605, 0.1214, 0.0806, 0.0659]
    Uh = []
    for row in Max_Min:
        data = []
        for j in range(0, 2):
            fenzi = 0.0
            fenmu = 0.0
            for t in w[0:5]:
                fenzi += t * (1 - row[j][w.index(t)])
                fenmu += t * row[j][w.index(t)]
            if fenmu != 0:
                res = (fenzi / fenmu) * (fenzi / fenmu)
            else:
                res = 0
            res = 1.0 / (res + 1.0)
            data.append(res)
        Uh.append(data)
    final_datas = []
    sums1 = 0
    sums2 = 0
    for i in range(5):
        sums1 += Uh[i][0]
        sums2 += Uh[i][1]
    datass1 = []
    datass2 = []
    all_datas = []
    for i in range(5):
        d1 = Uh[i][0] / sums1
        d2 = Uh[i][1] / sums2
        datass1.append(d1)
        datass2.append(d2)
    all_datas.append(datass1)
    all_datas.append(datass2)
    all2=0
    all1=0
    for t in range(5):
        all1 += (t + 1.0) * all_datas[0][t]
        all2+=(t+1.0)*all_datas[1][t]
    final_final_data=[]
    final_final_data.append(all1)
    final_final_data.append(all2)
    return final_final_data
if __name__=="__main__":
    da = [[6.0725, 8.6904, 8.8429, 1.6120, 7.8636, 0.3052, 0.00087],
          [0.0936, 0.1726, 0.0623, 0.0651, 0.3296, 0.1021, 0.2688],
          [3.3885, 7.2506, 4.7665, 0.7146, 1.1275, 5.9302, 0.3445],
          [2.8638, 1.0477, 2.1796, 2.8776, 0.2461, 2.0523, 1.7453],
          [0.6820, 0.5829, 1.3072, 1.3902, 0.8619, 1.4019, 1.9388],
          [0.3770, 0.0913, 0.5910, 0.6610, 0.9862, 0.5254, 0.5813],
          [2.4642, 2.3313, 2.7101, 0.3368, 3.3849, 1.2981, 1.9800]]
    print datas(da)