import math
import getpass  # ✅ Importing getpass

# Load top 10,000 common passwords from file
def load_common_passwords(file_path="common_passwords.txt"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        print("Warning: common_passwords.txt file not found.")
        return set()

# Calculate entropy based on charset and length
def calculate_entropy(password):
    charset_size = 0
    if any(c.islower() for c in password):
        charset_size += 26
    if any(c.isupper() for c in password):
        charset_size += 26
    if any(c.isdigit() for c in password):
        charset_size += 10
    if any(c in "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?`~" for c in password):
        charset_size += 32  # Estimated number of special chars

    # Entropy = length * log2(charset size)
    if charset_size == 0:
        return 0
    return round(len(password) * math.log2(charset_size), 2)

# Estimate brute-force time assuming 1 billion guesses per second
def estimate_crack_time(entropy):
    guesses = 2 ** entropy
    seconds = guesses / 1e9
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.2f} minutes"
    elif seconds < 86400:
        return f"{seconds/3600:.2f} hours"
    else:
        return f"{seconds/86400:.2f} days"

# Evaluate the strength of a password
def analyze_password(password, common_passwords):
    entropy = calculate_entropy(password)
    crack_time = estimate_crack_time(entropy)
    is_common = password in common_passwords

    print("\n🔐 Password Strength Report\n")
    print(f"🧠 Entropy: {entropy} bits")
    print("ℹ️  Entropy measures how unpredictable your password is.")
    print("    Higher entropy = harder to guess.")
    if entropy < 40:
        print("❌ This password is weak (entropy < 40).")
    elif entropy < 60:
        print("⚠️  This password is moderate (entropy between 40–60).")
    else:
        print("✅ This password is strong (entropy > 60).")

    print(f"\n🕒 Estimated Time to Crack (Brute-force): {crack_time}")
    
    if is_common:
        print("🚨 This password was found in a list of 10,000 common leaked passwords.")
    else:
        print("✅ This password is NOT in the top 10,000 common passwords list.")
    
    print("\n🔁 Tip: Use a longer password with a mix of uppercase, lowercase, numbers, and special characters.")

# Main execution
if __name__ == "__main__":
    user_pass = getpass.getpass("Enter your password to evaluate: ")  # 🔐 Hidden password input
    common_passwords = load_common_passwords()
    analyze_password(user_pass, common_passwords)