import streamlit as st
import datetime

# ---------------- BANK LOGIC ---------------- #

class BankAccount:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        self.balance = 0
        self.th = []

    def current_time(self):
        return datetime.datetime.now().strftime("%d %B %y, %H:%M:%S")

    def deposit(self, amount):
        self.balance += amount
        self.th.append(f"{amount} Deposit on {self.current_time()}")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.th.append(f"{amount} Withdraw on {self.current_time()}")
            return True
        return False


# ---------------- SESSION STATE ---------------- #

if "accounts" not in st.session_state:
    st.session_state.accounts = {}

if "current_account" not in st.session_state:
    st.session_state.current_account = None


# ---------------- UI ---------------- #

st.title("🏦 Harshit Small Finance Bank")

# ----------- NOT LOGGED IN ----------- #
if st.session_state.current_account is None:

    option = st.radio("Choose an option", ["Create Account", "Login"])

    name = st.text_input("Account Name")
    pin = st.text_input("PIN (4 digits)", type="password")

    if st.button(option):

        # CREATE ACCOUNT
        if option == "Create Account":
            if name in st.session_state.accounts:
                st.error("Account already exists")
            elif len(pin) != 4:
                st.error("PIN must be exactly 4 digits")
            else:
                st.session_state.accounts[name] = BankAccount(name, pin)
                st.session_state.current_account = name
                st.success("Account created & logged in")

        # LOGIN
        else:
            if name not in st.session_state.accounts:
                st.error("Account does not exist")
            elif st.session_state.accounts[name].pin != pin:
                st.error("Incorrect PIN")
            else:
                st.session_state.current_account = name
                st.success("Login successful")


# ----------- LOGGED IN ----------- #
else:
    acc = st.session_state.accounts[st.session_state.current_account]

    st.subheader(f"Welcome {acc.name}")
    action = st.selectbox(
        "Choose Action",
        [
            "Deposit",
            "Withdraw",
            "Check Balance",
            "Transaction History",
            "Reset PIN",
            "Logout"
        ]
    )

    if action == "Deposit":
        amount = st.number_input("Enter amount", min_value=1)
        if st.button("Deposit"):
            acc.deposit(amount)
            st.success(f"Rs.{amount} deposited")

    elif action == "Withdraw":
        amount = st.number_input("Enter amount", min_value=1)
        if st.button("Withdraw"):
            if acc.withdraw(amount):
                st.success(f"Rs.{amount} withdrawn")
            else:
                st.error("Insufficient balance")

    elif action == "Check Balance":
        st.info(f"Current Balance: Rs.{acc.balance}")

    elif action == "Transaction History":
        if acc.th:
            for t in acc.th:
                st.write(t)
        else:
            st.warning("No transactions found")

    elif action == "Reset PIN":
        new_pin = st.text_input("Enter new 4-digit PIN", type="password")
        if st.button("Reset PIN"):
            if len(new_pin) != 4:
                st.error("PIN must be exactly 4 digits")
            else:
                acc.pin = new_pin
                st.success("PIN updated successfully")

    elif action == "Logout":
        st.session_state.current_account = None
        st.success("Logged out successfully")