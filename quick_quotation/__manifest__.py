{
  "name"                 :  "Quick Quotation",
  "summary"              :  """This module create a quotation in quick mode.""",
  "category"             :  "Sales",
  "version"              :  "14.0.0.0",
  "sequence"             :  "10",
  "author"               :  "Phidias",
  "license"              :  "Other proprietary",
  "website"              :  "https://www.phidias.fr",
  "description"          :  """This module create a quotation in quick mode.""",
  "depends"              :  [
                             'barcodes',
                             'sale_management',
                            ],
  "data"                 :  [
    'views/sale_views.xml',
    'wizard/order_line_qty.xml',
    'security/ir.model.access.csv',
    'views/barcode_templates.xml',
  ],
  "application"          :  False,
}