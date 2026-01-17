# Installation Guide - Format and Lint Code

Complete setup instructions for all supported formatters and linters.

## Quick Start (All Tools)

### macOS (Homebrew)
```bash
# Python tools
brew install black flake8 pylint
pip install isort

# JavaScript tools
brew install node prettier
npm install -g eslint

# Go tools
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

# Rust tools
rustup component add rustfmt clippy

# Shell tools
brew install shellcheck shfmt

# Other
brew install yamllint markdownlint
```

### Linux (Ubuntu/Debian)
```bash
# Python tools
sudo apt install python3-pip
pip3 install black flake8 pylint isort

# JavaScript tools
sudo apt install nodejs npm
npm install -g prettier eslint

# Go tools
curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $(go env GOPATH)/bin

# Rust tools
rustup component add rustfmt clippy

# Shell tools
sudo apt install shellcheck
GO111MODULE=on go install mvdan.cc/sh/v3/cmd/shfmt@latest

# Other
sudo apt install yamllint
npm install -g markdownlint-cli
```

### Windows (PowerShell)
```powershell
# Using Chocolatey
choco install python nodejs golang rust

# Python tools
pip install black flake8 pylint isort

# JavaScript tools
npm install -g prettier eslint

# Rust tools
rustup component add rustfmt clippy

# Other
pip install yamllint
npm install -g markdownlint-cli
```

---

## Language-Specific Installation

### Python

#### Black (Formatter)
```bash
# Install
pip install black

# Verify
black --version
```

Recommended config in `pyproject.toml`:
```toml
[tool.black]
line-length = 100
target-version = ['py310']
```

#### Flake8 (Linter)
```bash
# Install
pip install flake8

# Verify
flake8 --version
```

Recommended config in `.flake8`:
```ini
[flake8]
max-line-length = 100
extend-ignore = E203, W503
exclude = .git,__pycache__,venv,tests
```

#### Pylint (Code Analyzer)
```bash
# Install
pip install pylint

# Verify
pylint --version
```

Recommended config in `.pylintrc`:
```ini
[MASTER]
max-line-length = 100

[MESSAGES CONTROL]
disable = C0111,R0801
```

#### isort (Import Sorter)
```bash
# Install
pip install isort

# Verify
isort --version
```

Recommended config in `pyproject.toml`:
```toml
[tool.isort]
profile = "black"
line_length = 100
```

---

### JavaScript/TypeScript

#### Prettier (Formatter)
```bash
# Install globally
npm install -g prettier

# Or install in build
npm install --save-dev prettier

# Verify
prettier --version
```

Recommended config in `.prettierrc.json`:
```json
{
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "semi": true,
  "singleQuote": true,
  "trailingComma": "es5",
  "bracketSpacing": true,
  "arrowParens": "always"
}
```

Ignore file `.prettierignore`:
```
node_modules
dist
build
coverage
.next
```

#### ESLint (Linter)
```bash
# Install
npm install -g eslint

# Or in build
npm install --save-dev eslint

# Initialize (interactive)
eslint --init

# Verify
eslint --version
```

Basic config in `.eslintrc.json`:
```json
{
  "env": {
    "browser": true,
    "es2021": true,
    "node": true
  },
  "extends": ["eslint:recommended"],
  "rules": {
    "indent": ["error", 2],
    "quotes": ["error", "single"],
    "semi": ["error", "always"]
  }
}
```

Ignore file `.eslintignore`:
```
node_modules
dist
build
coverage
```

---

### Go

#### Gofmt (Formatter)
```bash
# Built-in with Go
go version

# Also install goimports for import sorting
go install golang.org/x/tools/cmd/goimports@latest

# Verify
gofmt -h
```

#### golangci-lint (Linter)
```bash
# Install
curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $(go env GOPATH)/bin

# Verify
golangci-lint --version
```

Recommended config in `.golangci.yml`:
```yaml
linters:
  enable:
    - gofmt
    - vet
    - govet
    - errcheck
    - staticcheck

issues:
  exclude-use-default: false
```

---

### Rust

#### Rustfmt (Formatter)
```bash
# Built-in with Rust
rustup component add rustfmt

# Verify
rustfmt --version
```

