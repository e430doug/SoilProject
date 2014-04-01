import math
import plotly


py = plotly.plotly("doug.durham", "j9ym75bpyi")


xVals = [ (float (x) * math.pi/20.0) for x in range(0, 40)]

yVals = [math.sin(x) for x in xVals]




dd = {
    'name': 'Doug Test', # the "name" of this series is the Continent
    'x': xVals,
    'y': yVals,
    'type': 'scatter',
    'mode': 'markers',
}


layout = {
    'xaxis': {'title': 'X Value'},
        'yaxis': {'title': 'Magnitude'},
            'title': 'Sine curve'
            }
            
            
py.plot(dd, layout=layout,
         filename='Doug Graph yun', fileopt='overwrite',
                  world_readable=True, width=1000, height=650)
