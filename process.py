import pubchempy as pcp
from cmath import sqrt
import math


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
results = pcp.get_compounds(name, 'name', record_type='3d')
compound = results[0]

dictoflistsofdicts = compound.to_dict(properties=['atoms', 'bonds'])
atomslistofdicts = dictoflistsofdicts["atoms"]
bondslistofdicts = dictoflistsofdicts["bonds"] #josh wants this

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

def findDistance(atom1,atom2):
    x1 = atom1.x
    x2 = atom2.x
    y1 = atom1.y
    y2 = atom2.y
    z1 = atom1.z
    z2 = atom2.z
    distance = math.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)
    return distance

pullConstant = 1
def pull(distance,parentCharge,childCharge):
    if distance != 0:
        return pullConstant*parentCharge*childCharge/distance**2
    else:
        return 1


def determineForce(Comp):
    for parent in (Comp):
        for child in Comp:
            if parent.charge >= child.charge:
                parent.electrons *= pull(findDistance(parent,child),parent.charge,child.charge)
                child.electrons /= pull(findDistance(parent,child),parent.charge,child.charge)
            else:
                child.electrons *= pull(findDistance(parent,child),parent.charge,child.charge)
                parent.electrons /= pull(findDistance(parent,child),parent.charge,child.charge)






