"""Authentication manager using streamlit-authenticator"""
import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from datetime import datetime, timedelta

class AuthManager:
    def __init__(self, config_file='config/credentials.yml'):
        """Initialize authentication manager"""
        self.config_file = config_file
        self.load_config()
        self.authenticator = stauth.Authenticate(
            self.config['credentials'],
            self.config['cookie']['name'],
            self.config['cookie']['key'],
            self.config['cookie']['expiry_days']
        )
    
    def load_config(self):
        """Load authentication config"""
        try:
            with open(self.config_file) as file:
                self.config = yaml.load(file, Loader=SafeLoader)
        except FileNotFoundError:
            self.create_default_config()
    
    def create_default_config(self):
        """Create default config file"""
        self.config = {
            'cookie': {
                'expiry_days': 30,
                'key': 'medghor_signature_key',
                'name': 'medghor_cookie'
            },
            'credentials': {
                'usernames': {
                    'admin': {
                        'email': 'admin@medghor.com',
                        'failed_login_attempts': 0,
                        'first_name': 'Admin',
                        'last_name': 'User',
                        'logged_in': False,
                        'password': 'admin123',  # Will be hashed
                        'roles': ['admin']
                    }
                }
            }
        }
        
        # Hash passwords
        stauth.Hasher.hash_passwords(self.config['credentials'])
        
        # Save config
        with open(self.config_file, 'w') as file:
            yaml.dump(self.config, file, default_flow_style=False)
    
    def login(self):
        """Display login form and authenticate"""
        try:
            return self.authenticator.login('main')
        except Exception as e:
            st.error(f"Login error: {e}")
            return None
    
    def logout(self):
        """Logout current user"""
        self.authenticator.logout('Logout', 'sidebar')
    
    def register_user(self):
        """Display registration form"""
        try:
            if self.authenticator.register_user('main'):
                st.success('User registered successfully')
                # Save updated config
                with open(self.config_file, 'w') as file:
                    yaml.dump(self.config, file, default_flow_style=False)
        except Exception as e:
            st.error(e)
    
    def reset_password(self):
        """Display password reset form"""
        try:
            if self.authenticator.reset_password(st.session_state['username'], 'main'):
                st.success('Password reset successfully')
                with open(self.config_file, 'w') as file:
                    yaml.dump(self.config, file, default_flow_style=False)
        except Exception as e:
            st.error(e)
    
    def update_user_details(self):
        """Display user details update form"""
        try:
            if self.authenticator.update_user_details(st.session_state['username'], 'main'):
                st.success('User details updated successfully')
                with open(self.config_file, 'w') as file:
                    yaml.dump(self.config, file, default_flow_style=False)
        except Exception as e:
            st.error(e)
