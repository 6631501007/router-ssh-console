from flask import Flask, request, jsonify
from flask_cors import CORS
import paramiko
import time

app = Flask(__name__)
CORS(app)

import os

USERNAME = os.getenv("ROUTER_USERNAME", "admin")
PASSWORD = os.getenv("ROUTER_PASSWORD", "cisco")


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "Backend is running"
    })


@app.route("/api/execute", methods=["POST"])
def execute_command():

    data = request.get_json()

    router_ip = data.get("ip")
    command = data.get("command")

    if not router_ip:
        return jsonify({
            "success": False,
            "message": "Router IP is required"
        }), 400

    if not command:
        return jsonify({
            "success": False,
            "message": "Router command is required"
        }), 400

    ssh = None

    try:

        print(f"Connecting to {router_ip}")

        ssh = paramiko.SSHClient()

        ssh.set_missing_host_key_policy(
            paramiko.AutoAddPolicy()
        )

        ssh.connect(
            hostname=router_ip,
            port=22,
            username=USERNAME,
            password=PASSWORD,
            timeout=10,
            look_for_keys=False,
            allow_agent=False
        )

        print("SSH connected")

        channel = ssh.invoke_shell()

        time.sleep(1)

        if channel.recv_ready():
            channel.recv(65535)

        channel.send(command + "\n")

        time.sleep(2)

        output = ""

        while channel.recv_ready():

            output += channel.recv(65535).decode(
                "utf-8",
                errors="ignore"
            )

        channel.close()
        ssh.close()

        return jsonify({
            "success": True,
            "ip": router_ip,
            "command": command,
            "output": output
        })

    except Exception as e:

        print("SSH ERROR:", str(e))

        if ssh:
            ssh.close()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
