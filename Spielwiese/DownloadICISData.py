'''
Created on 19.12.2016

@author: prudnik
'''
import json
import requests


#url = "https://analytics.icis.com/wp-content/plugins/tschachsolutions/inc/highChartsInterface/api/hcapi.php?csv=1&dlkey=fa45e3dd-8185-42fc-a969-1b0653b66ad2&query_id=ICIS_power_spotprice_forecast_dispatch_full_download_withModelRunTime_v2&div=hcdl5852726e01352159310899&form_hcdl5852726e01352159310899%5B%5D=ts_D1&dformat=csv"

host        = 'analytics.icis.com'
baseURL     = '/wp-content/plugins/tschachsolutions/inc/highChartsInterface/api/hcapi.php'
get_parameter = "?csv=1&dlkey=fa45e3dd-8185-42fc-a969-1b0653b66ad2&query_id=ICIS_power_spotprice_forecast_dispatch_full_download_withModelRunTime_v2&div=hcdl5852726e01352159310899&form_hcdl5852726e01352159310899%5B%5D=ts_D1&dformat=csv"


def runProgram():
    try:
        # -------------------------------------------------------------------
        # request data from site
        # -------------------------------------------------------------------
        url= "https://{0}{1}{2}".format(host,baseURL,get_parameter)
        response = requests.get(url)
        if response.content != None:
            records = response.content.split("\n")
            for record in records:
                print record 
        #print(response.content)
    except Exception as e:
        print(str(e))    



if __name__ == "__main__":
    runProgram()
