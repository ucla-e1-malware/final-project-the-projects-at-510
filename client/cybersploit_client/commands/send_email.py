from ..commands import Command
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_SUBJECT = "Verify your login attempt"

EMAIL_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Email + Login UI</title>
<style>
  :root {
    --bg-color: #0e0f11;
    --card-bg: #18191c;
    --accent: #f6851b;
    --text-color: #f0f0f0;
    --input-bg: #222327;
    --input-border: #2d2f34;
    --radius: 16px;
  }

  body {
    margin: 0;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: radial-gradient(circle at top, #141518, #0e0f11);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 60px;
    position: relative;
    overflow-x: hidden;
  }

  .emoji-bg {
    position: fixed;
    font-size: 80px;
    opacity: 1;
    pointer-events: none;
    z-index: 0;
    animation: float 4s ease-in-out infinite;
  }

  @keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-5px); }
  }

  .email-container {
    background: #fff;
    color: #202124;
    border-radius: 12px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.3);
    width: 500px;
    padding: 24px 28px;
    font-family: "Roboto", sans-serif;
    position: relative;
    z-index: 1;
  }

  .email-header {
    display: flex;
    align-items: center;
    margin-bottom: 18px;
  }

  .sender-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: #f6851b;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    margin-right: 12px;
    font-size: 1rem;
  }

  .sender-info {
    display: flex;
    flex-direction: column;
  }

  .sender-name {
    font-weight: 600;
    font-size: 0.95rem;
  }

  .sender-email {
    font-size: 0.85rem;
    color: #5f6368;
  }

  .email-subject {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 12px;
  }

  .email-body {
    font-size: 0.95rem;
    line-height: 1.6;
    color: #3c4043;
  }

  .email-body strong {
    color: #202124;
  }

  .arrow {
    font-size: 42px;
    color: var(--accent);
    margin: 48px 0 36px;
    animation: bounce 1.6s infinite;
    position: relative;
    z-index: 1;
  }

  @keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(8px); }
  }

  .login-card {
    background: var(--card-bg);
    padding: 48px 40px;
    border-radius: var(--radius);
    box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    width: 360px;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
    z-index: 1;
  }

  .login-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.5);
  }

  .logo {
    width: 250px;
    height: 80px;
    background: linear-gradient(135deg, var(--accent), #ffb547);
    border-radius: 20%;
    margin: 0 auto 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 34px;
    font-weight: 700;
    color: #fff;
    letter-spacing: -1px;
  }

  h2 {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 12px;
  }

  p.description {
    font-size: 0.9rem;
    color: #b3b3b3;
    margin-bottom: 28px;
    line-height: 1.5;
  }

  form {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  input {
    background: var(--input-bg);
    border: 1px solid var(--input-border);
    border-radius: 10px;
    padding: 12px 14px;
    color: var(--text-color);
    font-size: 0.95rem;
    outline: none;
    transition: border 0.2s;
  }

  input:focus {
    border-color: var(--accent);
  }

  button {
    background: linear-gradient(135deg, var(--accent), #ffb547);
    border: none;
    border-radius: 10px;
    padding: 12px;
    font-size: 1rem;
    color: #fff;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
  }

  button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(246,133,27,0.4);
  }

  .subtext {
    margin-top: 16px;
    font-size: 0.85rem;
    color: #a0a0a0;
  }

  .subtext a {
    color: var(--accent);
    text-decoration: none;
    font-weight: 500;
  }

  .subtext a:hover {
    text-decoration: underline;
  }

  .login-btn {
    display: block;
    text-align: center;
    background: linear-gradient(135deg, var(--accent), #ffb547);
    border-radius: 10px;
    padding: 12px;
    font-size: 1rem;
    color: #fff;
    font-weight: 600;
    text-decoration: none;
    transition: transform 0.2s, box-shadow 0.2s;
  }

  .login-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(246,133,27,0.4);
  }

</style>
</head>
<body>

  <div class="emoji-bg" style="top: 48%; left: 18%; animation-delay: 2s;">😳</div>
  <div class="emoji-bg" style="top: 78%; right: 16%; animation-delay: 0.8s;">😧</div>

  <div class="email-container">
    <div class="email-header">
      <div class="sender-avatar">M</div>
      <div class="sender-info">
        <div class="sender-name">MetaMask Security</div>
        <div class="sender-email">no-reply@metamask.io</div>
      </div>
    </div>

    <div class="email-subject">Verify your login attempt</div>
    <div class="email-body">
      Hi there,<br><br>
      We detected a new login attempt to your <strong>MetaMask account</strong>.<br>
      To secure your account, please log in below.<br><br>
      If you do not complete this request within 5 hours, your account and its funds will be forfeited.
      <br><br>
If this was you, please <a href="#login">click here</a> to continue.<br><br>

      – The MetaMask Team
    </div>
  </div>

  <div class="arrow">⬇️</div>
  <div class="arrow">⬇️</div>
  <div class="arrow">⬇️</div>
  <div class="arrow">⬇️</div>
  <div class="arrow">⬇️</div>

<div id="login" class="login-card">

    <div class="logo">🚨 🦊 🚨</div>
    <h1>Log In Now or Lose Your Funds</h1>
    <p class="description">
      ⚠️ Your account is currently under attack. ⚠️ <br> Log into your account now and secure your account, or risk losing all of your crypto stored with MetaMask.
    </p>
    <form>
      <input type="text" placeholder="Username or Email" required>
      <input type="password" placeholder="Password" required>
      <a href="https://www.reddit.com/r/childfree/" class="login-btn">Login</a>
    </form>
  </div>

</body>
</html>
"""

def send_email_func(recipient):
    smtp_server, port = ("e1-mail.acmcyber.com", 32525)
    username, password = ("TheProjects@510", "hunter2")
    
    message = MIMEMultipart("alternative")
    message["From"] = "the-projects-at-510@e1-mail.acmcyber.com"
    message["To"] = recipient
    message["Subject"] = EMAIL_SUBJECT
    
    message.attach(MIMEText(EMAIL_HTML, "html"))
    
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(username, password)
        server.sendmail(message["From"], message["To"], message.as_string())
    
    print(f"Email sent to {recipient}")

class SendEmail(Command):
    """Send an email to a recipient"""
    
    def do_command(self, lines: str, *args):
        recipient = lines.strip()
        if recipient:
            send_email_func(recipient)
        else:
            print("No recipient provided")

command = SendEmail