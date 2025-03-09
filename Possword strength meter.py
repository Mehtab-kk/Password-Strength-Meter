import streamlit as st
import re
import random
import string

# List of common weak passwords
WEAK_PASSWORDS = {"password123", "123456", "qwerty", "abc123", "letmein"}

def password_strength(password):
    score = 0
    if len(password) >= 12:  # Require at least 12 characters for a strong password
        score += 2
    elif len(password) >= 8:
        score += 1
    if re.search(r"[A-Z]", password):
        score += 2  # Uppercase letters are more valuable
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"[0-9]", password):
        score += 2  # Numbers are more valuable
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 3  # Special characters are the most valuable
    return score

def strength_to_emoji(score):
    if score < 4:
        return "🔴 Weak"
    elif score < 7:
        return "🟡 Moderate"
    else:
        return "🟢 Strong"

def generate_password(length=12, include_uppercase=True, include_lowercase=True, include_numbers=True, include_special=True):
    characters = ""
    if include_uppercase:
        characters += string.ascii_uppercase
    if include_lowercase:
        characters += string.ascii_lowercase
    if include_numbers:
        characters += string.digits
    if include_special:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

import time

st.title("🔒 Password Strength Meter 🎉")
st.sidebar.header("🔒 Password Options")
password = st.text_input("🔑 Enter your password (minimum 8 characters, 1 uppercase, 1 lowercase, 1 number, 1 special character):", key="password", on_change=None)

if st.sidebar.button("✨ Generate Password", key="generate_password", disabled=False):
    password = generate_password()  # Generates a password of 12 characters by default
    st.text_input("🔑 Generated Password:", value=password, key="generated_password", disabled=True)

include_uppercase = st.sidebar.checkbox("🔠 Include Uppercase Letters", value=True)
include_lowercase = st.sidebar.checkbox("🔡 Include Lowercase Letters", value=True)
include_numbers = st.sidebar.checkbox("🔢 Include Numbers", value=True)
include_special = st.sidebar.checkbox("🔣 Include Special Characters", value=True)

if password:
    if len(password) < 8:
        st.error("Please enter at least 8 characters.")
    elif not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password) or not re.search(r"[0-9]", password) or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        st.error("Your password must include at least one uppercase letter, one lowercase letter, one number, and one special character.")
    elif password in WEAK_PASSWORDS:
        st.error("This password is too weak. Please choose a different one.")
    else:
        strength_score = password_strength(password)
        emoji = strength_to_emoji(strength_score)
        st.write(f"Password Strength: {emoji}")
        st.progress(strength_score / 10)

if st.button("✅ Check Password"):
    if password:
        st.success("Your password is included!")
        st.balloons()  # Adding a balloon animation effect when the password is checked
    else:
        st.error("Please enter a password.")