#### Clippy (Linter)
```bash
# Built-in with Rust
rustup component add clippy

# Verify
cargo clippy --version
```

Recommended config in `rustfmt.toml`:
```toml
edition = "2021"
max_width = 100
hard_tabs = false
```

---

### YAML

#### yamllint (Linter)
```bash
# Install
pip install yamllint

# Verify
yamllint --version
```

Recommended config in `.yamllint`:
```yaml
rules:
  line-length:
    max: 120
  indentation:
    spaces: 2
  document-start: disable
```

---

### Shell

#### shellcheck (Linter)
```bash
# Install
brew install shellcheck        # macOS
sudo apt install shellcheck    # Linux
choco install shellcheck       # Windows
```

#### shfmt (Formatter)
```bash
# Install
GO111MODULE=on go install mvdan.cc/sh/v3/cmd/shfmt@latest

# Verify
shfmt --version
```

---

### Markdown

#### markdownlint (Linter)
```bash
# Install
npm install -g markdownlint-cli

# Verify
markdownlint --version
```

Recommended config in `.markdownlint.json`:
```json
{
  "line-length": {
    "line_length": 100
  },
  "no-hard-tabs": true,
  "no-trailing-spaces": true,
  "single-h1": true
}
```

---

## Installation Verification

Create a test script to verify all tools are installed:

```bash
#!/bin/bash

echo "Format & Lint Tools Installation Check"
echo "======================================="

# Python
echo -n "Black: "
black --version 2>/dev/null || echo "NOT INSTALLED"

echo -n "Flake8: "
flake8 --version 2>/dev/null || echo "NOT INSTALLED"

echo -n "Pylint: "
pylint --version 2>/dev/null || echo "NOT INSTALLED"

# JavaScript
echo -n "Prettier: "
prettier --version 2>/dev/null || echo "NOT INSTALLED"

echo -n "ESLint: "
eslint --version 2>/dev/null || echo "NOT INSTALLED"

# Go
echo -n "Gofmt: "
gofmt -h 2>/dev/null | head -1 || echo "NOT INSTALLED"

echo -n "Golangci-lint: "
golangci-lint --version 2>/dev/null || echo "NOT INSTALLED"

# Rust
echo -n "Rustfmt: "
rustfmt --version 2>/dev/null || echo "NOT INSTALLED"

# Other
echo -n "Yamllint: "
yamllint --version 2>/dev/null || echo "NOT INSTALLED"

echo -n "Shellcheck: "
shellcheck --version 2>/dev/null | head -1 || echo "NOT INSTALLED"

echo "======================================="
```

---

## Docker Setup (Alternative)

If you prefer Docker, use a container with all tools pre-installed:

```dockerfile
FROM python:3.10-slim

# Install system packages
RUN apt-get update && apt-get install -y \
    nodejs npm \
    golang-go \
    shellcheck \
    yamllint

# Install Python tools
RUN pip install black flake8 pylint isort

# Install Node tools
RUN npm install -g prettier eslint

# Install Go tools
RUN go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

WORKDIR /workspace
ENTRYPOINT ["sh"]
```

Use with:
```bash
docker build -t format-lint .
docker run -v $(pwd):/workspace format-lint
```

---

## Troubleshooting

### Tool not found errors

```bash
# Add pip packages to PATH (Python)
export PATH="$HOME/.local/bin:$PATH"

# Add npm global packages to PATH
export PATH="$(npm config get prefix)/bin:$PATH"

# Add Go binaries to PATH
export PATH="$PATH:$(go env GOPATH)/bin"
```

### Permission denied on hook

```bash
chmod +x .git/hooks/pre-commit
```

### Version conflicts

```bash
# Python: Use virtual environments
python -m venv venv
source venv/bin/activate
pip install black flake8 pylint isort

# Node: Use build-local installation
npm install --save-dev prettier eslint
npx prettier --version
```

---

## Next Steps

1. **Install preferred tools**: Pick languages you use
2. **Copy config files**: Use templates from this skill
3. **Test installation**: Run verification script
4. **Install pre-commit hook** (optional): `format code --install-hook`
5. **Customize rules**: Edit config files to match your style

