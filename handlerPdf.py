from PyPDF2 import PdfFileWriter, PdfFileReader
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class cutterPDF():
    def __init__(self, file_name, email):
        self.inputpdf = PdfFileReader(open(file_name, "rb"))
        self.numPages = self.inputpdf.numPages
        self.range_of_pages = list(self.split(range(self.numPages), 7))
        self.new_file_name = file_name.replace(".pdf", "")
        self.weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.email = email

    def split(self,a, n):
        k, m = divmod(len(a), n)
        return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

    def send_email(self, book_name, day):

        fromaddr = os.getenv('username')
        password = os.getenv('password')
        toaddr = self.email
        msg = MIMEMultipart()
        msg['From'] = "Rice - Book Challenge <" + fromaddr + ">"
        msg['To'] = toaddr
        msg['Subject'] = "This is your book: " + book_name.replace("download/","").replace(".pdf","") + " for " + day

        signature = '''<p class=MsoNormal style='text-autospace:none'><b><span lang=EN-US style='font-size:10.0pt;color:#548DD4;mso-fareast-language:HU'>Phi Huy Hoang</span></b><b><span lang=EN-US style='font-size:10.0pt;color:navy;mso-fareast-language:HU'><br></span></b><span lang=EN-US style='font-size:8.0pt;color:#1F497D;mso-fareast-language:HU'>Intern<o:p></o:p></span></p><p class=MsoNormal style='text-autospace:none'><span lang=EN-US style='font-size:8.0pt;color:#1F497D;mso-fareast-language:HU'>Machine Learning |&nbsp;SAP Leonardo<o:p></o:p></span></p></div></body></html>'''
        description = """<p class=MsoNormal><b>This is your book: """ + book_name.replace("download/","").replace(".pdf","") + """ for """ + day + """<o:p></o:p></b></p>"""
        body = "Hi friend," + description + signature
        msg.attach(MIMEText(body, 'html'))
        attachment = open(book_name, "rb")

        p = MIMEBase('application', 'octet-stream')

        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % book_name)
        msg.attach(p)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(fromaddr, password)
        text = msg
        s.sendmail(fromaddr, toaddr, text.as_string())
        s.quit()

    def makePdf(self,name,day,length):
        output = PdfFileWriter()
        for i in length:
            output.addPage(self.inputpdf.getPage(i))
        output_file = name+"-%s.pdf" % day
        with open(output_file, "wb") as outputStream:
            output.write(outputStream)
        print(output_file)

    def action(self):
        for i in range(self.numPages):
            if i in self.range_of_pages[0]:
                self.makePdf(self.new_file_name, self.weekday[0], self.range_of_pages[0])
            elif i in self.range_of_pages[1]:
                self.makePdf(self.new_file_name, self.weekday[1], self.range_of_pages[1])
            elif i in self.range_of_pages[2]:
                self.makePdf(self.new_file_name, self.weekday[2], self.range_of_pages[2])
            elif i in self.range_of_pages[3]:
                self.makePdf(self.new_file_name, self.weekday[3], self.range_of_pages[3])
            elif i in self.range_of_pages[4]:
                self.makePdf(self.new_file_name, self.weekday[4], self.range_of_pages[4])
            elif i in self.range_of_pages[5]:
                self.makePdf(self.new_file_name, self.weekday[5], self.range_of_pages[5])
            elif i in self.range_of_pages[6]:
                self.makePdf(self.new_file_name, self.weekday[6], self.range_of_pages[6])

        for i in range(7):
            self.send_email(self.new_file_name+"-%s.pdf" % self.weekday[i], self.weekday[i])
            print("Page %s done!" % i)