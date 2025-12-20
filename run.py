# -*- coding: utf-8 -*-
"""Script para iniciar o dashboard do Robo Trade"""
import os

if __name__ == "__main__":
    from robo_trade.dashboard import app
    
    # Configurações de ambiente
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("DEBUG", "false").lower() in ("1", "true", "yes")
    
    app.run(host=host, port=port, debug=debug)
