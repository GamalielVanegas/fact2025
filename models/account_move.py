# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = "account.move"

    dte_version = fields.Integer(default=2)
    dte_codigo_generacion = fields.Char(readonly=True, copy=False)
    dte_numero_control = fields.Char(readonly=True, copy=False)
    dte_sello = fields.Char(readonly=True, copy=False)
    dte_estado = fields.Char(readonly=True, copy=False)
    dte_last_response = fields.Text(readonly=True, copy=False)

    def action_post(self):
        res = super().action_post()
        ICP = self.env["ir.config_parameter"].sudo()
        # Si no hay firmador configurado, no intentamos nada (evita errores al inicio)
        if not ICP.get_param("dte_sv.firmador_url"):
            return res
        for move in self:
            if move.move_type != "out_invoice":
                continue
            try:
                builder = self.env["dte.sv.builder"]
                dte = builder.build_fe_from_move(move, version=move.dte_version)
                jws = self.env["dte.sv.signer"].sign(dte)
                api = self.env["dte.sv.api"]
                r = api.send_one("01", jws, dte["identificacion"]["codigoGeneracion"],
                                 version=dte["identificacion"]["version"],
                                 ambiente=dte["identificacion"]["ambiente"])
                move.write({
                    "dte_sello": r.get("selloRecibido"),
                    "dte_estado": r.get("estado") or "ENVIADO",
                    "dte_last_response": str(r),
                })
                move.message_post(body=_("DTE enviado a MH. Estado: %s") % (r.get("estado") or "N/A"))
            except Exception as e:
                _logger.exception("Error enviando DTE")
                move.write({
                    "dte_estado": "ERROR",
                    "dte_last_response": str(e),
                })
                move.message_post(body=_("Error DTE: %s") % str(e))
        return res
