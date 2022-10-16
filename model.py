import numpy as np
import plotly.graph_objects as go
from process.py import charge_dict

def spheres(size, clr, xd, yd, zd):
    theta = np.linspace(0, 2 * np.pi, 100)
    phi = np.linspace(0, np.pi, 100)
    x0 = xd + size * np.outer(np.cos(theta), np.sin(phi))
    y0 = yd + size * np.outer(np.sin(theta), np.sin(phi))
    z0 = zd + size * np.outer(np.ones(100), np.cos(phi))
    trace = go.Surface(x=x0, y=y0, z=z0, colorscale=[[0, clr], [1, clr]])
    trace.update(showscale=False)
    return trace

def spherecloud(size, xd, yd, zd):
    X, Y, Z = np.mgrid[-10:10:40j, -10:10:40j, -10:10:40j]
    values = np.negative(np.multiply(size,
                                     np.sqrt(np.power(X - xd, 2) + np.power(Y - yd, 2) + np.power(Z - zd, 2))))
    cloud = go.Volume(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=values.flatten(),
        isomin=-3,
        isomax=0,
        opacity=0.1,  # needs to be small to see through all surfaces
        surface_count=15  # needs to be a large number for good volume rendering
    )
    return cloud


def bonding(x1, x2, y1, y2, z1, z2):
    trace = go.Streamtube(sizeref=0.75,
                          x=[x1, x1, 0], y=[y1, y1, 0], z=[z1, z1, 0],
                          u=[x2 - x1, x2 - x1, x2 - x1],
                          v=[y2 - y1, y2 - y1, y2 - y1],
                          w=[z2 - z1, z2 - z1, z2 - z1])
    return trace


def annot(x, y, z, txt, xancr='center'):
    string = dict(showarrow=False, x=x, y=y, z=z, text=txt, xanchor=xancr, font=dict(color='white', size=12))
    return string


renderlist = []
dictionary = {1: [.5, 2, 3, 2], 2: [.5, 1, 2, -1]}
for key, val in dictionary.items():
    renderlist.append(spheres(val[0], '#000000', val[1], val[2], val[3]))
    renderlist.append(spherecloud(val[0] * 3, val[1], val[2], val[3]))
bondlist = [{'aid1': 1, 'aid2': 2, 'order': 1}]
for bond in bondlist:
    a1 = dictionary.get(bond.get('aid1'))
    a2 = dictionary.get(bond.get('aid2'))
    renderlist.append(bonding(a1[1], a2[1], a1[2], a2[2], a1[3], a2[3]))

fig = go.Figure(data=renderlist)
fig.show()
