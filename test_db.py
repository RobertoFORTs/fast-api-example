from simple_api.infra.db import engine
from simple_api.core.logging import log

try:
    conn = engine.connect()
    log.info("Conexão com o DB bem-sucedida!")
    conn.close()
except Exception as e:
    log.info("Erro ao conectar:", e)