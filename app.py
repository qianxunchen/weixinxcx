from models.base import create_app
from app.view import api as v
from app.user import user as U
from app.sales import salesapi as S
from app.purchase import purapi as P

app = create_app()

app.register_blueprint(v)
app.register_blueprint(U)
app.register_blueprint(S)
app.register_blueprint(P)


if __name__ == "__main__":
    app.run(debug=True)

