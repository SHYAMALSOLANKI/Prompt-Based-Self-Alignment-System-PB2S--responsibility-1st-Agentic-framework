"""
PB2S Dashboard Launcher - Metadata-Safe Version
This version bypasses the importlib.metadata issues by setting up a clean environment first.
"""

import os
import sys

# Fix environment before importing anything else
def setup_environment():
    """Setup environment to avoid metadata conflicts"""
    
    # Set environment variables to disable problematic features
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    os.environ['STREAMLIT_GLOBAL_DEVELOPMENT_MODE'] = 'false'
    
    # Disable version checking that causes metadata issues
    import types
    
    # Create a mock importlib.metadata module if needed
    try:
        import importlib.metadata
    except ImportError:
        # Create a fake metadata module
        fake_metadata = types.ModuleType('metadata')
        
        def fake_version(package_name):
            # Return reasonable default versions for known packages
            versions = {
                'streamlit': '1.49.1',
                'altair': '5.0.0',
                'pandas': '2.0.0',
                'numpy': '1.24.0',
                'requests': '2.31.0',
                'tornado': '6.3.0'
            }
            return versions.get(package_name, '1.0.0')
        
        def fake_distribution(package_name):
            class FakeDist:
                def __init__(self, name):
                    self.metadata = {'Name': name, 'Version': fake_version(name)}
                    self.version = fake_version(name)
            return FakeDist(package_name)
        
        fake_metadata.version = fake_version
        fake_metadata.distribution = fake_distribution
        
        # Insert into sys.modules
        sys.modules['importlib.metadata'] = fake_metadata
        importlib.metadata = fake_metadata

def patch_streamlit():
    """Patch Streamlit to avoid metadata calls"""
    try:
        # Import and patch before streamlit loads
        import importlib
        import types
        
        # Patch the version module specifically
        def create_fake_version_module():
            version_module = types.ModuleType('streamlit.version')
            version_module.__version__ = '1.49.1'
            version_module.VERSION = '1.49.1'
            return version_module
        
        # Pre-load the version module
        sys.modules['streamlit.version'] = create_fake_version_module()
        
        # Also patch streamlit._version if it exists
        sys.modules['streamlit._version'] = create_fake_version_module()
        
    except Exception as e:
        print(f"Warning: Could not patch streamlit version: {e}")

def main():
    """Main launcher function"""
    try:
        # Setup environment first
        setup_environment()
        
        # Patch Streamlit
        patch_streamlit()
        
        # Now import streamlit
        import streamlit as st
        from streamlit.web import cli as stcli
        import subprocess
        import threading
        import time
        
        # Also start the Main Brain server
        def start_main_brain():
            try:
                from server.main import app
                import uvicorn
                uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")
            except Exception as e:
                print(f"Could not start Main Brain server: {e}")
        
        # Start Main Brain in a separate thread
        brain_thread = threading.Thread(target=start_main_brain, daemon=True)
        brain_thread.start()
        
        # Wait a moment for server to start
        time.sleep(2)
        
        # Configure Streamlit
        st.set_page_config(
            page_title="PB2S Dashboard",
            page_icon="🧠",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Import the main dashboard content
        exec(open('pb2s_dashboard_content.py').read())
        
    except Exception as e:
        print(f"Error starting PB2S Dashboard: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()