import matplotlib.pyplot as pl


class helptools():

    @classmethod
    def draw(cls, x, y, title='Title', xlab='Users', ylab='Metric',
             filename='Default.png'):
        pl.bar(x, y, facecolor='#9999ff', edgecolor='white', width=0.5)
        pl.title(title)
        pl.xlabel(xlab)
        pl.ylabel(ylab)
        pl.xticks(x)
        pl.yticks(y)
        pl.savefig('images/' + filename)
        pl.close()