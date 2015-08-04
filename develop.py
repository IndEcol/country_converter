import country_converter as coco
import imp
imp.reload(coco)


cc = coco.CountryConverter()

#testnames = ['USA', 'VUT', 'TKL', 'AUT' ]
#names = ['USA', 'VUT', 'TKL', 'AUT' ]
#testnames = ['US', 'TW', 'WA']
#testnames = ['Vietnam' ]

#Btest = cc.data.name_standard
#Atest = cc.data.name_official
#outformat = ['name_standard', 'ISO3']


#Atest={
#'China',
#'Republic of China',
#'Peoples Republic of China',
#}
#Btest={
#'China',
#'Taiwan',
#}

#outformat = ['name_standard']
#out = cc.convert(names = testnames, src = 'ISO3', to = outformat, enforce_list = False, not_found = 'asd')
#out = coco.convert(names = testnames, src = 'ISO2', to = outformat, enforce_list = False, not_found = 'asd')
#A,B = coco.zip_lists(Atest, Btest)
#tt = coco.match(Atest, Btest)


#TODO: check with albani with same regex as afghan - should fill in both than

#testnames = ['zanzi', 'korea', 'us']
#testnames = ['austria']
#testnames = 'a'
#outformat = ['name_standard']
#out = cc.convert(names = testnames, src = 'regex', to = outformat, enforce_list = False, not_found = None)

dd = cc.data

