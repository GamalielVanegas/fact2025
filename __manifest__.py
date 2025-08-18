{
  "name": "DTE El Salvador",
  "version": "17.0.0.0.1",
  "author": "Tu Empresa",
  "category": "Accounting",
  "summary": "Integración DTE MH El Salvador",
  "depends": ["base", "account", "mail"],
  "data": [
    "security/ir.model.access.csv",
    "data/ir_sequence_data.xml",
    "views/dte_config_views.xml",
    "data/cat_forma_pago.xml",
    "data/cat_plazo.xml",
    "data/cat_uom.xml",
    "data/cat_tributo.xml"
  ],
  "installable": True,
  "application": False,
  "license": "OPL-1"
}
