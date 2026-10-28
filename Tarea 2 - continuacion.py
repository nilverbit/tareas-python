from abc import ABC, abstractmethod


class Matricula(ABC):
    PAGO = 60.00

    @abstractmethod
    def pago_matricula(self):
        return self.PAGO


# ======================================================================
# ESPECIALIZACIONES (se escriben UNA sola vez; cada una usa super()
# para tomar el monto calculado por la regla anterior)
# ======================================================================
class BeneficiarioBeca(Matricula):
    def pago_matricula(self):
        return super().pago_matricula() * 0.5


class IndiceAcademico(Matricula):
    def pago_matricula(self):
        return super().pago_matricula() + 15


class MatriculaExtemporanea(Matricula):
    def pago_matricula(self):
        return super().pago_matricula() + 15


# ========================= EL PRIMER PROGRAMADOR =========================
# beca -> índice -> extemporánea
class MatriculaCombinada1(BeneficiarioBeca, IndiceAcademico, MatriculaExtemporanea):
    pass


# ========================= EL SEGUNDO PROGRAMADOR ========================
# índice -> extemporánea -> beca
class MatriculaCombinada2(IndiceAcademico, MatriculaExtemporanea, BeneficiarioBeca):
    pass


# ======================================================================
# VERIFICACIÓN DEL PROBLEMA
# ======================================================================
print("=== PROBLEMA: herencia múltiple ===")
print("MRO 1:", [c.__name__ for c in MatriculaCombinada1.__mro__])
print("MRO 2:", [c.__name__ for c in MatriculaCombinada2.__mro__])
print("Versión 1:", MatriculaCombinada1().pago_matricula())  # 45.0
print("Versión 2:", MatriculaCombinada2().pago_matricula())  # 60.0

# Escribir primero la general -> MRO inconsistente
try:
    class Invalida(Matricula, BeneficiarioBeca):
        pass
except TypeError as e:
    print("Matricula primero ->", e)


# ======================================================================
# REDISEÑO: composición en lugar de herencia múltiple
# El monto ya no depende del orden de las bases, sino de una lista
# ordenada de reglas que se decide para cada estudiante.
# ======================================================================
class Regla(ABC):
    @abstractmethod
    def aplicar(self, monto):
        """Recibe el monto actual y devuelve el monto modificado."""


class ReglaBeca(Regla):
    def aplicar(self, monto):
        return monto * 0.5


class ReglaIndiceAcademico(Regla):
    def aplicar(self, monto):
        return monto + 15


class ReglaExtemporanea(Regla):
    def aplicar(self, monto):
        return monto + 15


class MatriculaConReglas(Matricula):
    """Continúa la clase Matricula: el pago base sigue siendo PAGO."""

    def __init__(self, reglas=None):
        self.reglas = list(reglas or [])   # el orden de la lista ES el orden del cobro

    def pago_matricula(self):
        monto = super().pago_matricula()
        for regla in self.reglas:
            monto = regla.aplicar(monto)
        return monto


def armar_reglas(becario=False, indice_desaprobatorio=False,
                 extemporanea=False, beca_antes=False):
    """Política institucional: decide qué cobros aplican y en qué orden."""
    recargos = []
    if indice_desaprobatorio:
        recargos.append(ReglaIndiceAcademico())
    if extemporanea:
        recargos.append(ReglaExtemporanea())

    if not becario:
        return recargos
    beca = [ReglaBeca()]
    return beca + recargos if beca_antes else recargos + beca


print("\n=== REDISEÑO: composición ===")
luis = MatriculaConReglas(armar_reglas(True, True, True, beca_antes=False))
rosa = MatriculaConReglas(armar_reglas(True, True, True, beca_antes=False))
print("Beca DESPUÉS de recargos -> Luis:", luis.pago_matricula(),
      "| Rosa:", rosa.pago_matricula())                       # 45.0 y 45.0

antes = MatriculaConReglas(armar_reglas(True, True, True, beca_antes=True))
print("Beca ANTES de recargos   ->", antes.pago_matricula())  # 60.0
