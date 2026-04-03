from flask import Blueprint, jsonify
from app.services.dashboard_service import get_dashboard_summary
from app.middleware.auth_middleware import login_required

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/summary", methods=["GET"])
@login_required
def dashboard_summary():
    data = get_dashboard_summary()
    return jsonify(data), 200