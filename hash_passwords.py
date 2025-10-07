import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# Load credentials
with open('config/credentials.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Hash the password
stauth.Hasher.hash_passwords(config['credentials'])

# Save with hashed password
with open('config/credentials.yml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)

print("✅ Password hashed successfully!")
print("\n📝 Login Credentials:")
print("Username: admin2025")
print("Password: Medghor@2025")
