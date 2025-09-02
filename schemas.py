from pydantic import BaseModel

class FotoBase(BaseModel):
    name_hash: str

class FotoCreate(FotoBase):
    pass

class Foto(FotoBase):
    id: int
    
    class Config:
        orm_mode = True
