import numpy as np
import plotly.graph_objects as go
import pubchempy as pcp
import math

name = "methane"


class atomR:
    def __init__(self, aid, element, charge, x, y, z, electrons):
        self.aid = aid
        self.element = element
        self.charge = charge
        self.x = x
        self.y = y
        self.z = z
        self.electrons = electrons


name = input("What is the name of the compound? ")


def aaron(name):
    # name = input("What is the name of the compound? ")
    results = pcp.get_compounds(name, 'name', record_type='3d')
    try:
        compound = results[0]
    except IndexError:
        print("Invalid Compound")
        return None

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
    atoms = []
    for atom in atomslistofdicts:
        atoms.append(atomR(atom['aid'], atom['element'], 0, atom['x'], atom['y'], atom['z'], 0))

    for atom in atoms:
        for i, (key, value) in enumerate(charge_dict.items()):
            if atom.element == key:
                atom.charge = value
        for i, (key, value) in enumerate(electrons_dict.items()):
            if atom.element == key:
                atom.electrons = value
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
    atoms = []
    for atom in atomslistofdicts:
        atoms.append(atomR(atom['aid'], atom['element'], 0, atom['x'], atom['y'], atom['z'], 0))

    for atom in atoms:
        for i, (key, value) in enumerate(charge_dict.items()):
            if atom.element == key:
                atom.charge = value
        for i, (key, value) in enumerate(electrons_dict.items()):
            if atom.element == key:
                atom.electrons = value
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
            sum += (1 / findDistance(i, parent) ** 2 * abs(i.charge - parent.charge)) / 2
        parent.electrons *= sum
    return comp


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
    X, Y, Z = np.mgrid[-10:100:400j, -10:10:40j, -10:10:40j]
    values = np.multiply(size,
             np.sqrt(np.power(X - xd, 2) + np.power(Y - yd, 2) + np.power(Z - zd, 2)))
    cloud = go.Volume(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=values.flatten(),
        isomin=0,
        isomax=3,
        opacity=0.1,  # needs to be small to see through all surfaces
        surface_count=15  # needs to be a large number for good volume rendering
    )
    return cloud


def bonding(x1, x2, y1, y2, z1, z2):
    trace = go.Streamtube(sizeref=0.75,
                          x=[0, x1, x1], y=[y1, 0, y1], z=[z1, z1, 0],
                          u=[x2 - x1, x2 - x1, x2 - x1],
                          v=[y2 - y1, y2 - y1, y2 - y1],
                          w=[z2 - z1, z2 - z1, z2 - z1])
    return trace


def render(uatoms, dictionary, bondlist):
    renderlist = []
    for atom in uatoms:
        renderlist.append(spheres(0.5, '#000000', atom.x, atom.y, atom.z))
        renderlist.append(spherecloud(atom.electrons / 5, atom.x, atom.y, atom.z))
    for bond in bondlist:
        print(dictionary)
        a1 = dictionary[bond['aid1'] - 1]
        a2 = dictionary[bond['aid2'] - 1]
        print(a2.x)
        renderlist.append(bonding(a1.x, a2.x, a1.y, a2.y, a1.z, a2.z))

    fig = go.Figure(data=renderlist)
    fig.show()
    # return fig.write_html("compound.html")


def run(name):
    atoms = aaron(name)
    uatoms = findForce(atoms)
    bonds, apoints = josh(name)
    return render(uatoms, apoints, bonds)


run(name)
