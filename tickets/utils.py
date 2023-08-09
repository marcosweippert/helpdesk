# utils.py (aplicativo helpdesk)

from .models import Ticket, Attachment

def attach_files_to_ticket(ticket, files):
    for file in files:
        attachment = Attachment.objects.create(file=file)
        ticket.attachments.add(attachment)
