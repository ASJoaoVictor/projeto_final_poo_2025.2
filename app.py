from flask import Flask, redirect
from routes.auth_route import auth_bp

app = Flask(__name__)
app.register_blueprint(auth_bp)

@app.route("/")
def default():
    return redirect("/auth/login")

if __name__ == "__main__":
    app.run(debug=True)