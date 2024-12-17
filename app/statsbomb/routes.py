from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.statsbomb import statsbomb_bp
from app import db
from statsbombpy import sb

@statsbomb_bp.route("/competitions", methods=["GET"])
@jwt_required()
def get_competitions():
    dataframe = sb.competitions(fmt="dict")
    filtering_terms={"competitions": ["Champions League", "La Liga", "Copa America", "League 1", "FIFA World Cup"], "season": ["2003/2004", "2004/2005", "2005/2006", "2006/2007", "2007/2008", "2008/2009", "2009/2010", "2010/2011", "2011/2012", "2012/2013", "2013/2014", "2014/2015", "2015/2016", "2016/2017", "2017/2018", "2018/2019", "2019/2020", "2020/2021", "2018", "2020", "2024"], "gender": "male"}
    filter_competitions = lambda d: [v for k, v in d.items() if (k[1] in filtering_terms["competitions"] and k[2] in filtering_terms["season"] and k[3]==filtering_terms["gender"])]
    filtered_competitions = filter_competitions(dataframe)
    return jsonify(filtered_competitions), 200

@statsbomb_bp.route("/shots", methods=["GET"])
@jwt_required()
def get_match_shots():
    match_id = request.args.get('match')
    filter = {"id": 5503, "name":"Lionel Andrés Messi Cuccittini"}
    if match_id:
        data = sb.events(match_id=match_id, split=True)
        shots = data["shots"]
        messi_shots = shots[shots["player"] == "Lionel Andrés Messi Cuccittini"]
        messi_shots_formatted = messi_shots[["id", "timestamp", "location", "shot_statsbomb_xg", "shot_end_location", "shot_outcome", "shot_body_part", "shot_type", "under_pressure", "shot_one_on_one"]]
        return messi_shots_formatted.to_json(indent=4) 

    return jsonify({"msg": "Match not found"}), 404
    