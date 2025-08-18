# -*- coding: utf-8 -*-
from odoo import models, fields

class ResConfigSettingsDTE(models.TransientModel):
    _inherit = "res.config.settings"

    # Firmador / Autenticación
    dte_firmador_url = fields.Char("URL Firmador", config_parameter="dte_sv.firmador_url")
    dte_api_user = fields.Char("Usuario (NIT)", config_parameter="dte_sv.api_user")
    dte_api_password = fields.Char("Password API", config_parameter="dte_sv.api_password")
    dte_key_pass = fields.Char("Password .key", config_parameter="dte_sv.key_pass")
    dte_env_url_prueba = fields.Char("API Pruebas", config_parameter="dte_sv.env_url_prueba")
    dte_env_url_prod = fields.Char("API Producción", config_parameter="dte_sv.env_url_prod")
    dte_timeout = fields.Integer("Timeout (s)", default=30, config_parameter="dte_sv.timeout")

    # Emisor
    dte_emisor_nrc = fields.Char("NRC", config_parameter="dte_sv.emisor_nrc")
    dte_emisor_cod_actividad = fields.Char("Código Actividad", config_parameter="dte_sv.emisor_cod_actividad")
    dte_emisor_desc_actividad = fields.Char("Descripción Actividad", config_parameter="dte_sv.emisor_desc_actividad")
    dte_emisor_nombre_comercial = fields.Char("Nombre Comercial", config_parameter="dte_sv.emisor_nombre_comercial")
    dte_emisor_tipo_establecimiento = fields.Char("Tipo Establecimiento", config_parameter="dte_sv.emisor_tipo_establecimiento")
    dte_emisor_departamento = fields.Char("Departamento", config_parameter="dte_sv.emisor_departamento")
    dte_emisor_municipio = fields.Char("Municipio", config_parameter="dte_sv.emisor_municipio")
    dte_emisor_dir_complemento = fields.Char("Dirección (complemento)", config_parameter="dte_sv.emisor_dir_complemento")
    dte_emisor_telefono = fields.Char("Teléfono", config_parameter="dte_sv.emisor_telefono")
    dte_emisor_correo = fields.Char("Correo", config_parameter="dte_sv.emisor_correo")

    # Control/Ambiente
    dte_control_serie = fields.Char("Serie (8 dígitos casa+punto)", config_parameter="dte_sv.control_serie")
    dte_ambiente = fields.Selection(
        [("00", "Pruebas"), ("01", "Producción")],
        string="Ambiente",
        default="00",
        config_parameter="dte_sv.ambiente",
    )
