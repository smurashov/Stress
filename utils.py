import matplotlib.pyplot as pl
import time
import os


def timecheck(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        with open(os.getcwd() + '/testresults.txt', "a") as myfile:
            myfile.write(str(te - ts) + "  " + method.__name__ + '\n')
        return result

    return timed

class helptools():

    @classmethod
    def draw(cls, x, y, title='Title', xlab='Users', ylab='Metric',
             filename='Default.png'):
        pl.bar(x, y, facecolor='#9999ff', edgecolor='white', width=2)
        pl.title(title)
        pl.xlabel(xlab)
        pl.ylabel(ylab)
        pl.xticks(x)
        pl.yticks(y)
        pl.savefig('images/' + filename)
        pl.close()

    @classmethod
    def pars(cls, wtf):
        mass = []
        for x in wtf.text.strip('[').strip(']').strip(',').split():
            mass.append(float(x.encode('utf-8'
                                       '').strip('[').strip(']').strip(',')))
        return mass

    @classmethod
    def RAM_average(cls, wtf):
        return sum(filter(lambda x: x > 100,
                          wtf)) / len(filter(lambda x: x > 100, wtf))

    @classmethod
    def CPU_data(cls, wtf):
        return filter(lambda x: x <= 100, wtf)

    @classmethod
    def CPU_numb(cls, mass1, mass2):
        return len(mass1) / len((filter(lambda x: x > 100, mass2)))