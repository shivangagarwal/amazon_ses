# amazon_ses


Requirements:

Python Boto Library

AWS access Key and Secret: You can create new pair in Amazon AWS console


Usage:

import emailSES

sender_id = "sender@example.com"

to_addresses = "to_address@example.com"

subject = "Test Subject"

body = "This is a test body"

email_type = "text" #It can have values text or html

send_email(sender_id, subject, body, to_addresses, None, None, email_type)
