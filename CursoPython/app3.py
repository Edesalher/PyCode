from pathlib import Path

# Absolute path
# c:\Programs Files\Microsoft
# /usr/local/bin

path = Path()
for file in path.glob('*'):
    print(file)
