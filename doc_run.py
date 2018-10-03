import os

from flagger import Swagger

from run import create_app

app = create_app(os.getenv("APP_SETTINGS") or "default")

swagger = Swagger(app)


app.route('api/v2/menu', methods=['GET'])


def get():
    """ get menu.
    ---
    parameters:
        - name: token
        in: path
        type: string
        required = True
"""


@app.route('/')
def hello_world():
    "test that flask app is running"
    return "To view the docs visit: https://fasty-v2.herokuapp.com/apidocs"


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
app.run('0.0.0.0', port=port)
