from odoo import models, fields, api
from datetime import date


class GearGuardMaintenanceRequest(models.Model):
    _name = "gearguard.maintenance.request"
    _description = "Maintenance Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "id desc"

    # ------------------------------------------------------------
    # BASIC INFO
    # ------------------------------------------------------------

    name = fields.Char(
        string="Request Title",
        required=True,
        tracking=True,
    )

    request_type = fields.Selection(
        [
            ("corrective", "Corrective"),
            ("preventive", "Preventive"),
        ],
        default="corrective",
        tracking=True,
        required=True,
    )

    priority = fields.Selection(
        [
            ("0", "Low"),
            ("1", "Normal"),
            ("2", "High"),
            ("3", "Urgent"),
        ],
        default="1",
        tracking=True,
    )

    description = fields.Text(
        string="Problem Description"
    )

    solution = fields.Text(
        string="Solution / Work Done"
    )

    # ------------------------------------------------------------
    # RELATIONS
    # ------------------------------------------------------------

    equipment_id = fields.Many2one(
        "gearguard.maintenance.equipment",
        string="Equipment",
        required=True,
        ondelete="cascade",
    )

    maintenance_team_id = fields.Many2one(
        "gearguard.maintenance.team",
        string="Maintenance Team",
        ondelete="set null",
    )

    technician_id = fields.Many2one(
        "res.users",
        string="Technician",
        tracking=True,
    )

    # ------------------------------------------------------------
    # DATES & STATUS
    # ------------------------------------------------------------

    request_date = fields.Date(
        default=fields.Date.context_today,
        string="Request Date",
    )

    scheduled_date = fields.Date(
        string="Scheduled Date"
    )

    is_closed = fields.Boolean(
        default=False,
        tracking=True,
    )

    kanban_state = fields.Selection(
        [
            ("normal", "In Progress"),
            ("done", "Done"),
            ("blocked", "Blocked"),
        ],
        default="normal",
        tracking=True,
    )

    # ------------------------------------------------------------
    # COMPUTED FLAGS
    # ------------------------------------------------------------

    is_overdue = fields.Boolean(
        compute="_compute_is_overdue",
        store=True,
    )

    # ------------------------------------------------------------
    # COMPUTES
    # ------------------------------------------------------------

    @api.depends("scheduled_date", "is_closed")
    def _compute_is_overdue(self):
        today = date.today()
        for record in self:
            record.is_overdue = bool(
                record.scheduled_date
                and record.scheduled_date < today
                and not record.is_closed
            )

    # ------------------------------------------------------------
    # ACTIONS (USED IN VIEWS)
    # ------------------------------------------------------------

    def action_mark_done(self):
        for record in self:
            record.is_closed = True
            record.kanban_state = "done"
