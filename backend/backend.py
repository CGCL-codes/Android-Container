from flask import Flask, request, send_from_directory
from image_migrate import *
from container_migrate import *
from json import *

app = Flask(__name__)


@app.route('/migrate/container', methods=["GET"])
def container_migrate():
    container_id = request.args.get("container_id")
    checkpoint_name = request.args.get("checkpoint_name")
    res = {}
    path = migrate(container_id,checkpoint_name)
    res['code'] = 0
    res['path'] = path
    return json.dumps(res,ensure_ascii=False)


@app.route('/migrate/image', methods=["GET"])
def image_migrate():
    container_id = request.args.get("container_id")
    repository = request.args.get("repository")
    tag = request.args.get("tag")
    res = {}
    path = get_target_tar(container_id, repository, tag)
    res['code'] = 1
    res['path'] = path
    return json.dumps(res,ensure_ascii=False)

@app.route('/hello', methods=["GET"])
def hello():
    return "hello world!"


if __name__ == "__main__":
    start_nginx()
    app.run(host='192.168.0.239', port=8081)
