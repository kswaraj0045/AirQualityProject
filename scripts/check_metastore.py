import subprocess

sql = 'SELECT * FROM "VERSION";'
cmd = ['docker', 'exec', '-i', 'hive-metastore-postgresql', 'psql', '-U', 'hive', '-d', 'metastore']
p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(sql)
print("STDOUT:\n", out)
print("STDERR:\n", err)
