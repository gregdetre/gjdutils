#!/bin/bash
set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting Test PyPI package testing...${NC}"

# Create a temporary virtualenv for testing
VENV_PATH="/tmp/test-gjdutils-pypi"
echo -e "\n${GREEN}Creating test virtualenv at ${VENV_PATH}...${NC}"
python -m venv "${VENV_PATH}"
source "${VENV_PATH}/bin/activate"

# Install the package from Test PyPI
echo -e "\n${GREEN}Installing package from Test PyPI...${NC}"
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ gjdutils

# Test basic functionality
echo -e "\n${GREEN}Testing basic functionality...${NC}"
python -c "import gjdutils; print(f'gjdutils version: {gjdutils.__version__}')"

# Optional feature sets testing
echo -e "\n${GREEN}Testing optional feature installations...${NC}"
for feature in "dt" "llm" "html_web"; do
    echo -e "${YELLOW}Testing feature set: ${feature}${NC}"
    pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ "gjdutils[${feature}]"
done

# Deactivate and clean up virtualenv
deactivate
rm -rf "${VENV_PATH}"

echo -e "\n${GREEN}Test PyPI testing completed successfully!${NC}" 