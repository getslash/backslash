from flask import send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from .app import app
from flask import json, request, jsonify
from models import Session, Test

db = SQLAlchemy(app)


def session_exists(id):
    requested_session = Session.query.filter_by(session_id=id).first()
    if requested_session:
        return True
    else:
        return False

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/sessions/new", methods=['POST'])
def add_session():
    session_id = request.form['id']
    test_session = Session(session_id)
    db.session.add(test_session)
    db.session.commit()
    return json.dumps(test_session.json())

@app.route('/session/<session_id>/get_object')
def session_get_object(session_id):
    requested_session = Session.query.filter_by(session_id=session_id).first()
    return requested_session.json()

@app.route('/session/<session_id>/add_test/<test_id>')
def session_add_test(session_id, test_id):
    requested_session = Session.query.filter_by(session_id=session_id).first()
    if requested_session:
        test_obj = Test(requested_session.id, test_id)
        db.session.add(test_obj)
        db.session.commit()
        return test_obj.json()
    else:
        return jsonify({"error": "Session doesn't exist"})

@app.route('/session/<session_id>/add_userID', methods=['POST'])
def session_add_user_id(session_id):
    requested_session = Session.query.filter_by(session_id=session_id).first()
    if requested_session:
        user_id = request.form['userID']
        requested_session.user_id = user_id
        db.session.merge(requested_session)
        db.session.commit()
        return jsonify({"success": "OK"})
    else:
        return jsonify({"error": "Session doesn't exist"})

@app.route('/sessions')
def get_all_sessions():
    return jsonify(sessions=[x.serialize for x in Session.query.all()])

@app.route('/session/<session_id>/get_all_tests')
def session_get_all_tests(session_id):
    if session_exists(session_id):
        all_tests = Test.query.join(Session, session_id == Session.session_id).all()
        return jsonify(tests=[x.serialize for x in all_tests])
    else:
        return jsonify({"error": "Session doesn't exist"})

