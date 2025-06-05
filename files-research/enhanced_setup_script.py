# setup_enhanced_mama_bear.py
"""
🐻 Enhanced Mama Bear Setup Script
Automated setup for next-level browser control and computer use capabilities
"""

import os
import sys
import subprocess
import json
import asyncio
from pathlib import Path
from typing import Dict, Any, List
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedMamaBearSetup:
    """Setup manager for Enhanced Mama Bear capabilities"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.backend_dir = self.project_root / 'backend'
        self.frontend_dir = self.project_root / 'frontend'
        self.config_dir = self.project_root / 'config'
        
        # Required environment variables
        self.required_env_vars = [
            'GEMINI_API_KEY',
            'SCRAPYBARA_API_KEY',
            'ANTHROPIC_API_KEY',  # Optional but recommended
            'OPENAI_API_KEY',     # Optional but recommended
            'MEM0_API_KEY'        # Optional but recommended
        ]
        
        # Enhanced dependencies
        self.backend_dependencies = [
            'flask>=3.0.0',
            'flask-socketio>=5.3.6',
            'flask-cors>=4.0.0',
            'aiohttp>=3.9.1',
            'asyncio',
            'aiofiles>=24.1.0',
            'python-socketio>=5.11.0',
            'websockets>=12.0',
            'google-generativeai>=0.7.2',
            'anthropic>=0.34.0',
            'openai>=1.45.0',
            'mem0ai>=0.1.0',
            'requests>=2.31.0',
            'python-dotenv>=1.0.0',
            'pydantic>=2.5.0',
            'dataclasses-json>=0.6.3',
            'sqlalchemy>=2.0.23'
        ]
        
        self.frontend_dependencies = [
            '@types/react@^18.0.0',
            '@types/react-dom@^18.0.0',
            'react@^18.2.0',
            'react-dom@^18.2.0',
            'react-router-dom@^6.8.0',
            'socket.io-client@^4.7.0',
            'framer-motion@^10.16.0',
            'tailwindcss@^3.3.0',
            '@tailwindcss/forms@^0.5.0',
            '@headlessui/react@^1.7.0',
            '@heroicons/react@^2.0.0',
            'lucide-react@^0.263.1',
            'clsx@^2.0.0',
            'date-fns@^2.30.0'
        ]
    
    def print_banner(self):
        """Print setup banner"""
        print("""
🐻 Enhanced Mama Bear Setup
═══════════════════════════════════════════════════════════════
   Next-Level Browser Control & Computer Use Agent Setup
   
   Features being installed:
   🌐 Shared Browser Sessions with Real-time Collaboration
   🤖 Computer Use Agent for Desktop Automation  
   🔐 Authenticated Web Session Management
   🔍 Multi-Instance Research Environments
   🧠 Intelligent Agent Orchestration
   💾 Enhanced Memory with Mem0 Integration
   
