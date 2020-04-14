from flask import Flask, jsonify, request
from flask import current_app as app
from .models import db, Action, User
import datetime
from collections import defaultdict
from typing import List

### API URL's
BASE_URL = "/api/v1/"

LOG_URL = "log/"
RETRIEVE_URL = "retrieve/"

### Parameters
USER_ID_PARAM = "userId"
SESSION_ID_PARAM = "sessionId"
ACTIONS_PARAM = "actions"
TIME_PARAM = "time"
START_PARAM = "start"
END_PARAM = "end"
LOG_TYPE_PARAM = "type"
PROPERTIES_PARAM = "properties"
LOGS_PARAM = "logs"
STATUS_PARAM = "status"

### Status
SUCCESS_STATUS = "success"
FAILED_STATUS = "failed"
USER_EXISTS_STATUS = "User already exists"

### API
@app.route(BASE_URL+LOG_URL, methods=["POST"], strict_slashes=False)
def log():
    # TODO: Normally there would be an API key parameter for authorizing the requests (Returns Unauthorized request 401 if API key is invalid)
    # TODO: Hasn't been added for sake of time
    resJson = request.get_json()
    if resJson:
        userId = resJson[USER_ID_PARAM]
        sessionId = resJson[SESSION_ID_PARAM]
        actions = list(resJson[ACTIONS_PARAM])
        if userId and sessionId:
            existingUser = User.query.filter(User.username == userId).first()
            if existingUser:
                for act in actions:
                    time = act[TIME_PARAM]
                    logType = act[LOG_TYPE_PARAM]
                    properties = act[PROPERTIES_PARAM]
                    if time and logType and properties:
                        try:
                            isoTime = datetime.datetime.fromisoformat(act[TIME_PARAM].replace('Z', '+00:00'))
                            # TODO: DO we need to validate certain log types?
                            newAction = Action(logType, existingUser.id, sessionId, properties, isoTime)
                            db.session.add(newAction)
                            db.session.commit()
                        except:
                            return jsonify({STATUS_PARAM: FAILED_STATUS}), 400
                    else:
                        return jsonify({STATUS_PARAM: FAILED_STATUS}), 400
                return jsonify({STATUS_PARAM: SUCCESS_STATUS}), 201

    return jsonify({STATUS_PARAM: FAILED_STATUS}), 400

@app.route(BASE_URL+RETRIEVE_URL, methods=["GET"], strict_slashes=False)
def retrieve():

    def _constructJSONLogs(actions: List[Action]):
        for action in actions:
            res[(action.user.username, action.sessionId)].append({
                TIME_PARAM: datetime.datetime.isoformat(action.date),
                LOG_TYPE_PARAM: action.logType,
                PROPERTIES_PARAM: action.properties
            })

        listRes = [{
            USER_ID_PARAM: key[0],
            SESSION_ID_PARAM: key[1],
            ACTIONS_PARAM: val
        } for key, val in res.items()]
        return jsonify({
            STATUS_PARAM: SUCCESS_STATUS,
            LOGS_PARAM: listRes
        })

    # TODO: Normally there would be an API key parameter for authorizing the requests (Returns Unauthorized request 401 if API key is invalid)
    # TODO: Hasn't been added for sake of time
    userId = request.args.get(USER_ID_PARAM)
    start = request.args.get(START_PARAM)
    end = request.args.get(END_PARAM)
    logType = request.args.get(LOG_TYPE_PARAM)
    res = defaultdict(list)

    existingUser = None
    if userId: 
        existingUser = User.query.filter(User.username == userId).first()
    query = Action.query
    if existingUser: 
        query = query.filter(Action.userId == existingUser.id)
    if start:
        try: 
            isoStart = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
            query = query.filter(Action.date >= isoStart)
        except:
            return jsonify({STATUS_PARAM: FAILED_STATUS}), 400
    if end:
        try:
            isoEnd =  datetime.datetime.fromisoformat(end.replace('Z', '+00:00'))
            query =  query.filter(Action.date <= isoEnd)
        except:
            return jsonify({STATUS_PARAM: FAILED_STATUS}), 400
    if logType:
        query = query.filter(Action.logType == logType)
    actions = query.all()

    return _constructJSONLogs(actions), 200



### TEST/DUMMY API for adding users
### NOT AN ACTUAL API FOR PRODUCTION
@app.route(BASE_URL+"testuser", methods=["POST"], strict_slashes=False)
def createTestUser():
    username = request.form[USER_ID_PARAM]
    if username:
        existingUser = User.query.filter(User.username == username).first()
        if not existingUser:
            newUser = User(username)
            db.session.add(newUser)
            db.session.commit()
            return jsonify({STATUS_PARAM: SUCCESS_STATUS}), 201
        else:
            return jsonify({STATUS_PARAM: USER_EXISTS_STATUS}), 200
    else:
        return jsonify({STATUS_PARAM: FAILED_STATUS}), 400


@app.route(BASE_URL+"testusers", methods=["POST"], strict_slashes=False)
def createTestUsers():
    resJson = request.get_json()
    if resJson:
        users = resJson["users"]
        for user in users:
            userId = user[USER_ID_PARAM]
            if userId:
                existingUser = User.query.filter(User.username == userId).first()
                if not existingUser:
                    newUser = User(userId)
                    db.session.add(newUser)
        db.session.commit()
        return jsonify({STATUS_PARAM: SUCCESS_STATUS}), 201
    else:
        return jsonify({STATUS_PARAM: FAILED_STATUS}), 400
