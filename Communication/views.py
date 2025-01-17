import imaplib
import smtplib
import email
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from django.http import JsonResponse
@login_required
def email_login_view(request):
    if request.method == 'POST':
        email_address = request.POST.get('email')
        password = request.POST.get('password')

        # Store credentials in the session
        request.session['email'] = email_address
        request.session['password'] = password
        return redirect('fetch_emails')

    return render(request, 'emaillogin.html')

@login_required

def fetch_emails_view(request):
    if 'email' not in request.session or 'password' not in request.session:
        return redirect('emaillogin')  # Redirect to login if not authenticated

    email_address = request.session['email']
    password = request.session['password']

    try:
        # Connect to Gmail's IMAP server
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(email_address, password)
        mail.select('inbox')

        # Search for unseen and all emails
        _, unseen_data = mail.search(None, 'UNSEEN')
        unseen_ids = unseen_data[0].split()

        _, all_data = mail.search(None, 'ALL')
        all_ids = all_data[0].split()

        seen_ids = [e_id for e_id in all_ids if e_id not in unseen_ids]

        def fetch_emails(email_ids):
            emails = []
            for e_id in email_ids:
                _, msg_data = mail.fetch(e_id, '(RFC822)')
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                # Extract subject and sender
                subject = msg.get('subject')
                sender = msg.get('from')

                # Parse the body
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain" and part.get("Content-Disposition") is None:
                            body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                            break
                        elif part.get_content_type() == "text/html":
                            html_content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                            body = BeautifulSoup(html_content, 'html.parser').get_text()
                            break
                else:
                    if msg.get_content_type() == "text/plain":
                        body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
                    elif msg.get_content_type() == "text/html":
                        html_content = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
                        body = BeautifulSoup(html_content, 'html.parser').get_text()

                emails.append({
                    'id': e_id.decode(),
                    'subject': subject,
                    'sender': sender,
                    'body': body.strip()
                })
            return emails

        unseen_emails = fetch_emails(unseen_ids)[::-1]
        seen_emails = fetch_emails(seen_ids)[::-1]
        all_emails = fetch_emails(all_ids)[::-1]

        mail.logout()

        # Render categories
        return render(request, 'emails_list.html', {
            'unseen_emails': unseen_emails,
            'seen_emails': seen_emails,
            'all_emails': all_emails
        })

    except imaplib.IMAP4.error as e:
        return render(request, 'emails_list.html', {'error': f'Failed to fetch emails: {e}'})

    except Exception as e:
        return render(request, 'emails_list.html', {'error': f'An unexpected error occurred: {e}'})

@login_required

def reply_email_view(request):
    if 'email' not in request.session or 'password' not in request.session:
        return JsonResponse({'error': 'Unauthorized access. Please log in first.'}, status=401)

    email_address = request.session['email']
    password = request.session['password']

    if request.method == 'POST':
        recipient = request.POST.get('recipient')
        subject = request.POST.get('subject')
        body = request.POST.get('body')

        try:
            # Connect to SMTP server
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_address, password)

            # Compose and send the email
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(email_address, recipient, message)
            server.quit()
            return JsonResponse({'success': 'Email sent successfully!'})

        except Exception as e:
            return JsonResponse({'error': f'Failed to send email: {e}'}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required

def compose_email_view(request):
    if 'email' not in request.session or 'password' not in request.session:
        return JsonResponse({'error': 'Unauthorized access. Please log in first.'}, status=401)

    email_address = request.session['email']
    password = request.session['password']

    if request.method == 'POST':
        recipient = request.POST.get('recipient')
        subject = request.POST.get('subject')
        body = request.POST.get('body')

        try:
            # Connect to SMTP server
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_address, password)

            # Compose and send the email
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(email_address, recipient, message)
            server.quit()

            return JsonResponse({'success': 'Email sent successfully!'})

        except Exception as e:
            return JsonResponse({'error': f'Failed to send email: {e}'}, status=500)

    return render(request, 'compose_email.html')
