#!/usr/bin/env python
"""
Generate secure secret keys for production environment
"""
import secrets
import sys


def generate_secret_key(length: int = 32) -> str:
    """Generate a secure random secret key"""
    return secrets.token_hex(length)


def main():
    """Generate and display secret keys"""
    print("=" * 80)
    print("SECRET KEY GENERATOR")
    print("=" * 80)
    print()
    print("Generating secure random keys for production use...")
    print()
    
    # Generate two different keys
    secret_key = generate_secret_key(32)  # 64 hex characters
    jwt_secret = generate_secret_key(32)  # 64 hex characters
    
    print("Generated Keys:")
    print("-" * 80)
    print()
    print(f"SECRET_KEY={secret_key}")
    print(f"JWT_SECRET={jwt_secret}")
    print()
    print("-" * 80)
    print()
    print("📋 INSTRUCTIONS:")
    print()
    print("1. Copy the keys above")
    print("2. Open your .env.prod file")
    print("3. Replace CHANGE_ME_USE_STRONG_SECRET with the generated keys")
    print()
    print("⚠️  IMPORTANT SECURITY NOTES:")
    print("   • Keep these keys SECRET - never commit them to version control")
    print("   • Use different keys for development and production")
    print("   • Store production keys securely (e.g., environment variables, secrets manager)")
    print("   • Rotate keys periodically (e.g., every 90 days)")
    print("   • If keys are compromised, generate new ones immediately")
    print()
    print("✅ These keys are cryptographically secure and suitable for production use.")
    print()
    
    # Optionally offer to update the file
    print("=" * 80)
    update = input("\nDo you want to automatically update .env.prod? (y/n): ").strip().lower()
    
    if update == 'y':
        try:
            import os
            env_prod_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                '.env.prod'
            )
            
            if not os.path.exists(env_prod_path):
                print(f"\n❌ Error: .env.prod not found at {env_prod_path}")
                return 1
            
            # Read the file
            with open(env_prod_path, 'r') as f:
                content = f.read()
            
            # Create backup
            backup_path = env_prod_path + '.backup'
            with open(backup_path, 'w') as f:
                f.write(content)
            print(f"\n✅ Backup created: {backup_path}")
            
            # Replace the keys
            content = content.replace(
                'SECRET_KEY=CHANGE_ME_USE_STRONG_SECRET',
                f'SECRET_KEY={secret_key}'
            )
            content = content.replace(
                'JWT_SECRET=CHANGE_ME_USE_STRONG_SECRET',
                f'JWT_SECRET={jwt_secret}'
            )
            
            # Write updated content
            with open(env_prod_path, 'w') as f:
                f.write(content)
            
            print(f"✅ Updated: {env_prod_path}")
            print("\n🎉 Production secrets have been set!")
            print("\n⚠️  Remember to:")
            print("   1. Delete the backup file after verifying")
            print("   2. Never commit .env.prod to version control")
            print("   3. Use environment variables in production deployment")
            
        except Exception as e:
            print(f"\n❌ Error updating file: {e}")
            print("Please update .env.prod manually with the keys shown above.")
            return 1
    else:
        print("\n✅ Keys generated. Please update .env.prod manually.")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        sys.exit(1)
