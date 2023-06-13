from sched_mod.schedule import *
import time
from controls.bus001 import *

def monPrint(inData1, indata2, start):

    print(int(time.time() - start), inData1, "   ", indata2)



if __name__ == '__main__':

    sapcontrols = set()
    timenowvar = time.time()

    sapcontrols.add(SapControl(monPrint, 'a', 'aaaa', start=timenowvar))
    sapcontrols.add(SapControl(monPrint, 'b', 'bbbbb', start=timenowvar))

    abc = Schedule(time.time(), 8, sapcontrols)
    abc.run()


