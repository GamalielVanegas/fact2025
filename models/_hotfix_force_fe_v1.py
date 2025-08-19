# -*- coding: utf-8 -*-
import logging
from odoo import models

_logger = logging.getLogger(__name__)

class DteBuilderForceV1(models.Model):
    _inherit = "dte.sv.builder"

    def build_fe_from_move(self, move, version=None, *args, **kwargs):
        # Fuerza v1 para FE (tipoDte=01)
        version = 1
        dte = super().build_fe_from_move(move, version=version, *args, **kwargs)
        try:
            if isinstance(dte, dict):
                dte.setdefault("identificacion", {})["version"] = 1
            _logger.info("dte_sv.force_v1: build_fe_from_move -> version=1 aplicada")
        except Exception:
            _logger.exception("dte_sv.force_v1: no se pudo asegurar identificacion.version=1")
        return dte
