✉️ PROMAIL – Desktop Email Application

Promail is a modern desktop email application built with Python and Tkinter. It provides a clean, dark-themed interface for email login, dashboard navigation, composing messages, and sending emails through SMTP.

🚀 Features
Modern Login Interface – Clean and professional login screen.
Email Validation – Checks email address format.
Password Visibility – Show or hide your password.
Dashboard – A centralized email management interface.
Compose Email – Write emails with recipient, subject, and message.
SMTP Integration – Send emails securely using SMTP over SSL.
Logout Functionality – Safely return to the login screen.
Error Handling – Displays helpful error and success notifications.
Dark UI Theme – Modern navy, cyan, and white color scheme.
🛠️ Technologies Used
Python 3
Tkinter – Graphical User Interface
SMTP – Email delivery
SSL – Secure email connection
Regular Expressions – Email validation
EmailMessage – Email message formatting
📁 Project Structure
text
Promail/
│
├── promail.py
├── README.md
└── requirements.txt

⚙️ Installation
1. Clone the repository
bash
git clone https://github.com/YOUR_USERNAME/Promail.git

2. Navigate to the project folder
bash
cd Promail

3. Run the application

Python 3 is required. Tkinter is included with most standard Python installations.

bash
python promail.py

📧 Email Configuration

Promail uses SMTP to send emails.

For Gmail:

Enable 2-Step Verification on your Google account.
Generate a Google App Password.
Configure the following environment variables.

Windows PowerShell:

powershell
$env:PROMAIL_EMAIL="your_email@gmail.com"
$env:PROMAIL_APP_PASSWORD="your_app_password"
python promail.py


Linux / macOS:

bash
export PROMAIL_EMAIL="your_email@gmail.com"
export PROMAIL_APP_PASSWORD="your_app_password"
python promail.py


Optional SMTP configuration:

bash
PROMAIL_SMTP_HOST=smtp.gmail.com
PROMAIL_SMTP_PORT=465


Security note: Never hardcode email passwords or upload App Passwords to GitHub.

🖥️ Application Screens
Login Screen
Email Dashboard
Compose Email Window
Email Sending Notifications
Logout Interface
🔮 Future Improvements
Real-time inbox synchronization using IMAP.
User registration and authentication.
Inbox email viewing.
Sent email history.
Email attachments.
Search and filter emails.
Save and manage drafts.
Delete and archive emails.
Multiple email account support.
Improved security and credential management.
⚠️ Current Limitations
Login currently validates email format but does not authenticate user credentials.
Inbox, Sent, Drafts, Starred, and Trash are interface placeholders.
SMTP sending requires valid email credentials and provider configuration.
Gmail SMTP is the default configuration.
🤝 Contributing

Contributions are welcome!

Fork this repository.
Create a new feature branch.
Commit your changes.
Push your branch.
Submit a Pull Request.
📄 License

This project is available under the MIT License. Add a LICENSE file to the repository to apply the license formally.

Developed with ❤️ using Python and Tkinter.

Promail – Your emails. Your world.