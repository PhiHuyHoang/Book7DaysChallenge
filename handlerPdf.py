from PyPDF2 import PdfFileWriter, PdfFileReader
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class cutterPDF():
    def __init__(self, file_name):
        self.inputpdf = PdfFileReader(open(file_name, "rb"))
        self.numPages = self.inputpdf.numPages
        self.range_of_pages = list(self.split(range(self.numPages), 7))
        self.new_file_name = file_name.replace(".pdf", "")
        self.weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    def split(self,a, n):
        k, m = divmod(len(a), n)
        return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


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
            print("Page %s done!" % i)