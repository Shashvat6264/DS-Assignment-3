import subprocess
import shlex
import time

commands = (
    "gnome-terminal --tab -- bash -c \"./run.sh node0; exec bash\"",
    "gnome-terminal --tab -- bash -c \"./run.sh node1; exec bash\"",
    "gnome-terminal --tab -- bash -c \"./run.sh node2; exec bash\""
)

for c in commands:
    subprocess.run(shlex.split(c))
    time.sleep(0.5)