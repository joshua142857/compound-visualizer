import numpy as np
import plotly.graph_objects as go
import pubchempy as pcp
import math
from flask import Flask, redirect, url_for, request


class atomR:
    def __init__(self, aid, element, charge, x, y, z, electrons, color):
        self.aid = aid
        self.element = element
        self.charge = charge
        self.x = x
        self.y = y
        self.z = z
        self.electrons = electrons
        self.color = color


def aaron(name):
    # name = input("What is the name of the compound? ")
    results = pcp.get_compounds(name, 'name', record_type='3d')
    compound = results[0]

    dictoflistsofdicts = compound.to_dict(properties=['atoms', 'bonds'])
    atomslistofdicts = dictoflistsofdicts["atoms"]
    bondslistofdicts = dictoflistsofdicts["bonds"]  # josh wants this

    charge_dict = {
        'C': 2.55,
        'H': 2.2,
        'O': 3.44,
        'N': 3.04,
        'P': 2.19,
        'S': 2.58
    }

    electrons_dict = {
        'C': 4,
        'H': 1,
        'O': 6,
        'N': 5,
        'P': 5,
        'S': 6
    }

    color_dict = {
        'C': "#000000",  # black
        'H': "#ffffff",  # white
        'O': "#ff0000",  # red
        'N': "#0000ff",  # blue
        'P': "#7f007f",  # purple
        'S': "#ffff00"  # yellow
    }

    atoms = []
    for atom in atomslistofdicts:
        atoms.append(atomR(atom['aid'], atom['element'], 0, atom['x'], atom['y'], atom['z'], 0, ""))

    for atom in atoms:
        for i, (key, value) in enumerate(charge_dict.items()):
            if atom.element == key:
                atom.charge = value
        for i, (key, value) in enumerate(electrons_dict.items()):
            if atom.element == key:
                atom.electrons = value
        for i, (key, value) in enumerate(color_dict.items()):
            if atom.element == key:
                atom.color = value
    return atoms


def josh(name):
    # name = input("What is the name of the compound? ")
    results = pcp.get_compounds(name, 'name', record_type='3d')
    compound = results[0]

    dictoflistsofdicts = compound.to_dict(properties=['atoms', 'bonds'])
    atomslistofdicts = dictoflistsofdicts["atoms"]
    bondslistofdicts = dictoflistsofdicts["bonds"]  # josh wants this

    charge_dict = {
        'C': 2.55,
        'H': 2.2,
        'O': 3.44,
        'N': 3.04,
        'P': 2.19,
        'S': 2.58
    }

    electrons_dict = {
        'C': 4,
        'H': 1,
        'O': 6,
        'N': 5,
        'P': 5,
        'S': 6
    }

    color_dict = {
        'C': "#000000",  # black
        'H': "#ffffff",  # white
        'O': "#ff0000",  # red
        'N': "#0000ff",  # blue
        'P': "#7f007f",  # purple
        'S': "#ffff00"  # yellow
    }

    atoms = []
    for atom in atomslistofdicts:
        atoms.append(atomR(atom['aid'], atom['element'], 0, atom['x'], atom['y'], atom['z'], 0, ""))

    for atom in atoms:
        for i, (key, value) in enumerate(charge_dict.items()):
            if atom.element == key:
                atom.charge = value
        for i, (key, value) in enumerate(electrons_dict.items()):
            if atom.element == key:
                atom.electrons = value
        for i, (key, value) in enumerate(color_dict.items()):
            if atom.element == key:
                atom.color = value
    atomsforjosh = {i: atoms[i] for i in range(len(atoms))}
    return bondslistofdicts, atomsforjosh


def findDistance(atom1, atom2):
    x1 = atom1.x
    x2 = atom2.x
    y1 = atom1.y
    y2 = atom2.y
    z1 = atom1.z
    z2 = atom2.z
    distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
    return distance


def findForce(comp):
    for parent in comp:
        lst = []
        for child in comp:
            if parent != child:
                lst.append(child)
        sum = 0
        for i in lst:
            sum += (1 / findDistance(i, parent) ** 4 * abs(i.charge - parent.charge)) / 2
        parent.electrons *= sum
    return comp


def spheres(size, clr, xd, yd, zd):
    theta = np.linspace(0, 2 * np.pi, 80)
    phi = np.linspace(0, np.pi, 80)
    x0 = xd + size * np.outer(np.cos(theta), np.sin(phi))
    y0 = yd + size * np.outer(np.sin(theta), np.sin(phi))
    z0 = zd + size * np.outer(np.ones(80), np.cos(phi))
    trace = go.Surface(x=x0, y=y0, z=z0, colorscale=[[0, clr], [1, clr]])
    trace.update(showscale=False)
    return trace


def spherecloud(size, xd, yd, zd):
    X, Y, Z = np.mgrid[-10:10:40j, -10:10:40j, -10:10:40j]
    values = np.sqrt(np.power(X - xd, 2) + np.power(Y - yd, 2) + np.power(Z - zd, 2))
    cloud = go.Volume(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=values.flatten(),
        isomin=0,
        isomax=size ** .25,
        opacity=0.1,
        surface_count=7,
        showscale=False
    )
    return cloud


