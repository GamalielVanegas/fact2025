# -*- coding: utf-8 -*-
import uuid
from datetime import datetime
from odoo.tools import float_round

def _get_icp(env):
    return env["ir.config_parameter"].sudo()

def numero_control(env, tipo_dte: str) -> str:
    """DTE-<tipo>-<casa+punto(8)>-<secuencial(15)>"""
    ICP = _get_icp(env)
    serie = (ICP.get_param("dte_sv.control_serie") or "00000000").strip()
    if len(serie) != 8 or not serie.isdigit():
        serie = "00000000"
    seq = env["ir.sequence"].next_by_code("dte.sv.control") or "1"
    sec = str(seq).zfill(15)
    return f"DTE-{tipo_dte}-{serie}-{sec}"

def identificacion(env, move, tipo_dte="01", version=2):
    ICP = _get_icp(env)
    amb = (ICP.get_param("dte_sv.ambiente") or "00").strip()
    fec = (move.invoice_date or datetime.utcnow().date()).strftime("%Y-%m-%d")
    hor = datetime.utcnow().strftime("%H:%M:%S")
    if not move.dte_codigo_generacion:
        move.dte_codigo_generacion = str(uuid.uuid4())
    if not move.dte_numero_control:
        move.dte_numero_control = numero_control(env, tipo_dte)
    return {
        "version": version,
        "ambiente": amb,
        "tipoDte": tipo_dte,
        "numeroControl": move.dte_numero_control,
        "codigoGeneracion": move.dte_codigo_generacion,
        "tipoModelo": 1,
        "tipoOperacion": 1,
        "fecEmi": fec,
        "horEmi": hor,
        "tipoMoneda": (move.currency_id and move.currency_id.name) or "USD",
    }

def emisor(env, company):
    ICP = _get_icp(env)
    return {
        "nit": ICP.get_param("dte_sv.api_user") or (company.vat or ""),
        "nrc": ICP.get_param("dte_sv.emisor_nrc") or "",
        "nombre": company.name or "",
        "codActividad": ICP.get_param("dte_sv.emisor_cod_actividad") or "",
        "descActividad": ICP.get_param("dte_sv.emisor_desc_actividad") or "",
        "nombreComercial": ICP.get_param("dte_sv.emisor_nombre_comercial") or (company.name or ""),
        "tipoEstablecimiento": ICP.get_param("dte_sv.emisor_tipo_establecimiento") or "01",
        "direccion": {
            "departamento": ICP.get_param("dte_sv.emisor_departamento") or "06",
            "municipio": ICP.get_param("dte_sv.emisor_municipio") or "14",
            "complemento": ICP.get_param("dte_sv.emisor_dir_complemento") or "",
        },
        "telefono": ICP.get_param("dte_sv.emisor_telefono") or "",
        "correo": ICP.get_param("dte_sv.emisor_correo") or "",
        "codEstableMH": None, "codEstable": None, "codPuntoVentaMH": None, "codPuntoVenta": None,
    }

def receptor(move):
    p = move.partner_id
    addr = (p.contact_address or p.street or "")[:100] if p else ""
    return {
        "nombre": (p.display_name if p else "CONSUMIDOR FINAL") or "CONSUMIDOR FINAL",
        "direccion": {"departamento": "06", "municipio": "14", "complemento": addr},
    }

def cuerpo_documento(move):
    items = []
    i = 1
    for line in move.invoice_line_ids:
        qty = line.quantity or 0.0
        price = line.price_unit or 0.0
        gravada = float_round(qty * price, 2)
        items.append({
            "numItem": i, "tipoItem": 1,
            "codigo": line.product_id.default_code or "",
            "descripcion": (line.name or line.product_id.display_name or "Línea")[:180],
            "cantidad": qty, "uniMedida": 59,
            "precioUni": price, "montoDescu": 0.0,
            "ventaNoSuj": 0.0, "ventaExenta": 0.0, "ventaGravada": gravada,
        })
        i += 1
    if not items:
        items.append({
            "numItem": 1, "tipoItem": 1,
            "codigo": "SKU-001", "descripcion": "Servicio",
            "cantidad": 1, "uniMedida": 59, "precioUni": 10.0, "montoDescu": 0.0,
            "ventaNoSuj": 0.0, "ventaExenta": 0.0, "ventaGravada": 10.0,
        })
    return items

def resumen(move):
    items = cuerpo_documento(move)
    total_gravada = float_round(sum(i["ventaGravada"] for i in items), 2)
    iva = float_round(total_gravada * 0.13, 2)
    total = float_round(total_gravada + iva, 2)
    return {
        "totalNoSuj": 0.0, "totalExenta": 0.0, "totalGravada": total_gravada,
        "subTotalVentas": total_gravada,
        "descuNoSuj": 0.0, "descuExenta": 0.0, "descuGravada": 0.0,
        "porcentajeDescuento": 0.0, "totalDescu": 0.0,
        "tributos": [{"codigo": "20", "descripcion": "IVA", "valor": iva}],
        "totalIva": iva, "saldoFavor": 0.0, "condicionOpera": "1",
        "totalNoGravado": 0.0, "totalPagar": total, "montoTotalOperacion": total,
        "pagoReserva": 0.0, "totalSujetoRetencion": 0.0, "totalIVAretenido": 0.0, "totalPagoSinEfectivo": 0.0,
        "formaPago": [{"codigo":"01","monto": total}],
    }
