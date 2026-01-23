# Test install.sh on fresh Ubuntu
FROM ubuntu:22.04

# Minimal setup
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y curl

# Copy local installer for testing
COPY install.sh /tmp/install.sh
RUN chmod +x /tmp/install.sh

# Run installer (non-interactive test - just check if it runs)
# In real usage, user would run: curl -fsSL https://... | bash
CMD ["/bin/bash", "-c", "echo '2' | /tmp/install.sh || echo 'Installer failed but container still running for debugging'"]
