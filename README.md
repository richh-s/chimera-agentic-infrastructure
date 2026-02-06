# Chimera Agentic Infrastructure

Spec-driven, governed agentic infrastructure for Project Chimera.

## 🚀 Quick Start

```bash
git clone https://github.com/your-username/chimera-agentic-infrastructure.git
cd chimera-agentic-infrastructure
make setup
🔧 Development Commands
bash
make lint      # Run Ruff linter
make security  # Run Bandit scanner  
make test      # Run pytest suite
make check     # Run all quality checks
🏗️ Architecture
Modular agents: Skill-based composition

Built-in governance: Policy enforcement

Security-first: Containerized execution

Observable: Comprehensive telemetry

🛡️ Security
Automated security scanning with Bandit:

Vulnerability detection

Dependency auditing

Container isolation

Exception: B101 skipped for test asserts

📁 Project Structure
text
src/           # Core framework
tests/         # Test suite  
specs/         # Technical specifications
Dockerfile     # Container definition
Makefile       # Development automation
🧪 Testing
python
# Skill interface contract
def invoke(inputs: dict) -> dict:
    return {
        "success": True,
        "confidence": 0.95,
        "output": {"result": "..."}
    }
🤖 Coderabbit Test
Testing AI-powered code review capabilities with Coderabbit. This update should trigger:

Documentation analysis

Code quality suggestions

Security recommendations

Best practices feedback