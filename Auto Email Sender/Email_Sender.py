
import tkinter as tk
from tkinter import ttk, messagebox
import smtplib
import re
import ssl
import os
from email.message import EmailMessage



# APPLICATION CONFIGURATION


APP_NAME = "PROMAIL"
BG = "#0F172A"
CARD = "#1E293B"
ACCENT = "#38BDF8"
WHITE = "#F8FAFC"
MUTED = "#94A3B8"
GREEN = "#22C55E"
RED = "#EF4444"


class PromailApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Promail | Email Client")
        self.root.geometry("1000x650")
        self.root.minsize(800, 550)
        self.root.configure(bg=BG)

        self.user_email = ""

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.show_login()


    # CLEAR WINDOW


    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


    # EMAIL VALIDATION


    def valid_email(self, email):
        pattern = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"
        return re.match(pattern, email) is not None

    # LOGIN SCREEN


    def show_login(self):
        self.clear_window()

        container = tk.Frame(self.root, bg=BG)
        container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            container,
            text="✉ PROMAIL",
            font=("Calibri", 32, "bold"),
            fg=ACCENT,
            bg=BG
        ).pack(pady=(0, 5))

        tk.Label(
            container,
            text="Your emails. Your world.",
            font=("Calibri", 12),
            fg=MUTED,
            bg=BG
        ).pack(pady=(0, 25))

        card = tk.Frame(
            container,
            bg=CARD,
            padx=45,
            pady=35
        )
        card.pack()

        tk.Label(
            card,
            text="Welcome Back",
            font=("Calibri", 23, "bold"),
            fg=WHITE,
            bg=CARD
        ).pack(pady=(0, 5))

        tk.Label(
            card,
            text="Sign in to continue to Promail",
            font=("Calibri", 11),
            fg=MUTED,
            bg=CARD
        ).pack(pady=(0, 25))

        tk.Label(
            card,
            text="EMAIL ADDRESS",
            font=("Calibri", 10, "bold"),
            fg=WHITE,
            bg=CARD
        ).pack(anchor="w")

        self.email_entry = tk.Entry(
            card,
            width=35,
            font=("Calibri", 12),
            bg="#334155",
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat"
        )
        self.email_entry.pack(ipady=10, pady=(7, 18))

        tk.Label(
            card,
            text="PASSWORD",
            font=("Calibri", 10, "bold"),
            fg=WHITE,
            bg=CARD
        ).pack(anchor="w")

        password_frame = tk.Frame(card, bg="#334155")
        password_frame.pack(fill="x", pady=(7, 10))

        self.password_entry = tk.Entry(
            password_frame,
            width=29,
            show="*",
            font=("Calibri", 12),
            bg="#334155",
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat"
        )
        self.password_entry.pack(
            side="left",
            ipady=10,
            padx=8
        )

        self.show_password = False

        self.toggle_btn = tk.Button(
            password_frame,
            text="Show",
            bg="#334155",
            fg=ACCENT,
            relief="flat",
            command=self.toggle_password
        )
        self.toggle_btn.pack(side="right", padx=5)

        self.status_label = tk.Label(
            card,
            text="",
            fg=RED,
            bg=CARD,
            font=("Calibri", 10)
        )
        self.status_label.pack()

        tk.Button(
            card,
            text="LOGIN",
            font=("Calibri", 12, "bold"),
            bg=ACCENT,
            fg=BG,
            activebackground="#0EA5E9",
            relief="flat",
            cursor="hand2",
            command=self.login
        ).pack(fill="x", ipady=10, pady=(10, 15))

        tk.Label(
            container,
            text="© 2026 Promail | Secure Email Experience",
            font=("Calibri", 9),
            fg=MUTED,
            bg=BG
        ).pack(pady=20)

        self.email_entry.focus()

        self.root.bind("<Return>", lambda event: self.login())


    # SHOW / HIDE PASSWORD


    def toggle_password(self):
        self.show_password = not self.show_password

        self.password_entry.config(
            show="" if self.show_password else "*"
        )

        self.toggle_btn.config(
            text="Hide" if self.show_password else "Show"
        )


    # LOGIN FUNCTION


    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        if not email or not password:
            self.status_label.config(
                text="Please fill in all fields."
            )
            return

        if not self.valid_email(email):
            self.status_label.config(
                text="Please enter a valid email address."
            )
            return

        # SMTP credentials are not automatically
        # verified by this local login.
        self.user_email = email

        self.show_dashboard()

    # DASHBOARD


    def show_dashboard(self):
        self.clear_window()
        self.root.unbind("<Return>")

        sidebar = tk.Frame(
            self.root,
            bg="#111827",
            width=220
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="✉ PROMAIL",
            font=("Calibri", 23, "bold"),
            fg=ACCENT,
            bg="#111827"
        ).pack(pady=30)

        tk.Button(
            sidebar,
            text="+ Compose Email",
            font=("Calibri", 11, "bold"),
            bg=ACCENT,
            fg=BG,
            relief="flat",
            cursor="hand2",
            command=self.compose_email
        ).pack(fill="x", padx=15, pady=15, ipady=10)

        for item in ["Inbox", "Sent", "Drafts", "Starred", "Trash"]:
            tk.Button(
                sidebar,
                text="   " + item,
                font=("Calibri", 12),
                bg="#111827",
                fg=WHITE,
                activebackground=CARD,
                activeforeground=ACCENT,
                relief="flat",
                anchor="w",
                cursor="hand2"
            ).pack(fill="x", padx=10, pady=5, ipady=8)

        tk.Button(
            sidebar,
            text="Logout",
            font=("Calibri", 11, "bold"),
            bg=RED,
            fg=WHITE,
            relief="flat",
            cursor="hand2",
            command=self.logout
        ).pack(side="bottom", fill="x", padx=15, pady=20, ipady=8)

        main = tk.Frame(self.root, bg=BG)
        main.pack(side="left", fill="both", expand=True)

        header = tk.Frame(main, bg=BG)
        header.pack(fill="x", padx=30, pady=25)

        tk.Label(
            header,
            text="Dashboard",
            font=("Calibri", 27, "bold"),
            fg=WHITE,
            bg=BG
        ).pack(side="left")

        tk.Label(
            header,
            text=self.user_email,
            font=("Calibri", 11),
            fg=MUTED,
            bg=BG
        ).pack(side="right")

        tk.Label(
            main,
            text="Welcome to Promail!",
            font=("Calibri", 21, "bold"),
            fg=ACCENT,
            bg=BG
        ).pack(anchor="w", padx=30, pady=10)

        tk.Label(
            main,
            text="Manage your email communication in one place.",
            font=("Calibri", 12),
            fg=MUTED,
            bg=BG
        ).pack(anchor="w", padx=30)

        # Dashboard cards

        cards = tk.Frame(main, bg=BG)
        cards.pack(fill="x", padx=30, pady=35)

        for title, subtitle in [
            ("INBOX", "Your received emails"),
            ("SENT", "Your sent messages"),
            ("DRAFTS", "Your saved drafts")
        ]:
            card = tk.Frame(
                cards,
                bg=CARD,
                padx=20,
                pady=25
            )
            card.pack(side="left", fill="both", expand=True, padx=7)

            tk.Label(
                card,
                text=title,
                font=("Calibri", 15, "bold"),
                fg=ACCENT,
                bg=CARD
            ).pack(anchor="w")

            tk.Label(
                card,
                text=subtitle,
                font=("Calibri", 10),
                fg=MUTED,
                bg=CARD
            ).pack(anchor="w", pady=10)

        tk.Label(
            main,
            text="Quick Actions",
            font=("Calibri", 18, "bold"),
            fg=WHITE,
            bg=BG
        ).pack(anchor="w", padx=30, pady=10)

        tk.Button(
            main,
            text="✉  Compose a New Email",
            font=("Calibri", 12, "bold"),
            bg=ACCENT,
            fg=BG,
            relief="flat",
            command=self.compose_email
        ).pack(anchor="w", padx=30, pady=10, ipadx=15, ipady=10)


