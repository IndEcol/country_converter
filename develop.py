import country_converter as coco
import imp
imp.reload(coco)


cc = coco.CountryConverter()

#testnames = ['USA', 'VUT', 'TKL', 'AUT' ]
#names = ['USA', 'VUT', 'TKL', 'AUT' ]
testnames = ['US', 'TW', 'WA']
testnames = ['USA', 'VUT', 'TKL', 'AUT', 'Vietnam' ]
outformat = ['name_standard', 'ISO3']
outformat = ['name_standard']
#out = cc.convert(names = testnames, src = 'ISO3', to = outformat, enforce_list = False, not_found = 'asd')

dd = cc.data
dd['test'] = cc.convert(dd.name_official, src='regex')


#testnames = ['zanzi', 'korea', 'us']
#testnames = ['austria']
#testnames = 'a'
#outformat = ['name_standard']
#out = cc.convert(names = testnames, src = 'regex', to = outformat, enforce_list = False, not_found = None)
