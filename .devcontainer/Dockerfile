# Use Ubuntu 22.04 as base image for consistent development environment
FROM ubuntu:22.04

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /workspace

# Update package lists and install common development dependencies
RUN apt-get update && apt-get install -y \
    # Essential build tools
    build-essential \
    # Version control
    git \
    # Network utilities
    curl \
    wget \
    # Python 3 and pip
    python3 \
    python3-pip \
    python3-venv \
    # Node.js and npm (using NodeSource for latest LTS)
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    # Additional useful tools
    vim \
    nano \
    sudo \
    ca-certificates \
    gnupg \
    lsb-release \
    # Clean up apt cache to reduce image size
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Verify installations
RUN python3 --version && \
    pip3 --version && \
    node --version && \
    npm --version && \
    git --version

# Create a non-root user for development
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Set the default user
USER $USERNAME

# ============================================================================
# PROJECT-SPECIFIC DEPENDENCIES
# ============================================================================
# Uncomment the following lines once the container is built and you want to
# install project dependencies:
#
# Install Python dependencies from requirements.txt
# COPY requirements.txt /workspace/
# RUN pip3 install --user -r requirements.txt
#
# Install Node.js dependencies from package.json
# COPY frontend/package.json frontend/package-lock.json* /workspace/frontend/
# RUN cd /workspace/frontend && npm install
#
# Note: Dependencies can also be installed after the container starts using:
# - Backend: pip install -r requirements.txt
# - Frontend: cd frontend && npm install
# ============================================================================

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1
ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"

# Expose ports for Django and Vue.js development servers
EXPOSE 8000 5173

# Default command
CMD ["/bin/bash"]