def bonding(x1, x2, y1, y2, z1, z2):
    trace = go.Streamtube(sizeref=0.1,
                          x=[0, 0, 0], y=[0, 0.1, 0], z=[0, 0, 0],
                          u=[x2 - x1, 1, 1],
                          v=[y2 - y1, 1, 1],
                          w=[z2 - z1, 1, 1],
                          starts=dict(
                              x=[x1],
                              y=[y1],
                              z=[z1]
                          ),
                          colorscale='gray',
                          showscale=False)
    return trace


def bondcloud(size, xd, yd, zd):
    X, Y, Z = np.mgrid[-10:10:40j, -10:10:40j, -10:10:40j]
    values = np.sqrt(np.power(X - xd, 2) + np.power(Y - yd, 2) + np.power(Z - zd, 2))
    cloud = go.Volume(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=values.flatten(),
        isomin=0,
        isomax=size,
        opacity=0.2,
        surface_count=2,
        showscale=False
    )
    return cloud



def render(uatoms, dictionary, bondlist, name):
    renderlist = []
    k = 2
    for atom in uatoms:
        renderlist.append(spheres(.2, atom.color, k * atom.x, k * atom.y, k * atom.z))
        renderlist.append(spherecloud(atom.electrons, k * atom.x, k * atom.y, k * atom.z))
    for bond in bondlist:
        a1 = dictionary[bond['aid1'] - 1]
        a2 = dictionary[bond['aid2'] - 1]
        # renderlist.append(bonding(k * a1.x, k * a2.x, k * a1.y, k * a2.y, k * a1.z, k * a2.z))
        renderlist.append(bondcloud((2 * a1.electrons ** (.25) + a2.electrons ** (.25)) / 6,
                                    a1.x * k + (a2.x - a1.x) * k / 3,
                                    a1.y * k + (a2.y - a1.y) * k / 3,
                                    a1.z * k + (a2.z - a1.z) * k / 3)
                          )
        renderlist.append(bondcloud((a1.electrons ** (.25) + 2 * a2.electrons ** (.25)) / 6,
                                    a1.x * k + (a2.x - a1.x) * 2 * k / 3,
                                    a1.y * k + (a2.y - a1.y) * 2 * k / 3,
                                    a1.z * k + (a2.z - a1.z) * 2 * k / 3)
                          )
    layout = go.Layout(title=name, showlegend=False, margin=dict(l=0, r=0, t=0, b=0),
                       scene=dict(xaxis=dict(title='',
                                             range=[-10, 10],
                                             backgroundcolor='white',
                                             color='white',
                                             gridcolor='white'),
                                  yaxis=dict(title='',
                                             range=[-10, 10],
                                             backgroundcolor='white',
                                             color='white',
                                             gridcolor='white'
                                             ),
                                  zaxis=dict(title='',
                                             range=[-10, 10],
                                             backgroundcolor='white',
                                             color='white',
                                             gridcolor='white'
                                             )
                                  ))
    fig = go.Figure(data=renderlist, layout=layout)
    fig.show()
    return fig.write_html("compound.html")


def run(name):
    atoms = aaron(name)
    uatoms = findForce(atoms)
    bonds, apoints = josh(name)
    return render(uatoms, apoints, bonds, name)


app = Flask(__name__)


@app.route('/')
def home():
    return HOME_HTML


HOME_HTML = """ <html>
<body>
<h1> Welcome to Orgo Structure Finder</h1>
<h2> What is molecular orbital theory combined with valence shell electron pair repulsion(VSEPR)? </h2>
When Schrodinger introduced the concept which electrons existed as waves of probable location, rather than precise
location, models of atomic bonding must be reimagined. Previous models used the electronegativities of 
atoms which make up a structure to determine which atoms had a greater affinity for electrons and therefore 
pulled electrons towards it. However to combine these ideas, models reimagine individual electrons within the model as
clouds, or areas of probable location of such electron.<br><br>

For example, given a compound made up of 2 elements A, linked to each other, and a more electronegative element B, linked
 to one of the As, element B would attract more electrons, due to it being more electronegative; therefore, electrons
 would have a greater possibility to be found near B rather than any of the As and the neighboring A would have a less
 than normal likelihood of electrons surrounding it. Therefore the cloud of B being larger, also causes A to be smaller.
 However, there is a distance factor as well. The A element less far away would experience less of the B's
 pull. Therefore the A furthest from B has a larger electron cloud than the A closest to A.<br><br>

 These ideas may be hard to visualize on your own. Using pubChem's database we have created a open ended program
 which allows for one to model the electron clouds around atoms of any organic compound, given the name of 
 the chemical. 
 <br><br>

<form action  = "/main">
   Input Chemical Name = <input type = 'text' name = 'formula'><br>
   <input type='submit' value='Continue'>
</form>
</body>
"""


@app.route('/main')
def main():
    x = request.args.get('formula')
    run(x)
    return MAIN_HTML.format(x)


MAIN_HTML = """
<html>
<body>
<h1>
Window(s) opened containing diagrams<br> To view, navigate away from window
</h1>
</script>
<body>
</html>
"""

if __name__ == '__main__':
    app.run(host="localhost", debug=True)
