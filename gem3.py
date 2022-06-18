#   pdf  - path
import urllib.request
from bs4 import BeautifulSoup
import requests
pdf_path = "https://bidplus.gem.gov.in/bidlists"

#           mongo
from http import client
from pydoc import cli
import pymongo

client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
mydb = client['dataandreaddata']
all_information = mydb.alltabdata
pdf_read = mydb.pdfreaddata

host = 'https://bidplus.gem.gov.in'
url = 'https://bidplus.gem.gov.in/bidlists'

next_tab = ['/bidlists','/servicelists','/bidlists/bunch','/bidlists/service_bunch','/custom-item']     #  '/ralists',

import pdfplumber

def pdf_read_function(pdf_re):
    pdf = pdfplumber.open('zpdfall/Gem-Bidding-'+pdf_re + '.pdf')
    page = pdf.pages[0]
    text = page.extract_text()
    allpdfread = {}
    for row in text.split('\n'):
        if row.startswith('Bid End Date/Time '):
            end_date = row.split()[-2]
            end_time = row.split()[-1]
            allpdfread['end_date']=end_date
            allpdfread['end_time']=end_time

            # print('Bid End Date: ',end_date)
            # print('Bid End Time: ',end_time)
        if row.startswith('Bid Opening Date/Time '):
            opening_date = row.split()[-2]
            opening_time = row.split()[-1]
            allpdfread['opening_date']=opening_date
            allpdfread['opening_time']=opening_time
            # print('Bid Opening Date: ',opening_date)
            # print('Bid Opening Time: ',opening_time)
        if row.startswith('Bid Offer Validity'):
            offer_val = row.split()[-2]
            allpdfread['offer_val']=offer_val
            # print('Bid Offer Validity: ',offer_val)
        if row.startswith('Ministry/State Name'):
            ministry = row.split()[2:]
            min_state_name = ' '.join([str(elem) for elem in ministry])
            allpdfread['min_state_name']=min_state_name
            # print('ministry State Name: ',min_state_name)
        if row.startswith('Department Name'):
            department = row.split()[2:]
            department_name = ' '.join([str(elem) for elem in department])
            allpdfread['department_name']=department_name
            # print('Department Name: ',department_name)
        if row.startswith('Organisation Name'):
            org = row.split()[2:]
            organisation = ' '.join([str(elem) for elem in org])
            allpdfread['organisation']=organisation
            # print('Organisation Name : ',organisation)
        if row.startswith('Office Name'):
            office = row.split()[2:]
            office_name = ' '.join([str(elem) for elem in office])
            allpdfread['office_name']=office_name
            # print('Office Name: ',office_name)
        if row.startswith('Total Quantity'):
            Qty = row.split()[-1]
            allpdfread['Qty']=Qty
            # print('Quantity: ',Qty)
        if row.startswith('Item Category'):
            cat = row.split()[2:]
            item_category = ' '.join([str(elem) for elem in cat])
            allpdfread['item_category']=item_category
            # print('Item Category: ',item_category)

            mse18 = text.split('\n')
            mse = mse18[18]
            allpdfread['mse']=mse

            # print('MSE: ',mse[18])
            startup21 = text.split('\n')
            startup = startup21[21]
            allpdfread['startup']=startup
            # print('Startup: ',startup)
          

        # allpdfrea= {
        # 'end_date':end_date,
        # 'end_time': end_time,
        # 'opening_date': opening_date,
        # 'offer_val': offer_val,
        # 'min_state_name': min_state_name,
        # 'department_name': department_name,
        # 'organisation': organisation,
        # 'office_name': office_name,
        # 'Qty': Qty,
        # 'item_category': item_category,
        # 'mse': mse,
        # 'startup': startup,
        # }
        # print(allpdfread)
            pdf_read.insert_one(allpdfread) 

    pdf.close()
# pdf_read_function()



def download_file_function(urlpdf, filename):
    response = requests.get(pdf_path)
    pdfNo = urlpdf.split('/')[-1]
    print(pdfNo)
    
    response = urllib.request.urlopen(urlpdf)    
    file = open(filename+str(pdfNo) + ".pdf", 'wb')
    # print(file)
    file.write(response.read())
    file.close()
    pdf_read_function(pdfNo)
        
def repeat_function(url):
    # print(url)
    if url :
        response = requests.get(url)
        htmlcontent = response.content
        soup = BeautifulSoup(htmlcontent, 'html.parser')
        ul = soup.find_all('ul', attrs={'class': "pagination"})
        a = ul[0].find_all('li')[0].find_all('a')
        hostpdf = 'https://bidplus.gem.gov.in'
        for i in a:
            allPageNumber_Encoded = i['href']
            if allPageNumber_Encoded =='#':
                ind = a.index(i)
                if ind != len(a)-1:
                    ind+=1
                    next_page = host + a[ind]['href']
                    print(next_page)
                    if next_page!='#':
                        containers = soup.findAll('div', {'class':'border block'})
                        for container in containers:
                            bid_no = container.findAll('a', href=True)[0]
                            urlpdf = hostpdf + bid_no['href']
                            # pdfNo = urlpdf.split('/')[-1]
                            # print(urlpdf)

                            bid = container.findAll('p', {'class':'bid_no pull-left'})
                            bid_no = bid[0].text.split()[2]   
                            # print(bid_no)
                               #Item  and  Qty
                            items =  container.findAll('div', {'class':'col-block'})
                            item = ' '.join([str(elem) for elem in items[0].text.split()[1:-3]])
                            qty = items[0].text.split()[-1]
                            #   Department  &  Address
                            dep_add =  container.findAll('p', {'class':'add-height'})
                            depNameAdd = (dep_add[0].text.strip())
                            #   Tender start Date / end Time
                            tender=  container.findAll('div', {'class':'col-block'})
                            s_d = tender[2].text.split()[2:3]
                            start_date =' '.join([str(elem) for elem in s_d])
                            s_t = tender[2].text.split()[3:5]
                            start_time = ' '.join([str(elem) for elem in s_t])
                            e_d = tender[2].text.split()[-3:-2]
                            end_date =' '.join([str(elem) for elem in e_d])
                            e_t = tender[2].text.split()[-2:]
                            end_time = ' '.join([str(elem) for elem in e_t])


                            alldata = {
                                'bid_no':bid_no,
                                'item': item,
                                'qty': qty,
                                'depNameAdd': depNameAdd,
                                'start_date': start_date,
                                'start_time': start_time,
                                'end_date': end_date,
                                'end_time': end_time,
                                'urlpdf': urlpdf,
                            }
                            all_information.insert_one(alldata)  
                            
                            download_file_function(urlpdf, "zpdfall/Gem-Bidding-")
                            
                    return repeat_function(next_page)

# repeat_function(url)   
for miniurl in next_tab:
    tab = host + miniurl
    repeat_function(tab)


