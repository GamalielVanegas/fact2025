# -*- coding: utf-8 -*-
from . import comunes

def build_from_move(env, move, version=2):
    return {
        "identificacion": comunes.identificacion(env, move, tipo_dte="01", version=version),
        "emisor": comunes.emisor(env, move.company_id),
        "receptor": comunes.receptor(move),
        "otrosDocumentos": None,
        "ventaTercero": None,
        "cuerpoDocumento": comunes.cuerpo_documento(move),
        "resumen": comunes.resumen(move),
    }
