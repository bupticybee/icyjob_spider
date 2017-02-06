import re

def get_mail(fobj):  
    regex = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b", re.IGNORECASE)  
    mails = re.findall(regex, fobj)  
    return mails  
  
