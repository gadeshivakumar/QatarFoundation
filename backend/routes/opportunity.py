from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import Opportunity
from extensions import db

opportunity_bp = Blueprint("opportunity", __name__, url_prefix="/api/opportunities")


# CREATE OPPORTUNITY
@opportunity_bp.route("", methods=["POST"])
@login_required
def create_opportunity():
    data = request.get_json()

    try:
        opp = Opportunity(
            name=data.get("name"),
            duration=data.get("duration"),
            start_date=data.get("start_date"),
            description=data.get("description"),
            skills=",".join(data.get("skills", [])),
            category=data.get("category"),
            future_opportunities=data.get("future_opportunities"),
            max_applicants=data.get("max_applicants"),
            admin_id=current_user.id
        )

        db.session.add(opp)
        db.session.commit()

        return jsonify({"message": "Opportunity created"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# GET ALL OPPORTUNITIES (ONLY CURRENT USER)
@opportunity_bp.route("", methods=["GET"])
@login_required
def get_opportunities():
    opportunities = Opportunity.query.filter_by(admin_id=current_user.id).all()

    result = []
    for opp in opportunities:
        result.append({
            "id": opp.id,
            "name": opp.name,
            "duration": opp.duration,
            "start_date": opp.start_date,
            "description": opp.description,
            "skills": opp.skills.split(","),
            "category": opp.category,
            "future_opportunities": opp.future_opportunities,
            "max_applicants": opp.max_applicants
        })

    return jsonify(result)


# DELETE OPPORTUNITY
@opportunity_bp.route("/<int:opp_id>", methods=["DELETE"])
@login_required
def delete_opportunity(opp_id):
    opp = Opportunity.query.filter_by(id=opp_id, admin_id=current_user.id).first()

    if not opp:
        return jsonify({"error": "Not found"}), 404

    db.session.delete(opp)
    db.session.commit()

    return jsonify({"message": "Deleted successfully"})


@opportunity_bp.route("/<int:opp_id>", methods=["PUT"])
@login_required
def update_opportunity(opp_id):
    data = request.get_json()

    opp = Opportunity.query.filter_by(id=opp_id, admin_id=current_user.id).first()

    if not opp:
        return jsonify({"error": "Not found"}), 404

    # update fields
    opp.name = data.get("name", opp.name)
    opp.duration = data.get("duration", opp.duration)
    opp.start_date = data.get("start_date", opp.start_date)
    opp.description = data.get("description", opp.description)
    opp.skills = ",".join(data.get("skills", opp.skills.split(",")))
    opp.category = data.get("category", opp.category)
    opp.future_opportunities = data.get("future_opportunities", opp.future_opportunities)
    opp.max_applicants = data.get("max_applicants", opp.max_applicants)

    db.session.commit()

    return jsonify({"message": "Updated successfully"})


@opportunity_bp.route("/<int:opp_id>", methods=["GET"])
@login_required
def get_opportunity(opp_id):
    opp = Opportunity.query.filter_by(id=opp_id, admin_id=current_user.id).first()

    if not opp:
        return jsonify({"error": "Not found"}), 404

    return jsonify({
        "id": opp.id,
        "name": opp.name,
        "duration": opp.duration,
        "start_date": opp.start_date,
        "description": opp.description,
        "skills": opp.skills.split(","),
        "category": opp.category,
        "future_opportunities": opp.future_opportunities,
        "max_applicants": opp.max_applicants
    })