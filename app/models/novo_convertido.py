from datetime import date
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.db.session import Base

class NovoConvertido(Base):
    __tablename__ = "novos_convertidos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    telefone = Column(String(20), nullable=False)   
    cep = Column(String(10), nullable=False)        
    endereco = Column(String(255), nullable=False)  
    complemento = Column(String(255), nullable=True)
    cidade = Column(String(100), nullable=False)
    bairro = Column(String(100), nullable=False)    
    uf = Column(String(2), nullable=False)          
    data_nascimento = Column(Date, nullable=False)
    data_cadastro = Column(Date, nullable=False, default=date.today, server_default=sa.text('CURRENT_DATE'))
    data_conversao = Column(Date, nullable=False)
    discipulador_id = Column(Integer, ForeignKey("users.id"))

    @property
    def idade(self) -> int:
        """Calcula idade em tempo de execução a partir de data_nascimento."""
        if self.data_nascimento:
            hoje = date.today()
            idade_calc = hoje.year - self.data_nascimento.year
            if (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day):
                idade_calc -= 1
            return idade_calc
        return None
