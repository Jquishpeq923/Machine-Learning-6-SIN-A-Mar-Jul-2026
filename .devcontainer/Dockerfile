# FROM tells Docker: "start from this existing image"
# python:3.12-slim contains exactly Python 3.12 and nothing else 
# no editors, no extra tools, no bloat. 
# The -slim suffix is ​​important
# there's also python:3.12 (larger, includes compilers and development tools) 
# and python:3.12-alpine (absolutely minimal, based on Alpine Linux).
FROM python:3.12-slim

# The `RUN` command executes a command within the container during the build process. 
# Here, a single `RUN` statement is chained with `&&` for a very specific reason: 
# each `RUN` in a Dockerfile creates a new layer in the image. 
# If `apt-get update` were placed in one layer and `apt-get install` in another, 
# Docker could cache the first layer and use an outdated package list in future builds. 
# Chaining them into a single `RUN` ensures that the package list is always updated 
# before installation.

# apt-get update: Update the Debian package index (the slim image is based on Debian)
# apt-get install -y: Installs packages with a yes by default (avoid user interaction)
# curl is needed to install uv
# git is needed by github
# git Large File Storage avoid conflicts with codespaces tempaltes
# Remove the index files that apt-get update downloaded. 
# They are no longer needed after installing the packages, and deleting them reduces the final image size.

RUN apt-get update && apt-get install -y \  
    curl \ 
    git \  
    git-lfs \ 
    && rm -rf /var/lib/apt/lists/* 

# Avoid git push errors on the container
RUN git lfs install --system

# downloads and installs curl
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# ENV defines an environment variable that persists in all subsequent layers of the Dockerfile 
# and within the running container. 
# The uv installer places the binary in /root/.local/bin. 
# without adding that path to the PATH, 
# the following RUN uv venv would fail with "command not found".
ENV PATH="/root/.local/bin:$PATH"

# sets the working directory for all subsequent instructions. 
# It is equivalent to doing `mkdir /app && cd /app`
# The name /app is chosen by convention—it's a neutral, 
# short name that's clearly distinguishable from system directories 
# like /usr or /home. The virtual environment created in the next line
# will reside in /app/.venv.
WORKDIR /app

# Create the virtual environment in /app/.venv.
RUN uv venv .venv

# COPY takes the requirements.txt file from the repository (the host machine) 
# and copies it into the container in the current working directory 
# (/app/requirements.txt)
COPY requirements.txt .

# Installs all the packages listed in the requirements file into the `.venv` virtual environment.
# the `--python .venv/bin/python` flag explicitly tells `uv` to install to
# that specific interpreter and not the system Python. 
# The `-r` flag means "read packages from this requirements file".
RUN uv pip install --python .venv/bin/python -r requirements.txt

# Normally, to activate a virtual environment, 
# you run `source .venv/bin/activate`
# but that only applies to the current shell session 
# and does not persist between Docker layers 
# or in the final container environment.
# VIRTUAL_ENV tells Python tools which environment is active, 
# and adding .venv/bin to the beginning of the PATH 
# ensures that when someone runs python or pip inside the container, 
# the system finds the virtual environment binaries first and not the system binaries.
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"