═══════════════════════════════════════════════════════════════
        """)
    
    def check_python_version(self):
        """Check Python version compatibility"""
        logger.info("🔍 Checking Python version...")
        
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 9):
            logger.error("❌ Python 3.9+ is required for Enhanced Mama Bear")
            logger.error(f"Current version: {version.major}.{version.minor}.{version.micro}")
            sys.exit(1)
        
        logger.info(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    
    def check_node_version(self):
        """Check Node.js version for frontend"""
        logger.info("🔍 Checking Node.js version...")
        
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                logger.info(f"✅ Node.js {version} found")
            else:
                logger.warning("⚠️ Node.js not found - frontend features may not work")
        except FileNotFoundError:
            logger.warning("⚠️ Node.js not installed - frontend features will be limited")
    
    def setup_directories(self):
        """Create necessary directories"""
        logger.info("📁 Setting up directory structure...")
        
        directories = [
            self.backend_dir / 'services',
            self.backend_dir / 'api',
            self.backend_dir / 'utils',
            self.backend_dir / 'database',
            self.backend_dir / 'testing',
            self.frontend_dir / 'src' / 'components' / 'enhanced',
            self.config_dir,
            Path('mama_bear_memory') / 'memories',
            Path('mama_bear_memory') / 'profiles',
            Path('mama_bear_memory') / 'patterns',
            Path('logs'),
            Path('uploads')
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"  📁 Created {directory}")
        
        logger.info("✅ Directory structure created")
    
    def check_environment_variables(self):
        """Check and setup environment variables"""
        logger.info("🔧 Checking environment variables...")
        
        env_file = self.project_root / '.env'
        missing_vars = []
        
        # Load existing .env if it exists
        existing_env = {}
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        existing_env[key] = value
        
        # Check required variables
        for var in self.required_env_vars:
            if var not in existing_env and var not in os.environ:
                missing_vars.append(var)
        
        if missing_vars:
            logger.warning(f"⚠️ Missing environment variables: {', '.join(missing_vars)}")
            
            # Create/update .env file
            self.create_env_template(env_file, existing_env, missing_vars)
        else:
            logger.info("✅ All required environment variables are set")
    
    def create_env_template(self, env_file: Path, existing_env: Dict[str, str], missing_vars: List[str]):
        """Create or update .env template"""
        logger.info("📝 Creating/updating .env template...")
        
        env_template = {
            'GEMINI_API_KEY': 'your_gemini_api_key_here',
            'GEMINI_API_KEY_BACKUP': 'your_backup_gemini_key_here',
            'SCRAPYBARA_API_KEY': 'your_scrapybara_api_key_here',
            'ANTHROPIC_API_KEY': 'your_anthropic_api_key_here',
            'OPENAI_API_KEY': 'your_openai_api_key_here',
            'MEM0_API_KEY': 'your_mem0_api_key_here',
            'MEM0_USER_ID': 'nathan_sanctuary',
            'GOOGLE_APPLICATION_CREDENTIALS': './config/google-credentials.json',
            'GOOGLE_CLOUD_PROJECT': 'your_project_id',
            'MAMA_BEAR_ENABLE_PROACTIVE': 'true',
            'MAMA_BEAR_DAILY_BRIEFING': 'true',
            'MAMA_BEAR_AUTO_OPTIMIZE': 'true',
            'MAMA_BEAR_MEMORY_RETENTION_DAYS': '30',
            'SCRAPYBARA_MAX_INSTANCES': '10',
            'SCRAPYBARA_PERMISSION_LEVEL': 'elevated',
            'DEBUG': 'true',
            'LOG_LEVEL': 'INFO',
            'BACKEND_PORT': '5001',
            'FRONTEND_PORT': '3000'
        }
        
        # Merge with existing
        final_env = {**env_template, **existing_env}
        
        # Write .env file
        with open(env_file, 'w') as f:
            f.write("# Enhanced Mama Bear Configuration\n")
            f.write("# Generated by setup script\n\n")
            
            f.write("# Required API Keys\n")
            for key in self.required_env_vars:
                f.write(f"{key}={final_env.get(key, 'your_key_here')}\n")
            
            f.write("\n# Optional but Recommended\n")
            optional_keys = [k for k in env_template.keys() if k not in self.required_env_vars]
            for key in optional_keys:
                f.write(f"{key}={final_env.get(key, env_template[key])}\n")
        
        logger.info(f"✅ .env file created at {env_file}")
        logger.warning("⚠️ Please update the API keys in .env before starting the application")
    
    def install_backend_dependencies(self):
        """Install Python backend dependencies"""
        logger.info("📦 Installing backend dependencies...")
        
        # Create requirements.txt
        requirements_file = self.backend_dir / 'requirements.txt'
        with open(requirements_file, 'w') as f:
            f.write("# Enhanced Mama Bear Backend Dependencies\n")
            f.write("# Generated by setup script\n\n")
            for dep in self.backend_dependencies:
                f.write(f"{dep}\n")
        
        logger.info(f"✅ Created {requirements_file}")
        
        # Install dependencies
        try:
            logger.info("Installing Python packages...")
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)
            ], check=True)
            logger.info("✅ Backend dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to install backend dependencies: {e}")
            logger.info("💡 Try running: pip install -r backend/requirements.txt")
    
    def install_frontend_dependencies(self):
        """Install Node.js frontend dependencies"""
        if not self.frontend_dir.exists():
            logger.info("📱 Creating frontend directory structure...")
            self.frontend_dir.mkdir(exist_ok=True)
        
        # Create package.json
        package_json = {
            "name": "enhanced-mama-bear-frontend",
            "version": "2.0.0",
            "private": True,
            "dependencies": {},
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "react-scripts test",
                "eject": "react-scripts eject"
            },
            "eslintConfig": {
                "extends": ["react-app", "react-app/jest"]
            },
            "browserslist": {
                "production": [">0.2%", "not dead", "not op_mini all"],
                "development": ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
            }
        }
        
        # Add dependencies
        for dep in self.frontend_dependencies:
            name, version = dep.split('@')
            package_json["dependencies"][name] = version
        
        package_file = self.frontend_dir / 'package.json'
        with open(package_file, 'w') as f:
            json.dump(package_json, f, indent=2)
        
        logger.info(f"✅ Created {package_file}")
        
        # Install if Node.js is available
        try:
            logger.info("📦 Installing frontend dependencies...")
            subprocess.run(['npm', 'install'], cwd=self.frontend_dir, check=True)
            logger.info("✅ Frontend dependencies installed successfully")
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("⚠️ Could not install frontend dependencies - Node.js may not be available")
            logger.info("💡 Try running: cd frontend && npm install")
    
    def create_config_files(self):
        """Create configuration files"""
        logger.info("⚙️ Creating configuration files...")
        
        # Database configuration
        db_config = {
            "database": {
                "url": "sqlite:///mama_bear.db",
                "echo": False,
                "pool_pre_ping": True
            },
            "memory": {
                "retention_days": 30,
                "max_cache_size": 1000,
                "cleanup_interval": 3600
            },
            "scrapybara": {
                "max_instances": 10,
                "default_timeout": 3600,
                "cleanup_interval": 1800
            }
        }
        
        config_file = self.config_dir / 'database.json'
        with open(config_file, 'w') as f:
            json.dump(db_config, f, indent=2)
        
        logger.info(f"✅ Created {config_file}")
        
        # Logging configuration
        logging_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                }
            },
            "handlers": {
                "default": {
                    "level": "INFO",
                    "formatter": "standard",
                    "class": "logging.StreamHandler"
                },
                "file": {
                    "level": "INFO",
                    "formatter": "standard",
                    "class": "logging.FileHandler",
                    "filename": "logs/mama_bear.log"
                }
            },
            "loggers": {
                "": {
                    "handlers": ["default", "file"],
                    "level": "INFO",
                    "propagate": False
                }
            }
        }
        
        logging_file = self.config_dir / 'logging.json'
        with open(logging_file, 'w') as f:
            json.dump(logging_config, f, indent=2)
        
        logger.info(f"✅ Created {logging_file}")
    
    def create_docker_files(self):
        """Create Docker configuration for easy deployment"""
        logger.info("🐳 Creating Docker configuration...")
        
        # Dockerfile for backend
        dockerfile_content = """FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ ./backend/
