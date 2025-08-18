# -*- coding: utf-8 -*-
import logging
import requests
from odoo import models

_logger = logging.getLogger(__name__)

class DteApi(models.AbstractModel):
    _name = "dte.sv.api"
    _description = "APIs DTE SV (MH)"

    def _base_url(self):
        ICP = self.env["ir.config_parameter"].sudo()
        amb = (ICP.get_param("dte_sv.ambiente") or "00").strip()
        if amb == "01":
            base = (ICP.get_param("dte_sv.env_url_prod") or "").rstrip("/")
        else:
            base = (ICP.get_param("dte_sv.env_url_prueba") or "").rstrip("/")
        if not base:
            raise ValueError("Falta URL de entorno (prueba o prod)")
        return base

    def _authz(self):
        ICP = self.env["ir.config_parameter"].sudo()
        user = (ICP.get_param("dte_sv.api_user") or "").strip()
        pwd = ICP.get_param("dte_sv.api_password") or ""
        base = self._base_url()
        url = f"{base}/seguridad/auth"
        r = requests.post(
            url,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={"user": user, "pwd": pwd},
            timeout=int(ICP.get_param("dte_sv.timeout") or 30),
        )
        r.raise_for_status()
        data = r.json()
        token = (data.get("body") or {}).get("token") or ""
        if not token:
            raise ValueError(f"Respuesta auth inesperada: {data}")
        # Evitar 'Bearer Bearer ...'
        if token.lower().startswith("bearer "):
            return token
        return f"Bearer {token}"

    def send_one(self, tipo, jws, codigo_generacion, version=3, ambiente="00"):
        base = self._base_url()
        url = f"{base}/fesv/recepciondte"
        body = {
            "ambiente": ambiente,
            "idEnvio": 1,
            "version": version,
            "tipoDte": tipo,
            "documento": jws,
            "codigoGeneracion": codigo_generacion,
        }
        _logger.info("Enviando DTE a MH (tipo=%s cod=%s ver=%s amb=%s)", tipo, codigo_generacion, version, ambiente)
        authz = self._authz()
        r = requests.post(
            url, json=body,
            headers={"Authorization": authz, "Content-Type": "application/json"},
            timeout=int(self.env["ir.config_parameter"].sudo().get_param("dte_sv.timeout") or 30),
        )
        try:
            data = r.json()
        except Exception:
            data = {"status_code": r.status_code, "text": r.text}
        if r.status_code >= 400:
            _logger.error("Recepción MH %s: %s", r.status_code, data)
        return data
