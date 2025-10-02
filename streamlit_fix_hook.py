# Hook to fix Streamlit metadata issues in PyInstaller
import sys
import os

# Fix for importlib.metadata issue with Streamlit
def fix_streamlit_metadata():
    try:
        import importlib.metadata as metadata
        
        # Create a fake distribution for streamlit if it doesn't exist
        class FakeDistribution:
            def __init__(self, name, version):
                self.name = name
                self.version = version
                self.metadata = {'Name': name, 'Version': version}
            
            def read_text(self, filename):
                if filename == 'METADATA':
                    return f"Name: {self.name}\nVersion: {self.version}\n"
                return ""
        
        # Monkey patch the from_name method
        original_from_name = metadata.distribution
        
        def patched_from_name(name):
            try:
                return original_from_name(name)
            except Exception:
                # Return fake distribution for known packages
                if name == 'streamlit':
                    return FakeDistribution('streamlit', '1.49.1')
                elif name == 'altair':
                    return FakeDistribution('altair', '5.0.0')
                elif name == 'pandas':
                    return FakeDistribution('pandas', '2.0.0')
                elif name == 'numpy':
                    return FakeDistribution('numpy', '1.24.0')
                else:
                    return FakeDistribution(name, '1.0.0')
        
        metadata.distribution = patched_from_name
        
        # Also patch the version function
        original_version = metadata.version
        
        def patched_version(name):
            try:
                return original_version(name)
            except Exception:
                if name == 'streamlit':
                    return '1.49.1'
                elif name == 'altair':
                    return '5.0.0'
                elif name == 'pandas':
                    return '2.0.0'
                elif name == 'numpy':
                    return '1.24.0'
                else:
                    return '1.0.0'
        
        metadata.version = patched_version
        
    except ImportError:
        pass  # If importlib.metadata is not available, continue without it

# Apply the fix immediately when imported
fix_streamlit_metadata()