import os

lPathVenvBin = os.path.join(os.path.dirname(__file__), '.venv', 'bin')
lPathGunicorn = os.path.join(lPathVenvBin, 'gunicorn')
lNameService = 'NotionGunicorn'
lPathService = f"/etc/systemd/system/{lNameService}.service"
lUsername = 'Your_Name'

lTextService = f"""[Unit]
Description=Gunicorn instance to serve Notion application
After=network.target

[Service]
User={lUsername}
WorkingDirectory={os.path.dirname(__file__)}
Environment="PATH={lPathVenvBin}"
ExecStart={lPathGunicorn} -w 4 -b 127.0.0.1:5000 server_run:app

[Install]
WantedBy=multi-user.target
"""

with open(lPathService, "w") as service_file:
    service_file.write(lTextService)

print(f"Service file created at {lPathService}")
