import os
import shutil
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import crud, models, schemas

# Criar tabelas no banco MySQL
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Fotos - MySQL")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# RF01 - Armazenar Foto
@app.post("/fotos/", response_model=schemas.Foto)
async def upload_foto(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db_foto = crud.create_foto(db, schemas.FotoCreate(name_hash=file.filename))
    return db_foto

# RF02 - Listar todas as fotos
@app.get("/fotos/", response_model=list[schemas.Foto])
def listar_fotos(db: Session = Depends(get_db)):
    return crud.get_fotos(db)

# RF03 - Consultar foto única
@app.get("/fotos/{foto_id}", response_model=schemas.Foto)
def consultar_foto(foto_id: int, db: Session = Depends(get_db)):
    db_foto = crud.get_foto(db, foto_id)
    if db_foto is None:
        raise HTTPException(status_code=404, detail="Foto não encontrada")
    return db_foto

# RF04 - Apagar foto
@app.delete("/fotos/{foto_id}")
def deletar_foto(foto_id: int, db: Session = Depends(get_db)):
    sucesso = crud.delete_foto(db, foto_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Foto não encontrada")
    return {"msg": "Foto deletada com sucesso"}
