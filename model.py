import numpy as np
import plotly.graph_objects as go


def spheres(size, clr, xd, yd, zd):
    # Set up 100 points. First, do angles
    theta = np.linspace(0, 2 * np.pi, 100)
    phi = np.linspace(0, np.pi, 100)

    # Set up coordinates for points on the sphere
    x0 = xd + size * np.outer(np.cos(theta), np.sin(phi))
    y0 = yd + size * np.outer(np.sin(theta), np.sin(phi))
    z0 = zd + size * np.outer(np.ones(100), np.cos(phi))

    # Set up trace
    trace = go.Surface(x=x0, y=y0, z=z0, colorscale=[[0, clr], [1, clr]])
    trace.update(showscale=False)

    return trace
def annot(x, y, z, txt, xancr='center'):
    string=dict(showarrow=False, x=x, y=y, z=z, text=txt, xanchor=xancr, font=dict(color='white',size=12))
    return string

spherelist = []
dictionary = {"hydrogen" : [1,2,3,2], "hydrogen1" : [.5,1,2,-1]}
print(dictionary)
for key, val in dictionary.items():
    spherelist.append(spheres(val[0], '#ff0000', val[1], val[2], val[3]))
print(spherelist)

fig = go.Figure(data=spherelist)

fig.show()


# X, Y, Z = np.mgrid[-10:10:40j, -10:10:40j, -10:10:40j]
# values = np.sqrt(np.power(X, 2) + np.power(Y, 2) + np.power(Z, 2))
# values += np.sqrt(np.power(X+1, 2) + np.power(Y+1, 2) + np.power(Z+1, 2))
# fig = go.Figure(data=go.Volume(
#     x=X.flatten(),
#     y=Y.flatten(),
#     z=Z.flatten(),
#     value=values.flatten(),
#     isomin=0,
#     isomax=10,
#     opacity=0.1,  # needs to be small to see through all surfaces
#     surface_count=20,  # needs to be a large number for good volume rendering
#     ))
# fig.show()