# register API routes
from src.api.v1.rtr_digipos import router as rtr_digipos


def register_routes(app):
    app.include_router(rtr_digipos)
    return app