COPY config/ ./config/
COPY mama_bear_memory/ ./mama_bear_memory/

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=backend/app.py

# Create necessary directories
RUN mkdir -p logs uploads mama_bear_memory/memories mama_bear_memory/profiles mama_bear_memory/patterns

# Expose port
EXPOSE 5001

# Run the application
CMD ["python", "backend/app.py"]
"""
        
        with open(self.project_root / 'Dockerfile', 'w') as f:
            f.write(dockerfile_content)
        
        # Docker Compose for full stack
        docker_compose_content = """version: '3.8'
services:
  enhanced-mama-bear-backend:
    build: .
    ports:
      - "5001:5001"
    environment:
      - FLASK_ENV=development
      - DEBUG=true
    env_file:
      - .env
    volumes:
      - ./backend:/app/backend
      - ./config:/app/config
      - ./mama_bear_memory:/app/mama_bear_memory
      - ./logs:/app/logs
    restart: unless-stopped
  
  enhanced-mama-bear-frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:5001
      - REACT_APP_WS_URL=ws://localhost:5001
    volumes:
      - ./frontend:/app
      - /app/node_modules
    depends_on:
      - enhanced-mama-bear-backend
    restart: unless-stopped

volumes:
  mama_bear_data:
"""
        
        with open(self.project_root / 'docker-compose.yml', 'w') as f:
            f.write(docker_compose_content)
        
        logger.info("✅ Docker configuration created")
    
    def run_initial_setup(self):
        """Run initial database and service setup"""
        logger.info("🔄 Running initial setup...")
        
        # Create init script
        init_script = """#!/usr/bin/env python3
