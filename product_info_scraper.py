import json

############# 02 size scrapers ###########

def size_url_scraper(page_source):

    products_column = page_source.find("ul", id="productListMain")
    product_individual = products_column.find_all("a", class_="itemImage")
    product_page_urls = []
    for product in product_individual:
        product_page_urls.append(product.get('href'))

    return product_page_urls

def size_product_info_scraper(page_source):


    name = page_source.find('h1')
    price = page_source.find('span',class_='pri')

    ###################### Code for Stock Availability   #######################

    v = page_source.find_all('script',type='text/javascript')
    s = v[2]
    o = s.text.split('[')
    l = o[1]
    l = l.replace('\n','')
    l = l.replace('\t','')
    split = l.split('name')
    sp = split[1:len(split)]
    stocks = []
    for i in sp:
        stocks.append(i[1:10].split('"')[1])

    product_info = {
    'name':name.text,
    'price':price.text,
    'stock':stocks,
    }

    ########################################################

    print(name.text,' ',price.text,'  -- ',stocks)#,len(stock_info))

    return product_info


############# 03_endclothing Scrapers ############

def endclothing_url_scraper(page_source):
    products = page_source.find_all('a',class_='sc-1koxpgo-0 bTJixI sc-5sgtnq-3 dMAnEc')
    product_page_urls = []
    for prod in products:
        product_page_urls.append(prod.get('href'))

    return product_page_urls


def endclothing_product_info_scraper(page_source):

    try:

        print('In endclothing_product_info_scraper() ')

        product_title = page_source.find('h1')
        product_price = page_source.find('span',id='pdp__details__final-price')

        stock_info = page_source.find_all('div',class_='sc-1g50eob-3 eOPTdx')

        st = []

        j = page_source.find('script',id='__NEXT_DATA__')
        a = json.loads(j.text)

        for i in a['props']['initialProps']['pageProps']['product']['sizes']['values']:

            st.append(i['label'])

        product_info = {

        'name':product_title.text,
        'price':product_price.text,
        'stock':st,
        }
        #for i in stock_info:
        #    st.append(i.text)

        #stock_column = page_source.find('button',class_='sc-8jr7xg-1 fujUki sc-1ybq7do-0 bfEAfO')
        #stock_info=stock_column.find('div',class_='sc-1j0b8up-0 Xpmnl')

        print(product_title.text,' ',product_price.text,'  ',st)
    except Exception as e:
        print('Error in endclothing_product_info_scraper -->',e)

    return product_info

############## footasylum Scraper ################

def footasylum_url_scraper(page_source):

    product_table = page_source.find('div',id = 'productDataOnPage')
    products = product_table.find_all('div',class_='gproduct')
    product_page_urls = []

    for prod in products:
        product_page_urls.append(prod.find('a').get('href'))

    return product_page_urls



########### prodirect Scrapers ###############

def prodirect_info_scraper(page_source):

    product  = page_source.find('div',id = 'define-profile')
    product_name = product.find('h1').text
    product_price = product.find('p',class_='price').text

    #Extracting Stock Availability
    op = page_source.find('select',id = 'size')
    o = op.find_all('option')
    l = []
    for i in o:
        l.append(i.text)
    l = l[1:len(l)]

    product_info = {

    'name':product_name.strip(),
    'price':product_price.strip(),
    'stock':l,
    }

    print(product_name,' ',product_price,' ',l)

    return product_info

################  JDSPORT SCRAPERS ################

def jdsport_product_info_scraper(page_source):

    product_title = page_source.find('span',class_='active').text.strip()
    #product_price = page_source.find('span',class_='now').find('span').text

    buttons = page_source.find('div',class_='options')

    stocks = buttons.find_all('button')

    stock_available = []
    for i in stocks:
        stock_available.append(i.text.strip())

    product_info = {

    'name':product_title,
    'stock':stock_available,

    }

    print(product_title,' ',' ',stock_available)

    return product_info

####################### sportsdirect Scrapers ###############

def sportsdirect_product_info_scraper(page_source):

    div = page_source.find('div',class_='logontitle')
    product_title = div.find('h1').find('span',id = 'lblProductName')
    product_price = div.find('div',class_='pdpPrice').find('span',class_ = 'productHasRef')
#stock_info = page_source.find_all('a',class_='addToBag')

    ul = page_source.find('ul',id='dnn_ctr103511_ViewTemplate_ctl00_ctl13_ulSizes')

    li = ul.find_all('li',class_='tooltip sizeButtonli')
    available_stocks = []

    for i in li:
        available_stocks.append(i.find('span').text)

    print(product_title.text,' ',product_price.text,'  ',available_stocks)

