# -*- coding: utf-8 -*-
import logging
import requests
from odoo import models, api

_logger = logging.getLogger(__name__)

class DteSigner(models.AbstractModel):
    _name = "dte.sv.signer"
    _description = "Firmador DTE SV (MH)"

    @api.model
    def sign(self, dte_dict: dict) -> str:
        """Envía el DTE sin firmar al firmador y devuelve el JWS (string)."""
        ICP = self.env["ir.config_parameter"].sudo()
        base = (ICP.get_param("dte_sv.firmador_url") or "").rstrip("/")
        nit = ICP.get_param("dte_sv.api_user")
        key_pass = ICP.get_param("dte_sv.key_pass")
        timeout = int(ICP.get_param("dte_sv.timeout") or 30)

        if not base or not nit or not key_pass:
            raise ValueError("Config incompleta: firmador_url/api_user/key_pass")

        payload = {"nit": nit, "activo": True, "passwordPri": key_pass, "dteJson": dte_dict}
        last_err = None
        for suffix in ("/firmardocumento/", "/firmardocumento"):
            url = f"{base}{suffix}"
            _logger.info("Firmando DTE con firmador MH: %s", url)
            try:
                r = requests.post(url, json=payload, timeout=timeout)
                if r.status_code == 404:
                    _logger.warning("Firmador 404 en %s, probando variante...", url)
                    continue
                r.raise_for_status()
                data = r.json()
                if data.get("status") != "OK" or not data.get("body"):
                    raise ValueError(f"Firmador rechazó la petición: {data}")
                jws = data["body"]
                _logger.info("DTE firmado OK (len=%s)", len(jws))
                return jws
            except Exception as e:
                last_err = e
                _logger.error("Error HTTP/JSON con firmador: %s", getattr(e, 'response', None) and getattr(e.response, 'text', str(e)) or str(e))
        raise last_err or ValueError("No se pudo firmar el DTE (todas las variantes fallaron)")
