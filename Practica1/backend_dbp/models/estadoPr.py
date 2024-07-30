from enum import Enum

class EstadoPr(Enum):
    Vencido = 'Vencido'
    PorCaducar = 'Por Caducar'
    Buen_Estado = 'Buen Estado'

    @property
    def serialize(self):
        return self.name