# Integration Test Dockerfile for install.sh
# This ACTUALLY runs the installer in a fresh Ubuntu container

FROM ubuntu:22.04

# Prevent interactive prompts during apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Install curl (only dependency)
RUN apt-get update && apt-get install -y curl ca-certificates

# Copy installer
COPY install.sh /tmp/install.sh
RUN chmod +x /tmp/install.sh

# Create test script that simulates user input
RUN echo '#!/bin/bash\n\
# Non-interactive test answers:\n\
# 1. VS Code? -> No (2)\n\
# 2. Nexus directory? -> /tmp/nexus\n\
# 3. Overwrite? -> No (if exists)\n\
echo -e "2\\n/tmp/nexus\\nn" | /tmp/install.sh\n\
\n\
# Verify installations\n\
echo ""\n\
echo "=== Verification ==="\n\
\n\
if command -v claude &> /dev/null; then\n\
  echo "✓ Claude Code installed: $(claude --version 2>&1 | head -1)"\n\
else\n\
  echo "✗ Claude Code NOT installed"\n\
  exit 1\n\
fi\n\
\n\
if command -v uv &> /dev/null; then\n\
  echo "✓ uv installed: $(uv --version)"\n\
else\n\
  echo "✗ uv NOT installed"\n\
  exit 1\n\
fi\n\
\n\
if command -v git &> /dev/null; then\n\
  echo "✓ Git installed: $(git --version)"\n\
else\n\
  echo "✗ Git NOT installed"\n\
  exit 1\n\
fi\n\
\n\
echo ""\n\
echo "=== All tools verified! ==="\n\
' > /tmp/run-test.sh

RUN chmod +x /tmp/run-test.sh

# Run the test
CMD ["/tmp/run-test.sh"]
