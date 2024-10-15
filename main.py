from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import asyncpg
import asyncio

import warnings
from fastapi import FastAPI
import uvicorn

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')

bd = None

@app.get("/")
async def read_root():
    return {"message": "Hello, World"}






@app.on_event("startup")
async def startup():
    global bd
    bd = await asyncpg.connect(
        user='postgres',
        password='Senha4321!dfg',
        database='bd_patrocars',
        host='aws-0-sa-east-1.pooler.supabase.com',
        port=6543
    )


# Montadora

@app.get('/listar_montadoras', response_class=HTMLResponse)
async def list_montadoras(request: Request):
  montadoras = await bd.fetch('SELECT * FROM MONTADORA')
  print(montadoras)

  return templates.TemplateResponse(
    request, 'list_montadoras.html', context={'montadoras': montadoras}
  )

@app.get('/adicionar_montadora')
async def adicionar_montadora(request: Request):
  return templates.TemplateResponse(
    request, 'add_montadora.html'
  )

@app.post('/salvar_montadora')
async def adicionar_montadora(nome: str = Form(...), pais: str = Form(...), ano_fundacao: int = Form(...)):
  insercao = 'INSERT INTO MONTADORA (NOME, PAIS, ANO_FUNDACAO) VALUES ($1, $2, $3)'
  await bd.execute(insercao, nome, pais, ano_fundacao)

@app.get('/editar_montadora/{montadora_id}')
async def editar_form(request: Request, montadora_id: str):
    montadora_a_editar = None
    montadoras = await bd.fetch('SELECT * FROM MONTADORA')

    for montadora in montadoras: 
        if montadora['mont_id'] == int(montadora_id):
            montadora_a_editar = montadora

    if montadora_a_editar is None:
        return templates.TemplateResponse(
            request, '404.html'
        )
    
    return templates.TemplateResponse(
        request, 'editar_montadora.html', context={'montadora': montadora_a_editar}
    )

@app.post('/editar_salvar_montadora/{montadora_id}')
async def editar_montadora(montadora_id: int, nome: str = Form(...), pais: str = Form(...), ano_fundacao: int = Form(...)):
  atualizacao = 'UPDATE MONTADORA SET NOME = $1, PAIS = $2, ANO_FUNDACAO = $3 WHERE MONT_ID = $4'
  await bd.execute(atualizacao, nome, pais, ano_fundacao, montadora_id)


@app.get('/detalhar_montadora/{montadora_id}')
async def detalhar_montadora(request: Request, montadora_id: str):
    montadora_a_detalhar = None
    montadoras = await bd.fetch('SELECT * FROM MONTADORA')

    for montadora in montadoras: 
        if montadora['mont_id'] == int(montadora_id):
            montadora_a_detalhar = montadora

    if montadora_a_detalhar is None:
        return templates.TemplateResponse(
            request, '404.html'
        )
    
    return templates.TemplateResponse(
        request, 'detalhar_montadora.html', context={'montadora': montadora_a_detalhar}
    )

@app.get('/remover_montadora/{montadora_id}')
async def remover_form(request: Request, montadora_id: str):
    montadora_a_remover = None
    montadoras = await bd.fetch('SELECT * FROM MONTADORA')

    for montadora in montadoras: 
        if montadora['mont_id'] == int(montadora_id):
            montadora_a_remover = montadora

    if montadora_a_remover is None:
        return templates.TemplateResponse(
            request, '404.html'
        )
    
    return templates.TemplateResponse(
        request, 'remover_montadora.html', context={'montadora': montadora_a_remover}
    )

@app.post('/remover_salvar_montadora/{montadora_id}')
async def remover_montadora(montadora_id: int):
  delecao = 'DELETE FROM MONTADORA WHERE MONT_ID = $1'
  await bd.execute(delecao, montadora_id)

# Modelo Veículo

@app.get('/listar_modelos', response_class=HTMLResponse)
async def list_modelos(request: Request):
  modelos = await bd.fetch('SELECT * FROM MODELO_VEICULO')

  return templates.TemplateResponse(
    request, 'list_modelos.html', context={'modelos': modelos}
)

@app.get('/adicionar_modelo')
async def adicionar_modelo(request: Request):
    return templates.TemplateResponse(
        request, 'add_modelo.html'
)

@app.post('/salvar_modelo')
async def adicionar_modelo(nome: str = Form(...), montadora_id: int = Form(...), valor_referencia: float = Form(...),  motorizacao: int = Form(...), 
                           turbo: bool = Form(...), automatico: bool = Form(...)):
  insercao = 'INSERT INTO MODELO_VEICULO (NOME, MONT_ID, VALOR_REFERENCIA, MOTORIZACAO, TURBO, AUTOMATICO) VALUES ($1, $2, $3, $4, $5, $6)'
  await bd.execute(insercao, nome, montadora_id, valor_referencia, motorizacao, turbo, automatico)


@app.get('/editar_modelo/{mod_id}')
async def editar_form(request: Request, mod_id: str):
    modelo_a_editar = None
    modelos = await bd.fetch('SELECT * FROM MODELO_VEICULO')

    for modelo in modelos: 
        if modelo['mod_id'] == int(mod_id):
            modelo_a_editar = modelo

    if modelo_a_editar is None:
        return templates.TemplateResponse(
            request, '404.html'
        )
    
    return templates.TemplateResponse(
        request, 'editar_modelo.html', context={'modelo': modelo_a_editar}
    )

