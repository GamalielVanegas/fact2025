# -*- coding: utf-8 -*-
from odoo import models, api

class DteBuilder(models.AbstractModel):
    _name = "dte.sv.builder"
    _description = "Builder JSON DTE"

    @api.model
    def build_fe_from_move(self, move, version=2):
        from ..dte_json_builder import fe
        return fe.build_from_move(self.env, move, version=version)