# COMPOSE EMAIL


    def compose_email(self):
        window = tk.Toplevel(self.root)
        window.title("Promail | Compose")
        window.geometry("600x550")
        window.configure(bg=BG)
        window.transient(self.root)

        tk.Label(
            window,
            text="Compose New Email",
            font=("Calibri", 22, "bold"),
            fg=ACCENT,
            bg=BG
        ).pack(pady=20)

        form = tk.Frame(window, bg=CARD, padx=25, pady=25)
        form.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(
            form,
            text="Recipient Email",
            fg=WHITE,
            bg=CARD
        ).pack(anchor="w")

        recipient = tk.Entry(form, font=("Calibri", 12))
        recipient.pack(fill="x", ipady=7, pady=8)

        tk.Label(
            form,
            text="Subject",
            fg=WHITE,
            bg=CARD
        ).pack(anchor="w")

        subject = tk.Entry(form, font=("Calibri", 12))
        subject.pack(fill="x", ipady=7, pady=8)

        tk.Label(
            form,
            text="Message",
            fg=WHITE,
            bg=CARD
        ).pack(anchor="w")

        body = tk.Text(
            form,
            height=10,
            font=("Calibri", 12),
            wrap="word"
        )
        body.pack(fill="both", expand=True, pady=8)

        tk.Button(
            form,
            text="SEND EMAIL",
            font=("Calibri", 11, "bold"),
            bg=ACCENT,
            fg=BG,
            relief="flat",
            cursor="hand2",
            command=lambda: self.send_email(
                recipient.get(),
                subject.get(),
                body.get("1.0", "end-1c"),
                window
            )
        ).pack(fill="x", ipady=10, pady=10)

 # SEND EMAIL USING SMTP


    def send_email(self, recipient, subject, body, window):

        recipient = recipient.strip()

        if not self.valid_email(recipient):
            messagebox.showerror(
                "Invalid Recipient",
                "Please enter a valid recipient email."
            )
            return

        if not subject.strip() or not body.strip():
            messagebox.showwarning(
                "Missing Information",
                "Please enter a subject and message."
            )
            return

        smtp_user = os.getenv("PROMAIL_EMAIL")
        smtp_password = os.getenv("PROMAIL_APP_PASSWORD")
        smtp_host = os.getenv("PROMAIL_SMTP_HOST", "smtp.gmail.com")
        smtp_port = int(os.getenv("PROMAIL_SMTP_PORT", "465"))

        if not smtp_user or not smtp_password:
            messagebox.showerror(
                "SMTP Configuration",
                "Set PROMAIL_EMAIL and PROMAIL_APP_PASSWORD "
                "environment variables before sending."
            )
            return

        try:
            msg = EmailMessage()
            msg["From"] = smtp_user
            msg["To"] = recipient
            msg["Subject"] = subject
            msg.set_content(body)

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL(
                smtp_host,
                smtp_port,
                context=context,
                timeout=20
            ) as server:

                server.login(smtp_user, smtp_password)
                server.send_message(msg)

            messagebox.showinfo(
                "Success",
                "Your email has been sent successfully!"
            )

            window.destroy()

        except (smtplib.SMTPException, OSError, ValueError) as error:
            messagebox.showerror(
                "Email Error",
                f"Unable to send email:\n{error}"
            )

# Logout function

    def logout(self):
        confirm = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        )

        if confirm:
            self.user_email = ""
            self.show_login()



if __name__ == "__main__":
    root = tk.Tk()
    app = PromailApp(root)
    root.mainloop()
