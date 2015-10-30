__author__ = 'mosquito'
import smtplib
from smtplib import SMTPConnectError, SMTPHeloError, SMTPServerDisconnected
from config import get_var
import datetime
import string


class MailUtils():
    """
    Provides commodity methods to send mails
    """
    logger = None
    _mail_values = None
    server = None

    def __init__(self, logger):
            self.logger = logger
            _mail_settings = ('MAIL_SERVER', 'MAIL_PORT', 'MAIL_USER', 'MAIL_PASSWORD')
            self._mail_values = dict(zip(_mail_settings, map(get_var, _mail_settings)))
            try:
                self.server = smtplib.SMTP(self._mail_values['MAIL_SERVER'], self._mail_values['MAIL_PORT'])
                self.server.ehlo()
                self.server.starttls()
                self.server.login(self._mail_values['MAIL_USER'], self._mail_values['MAIL_PASSWORD'])
            except (SMTPConnectError, SMTPHeloError) as e:
                self.logger.error('An error occurred trying to setup SMTP agent to send mails. More info ' + repr(e))

    def setup(self):
        """
        Tries to setup the MailUtils class by creating the SMTP object with the configuration parameters
        :rtype : bool
        :return: TRUE if setup was successful
        """
        try:
            self.server = smtplib.SMTP(self._mail_values['MAIL_SERVER'], self._mail_values['MAIL_PORT'])
            self.server.ehlo()
            self.server.starttls()
            self.server.login(self._mail_values['MAIL_USER'], self._mail_values['MAIL_PASSWORD'])
            return True
        except (SMTPConnectError, SMTPHeloError) as e:
            self.logger.error('An error occurred trying to setup SMTP agent to send mails. More info ' + repr(e))
            return False

    def send_mail(self, from_addr, to_addr, subject, text, include_ts):
        """
        Sends a text message to the specified address, from the specified address
        :from_addr: The from address to be used when sending the message
        :to_addr: The to address to be used when sending the message
        :subject: The subject for the message
        :include_ts: Specifies if a timestamp should be included along the text message
        :text: The text message
        """
        if not self.__check_connection():
            self.logger.info('Trying to reconnect to server')
            self.setup()
        else:
            try:
                message = ''
                if include_ts:
                    i = datetime.datetime.now()
                    message += '[%s] ' % i.isoformat()
                message += text
                body = string.join((
                    "From: %s" % from_addr,
                    "To: %s" % to_addr,
                    "Subject: %s" % subject,
                    "",
                    message
                ), "\r\n")
                self.server.sendmail(from_addr, [to_addr], body)
                self.logger.info('Sent mail correctly!')
            except SMTPServerDisconnected:
                self.logger.info('Could not send mail, looks like server disconnected us!')


    def __check_connection(self):
        """
        Checks if the current SMTP object is still connected to the server
        :connection: The reference to the SMTP object
        :rtype : bool
        :return: TRUE if connection to server still valid
        """
        try:
            status = self.server.noop()[0]
        except SMTPServerDisconnected:
            status = -1
            self.logger.info('Disconnected from server, need to reconnect')
        return True if status == 250 else False
