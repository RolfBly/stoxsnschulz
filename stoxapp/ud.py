from __future__ import division  
import requests  
import bs4  
import re  
import pickle
import os  
from operator import itemgetter, lt, le, gt, ge  

import hilo  

# helpers  
def pct2float(pct):  
    return float(pct.replace(',', '.').strip('%'))/100  

def txt2float(numtext):  
    return float(numtext.replace(',', '.'))  
    
def make_path(filename, dir='pickles'):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return '.\\{}\\{}.pkl'.format(dir, filename)
    
def save_thing(thing, path):
    with open(path, 'wb') as f:
        pickle.dump(thing, f, pickle.HIGHEST_PROTOCOL)

def make_table(Top, head, show=True):  
    '''Takes Top and header data, 
       creates neat header & table, 
       outputs it to console unless told otherwise, 
       returns header data + list of lists row data. '''
       
    N = len(Top)  
    if not 'Alles' in head:  
        head = 'Top {} {} '.format(N, head)  
   
    hdat = head, 'change', 'price', 'yrHi', 'yrLo', 'pct_BW', 'BW', 'index'  
   
    if show: 
        widthl = [28, 7, 7, 4] # column widths in hline and underline  
        widthd = {'w{}'.format(index): value for index, value in enumerate(widthl, 1)}  
        under = 8 * '='  
        hline = '  {0:{ul}<{w1}}  {1:{ul}>{w2}}  {2:{ul}>{w3}}  {3:{ul}>{w3}}  {4:{ul}>{w3}}  {5:{ul}>{w3}}  {6:{ul}>{w3}}  {7:{ul}<{w4}}'  
        print '\n'  
        print hline.format(*hdat, ul='', **widthd)  
        print hline.format(*under, ul='=', **widthd)  
        
        line = '  {:.<28}  {:>7}  {:>7.2f}  {:>7.2f}  {:>7.2f}  {:>6.1f}%  {:>7.2f}  {:<4}'  

    dlines = []
    for item in Top:  
        items = [item['stock'],  
                 item['pct_change_txt'],  
                 item['last_price'],  
                 item['yr_hi_val'],  
                 item['yr_lo_val'],  
                 item['pct_BW'],  
                 item['BW'],  
                 item['stock_index']]  

        dlines.append(items)
        if show: 
            print line.format(*items)
        
    return hdat, dlines
    
def get_topX_index(lst, threshold, key='pct_change_num'):  
    for i, dic in enumerate(lst):  
        if abs(dic[key]) >= threshold:  
            pass  
        else:  
            return i  
    return i + 1  

def filter_topX(lst, threshold, key='pct_BW', op='<='):  
    ops = {'>'  : gt,  
           '>=' : ge,  
           '<'  : lt,  
           '<=' : le}  
    func = ops[op]  
    outlist = []  
    for i, dic in enumerate(lst):  
        if func(abs(dic[key]), threshold):  
           outlist.append(dic)  

    return outlist  
   
# workers  
def getRates(beursindex):  
    '''extract from beursindex: stock name, last price, pct change  
       return stock name, last price as float,  
       pct change as text and float, index name, and link to stock page.  
    '''  

    page = requests.get('http://www.beleggen.nl/' + beursindex)  
    page.raise_for_status()  
    soup = bs4.BeautifulSoup(page.text, 'lxml')  

    table = soup.find('table', id=re.compile('koersOverzicht\d{1,2}'))  
    rows = table.find_all('tr')  
    
    stoxlist = []  
    for row in rows[2:]:        # skip header and index  
        symbol = row.find('a').contents[0]  
        link = row.find('a')['href']  
        tabledata = row.find_all('td')  
        rowdata = []  
        for cell in tabledata:  
            try:  
                rowdata.append(cell.contents[0])  
            except IndexError:  
                # tolerate empty rows for new stocks  
                pass  
       
        stock = {'stock': symbol,  
                 'last_price': txt2float(rowdata[1]),  
                 'pct_change_txt': rowdata[3],  
                 'pct_change_num': pct2float(rowdata[3]),  
                 'stock_index': beursindex,  
                 'link' : link}  

        stoxlist.append(stock)  

    return stoxlist  

