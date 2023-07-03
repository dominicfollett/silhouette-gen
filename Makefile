# Makefile

# Name of the Conda environment
ENV_NAME = silhouette_env

# Create and activate the Conda environment
create-env:
	@echo "Creating Conda environment..."
	conda create --name $(ENV_NAME) python=3 -y
	@echo "Activating Conda environment..."
	@echo "Use 'conda activate $(ENV_NAME)' to activate the environment."

# Install the required packages
install-packages:
	@echo "Installing required packages..."
	conda install --name $(ENV_NAME) -y numpy matplotlib scipy Pillow

# All target (create environment and install packages)
all: create-env install-packages
