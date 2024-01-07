# Use Ubuntu 22.04 (Jammy Jellyfish)
FROM ubuntu:jammy

# Set non-interactive frontend for apt to prevent interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Update the package repository and upgrade any existing packages
RUN apt-get update && \
    apt-get upgrade -y

# Install Python 3.11, PostgreSQL, Git, Zsh, wget, and Python 3 pip
RUN apt-get install -y python3.11 git zsh wget python3-pip sudo postgresql-client tree

# Clean up
RUN apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Set Python 3.11 as the default Python version
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

# Ensure that pip, setuptools, and wheel are up to date for Python 3.11
RUN python3.11 -m pip install --upgrade pip setuptools wheel

# Install Python dependencies from the requirements.txt file
COPY requirements.txt /
RUN pip install -r /requirements.txt

# Install Oh My Zsh
RUN sh -c "$(wget https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O -)"

# Necessary for Zsh as the default shell
CMD ["zsh"]

# Reset the frontend to its default value
ENV DEBIAN_FRONTEND=dialog
