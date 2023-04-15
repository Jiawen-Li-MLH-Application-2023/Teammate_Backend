from flask import Flask, Response, request
from datetime import datetime
import json
from team_resource import TeamResource
from flask_cors import CORS

# Create the Flask application object.
app = Flask(__name__)

CORS(app)


@app.route("/", methods = ['GET'])
def init():
    return "hello world"

@app.get("/api/health")
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "F22-Starter-Microservice",
        "health": "Good",
        "at time": t
    }

    # DFF TODO Explain status codes, content type, ... ...
    result = Response(json.dumps(msg), status=200, content_type="application/json")

    return result


@app.route("/team/", methods=["GET"])
def browse_all_team(course_id = "", limit = "", offset = ""):
    print(request.args)
    if "course_id" in request.args and "limit" in request.args and "offset" in request.args:
        course_id, limit, offset = request.args['course_id'], request.args['limit'], request.args['offset']
    print(course_id, limit, offset)
    result = TeamResource.browse_all_team(course_id, limit, offset)
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp

@app.route("/team/info/", methods=["get"])
def browse_team_info_by_input(course_id = "", team_captain_uni = ""):
    if "course_id" in request.args and "team_captain_uni" in request.args:
        course_id, team_captain_uni = request.args['course_id'], request.args['team_captain_uni']
    result = TeamResource.browse_team_info_by_input(course_id, team_captain_uni)
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp

@app.route("/team/add/",methods=["POST", "GET"])
def add_team():
    if request.is_json:
        try:
            request_data = request.get_json()
        except ValueError:
            return Response("[COURSE] UNABLE TO RETRIEVE REQUEST", status=400, content_type="text/plain")
    else:
        return Response("[COURSE] INVALID POST FORMAT: SHOULD BE JSON", status=400, content_type="text/plain")
    if not request_data:
        rsp = Response("[COURSE] INVALID INPUT", status=404, content_type="text/plain")
        return rsp
    team_name, team_captain_uni, team_captain, course_id, number_needed, team_message = request_data['team_name'], request_data['team_captain_uni'], request_data['team_captain'], request_data['course_id'], request_data['number_needed'], request_data['team_message']
    result, message = TeamResource.add_team(team_name, team_captain_uni, team_captain, course_id, number_needed, team_message)
    if result:
        rsp = Response("Team CREATED", status=200, content_type="text/plain")
    else:
        rsp = Response(message, status=404, content_type="text/plain")
    return rsp

@app.route("/team/edit/",methods=["POST", "GET"])
def edit_team():
    if request.is_json:
        try:
            request_data = request.get_json()
        except ValueError:
            return Response("[COURSE] UNABLE TO RETRIEVE REQUEST", status=400, content_type="text/plain")
    else:
        return Response("[COURSE] INVALID POST FORMAT: SHOULD BE JSON", status=400, content_type="text/plain")
    if not request_data:
        rsp = Response("[COURSE] INVALID INPUT", status=404, content_type="text/plain")
        return rsp
    team_name, team_captain_uni, team_captain, course_id, number_needed, team_message = request_data['team_name'], request_data['team_captain_uni'], request_data['team_captain'], request_data['course_id'], request_data['number_needed'], request_data['team_message']
    result= TeamResource.edit_team(team_name, team_captain_uni, team_captain, course_id, number_needed, team_message)
    if result:
        rsp = Response("Team UPDATED", status=200, content_type="text/plain")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp

@app.route("/team/delete/", methods=["POST", "GET"])
def delete_team():
    if request.is_json:
        try:
            request_data = request.get_json()
        except ValueError:
            return Response("[COURSE] UNABLE TO RETRIEVE REQUEST", status=400, content_type="text/plain")
    else:
        return Response("[COURSE] INVALID POST FORMAT: SHOULD BE JSON", status=400, content_type="text/plain")
    if not request_data:
        rsp = Response("[COURSE] INVALID INPUT", status=404, content_type="text/plain")
        return rsp
    team_captain_uni, course_id, team_id = request_data["team_captain_uni"], request_data["course_id"], request_data["team_id"]
    result = TeamResource.delete_team(team_captain_uni, course_id, team_id)
    if result:
        rsp = Response("DELETE SUCCESS", status=200, content_type="application.json")
    else:
        rsp = Response("No existed Preference is found!", status=404, content_type="text/plain")
    return rsp

@app.route("/team/team_member/", methods=["get"])
def browse_all_team_member(team_id = "", course_id = ""):
    if "course_id" in request.args and "team_id" in request.args:
        course_id, team_id = request.args['course_id'], request.args['team_id']
    result = TeamResource.get_all_team_member(team_id, course_id)
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp

@app.route("/team/add_member/", methods=["POST"])
def add_team_member():
    if request.is_json:
        try:
            request_data = request.get_json()
        except ValueError:
            return Response("[COURSE] UNABLE TO RETRIEVE REQUEST", status=400, content_type="text/plain")
    else:
        return Response("[COURSE] INVALID POST FORMAT: SHOULD BE JSON", status=400, content_type="text/plain")
    if not request_data:
        rsp = Response("[COURSE] INVALID INPUT", status=404, content_type="text/plain")
        return rsp
    uni, student_name, team_id, course_id = request_data["uni"], request_data["student_name"], request_data["team_id"], request_data["course_id"]
    result, message = TeamResource.add_team_member(uni, student_name, team_id, course_id)
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response(message, status=404, content_type="text/plain")
    return rsp

@app.route("/team/delete_member/",methods=["POST"])
def delete_team_member():
    if request.is_json:
        try:
            request_data = request.get_json()
        except ValueError:
            return Response("[COURSE] UNABLE TO RETRIEVE REQUEST", status=400, content_type="text/plain")
    else:
        return Response("[COURSE] INVALID POST FORMAT: SHOULD BE JSON", status=400, content_type="text/plain")
    if not request_data:
        rsp = Response("[COURSE] INVALID INPUT", status=404, content_type="text/plain")
        return rsp
    uni, team_id, course_id = request_data["uni"], request_data["team_id"], request_data["course_id"]
    print(uni, team_id, course_id)
    result = TeamResource.delete_team_member(uni, team_id, course_id)
    if result:
        rsp = Response("DELETE SUCCESS", status=200, content_type="application.json")
    else:
        rsp = Response("No existed Preference is found!", status=404, content_type="text/plain")
    return rsp


@app.route("/team/find_my_teammate/", methods=["get"])
def find_my_teammate(dept = "", timezone = ""):
    if "dept" in request.args and "timezone" in request.args:
        dept, timezone = request.args['dept'], request.args['timezone']
    result = TeamResource.find_my_teammate(dept, timezone)
    print(result)
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp


app.run(host="0.0.0.0", port=2233)