#################### mandmidirect Scraper #######################

def mandmdirect_product_info_scraper(page_source):

    product_title = page_source.find('div',id = 'description').find('h1',class_='st-product-title')

    product_price = page_source.find('div',class_='product-detail-info').find('div',id='item-price-desktop').find('div',class_='pd-price').find('h2')

    #stock = page_source.find_all('div',class_ = 'buySizeChartButton')

    stock_available = []

    ul = page_source.find('ul',class_='sizeSelect dropdown-menu')
    li = ul.find_all('li')

    for i in li:
        if i.find('span',class_='stockStatusMessage'):
            stock_available.append(i.find('a').find('span').text)


    product_info = {

    'name':product_title.text.strip(),
    'price':product_price.text.strip(),
    'stock':stock_available,
    }


    print(product_title.text,' ',product_price.text,'  ',stock_available)

    return product_info





#############  schuh Scrapers ########################

def schuh_product_info_scraper(page_source):

    product_title = page_source.find('h1')

    product_price = page_source.find('span',id='price')

    label = page_source.find('label',class_='select')
    op = label.find_all('option',class_='sizeAvailable')

    stock_available = []

    for i in op:
        stock_available.append(i.text)

    product_info = {

    'name':product_title.text.strip(),
    'price':product_price.text.strip(),
    'stock':stock_available,
    }


    print(product_title.text,' ',product_price.text,'  ',stock_available)

    return product_info


######################## amazon Scrapers #####################

def amazon_product_info_scraper(page_source):

    product_title = page_source.find('h1').text.strip()

    op = page_source.find_all('option',class_='dropdownAvailable')

    available_stocks = []

    for i in op:
        available_stocks.append(i.text.strip())

    product_info = {

    'name':product_title,
    'stock':available_stocks,
    }

    print(product_title,' ',available_stocks)

    return product_info


#################### Office Scrapers #################

def office_product_info_scraper(page_source):

    product_title = page_source.find('h3',class_='product__name').text

    #product_price = page_source.find('div',class_='product__saleprice product__saleprice--now js-price').text.strip()

    li=page_source.find('ul',class_='product__sizes-select js-size-select-list').find_all('li')
    available_stocks = []

    for i in li:
        available_stocks.append(i.get('data-name'))

    product_info = {

    'name':product_title,
    'stock':available_stocks,
    }

    print(product_title,'  ','  ',available_stocks)

    return product_info


######################   Jogging Scrapers ##########################

def jogging_product_info_scraper(page_source):

    product_title = page_source.find('span',class_='product-name-sub')

    if product_title is not None:
        product_title = product_title.text

    else:

        product_title = page_source.find('span',class_='product-name-sub').text
    price  =  page_source.find('span',class_='value').text.strip()

    div = page_source.find('div',class_="en-locale")
    available_stocks = []
    if div is not None:
        a = div.find_all('a')
        for i in a:
            if i.text.strip() == i.get('title').strip():
                available_stocks.append(i.text.strip())
            else:
                pass
    else:
        other_div = page.find('div',class_='size-tiles')
        other_a = other_div.find_all('a')

        for i in other_a:

            if i.text.strip() == i.get('title').strip():
                available_stocks.append(i.text.strip())
            else:
                pass

    product_info = {

    'name':product_title,
    'price':price,
    'stock':available_stocks,
    }



    print(product_title,' ',price,'  ',available_stocks)

    return product_info



############### Adidas Product Info Scraper ################
def adidas_product_info_scraper(page):

    info_page = page['info']
    stock_page = page['stock']

    ########
    jsn = json.loads(info_page.text)
    product_name = jsn['name']
    product_price = jsn['pricing_information']['currentPrice']
    ########

    jsn2 = json.loads(stock_page.text)

    stock_available = []
    for i in jsn2['variation_list']:
        if 'NOT' in i['availability_status']:
            pass
            #print('Not available')
        else:
            stock_available.append(i['size'])

    product_info = {

    'name':product_name,
    'price':product_price,
    'stock':stock_available,
    }

    print(product_name,product_price,stock_available)

    return product_info


########### offspring ##############
def offspring_product_info_scraper(page):
    ## Available Stocks
    ul = page.find('ul',class_='productDetail_purchaseOptions')
    l = ul.find('li')
    o = l.find_all('option')
    st = []

    for i in o:
        st.append(i.text)
    st = st[1:]

    #Product Title

    title = page.find('div',class_='product_info-container').find('p',class_='product-info__product').text

    #Product Price
    price = page.find('div',id = 'now_price').text.strip()

    product_info = {
        'name':title,
        'price':price,
        'stock':st,
    }
    return product_info
