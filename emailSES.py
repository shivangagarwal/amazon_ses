import logging
from boto.ses import SESConnection
from boto.exception import BotoServerError


logger = logging.getLogger(__name__)
#logging.basicConfig(level = logging.DEBUG)

#The security credentials of Amazon AWS. Must not be null
aws_access_key_id = "Your AWS Access Key ID"
aws_secret_access_key = "Your AWS Secret"
 


def make_amazon_ses_connection():
    '''
    This method will make the Amazon SES (Simple Email Service) connection. 
    For making the connection the AWS access key and the AWS Secret key will be
    needed.
    '''
    global logger, aws_access_key_id, aws_secret_access_key
    #remove extra whitespaces from the beginning and end
    assert aws_access_key_id is not None, "The aws_access_key_id is None."
    assert aws_secret_access_key is not None, "The aws_secret_access_key is None"
    aws_access_key_id = aws_access_key_id.strip()
    aws_secret_access_key = aws_secret_access_key.strip()
    connection = SESConnection(aws_access_key_id = aws_access_key_id, 
	    aws_secret_access_key = aws_secret_access_key)
    return connection

def send_email(sender_id, subject, body, to_addresses, cc_addresses = None, 
	bcc_addresses = None, content_type = "html"):
    '''
    This method sends the email using the global connection object.
    
    :type sender_id: string
    :param sender_id: This is the email id of the sender_id
    
    :type subject: string
    :param subject: This is the subject of the email

    :type body: string
    :param body: This is the body of the email

    :type to_addresses: list
    :param to_addresses: This is the list of address TO sender_id

    :type cc_addresses: list
    :param cc_addresses: CC addresses

    :type bcc_addresses: list
    :param bcc_addresses: BCC addresses

    :type content_type: string
    :param content_type: This signifies the type of email to be sent. 
    It can be either text / html. Default is html
    '''
    global logger
    assert sender_id is not None, "The sender_id is null. Cannot send email"
    assert to_addresses is not None, "No To addresses"
    assert len(to_addresses) > 0, "No To addresses."
    sender_id = sender_id.strip()
    EMAIL_TEXT = "text"
    EMAIL_HTML = "html"
    content_type = content_type.strip()
    if (content_type == EMAIL_TEXT or content_type == EMAIL_HTML):
	connection = make_amazon_ses_connection() #Make the connection object
	assert connection is not None, "Connection cannot be made"
	try:
	    connection.send_email(sender_id, subject, body,
		    to_addresses, cc_addresses, bcc_addresses, content_type)
	except BotoServerError as server_error:
	    server_error = str(server_error)
	    if 'Address blacklisted' in server_error and 'MessageRejected' in server_error:
		logger.info('Address blacklisted. Intended Receiver Email Address: %s' %(to_addresses))
	    else:
		logger.exception("Error: %s. Receiver Email Address: %s" %(server_error, to_addresses))
    else:
        print "The content type is not recognised. It must be either 'text' or 'html'"

#Unit Test Cases
if __name__ == "__main__":
    print "test_send_valid_normal_email"
    sender_id = "sender_id@example.com"
    to_addresses = 'to_address@example.com'
    subject = "Normal Test Email"
    body = "This is a normal test email"
    send_email(sender_id, subject, body, to_addresses,
		None, None, "text")