import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

async def main():
    print("🐻 Initializing Enhanced Mama Bear...")
    
    # Initialize database
    try:
        from backend.database.models import initialize_database
        engine, session = initialize_database()
        print("✅ Database initialized")
    except Exception as e:
        print(f"⚠️ Database initialization: {e}")
    
    # Test API connections
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv('GEMINI_API_KEY', 'test'))
        print("✅ Gemini API configured")
    except Exception as e:
        print(f"⚠️ Gemini API: {e}")
    
    print("🎉 Enhanced Mama Bear setup complete!")
    print()
    print("Next steps:")
    print("1. Update API keys in .env file")
    print("2. Run: python backend/app.py")
    print("3. Open: http://localhost:5001")
    print()
    print("🌟 Enhanced features will be available once API keys are configured!")

if __name__ == "__main__":
    asyncio.run(main())
"""
        
        init_file = self.project_root / 'init_enhanced_mama_bear.py'
        with open(init_file, 'w') as f:
            f.write(init_script)
        
        os.chmod(init_file, 0o755)
        logger.info(f"✅ Created initialization script: {init_file}")
    
    def print_completion_message(self):
        """Print setup completion message"""
        print("""
🎉 Enhanced Mama Bear Setup Complete!
═══════════════════════════════════════════════════════════════

✅ Directory structure created
✅ Dependencies configured  
✅ Configuration files created
✅ Docker setup ready
✅ Environment template created

🔧 Next Steps:
   1. Update API keys in .env file
   2. Run: python init_enhanced_mama_bear.py
   3. Start backend: python backend/app.py
   4. Start frontend: cd frontend && npm start
   5. Open: http://localhost:5001

🌟 Enhanced Features Available:
   🌐 Shared Browser Sessions
   🤖 Computer Use Agent  
   🔐 Authenticated Sessions
   🔍 Multi-Instance Research
   🧠 Intelligent Orchestration
   💾 Enhanced Memory System

📚 Documentation:
   • API docs will be at http://localhost:5001/docs
   • WebSocket events documented in code
   • Example usage in frontend components

🐻 Welcome to the next level of AI development assistance!
═══════════════════════════════════════════════════════════════
        """)
    
    async def run_setup(self):
        """Run the complete setup process"""
        self.print_banner()
        
        try:
            self.check_python_version()
            self.check_node_version()
            self.setup_directories()
            self.check_environment_variables()
            self.install_backend_dependencies()
            self.install_frontend_dependencies()
            self.create_config_files()
            self.create_docker_files()
            self.run_initial_setup()
            
            self.print_completion_message()
            
        except KeyboardInterrupt:
            logger.info("\n⚠️ Setup interrupted by user")
            sys.exit(1)
        except Exception as e:
            logger.error(f"❌ Setup failed: {e}")
            sys.exit(1)

def main():
    """Main setup function"""
    setup = EnhancedMamaBearSetup()
    asyncio.run(setup.run_setup())

if __name__ == "__main__":
    main()
