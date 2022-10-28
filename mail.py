class Mail:
    def __init__(self,mailFrom,mailSubject,mailBody,message):
        self.mailFrom = mailFrom
        self.mailSubject = mailSubject
        self.mailBody = mailBody
        self.message = message

    def __str__(self):
        return "From: "+self.mailFrom+"\n"+"Subject: "+self.mailSubject+"\n"+"Body: "+self.mailBody 