@app.post('/editar_salvar_modelo/{mod_id}')
async def editar_modelo(mod_id: int, nome: str = Form(...), montadora_id: int = Form(...), valor_referencia: float = Form(...),  motorizacao: int = Form(...), 
                           turbo: bool = Form(...), automatico: bool = Form(...)):
    atualizacao = 'UPDATE MODELO_VEICULO SET NOME = $1, MONT_ID = $2, VALOR_REFERENCIA = $3, MOTORIZACAO = $4, TURBO = $5, AUTOMATICO = $6 WHERE MOD_ID = $7'
    await bd.execute(atualizacao, nome, montadora_id, valor_referencia, motorizacao, turbo, automatico, mod_id)


@app.get('/detalhar_modelo/{mod_id}')
async def detalhar_modelo(request: Request, mod_id: str):
    modelo_a_detalhar = None
    modelos = await bd.fetch('SELECT * FROM MODELO_VEICULO')

    for modelo in modelos: 
        if modelo['mod_id'] == int(mod_id):
            modelo_a_detalhar = modelo

    if modelo_a_detalhar is None:
        return templates.TemplateResponse(
            request, '404.html'
        )
    
    return templates.TemplateResponse(
        request, 'detalhar_modelo.html', context={'modelo': modelo_a_detalhar}
    )

@app.get('/remover_modelo/{mod_id}')
async def remover_form(request: Request, mod_id: str):
    modelo_a_remover = None
    modelos = await bd.fetch('SELECT * FROM MODELO_VEICULO')

    for modelo in modelos: 
        if modelo['mod_id'] == int(mod_id):
            modelo_a_remover = modelo

    if modelo_a_remover is None:
        return templates.TemplateResponse(
            request, '404.html'
        )
    
    return templates.TemplateResponse(
        request, 'remover_modelo.html', context={'modelo': modelo_a_remover}
    )

@app.post('/remover_salvar_modelo/{mod_id}')
async def remover_modelo(mod_id: int):
    delecao = 'DELETE FROM MODELO_VEICULO WHERE MOD_ID = $1'
    await bd.execute(delecao, mod_id)

# Veículos

@app.get('/listar_veiculos', response_class=HTMLResponse)
async def list_veiculos(request: Request):
  veiculos = await bd.fetch('SELECT * FROM VEICULO')

  return templates.TemplateResponse(
    request, 'list_veiculos.html', context={'veiculos': veiculos}
)

@app.get('/adicionar_veiculo')
async def adicionar_veiculo(request: Request):
    return templates.TemplateResponse(
        request, 'add_veiculo.html'
)

@app.post('/salvar_veiculo')
async def adicionar_veiculo(mod_id: int = Form(...), cor: str = Form(...), ano_fabricacao: int = Form(...), ano_modelo: int = Form(...), 
                           valor: float = Form(...), placa: str = Form(...), vendido: bool = Form(...)):
    insercao = 'INSERT INTO VEICULO (MOD_ID, COR, ANO_FABRICACAO, ANO_MODELO, VALOR, PLACA, VENDIDO) VALUES ($1, $2, $3, $4, $5, $6, $7)'
    await bd.execute(insercao, mod_id, cor, ano_fabricacao, ano_modelo, valor, placa, vendido)


@app.get('/editar_veiculo/{veic_id}')
async def editar_form(request: Request, veic_id: str):
    veiculo_a_editar = None
    veiculos = await bd.fetch('SELECT * FROM VEICULO')

    for veiculo in veiculos: 
        if veiculo['veic_id'] == int(veic_id):
            veiculo_a_editar = veiculo

    if veiculo_a_editar is None:
        return templates.TemplateResponse(
            request, '404.html'
        )
    
    return templates.TemplateResponse(
        request, 'editar_veiculo.html', context={'veiculo': veiculo_a_editar}
    )

@app.post('/editar_salvar_veiculo/{veic_id}')
async def editar_veiculo(veic_id: int, mod_id: int = Form(...), cor: str = Form(...), ano_fabricacao: int = Form(...), ano_modelo: int = Form(...), 
                           valor: float = Form(...), placa: str = Form(...), vendido: bool = Form(...)):
    atualizacao = 'UPDATE VEICULO SET MOD_ID = $1, COR = $2, ANO_FABRICACAO = $3, ANO_MODELO = $4, VALOR = $5, PLACA = $6, VENDIDO = $7 WHERE VEIC_ID = $8'
    await bd.execute(atualizacao, mod_id, cor, ano_fabricacao, ano_modelo, valor, placa, vendido, veic_id)


@app.get('/detalhar_veiculo/{veic_id}')
async def detalhar_veiculo(request: Request, veic_id: str):
    veiculo_a_detalhar = None
    veiculos = await bd.fetch('SELECT * FROM VEICULO')

    for veiculo in veiculos: 
        if veiculo['veic_id'] == int(veic_id):
            veiculo_a_detalhar = veiculo

    if veiculo_a_detalhar is None:
        return templates.TemplateResponse(
            request, '404.html'
        )
    
    return templates.TemplateResponse(
        request, 'detalhar_veiculo.html', context={'veiculo': veiculo_a_detalhar}
    )

@app.get('/remover_veiculo/{veic_id}')
async def remover_form(request: Request, veic_id: str):
    veiculo_a_remover = None
    veiculos = await bd.fetch('SELECT * FROM VEICULO')

    for veiculo in veiculos: 
        if veiculo['veic_id'] == int(veic_id):
            veiculo_a_remover = veiculo

    if veiculo_a_remover is None:
        return templates.TemplateResponse(
            request, '404.html'
        )
    
    return templates.TemplateResponse(
        request, 'remover_veiculo.html', context={'veiculo': veiculo_a_remover}
    )

@app.post('/remover_salvar_veiculo/{veic_id}')
async def remover_veiculo(veic_id: int):
    delecao = 'DELETE FROM VEICULO WHERE VEIc_ID = $1'
    await bd.execute(delecao, veic_id)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=10000)