# MortyRAG

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/agreene90/MortyRAG/ci_cd.yml?branch=main&label=Build%20Status)](https://github.com/agreene90/MortyRAG/actions)
[![Docker Pulls](https://img.shields.io/docker/pulls/agreene90/mortyrag)](https://hub.docker.com/r/agreene90/mortyrag)
[![Docker Image Size](https://img.shields.io/docker/image-size/agreene90/mortyrag/latest)](https://hub.docker.com/r/agreene90/mortyrag)
[![GitHub Issues](https://img.shields.io/github/issues/agreene90/MortyRAG)](https://github.com/agreene90/MortyRAG/issues)
[![GitHub Forks](https://img.shields.io/github/forks/agreene90/MortyRAG)](https://github.com/agreene90/MortyRAG/network/members)
[![GitHub Stars](https://img.shields.io/github/stars/agreene90/MortyRAG)](https://github.com/agreene90/MortyRAG/stargazers)
[![GitHub License](https://img.shields.io/github/license/agreene90/MortyRAG)](https://github.com/agreene90/MortyRAG/blob/main/LICENSE)
[![Maintenance](https://img.shields.io/maintenance/yes/2024)](https://github.com/agreene90/MortyRAG)
[![Last Commit](https://img.shields.io/github/last-commit/agreene90/MortyRAG)](https://github.com/agreene90/MortyRAG/commits/main)

## Overview

This project, developed by Ant under HermiTech-LLC, implements a Retrieval-Augmented Generation (RAG) model that combines a document retrieval mechanism with a generative language model. The system is designed to produce witty, informative, and contextually appropriate responses, with a particular focus on physics-related content.

___
![mortspeak](https://github.com/agreene90/MortyRAG/blob/main/Screenshot%20from%202024-08-19%2023-18-01.png)
___

## Directory Structure

```plaintext
MortyRAG-main/
├── .github/workflows/           # GitHub Actions workflows
│   └── ci_cd.yml                # CI/CD pipeline configuration
├── custom_t5_rag_local_model_v1.0/
├── data/
│   ├── raw/
│   │   ├── 01_physics_with_wit_and_wisdom.txt
│   │   ├── 02_science_with_a_twist.txt
│   │   ├── 03_sci_fi_and_reality.txt
│   │   ├── 04_black_holes_fact_vs_fiction.txt
│   │   ├── 05_quantum_computing_future.txt
│   │   ├── 06_time_travel_fact_vs_fiction.txt
│   │   ├── 07_gods_of_thunder_mythology.txt
│   │   ├── 08_hidden_wonders_of_earth.txt
│   │   ├── 09_calculus_derivatives.txt
│   │   ├── 10_strange_but_true_history.txt
│   │   ├── 11_rise_of_ai_fiction_vs_reality.txt
│   │   ├── 12_exploring_alien_civilizations.txt
│   │   └── 13_pop_culture_tech_influence.txt
├── docs/
│   ├── api.md
│   ├── controller.md
│   ├── generation.md
│   ├── introduction.md
│   └── retrieval.md
├── LICENSE
├── README.md
├── Screenshot from 2024-08-19 23-18-01.png
├── generator.py         # Custom T5 model class for RAG with local file support
├── main.py              # Entry point script for the Optimization and Query handling GUI
├── rag.py               # Core logic for generating responses using the T5 model
├── requirements.txt     # Required Python packages
├── retriever.py         # Functions for reading and processing different file types
├── Dockerfile           # Dockerfile to build the Docker image for MortyRAG
└── create_shortcut.sh   # Script to create a desktop shortcut to run the Docker container
```

## Installation

### Using Docker

MortyRAG is now available as a Docker container, making it easy to deploy and run the application across different environments without needing to install dependencies manually.

### 1. Pull the Docker Image

First, pull the latest Docker image from the GitHub Container Registry:

```bash
docker pull ghcr.io/agreene90/mortyrag:latest
```

### 2. Running the Docker Container

To run the MortyRAG application using Docker, execute the following command:

```bash
docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix ghcr.io/agreene90/mortyrag:latest
```

This command will launch the MortyRAG Tkinter-based GUI in a Docker container with support for displaying the graphical interface on your local machine.

### 3. Creating a Desktop Shortcut for Easy Access

You can create a desktop shortcut to run the Dockerized MortyRAG application directly from your desktop.

#### **Creating the Shortcut Script**

If you prefer to automate this process, you can run a script that creates the shortcut:

```bash
cat << 'EOF' > create_shortcut.sh
#!/bin/bash
set -e

# Pull the latest Docker image
docker pull ghcr.io/agreene90/mortyrag:latest

# Create Desktop Entry for all users
DESKTOP_ENTRY="/usr/share/applications/MortyRAG.desktop"
echo "[Desktop Entry]" > "$DESKTOP_ENTRY"
echo "Version=1.0" >> "$DESKTOP_ENTRY"
echo "Name=MortyRAG" >> "$DESKTOP_ENTRY"
echo "Comment=Start MortyRAG Docker Container" >> "$DESKTOP_ENTRY"
echo "Exec=docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix ghcr.io/agreene90/mortyrag:latest" >> "$DESKTOP_ENTRY"
echo "Icon=docker" >> "$DESKTOP_ENTRY"
echo "Terminal=false" >> "$DESKTOP_ENTRY"
echo "Type=Application" >> "$DESKTOP_ENTRY"
echo "Categories=Development;" >> "$DESKTOP_ENTRY"
echo "StartupNotify=true" >> "$DESKTOP_ENTRY"

# Create a symlink to the user's desktop
ln -s "$DESKTOP_ENTRY" "$HOME/Desktop/MortyRAG.desktop"
chmod +x "$HOME/Desktop/MortyRAG.desktop"

echo "MortyRAG has been successfully installed and a shortcut has been added to your desktop."
EOF
```

## Documentation

Detailed documentation for each module can be found in the `docs/` directory. Each file provides an in-depth explanation of the module's purpose, usage, and key functions.

## License

This project is licensed under the BSD 3-Clause License - see the `LICENSE` file for details.
