from odoo import models, fields, api

class GearGuardMaintenanceTeam(models.Model):
    _name = 'gearguard.maintenance.team'
    _description = 'Maintenance Team'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    team_leader_id = fields.Many2one('res.users')
    member_ids = fields.Many2many('res.users')
    sequence = fields.Integer(default=10)
    color = fields.Integer()
    active = fields.Boolean(default=True)

    equipment_count = fields.Integer(compute='_compute_counts')
    request_count = fields.Integer(compute='_compute_counts')
    open_request_count = fields.Integer(compute='_compute_counts')

    # -------------------------
    # COMPUTE
    # -------------------------
    def _compute_counts(self):
        Equipment = self.env['gearguard.maintenance.equipment']
        Request = self.env['gearguard.maintenance.request']

        for team in self:
            team.equipment_count = Equipment.search_count([
                ('maintenance_team_id', '=', team.id)
            ])

            team.request_count = Request.search_count([
                ('maintenance_team_id', '=', team.id)
            ])

            team.open_request_count = Request.search_count([
                ('maintenance_team_id', '=', team.id),
                ('kanban_state', '!=', 'done')
            ])

    # -------------------------
    # BUTTON ACTIONS
    # -------------------------
    def action_view_equipment(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Equipment',
            'res_model': 'gearguard.maintenance.equipment',
            'view_mode': 'list,form',
            'domain': [('maintenance_team_id', '=', self.id)],
        }

    def action_view_all_requests(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Maintenance Requests',
            'res_model': 'gearguard.maintenance.request',
            'view_mode': 'kanban,list,form',
            'domain': [('maintenance_team_id', '=', self.id)],
        }

    def action_view_open_requests(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Open Maintenance Requests',
            'res_model': 'gearguard.maintenance.request',
            'view_mode': 'kanban,list,form',
            'domain': [
                ('maintenance_team_id', '=', self.id),
                ('kanban_state', '!=', 'done'),
            ],
        }
