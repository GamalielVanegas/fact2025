# -*- coding: utf-8 -*-
import logging
from odoo import models

_logger = logging.getLogger(__name__)

class DteApiForceV1(models.Model):
    _inherit = "dte.sv.api"

    def send_fe(self, dte, *args, **kwargs):
        try:
            if isinstance(dte, dict):
                dte.setdefault("identificacion", {})["version"] = 1
            _logger.info("dte_sv.force_v1: send_fe -> version=1 aplicada justo antes de enviar")
        except Exception:
            _logger.exception("dte_sv.force_v1: send_fe no pudo fijar version=1")
        return super().send_fe(dte, *args, **kwargs)
