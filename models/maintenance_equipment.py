from odoo import models, fields, api

class GearGuardMaintenanceEquipment(models.Model):
    _name = 'gearguard.maintenance.equipment'
    _description = 'Maintenance Equipment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    serial_number = fields.Char()
    department = fields.Char()
    maintenance_team_id = fields.Many2one('gearguard.maintenance.team')
    description = fields.Text()
    active = fields.Boolean(default=True)

    request_count = fields.Integer(
        compute='_compute_request_count',
        string='Requests'
    )

    # -------------------------
    # COMPUTE
    # -------------------------
    def _compute_request_count(self):
        Request = self.env['gearguard.maintenance.request']
        for rec in self:
            rec.request_count = Request.search_count([
                ('equipment_id', '=', rec.id)
            ])

    # -------------------------
    # BUTTON ACTION (FIX)
    # -------------------------
    def action_view_requests(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Maintenance Requests',
            'res_model': 'gearguard.maintenance.request',
            'view_mode': 'kanban,list,form',
            'domain': [('equipment_id', '=', self.id)],
            'context': {
                'default_equipment_id': self.id,
            }
        }
