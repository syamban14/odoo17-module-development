from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError

class Perpustakaan(models.Model):
    _name = 'perpustakaan.buku'
    _description = 'Data Buku Perpustakaan'

    name = fields.Char(string='Judul Buku', required=True)
    penulis = fields.Char(string='Penulis')
    tahun_terbit = fields.Integer(string='Tahun Terbit')
    kategori_id = fields.Many2one('perpustakaan.kategori', string='Kategori')
    user_id = fields.Many2one('res.users', string='Pencatat Buku', default=lambda self: self.env.user)

    @api.constrains('tahun_terbit')
    def check_tahun_terbit(self):
        tahun_sekarang = datetime.now().year
        for record in self:
            if record.tahun_terbit and record.tahun_terbit > tahun_sekarang:
                raise ValidationError("Tahun terbit tidak boleh lebih dari tahun sekarang.")

class Kategori(models.Model):
    _name = 'perpustakaan.kategori'
    _description = 'Kategori Buku'

    name = fields.Char(string='Nama Kategori', required=True)
    buku_ids = fields.One2many('perpustakaan.buku', 'kategori_id', string='Buku')

class Partner(models.Model):
    _inherit = 'res.partner'

    is_anggota_perpustakaan = fields.Boolean(string='Anggota Perpustakaan')