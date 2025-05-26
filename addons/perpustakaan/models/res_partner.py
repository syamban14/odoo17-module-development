from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_anggota_perpustakaan = fields.Boolean(string='Anggota Perpustakaan')
    # no_anggota = fields.Char(string='No Anggota', readonly=True)
    # tanggal_daftar = fields.Date(string='Tanggal Daftar', readonly=True)
    # buku_ids = fields.One2many('perpustakaan.buku', 'partner_id', string='Buku Pinjaman')