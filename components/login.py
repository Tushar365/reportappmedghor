"""Login and authentication UI components"""
import streamlit as st
from utils.auth import AuthManager
from utils.database import log_action

def render_login_page():
    """Render login page"""
    st.title("🔐 Medghor Login")
    st.markdown("Please login to access the Focus Item PDF Generator")
    
    auth_manager = AuthManager()
    
    # Login form
    auth_manager.login()
    
    # Check authentication status
    if st.session_state.get('authentication_status'):
        st.success(f"Welcome {st.session_state.get('name')}!")
        log_action(
            st.session_state.get('username'),
            'LOGIN',
            f"User logged in at {st.datetime.now()}"
        )
        return True
    elif st.session_state.get('authentication_status') is False:
        st.error('Username/password is incorrect')
        return False
    elif st.session_state.get('authentication_status') is None:
        st.warning('Please enter your username and password')
        
        # Show registration option
        with st.expander("📝 New User? Register Here"):
            auth_manager.register_user()
        
        return False

def render_user_menu():
    """Render user menu in sidebar"""
    if st.session_state.get('authentication_status'):
        auth_manager = AuthManager()
        
        st.sidebar.markdown("---")
        st.sidebar.write(f"👤 **{st.session_state.get('name')}**")
        st.sidebar.write(f"Role: {st.session_state.get('roles', ['viewer'])[0]}")
        
        # User menu options
        with st.sidebar.expander("⚙️ Account Settings"):
            if st.button("🔑 Change Password"):
                st.session_state.show_password_reset = True
            if st.button("✏️ Update Profile"):
                st.session_state.show_profile_update = True
        
        # Logout button
        auth_manager.logout()
        
        # Handle modals
        if st.session_state.get('show_password_reset'):
            auth_manager.reset_password()
        
        if st.session_state.get('show_profile_update'):
            auth_manager.update_user_details()

def check_permission(required_role):
    """Check if user has required permission"""
    user_roles = st.session_state.get('roles', [])
    
    role_hierarchy = {
        'admin': 3,
        'manager': 2,
        'viewer': 1
    }
    
    user_level = max([role_hierarchy.get(role, 0) for role in user_roles])
    required_level = role_hierarchy.get(required_role, 0)
    
    return user_level >= required_level
