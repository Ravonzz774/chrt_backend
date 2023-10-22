from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "your_secret_key"

# Настройки для Flask-Cookie
app.config["SESSION_COOKIE_NAME"] = "chrt_timetable_session_cookie"
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Strict"
app.config["SESSION_COOKIE_SECURE"] = True

db = SQLAlchemy(app)
serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    groups = db.Column(db.PickleType, nullable=True, default=[])


valid_groups = [
    "1263",
    "1264",
    "1259",
    "1260",
    "1262",
    "1265",
    "1257",
    "1258",
    "1261",
    "1245",
    "1227",
    "1229",
    "1221",
    "1243",
    "1220",
    "1246",
    "1230",
    "1228",
    "1244",
    "1253",
    "1254",
    "1232",
    "1233",
    "1223",
    "1222",
    "1255",
    "1231",
    "1234",
    "1256",
    "1249",
    "1250",
    "1238",
    "1224",
    "1237",
    "1235",
    "1236",
    "1251",
    "1252",
    "1239",
    "1240",
]


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Missing required fields"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400

    hashed_password = generate_password_hash(password)

    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    # Создаем куки с идентификатором пользователя
    response = jsonify({"message": "Registration successful."})
    session_token = serializer.dumps(new_user.id)
    response.set_cookie(
        "session_token", session_token, httponly=True, secure=True, samesite="Strict"
    )
    return response


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid username or password"}), 401

    # Создаем куки с идентификатором пользователя
    response = jsonify({"message": "Login successful."})
    session_token = serializer.dumps(user.id)
    response.set_cookie(
        "session_token", session_token, httponly=True, secure=True, samesite="Strict"
    )
    return response


@app.route("/api/logout", methods=["POST"])
def logout():
    # Удаляем куки с идентификатором пользователя
    response = jsonify({"message": "Logout successful."})
    response.delete_cookie("session_token")
    return response


@app.route("/api/profile", methods=["GET"])
def profile():
    # Получаем идентификатор пользователя из куки
    session_token = request.cookies.get("session_token")

    if not session_token:
        return jsonify({"message": "Unauthorized"}), 401

    try:
        user_id = serializer.loads(session_token, max_age=3600)
        user = User.query.get(user_id)
        if not user:
            raise Exception()

        return jsonify(
            {
                "message": "Profile page",
                "username": user.username,
                "groups": user.groups,
            }
        )
    except SignatureExpired:
        return jsonify({"message": "Session expired"}), 401
    except Exception:
        return jsonify({"message": "Invalid session"}), 401


@app.route("/api/groups", methods=["POST"])
def select_groups():
    data = request.get_json()
    groups = data.get("groups")

    if not groups:
        return jsonify({"message": "Missing groups list"}), 400

    # Check if all selected groups are valid

    invalid_groups = [group for group in groups if group not in valid_groups]

    if invalid_groups:
        return (
            jsonify(
                {
                    "message": "Invalid groups: {}".format(
                        ", ".join(str(group) for group in invalid_groups)
                    )
                }
            ),
            400,
        )

    # Получаем идентификатор пользователя из куки
    session_token = request.cookies.get("session_token")

    if not session_token:
        return jsonify({"message": "Unauthorized"}), 401

    try:
        user_id = serializer.loads(session_token, max_age=3600)
        user = User.query.get(user_id)
        if not user:
            raise Exception()

        # Обновляем список групп пользователя
        user.groups = list(set(user.groups + groups))  # Combine and remove duplicates
        db.session.commit()

        return jsonify({"message": "Groups selected successfully."})
    except SignatureExpired:
        return jsonify({"message": "Session expired"}), 401
    except Exception:
        return jsonify({"message": "Invalid session"}), 401


@app.route("/api/my_groups", methods=["GET"])
def get_my_groups():
    # Получаем идентификатор пользователя из куки
    session_token = request.cookies.get("session_token")

    if not session_token:
        return jsonify({"message": "Unauthorized"}), 401

    try:
        user_id = serializer.loads(session_token, max_age=3600)
        user = User.query.get(user_id)
        if not user:
            raise Exception()

        return jsonify({"message": "User's groups", "groups": user.groups})
    except SignatureExpired:
        return jsonify({"message": "Session expired"}), 401
    except Exception:
        return jsonify({"message": "Invalid session"}), 401


@app.route("/api/delete_groups", methods=["POST"])
def delete_groups():
    data = request.get_json()
    groups = data.get("groups")

    if not groups:
        return jsonify({"message": "Missing groups list"}), 400

    # Получаем идентификатор пользователя из куки
    session_token = request.cookies.get("session_token")

    if not session_token:
        return jsonify({"message": "Unauthorized"}), 401

    try:
        user_id = serializer.loads(session_token, max_age=3600)
        user = User.query.get(user_id)
        if not user:
            raise Exception()

        # Удаляем выбранные группы из списка групп пользователя
        user.groups = [group for group in user.groups if group not in groups]
        db.session.commit()

        return jsonify({"message": "Groups deleted successfully."})
    except SignatureExpired:
        return jsonify({"message": "Session expired"}), 401
    except Exception:
        return jsonify({"message": "Invalid session"}), 401


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
