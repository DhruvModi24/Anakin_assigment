import requests
import json
from pandas.io.json import json_normalize

http_proxy = "http:12.218.209.13:53281"
proxies = {
    "http": http_proxy
}
data_arr=[]
def list_crawler():
    # call json request to get all category with subcategory
    agent = requests.session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
    agent.get('https://www.bigbasket.com', headers=headers)
    home = 'https://www.bigbasket.com/auth/get_menu/?city_id=1'
    resp = agent.get(home,headers=headers).content
    cat_details_json = json.loads(resp)
    cat_list = cat_details_json['topcats'][:5]
    for cat in cat_list:
        super_category = cat['top_category']['name']
        sub_category_list = cat['sub_cats'][0]
        for subcat in sub_category_list:
            sub_cat1 = subcat['sub_category'][0]
            sub_cat2_list = subcat['cats']
            for sub_cat2 in sub_cat2_list:
                sub_cat2_name = sub_cat2['cat'][0]
                sub_cat2_slug = sub_cat2['cat'][1]
                final_product_list_url = 'https://www.bigbasket.com/custompage/sysgenpd/?type=pc&slug='+sub_cat2_slug
                resp2 = agent.get(final_product_list_url, headers=headers).content
                product_details_json = json.loads(resp2)
                parser(product_details_json,super_category,sub_cat1,sub_cat2_name)


def parser(product_details_json,super_category,sub_cat1,sub_cat2_name):
    products = product_details_json['tab_info'][0]['product_info']['products'][:10]
    for ii in products:
        try:
            sku_id = ii['sku']
        except:
            sku_id = ''

        try:
            image_url = ii['p_img_url']
        except:
            image_url = ''

        try:
            brand = ii['p_brand']
        except:
            brand = ''

        try:
            sku_name = ii['p_desc']
        except:
            sku_name = ''

        try:
            sku_size = ii['w']
        except:
            sku_size = ''

        try:
            mrp = ii['mrp']
        except:
            mrp = ''

        try:
            sp = ii['sp']
        except:
            sp = ''

        try:
            link = 'https://www.bigbasket.com'+ii['absolute_url']
        except:
            link = ''

        record = dict()
        record['City'] = 'Banglore'
        record['Super_Category'] = super_category
        record['Category'] = sub_cat1
        record['Sub_Category'] = sub_cat2_name
        record['SKU_ID'] = sku_id
        record['Image'] = image_url
        record['Brand'] = brand
        record['SKU Name'] = sku_name
        record['SKU Size'] = sku_size
        record['MRP'] = mrp
        record['SP'] = sp
        record['Link'] = link
        if mrp!='':
            record['Active'] = 'Yes'
            record['Out of Stock'] = 'No'
        else:
            record['Active'] = 'No'
            record['Out of Stock'] = 'Yes'
        print(record)
        data_arr.append(record)
def main():
    list_crawler()
    dts = json_normalize(data_arr)
    dts.to_csv('Big basket sample data.csv')
    print('Report Created ... [Thank You]')

main()