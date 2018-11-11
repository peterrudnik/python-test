'''
Created on 02.04.2017

@author: prudnik
@note: 
      
      The SDMX sponsoring institutions are 
          the Bank for International Settlements (BIS), 
          the European Central Bank (ECB), 
          Eurostat (the statistical office of the European Union), 
          the International Monetary Fund (IMF), 
          the Organisation for Economic Co-operation and Development (OECD), 
          the United Nations Statistics Division (UNSD), 
          and the World Bank.
      
      ['', 'INSEE', 'ECB', 'SGR', 'OECD', 'ESTAT']
      INSEE: Institut national de la statistique et des etudes economiques
      ECB    European Central Bank
      OECD   Organisation for Economic Co-operation and Development
      
'''
from pandasdmx import Request   


def test1():
    ecb = Request('ECB')
    cat_resp = ecb.get(resource_type = 'categoryscheme')
    cat_msg = cat_resp.msg
    print dir(cat_msg)
    print str(cat_msg.header)
    print str(cat_msg.categoryscheme)
    print str(cat_msg.dataflow)
    for key, value in cat_msg.dataflow.iteritems():
        print "{k}:{v}".format(k=key,v=value)
        
    # resource must be one of ['dataflow', 'datastructure', 'data', 'categoryscheme', 'codelist', 'conceptscheme']    
    flows = ecb.get(resource_type = 'dataflow') 
    print str(flows)  
    refs = dict(references = 'all')
    #dsd_resp = ecb.get(resource_type = 'datastructure', resource_id = 'EXR_PUB', params = refs)
    dsd_id = cat_msg.dataflows.EXR_PUB.structure.id
    dsd_id = cat_msg.dataflows.EXR.structure.id
    dsd_id = 'ECB_EXR1'
    dsd_resp = ecb.get(resource_type = 'datastructure', resource_id = dsd_id, params = refs)
    #print str(dsd_resp)
    print dir(dsd_resp)
    dsd = dsd_resp.msg.datastructures[dsd_id]
    print str(dsd)
    
    data_resp = ecb.get(resource_type = 'data', resource_id = 'EXR', key={'CURRENCY': 'USD+JPY'}, params = {'startPeriod': '2014'})
    print dir(data_resp)
    data = data_resp.msg.data
    #print dir(data.series)
    series_l = list(data.series)
    print series_l
    #categorisations = cat_msg.categorisations
    #print str(categorisations)
    #f = 1.0
    #print str(type(f))
    

if __name__ == "__main__":
    test1()
