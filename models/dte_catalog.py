# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DteCatalog(models.Model):
    _name = "dte.sv.catalog"
    _description = "Catálogos DTE SV"
    _rec_name = "display_name"

    type = fields.Char(required=True, index=True)
    code = fields.Char(required=True, index=True)
    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    display_name = fields.Char(compute="_compute_display_name", store=False)

    _sql_constraints = [
        ("uniq_type_code", "unique(type, code)", "Código ya existe para este catálogo."),
    ]

    @api.depends("type", "code", "name")
    def _compute_display_name(self):
        for r in self:
            r.display_name = f"[{r.type}:{r.code}] {r.name}" if r.type and r.code else (r.name or "")
