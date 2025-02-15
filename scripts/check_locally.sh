#!/bin/bash
set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting local package testing...${NC}"

# Clean existing builds
echo -e "\n${GREEN}Cleaning existing builds...${NC}"
rm -rf dist/ build/

# Build the package
echo -e "\n${GREEN}Building package...${NC}"
python -m build

# Create a temporary virtualenv for testing
VENV_PATH="/tmp/test-gjdutils"
echo -e "\n${GREEN}Creating test virtualenv at ${VENV_PATH}...${NC}"
python -m venv "${VENV_PATH}"
source "${VENV_PATH}/bin/activate"

# Install the package
echo -e "\n${GREEN}Installing package from local build...${NC}"
pip install $(ls dist/*.whl | tail -n1)

# Install dev dependencies for testing
echo -e "\n${GREEN}Installing dev dependencies...${NC}"
pip install ".[dev]"

# Test basic functionality
echo -e "\n${GREEN}Testing basic functionality...${NC}"
python -c "import gjdutils; print(f'gjdutils version: {gjdutils.__version__}')"

# Run the test suite
echo -e "\n${GREEN}Running test suite...${NC}"
python -m pytest

# Optional feature sets testing
echo -e "\n${GREEN}Testing optional feature installations...${NC}"
for feature in "dt" "llm" "audio_lang" "html_web"; do
    echo -e "${YELLOW}Testing feature set: ${feature}${NC}"
    pip install ".[${feature}]"
done

# Deactivate and clean up virtualenv
deactivate
rm -rf "${VENV_PATH}"

echo -e "\n${GREEN}Local testing completed successfully!${NC}" 