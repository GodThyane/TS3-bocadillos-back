import numpy as np
from scipy.stats import norm
import generateRandom as gr


class Queue_Guava:
    def __init__(self, muState1, muState2, muState3, muState4, muState42, sigma, muState5):
        self.stack = []
        self.productionTime = 480  # min
        self.dangerGuava = 0
        self.stackStation1 = []
        self.matrixStation1 = []
        self.matrixStationWait1 = []
        self.stackStation2 = []
        self.matrixStation2 = []
        self.matrixStationWait2 = []
        self.stackStation3 = []
        self.matrixStation3 = []
        self.matrixStationWait3 = []
        self.stackStation4 = []
        self.matrixStationWait4 = []
        self.stackStation42 = []
        self.matrixStationWait42 = []
        self.matrixStation4 = []
        self.stackStation5 = []
        self.matrixStation5 = []
        self.matrixStationWait5 = []
        self.randomsStation1 = norm.ppf(np.array(gr.congruenciaLineal(100000)), loc=muState1)
        self.randomsStation2 = norm.ppf(np.array(gr.congruenciaLineal(100000)), loc=muState2)
        self.randomsStation3 = norm.ppf(np.array(gr.congruenciaLineal(100000)), loc=muState3)
        self.randomsStation4 = norm.ppf(np.array(gr.congruenciaLineal(100000)), loc=muState4)
        self.randomsStation42 = norm.ppf(np.array(gr.congruenciaLineal(100000)), loc=muState42, scale=sigma)
        self.randomsStation5 = norm.ppf(np.array(gr.congruenciaLineal(100000)), loc=muState5)
        self.indexR1 = 0
        self.indexR2 = 0
        self.indexR3 = 0
        self.indexR4 = 0
        self.indexR42 = 0
        self.indexR5 = 0
        self.day = 1
        self.nBocadillosFinish = 0
        self.nGuavasUsed = 0

    def simulationInit(self):
        print("Stock en bodega: ", len(self.stack))
        for x in range(14):
            self.stack.append(0)
        print("Han llegado 14 guayabas")
        print("Stock en bodega: ", len(self.stack))

    def station_1(self):
        lastGuava = None
        stack = []
        i = 0
        danger = 0
        while len(self.stack) != 0:
            actualGuava = self.stack[0]

            if actualGuava < 24:
                if i == 0:
                    lastGuava = Station1_Guava(0, 0, self.randomsStation1[self.indexR1], self.day)
                else:
                    lastGuava = Station1_Guava(0, lastGuava.exit, self.randomsStation1[self.indexR1], self.day)
                if lastGuava.exit >= self.productionTime:
                    listStack = np.array(self.stack) + 24
                    self.stack = listStack.tolist()
                    break
                self.nGuavasUsed += 1
                self.stackStation1.append(lastGuava)
                stack.append(lastGuava)
                self.indexR1 += 1
                i += 1
                self.stack.pop(0)
            else:
                danger += 1
                self.stack.pop(0)
        print("Longitud ", len(self.stack))
        print("Se botaron " + str(danger) + " guayabas.")
        self.dangerGuava += danger
        return stack

    def station_2(self):
        lastGuava = None
        stack = []
        i = 0
        while len(self.stackStation1) != 0:
            station1H = self.stackStation1[0]
            if station1H.day == self.day:
                if i == 0:
                    lastGuava = Station1_Guava(station1H.exit, station1H.exit, self.randomsStation2[self.indexR2],
                                               self.day)
                else:
                    lastGuava = Station1_Guava(station1H.exit, lastGuava.exit, self.randomsStation2[self.indexR2],
                                               self.day)
            else:
                if i == 0:
                    lastGuava = Station1_Guava(0, 0, self.randomsStation2[self.indexR2], station1H.day)
                else:
                    lastGuava = Station1_Guava(0, lastGuava.exit, self.randomsStation2[self.indexR2], station1H.day)
            if lastGuava.exit >= self.productionTime:
                break
            else:
                self.stackStation1.pop(0)
            self.stackStation2.append(lastGuava)
            stack.append(lastGuava)
            self.indexR2 += 1
            i += 1

        return stack

    def station_3(self):
        lastGuava = None
        stack = []
        i = 0
        while len(self.stackStation2) != 0:
            station2H = self.stackStation2[0]
            if station2H.day == self.day:
                if i == 0:
                    lastGuava = Station1_Guava(station2H.exit, station2H.exit, self.randomsStation3[self.indexR3],
                                               self.day)
                else:
                    lastGuava = Station1_Guava(station2H.exit, lastGuava.exit, self.randomsStation3[self.indexR3],
                                               self.day)
            else:
                if i == 0:
                    lastGuava = Station1_Guava(0, 0, self.randomsStation3[self.indexR3], station2H.day)
                else:
                    lastGuava = Station1_Guava(0, lastGuava.exit, self.randomsStation3[self.indexR3], station2H.day)
            if lastGuava.exit >= self.productionTime:
                break
            else:
                self.stackStation2.pop(0)
            lastGuava.dayMold = self.day
            self.stackStation3.append(lastGuava)
            stack.append(lastGuava)
            self.indexR3 += 1
            i += 1
        return stack

    def station_4(self):
        lastGuava = None
        stack = []
        i = 0

        while len(self.stackStation4) != 0:
            station4H = self.stackStation4[0]
            if self.day - station4H.dayCut >= 1:
                if i == 0:
                    lastGuava = Station1_Guava(0, 0, self.randomsStation42[self.indexR5], station4H.day)
                else:
                    lastGuava = Station1_Guava(0, lastGuava.exit, self.randomsStation42[self.indexR5], station4H.day)
            else:
                break
            if lastGuava.exit >= self.productionTime:
                break
            else:
                self.stackStation4.pop(0)
            lastGuava.dayMold = station4H.dayMold
            lastGuava.dayCut = station4H.dayCut
            lastGuava.dayFinishCut = self.day
            self.stackStation42.append(lastGuava)
            stack.append(lastGuava)
            self.indexR42 += 1
            i += 1

        self.printStation("42", stack)
        self.matrixStationWait42.append(self.stackStation4.copy())
        stack = []

        while len(self.stackStation3) != 0:
            station3H = self.stackStation3[0]
            if self.day - station3H.dayMold >= 2:
                if i == 0:
                    lastGuava = Station1_Guava(0, 0, self.randomsStation4[self.indexR4], station3H.day)
                else:
                    lastGuava = Station1_Guava(0, lastGuava.exit, self.randomsStation4[self.indexR4], station3H.day)
            else:
                break
            if lastGuava.exit >= self.productionTime:
                break
            else:
                self.stackStation3.pop(0)
            lastGuava.dayMold = station3H.dayMold
            lastGuava.dayCut = self.day
            self.stackStation4.append(lastGuava)
            stack.append(lastGuava)
            self.indexR4 += 1
            i += 1

        return stack

    def station_5(self):
        lastGuava = None
        stack = []
        i = 0
        while len(self.stackStation42) != 0:
            station5h = self.stackStation42[0]
            if station5h.dayFinishCut == self.day:
                if i == 0:
                    lastGuava = Station1_Guava(station5h.exit, station5h.exit, self.randomsStation5[self.indexR5],
                                               station5h.day)
                else:
                    lastGuava = Station1_Guava(station5h.exit, station5h.exit, self.randomsStation5[self.indexR5],
                                               station5h.day)
            else:
                if i == 0:
                    lastGuava = Station1_Guava(0, 0, self.randomsStation5[self.indexR5], station5h.day)
                else:
                    lastGuava = Station1_Guava(0, lastGuava.exit, self.randomsStation5[self.indexR5], station5h.day)
            if lastGuava.exit >= self.productionTime:
                break
            else:
                self.stackStation42.pop(0)
            self.stackStation5.append(lastGuava)
            lastGuava.dayMold = station5h.dayMold
            lastGuava.dayCut = station5h.dayCut
            lastGuava.dayFinishCut = station5h.dayFinishCut
            stack.append(lastGuava)
            self.indexR5 += 1
            i += 1

        return stack

    def printStation(self, nStation, stack):
        print("Estación " + nStation + "; día: ", self.day)
        for x in stack:
            print(x)

    def start(self, days):
        for x in range(days):
            self.day = x
            self.simulationInit()
            stack = self.station_1()
            self.matrixStation1.append(stack)
            self.matrixStationWait1.append(self.stack.copy())
            self.printStation("1", stack)

            stack = self.station_2()
            self.matrixStation2.append(stack)
            self.matrixStationWait2.append(self.stackStation1.copy())
            self.printStation("2", stack)

            stack = self.station_3()
            self.matrixStation3.append(stack)
            self.matrixStationWait3.append(self.stackStation2.copy())
            self.printStation("3", stack)

            stack = self.station_4()
            self.matrixStation4.append(stack)
            self.matrixStationWait4.append(self.stackStation3.copy())
            self.printStation("4", stack)

            stack = self.station_5()
            self.nBocadillosFinish += len(stack)
            self.matrixStation5.append(stack)
            self.matrixStationWait5.append(self.stackStation42.copy())
            self.printStation("5", stack)

        print("Cajas de bocadillos hechos = ", self.nBocadillosFinish * 14)
        print("Cajas de guayabas usadas = ", self.nGuavasUsed)
        print("Cajas de guayabas dañadas = ", self.dangerGuava)
        print("Cajas de guayabas en bodega = ", len(self.stack))
        print("Cajas de guayabas en producción = ", self.nGuavasUsed - self.nBocadillosFinish)


class Station1_Guava:
    dayMold = -1
    dayCut = -1
    dayFinishCut = -1

    def __init__(self, at, start, ri, day):
        self.at = at
        self.start = max(start, at)
        self.et = ri
        self.exit = abs(self.start + self.et)
        self.wt = self.start - at
        self.day = day

    def __str__(self):
        return str(self.at) + "," + str(self.start) + "," + str(self.et) + "," + str(self.exit) + "," + str(
            self.wt) + "," + str(self.day) + "," + str(self.dayMold) + "," + str(self.dayCut) + "," + str(
            self.dayFinishCut)


queue = Queue_Guava(40, 65, 25, 25, 120, 20, 50)
queue.start(25)


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

    start = np.array(start)
    at = np.array(at)
    wt = start - at
    w = start == at
    l = []
    for x in range(n):
        l.append(sum(i <= ext[x] for i in at[x + 1:n]))

    queue = np.array([at, randomsRiA, iat, start, randomsRiS, et, ext, l, w, wt])

    return queue.T
