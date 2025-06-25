echo -e "Starting script\\n\\n"

sudo chown -R $USER /$USER

echo -e "alias ll='ls -halF'" >> ~/.bashrc
echo -e "source $(pwd)/.venv/bin/activate" >> ~/.bashrc
echo "Installing poetry with optionals"
poetry install --with tests

echo -e "\\n\\n"
echo "    current path:
$(pwd)
"
echo "    current folder contents:
$(ls)
"