def add_yrhilo(Top):  
    for stock in Top:  
        # print stock['link'] # debug: uncomment  
        details = hilo.stockpage(stock['link'])  
        try:  
            x = details[0] # force exception if there is no detail  
                           # can't do 'if details is not None' workaround,  
                           # cos details is type bs4.element.ResultSet  
            
            highlow = hilo.hi_lo(details)  
            for details in highlow:  
                hiorlo = 'hi' if 'Hoo' in details[0] else 'lo'  
                stock['yr_{}_val'.format(hiorlo)] = details[1]  
                stock['yr_{}_date'.format(hiorlo)] = details[2]  
                 
            stock['BW'] = stock['yr_hi_val'] - stock['yr_lo_val']  
            
            if stock['BW'] > 0:  
                stock['pct_BW'] = 100 * (stock['last_price'] - stock['yr_lo_val']) / stock['BW']  
            else:  
                stock['pct_BW'] = 0.0  

        except IndexError:  
            stock['yr_hi_val'] = stock['yr_lo_val'] = stock['BW'] = stock['pct_BW'] = -1.0  
            stock['yr_hi_date'] = None  
        
def main():  
    all_rates = getRates('aex') + getRates('amx') + getRates('ascx')  
    add_yrhilo(all_rates)  
    all_sorted = sorted(all_rates, key=itemgetter('pct_change_num'), reverse=True)  
    
    # Top X climbers  
    top10_ups = all_sorted[:10]  
    N = get_topX_index(top10_ups, threshold=0.01)  
    topN_ups = top10_ups[:N]  
    ups = make_table(topN_ups, 'stijgers')  # add show=False to hide output to console 
    save_thing(ups, make_path('ups'))  

    # Top X fallers  
    top10_downs = list(reversed(all_sorted[-10:]))  
    M = get_topX_index(top10_downs, threshold=0.01)  
    topM_downs = top10_downs[:M]
    topX_downs = filter_topX(topM_downs, threshold=30)  
    downs = make_table(topX_downs, 'dalers, pct_BW < 30%')  
    save_thing(downs, make_path('downs'))  

    # Top X bandwidth, pct_BW < 40%  
    all_sorted_by_BW = sorted(all_rates, key=itemgetter('BW'), reverse=True)  
    top10_BW = all_sorted_by_BW[:10]  
    topP_BW = filter_topX(top10_BW, threshold=40)  
    BW = make_table(topP_BW, 'BW, pct_BW < 40%')  
    save_thing(BW, make_path('BW'))  

    # Top X low scale, BW > 3 euro  
    all_sorted_by_scale = sorted(all_rates, key=itemgetter('pct_BW'))  
    top10_scale_low = all_sorted_by_scale[:10]  
    topX_scale_low = filter_topX(top10_scale_low, threshold=3, key='BW', op='>')  
    low_BW = make_table(topX_scale_low, 'onderin BW, BW > 3')  
    save_thing(low_BW, make_path('low_BW'))  

    # Top X penny stock, pct_BW < 25%  
    all_sorted_by_price = sorted(all_rates, key=itemgetter('last_price'))  
    top10_cheap = all_sorted_by_price[:10]  
    topX_cheap = filter_topX(top10_cheap, threshold=25)  
    cheaps = make_table(topX_cheap, 'El Chipo, pct_BW < 25%')  
    save_thing(cheaps, make_path('cheap'))  

    # top10_expensive = list(reversed(all_sorted_by_price[-10:]))  
    # make_table(top10_expensive, 'DUUR!')  

if __name__ == "__main__":  
    main()  
