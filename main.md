from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import asyncpg
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("Connecting to the database...")
        global bd
        bd = await asyncpg.connect(
            user='postgres',
            password='root',
            database='bd_patrocars',
            host='localhost'
        )
        print("Database connected")
        yield
    except Exception as e:
        print(f"Error during startup: {e}")
    finally:
        await bd.close()
        print("Database connection closed")

app = FastAPI(lifespan=lifespan)
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

# Montadora

@app.get('/listar_montadoras', response_class=HTMLResponse)
async def list_montadoras(request: Request):
    montadoras = await bd.fetch('SELECT * FROM MONTADORA')
    return templates.TemplateResponse('list_montadoras.html', {'request': request, 'montadoras': montadoras})

@app.get('/adicionar_montadora')
async def adicionar_montadora(request: Request):
    return templates.TemplateResponse('add_montadora.html', {'request': request})

@app.post('/salvar_montadora')
async def adicionar_montadora(nome: str = Form(...), pais: str = Form(...), ano_fundacao: int = Form(...)):
    await bd.execute(
        'INSERT INTO MONTADORA (NOME, PAIS, ANO_FUNDACAO) VALUES ($1, $2, $3)',
        nome, pais, ano_fundacao
    )

@app.get('/editar_montadora/{montadora_id}')
async def editar_form(request: Request, montadora_id: str):
    montadoras = await bd.fetch('SELECT * FROM MONTADORA')
    montadora_a_editar = next((m for m in montadoras if m['mont_id'] == int(montadora_id)), None)
    if montadora_a_editar is None:
        return templates.TemplateResponse('404.html', {'request': request})
    return templates.TemplateResponse('editar_montadora.html', {'request': request, 'montadora': montadora_a_editar})

@app.post('/editar_salvar_montadora/{montadora_id}')
async def editar_montadora(montadora_id: int, nome: str = Form(...), pais: str = Form(...), ano_fundacao: int = Form(...)):
    await bd.execute(
        'UPDATE MONTADORA SET NOME = $1, PAIS = $2, ANO_FUNDACAO = $3 WHERE MONT_ID = $4',
        nome, pais, ano_fundacao, montadora_id
    )

@app.get('/detalhar_montadora/{montadora_id}')
async def detalhar_montadora(request: Request, montadora_id: str):
    montadoras = await bd.fetch('SELECT * FROM MONTADORA')
    montadora_a_detalhar = next((m for m in montadoras if m['mont_id'] == int(montadora_id)), None)
    if montadora_a_detalhar is None:
        return templates.TemplateResponse('404.html', {'request': request})
    return templates.TemplateResponse('detalhar_montadora.html', {'request': request, 'montadora': montadora_a_detalhar})

@app.get('/remover_montadora/{montadora_id}')
async def remover_form(request: Request, montadora_id: str):
    montadoras = await bd.fetch('SELECT * FROM MONTADORA')
    montadora_a_remover = next((m for m in montadoras if m['mont_id'] == int(montadora_id)), None)
    if montadora_a_remover is None:
        return templates.TemplateResponse('404.html', {'request': request})
    return templates.TemplateResponse('remover_montadora.html', {'request': request, 'montadora': montadora_a_remover})

@app.post('/remover_salvar_montadora/{montadora_id}')
async def remover_montadora(montadora_id: int):
    await bd.execute('DELETE FROM MONTADORA WHERE MONT_ID = $1', montadora_id)

# Modelo Veículo

@app.get('/listar_modelos', response_class=HTMLResponse)
async def list_modelos(request: Request):
    modelos = await bd.fetch('SELECT * FROM MODELO_VEICULO')
    return templates.TemplateResponse('list_modelos.html', {'request': request, 'modelos': modelos})

@app.get('/adicionar_modelo')
async def adicionar_modelo(request: Request):
    return templates.TemplateResponse('add_modelo.html', {'request': request})

@app.post('/salvar_modelo')
async def adicionar_modelo(nome: str = Form(...), montadora_id: int = Form(...), valor_referencia: float = Form(...),
                           motorizacao: int = Form(...), turbo: bool = Form(...), automatico: bool = Form(...)):
    await bd.execute(
        'INSERT INTO MODELO_VEICULO (NOME, MONT_ID, VALOR_REFERENCIA, MOTORIZACAO, TURBO, AUTOMATICO) VALUES ($1, $2, $3, $4, $5, $6)',
        nome, montadora_id, valor_referencia, motorizacao, turbo, automatico
    )

@app.get('/editar_modelo/{mod_id}')
async def editar_form(request: Request, mod_id: str):
    modelos = await bd.fetch('SELECT * FROM MODELO_VEICULO')
    modelo_a_editar = next((m for m in modelos if m['mod_id'] == int(mod_id)), None)
    if modelo_a_editar is None:
        return templates.TemplateResponse('404.html', {'request': request})
    return templates.TemplateResponse('editar_modelo.html', {'request': request, 'modelo': modelo_a_editar})

@app.post('/editar_salvar_modelo/{mod_id}')
async def editar_modelo(mod_id: int, nome: str = Form(...), montadora_id: int = Form(...), valor_referencia: float = Form(...),
                        motorizacao: int = Form(...), turbo: bool = Form(...), automatico: bool = Form(...)):
    await bd.execute(
        'UPDATE MODELO_VEICULO SET NOME = $1, MONT_ID = $2, VALOR_REFERENCIA = $3, MOTORIZACAO = $4, TURBO = $5, AUTOMATICO = $6 WHERE MOD_ID = $7',
        nome, montadora_id, valor_referencia, motorizacao, turbo, automatico, mod_id
    )

# Similarly, other routes for "Veículo" follow the same pattern.

# Note: Adjust the template paths and database queries as needed.
