import subprocess

x = subprocess.check_output(["sudo", "python", "unlock_door.py"])
print x
print type(x)
if 'Blah' in x:
    print True
