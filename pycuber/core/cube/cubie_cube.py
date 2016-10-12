from .cube_array import CubeArray
from .cube_abc import CubeABC
from .constants import X, Y, Z
from ..formula import Step


rotation_parameters = {
    Step("L"): (X, 0, -1),
    Step("M"): (X, 1, -1),
    Step("R"): (X, 2, 1),

    Step("D"): (Y, 0, -1),
    Step("E"): (Y, 1, -1),
    Step("U"): (Y, 2, 1),

    Step("F"): (Z, 0, -1),
    Step("S"): (Z, 1, -1),
    Step("B"): (Z, 2, 1),
}

for step in list(rotation_parameters.keys()):
    axis, layer, k = rotation_parameters[step]
    rotation_parameters[step.inverse()] = (axis, layer, k * -1)
    rotation_parameters[step * 2] = (axis, layer, k * 2)

combinations = {
    Step("l"): [Step("L"), Step("M")],
    Step("r"): [Step("M'"), Step("R")],
    Step("x"): [Step("L'"), Step("M'"), Step("R")],

    Step("d"): [Step("D"), Step("E")],
    Step("u"): [Step("E'"), Step("U")],
    Step("y"): [Step("D'"), Step("E'"), Step("U")],

    Step("f"): [Step("F"), Step("S")],
    Step("b"): [Step("S'"), Step("B")],
    Step("z"): [Step("F"), Step("S"), Step("B'")],
}

for step, comb in list(combinations.items()):
    combinations[step.inverse()] = [s.inverse() for s in comb]
    combinations[step * 2] = [s * 2 for s in comb]


class CubieCube(CubeABC):

    def __init__(self):
        super().__init__()
        self.__data = CubeArray()

    def do_step(self, step):
        if step.face.isupper():
            self.__data.twist(*rotation_parameters[step])
        else:
            for s in combinations[step]:
                self.__data.twist(*rotation_parameters[s])
        return self

    def do_formula(self, formula):
        for step in formula:
            self.do_step(step)
        return self

    def get_face(self, face):
        if isinstance(face, str):
            face = "ULFRBD".index(face)
        return self.__data.get_face(face)