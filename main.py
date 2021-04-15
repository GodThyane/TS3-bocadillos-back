import numpy as np
from scipy.stats import norm
import generateRandom as gr


def simulation2(n, mu, sigma, nMax, min):
    at = min + (nMax - min) * np.array(gr.congruenciaLineal(n))
    st = norm.ppf(np.array(gr.congruenciaLineal(n)), loc=mu, scale=sigma)
    aat = []
    wt = []
    et = []
    ft = []
    for x in range(n):
        if x == 0:
            aat.append(at[0])
            wt.append(0)
            ft.append(0)
            et.append(at[0] + st[0])
        else:
            aat.append(aat[x - 1] + at[x])
            wt.append(max(aat[x], et[x - 1]) - aat[x])
            ft.append(max(aat[x], et[x - 1]) - et[x - 1])
            et.append(aat[x] + st[x] + wt[x])

    sft = abs(np.array(aat) - np.array(et))
    l = []
    for x in range(n):
        l.append(sum(i <= et[x] for i in aat[x + 1:n]))

    return np.array([at, aat, wt, ft, st, et, sft, l]).T


myq = simulation2(20, 90, 30, 60, 30)
l = myq[:, 7]
print(l)


def simulation(n, lam, mu):
    at = []
    randomsRiA = np.array(gr.congruenciaLineal(n))
    iat = abs(np.log(1 - randomsRiA) / lam)
    start = []
    randomsRiS = np.array(gr.congruenciaLineal(n))
    et = abs(np.log(1 - randomsRiS) / mu)
    ext = []
    for x in range(n):
        if x == 0:
            at.append(0)
            start.append(0)
            ext.append(et[0] + start[0])
        else:
            at.append(at[x - 1] + iat[x - 1])
            start.append(max(at[x], ext[x - 1]))
            ext.append(et[x] + start[x])

    wt = np.array(start) - np.array(at)
    w = np.array(start) == np.array(at)
    l = []
    for x in range(n):
        l.append(sum(i <= ext[x] for i in at[x + 1:n]))

    queue = np.array([at, randomsRiA, iat, start, randomsRiS, et, ext, l, w, wt])

    return queue.T


def station_1():
    print("Estación 1")


def station_2():
    print("Estación 2")


def station_3():
    print("Estación 3")


def station_4():
    print("Estación 4")


def station_5():
    print("Estación 5")
