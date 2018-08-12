import psycopg2
import sys
import pprint
import re
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def gen_query(state_arr,district_arr,tier_arr,column_arr,operation_arr,num_arr):
	
	#preapare lists
	column = "),SUM(".join(column_arr)
	columns = "','".join(column_arr)
	state = ",".join(state_arr)
	district = ",".join(district_arr)
	
	#total if not tier
	if not tier_arr:
		tier = "'total','rural','urban'"
	else:
		tier = ",".join(tier_arr)		
	
	if operation_arr:
		if operation_arr[0] in ["greater than", "more than", "above"]:
			if len(column_arr) == 2:
				query = "SELECT \"state\",\"district\",SUM("+column+") FROM jano_india WHERE tier IN ("+tier+") AND "+column_arr[0]+" > "+column_arr[1]+" GROUP BY \"state\",\"district\" ORDER BY \"state\",\"district\""
			elif num_arr:
				query = "SELECT \"state\",\"district\",SUM("+column+") FROM jano_india WHERE tier IN ("+tier+") AND "+column_arr[0]+" > "+num_arr[0]+" GROUP BY \"state\",\"district\" ORDER BY \"state\",\"district\""
		elif operation_arr[0] in ["less than", "below"]:
			if len(column_arr) == 2:
				query = "SELECT \"state\",\"district\",SUM("+column+") FROM jano_india WHERE tier IN ("+tier+") AND "+column_arr[0]+" < "+column_arr[1]+" GROUP BY \"state\",\"district\" ORDER BY \"state\",\"district\""
			elif num_arr:
				query = "SELECT \"state\",\"district\",SUM("+column+") FROM jano_india WHERE tier IN ("+tier+") AND "+column_arr[0]+" < "+num_arr[0]+" GROUP BY \"state\",\"district\" ORDER BY \"state\",\"district\""
	else:	
		if not state_arr and not district_arr:	
			query = "SELECT \"state\",\"district\",SUM("+column+") FROM jano_india WHERE tier in ("+tier+") GROUP BY \"state\",\"district\" ORDER BY \"state\",\"district\""
		elif not state_arr:
			query = "SELECT \"state\",\"district\",SUM("+column+") FROM jano_india WHERE district in ("+district+") and tier in ("+tier+") GROUP BY \"state\",\"district\" ORDER BY \"state\",\"district\""
		elif not district_arr:
			query = "SELECT \"state\",\"district\",SUM("+column+") FROM jano_india WHERE state in ("+state+") and tier in ("+tier+") GROUP BY \"state\",\"district\" ORDER BY \"state\",\"district\""
		else:
			query = "SELECT \"state\",\"district\",SUM("+column+") FROM jano_india WHERE state in ("+state+") and district in ("+district+") and tier in ("+tier+") GROUP BY \"state\",\"district\" ORDER BY \"state\",\"district\""
	
	columns = str('("state","district",'+columns.replace("','",",")+')')
	print(query,"columns:",columns)
	return columns,query
	
def query(text):
	text = text.lower().replace("marginal workers","MW").replace("households","houses")
	states = ['andaman and nicobar islands', 'andhra pradesh', 'arunachal pradesh', 'assam', 'bihar', 'chandigarh', 'chhattisgarh', 'dadra and nagar haveli', 'daman and diu', 'delhi', 'goa', 'gujrat', 'harayana', 'himachal pradesh', 'jammu and kashmir', 'jharkhand', 'karnataka', 'kerala', 'lakshadweep', 'madhya pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamilnadu','telangana', 'tripura', 'uttar pradesh', 'uttarakhand', 'west bengal']
	districts = ["adilabad","agar malwa","agra","ahmadabad","ahmadgar","aizawl","ajmer","akola","alappuzha","aligarh","alipurduar","alirajpur","allahabad","almora","alwar","ambala","ambedkar nagar","amethi","amravati","amreli","amritsar","anand","anantapur","anantnag","anjaw","anugul","anuppur","araria","aravalli","ariyalur","arwal","ashoknagar","auraiya","aurangabad","azamgarh","badgam","bagalkot","bageshwar","baghpat","bahraich","baksa","balaghat","balangir","baleshwar","ballia","balod","baloda bazar","balrampur","banas kantha","banda","bandipore","bangalore","bangalore rural","banka","bankura","banswara","barabanki","baramula","baran","barddhaman","bareilly","bargarh","barmer","barnala","barpeta","barwani","bastar","basti","bathinda","baudh","begusarai","belgaum","bellary","bemetara","betul","bhadrak","bhagalpur","bhandara","bharatpur","bharuch","bhavnagar","bhilwara","bhind","bhiwani","bhojpur","bhopal","bid","bidar","bijapur","bijnor","bikaner","bilaspur","birbhum","bishnupur","bokaro","bongaigaon","botad","budaun","bulandshahar","buldana","bundi","burhanpur","buxar","cachar","central","chamarajanagar","chamba","chamoli","champawat","champhai","chandauli","chandel","chandigarh","chandrapur","changlang","chatra","chennai","chhatarpur","chhindwara","chhota udepur","chikkaballapura","chikmagalur","chirang","chitradurga","chitrakoot","chittaurgarh","chittoor","churu","churuchandpur","coimbatore","cuddalore","cuttack","dadra & nagar haveli","dakshin bastar dantewada","dakshin dinajpur","dakshina kannada","daman","damoh","darbhanga","darjiling","darrang","datia","dausa","davanagere","debagarh","dehradun","deoghar","deoria","devbhoomi dwarka","dewas","dhalai","dhamtari","dhanbad","dhar","dharmapuri","dharwad","dhaulpur","dhemaji","dhenkanal","dhubri","dhule","dibang valley","dibrugarh","dima hasao","dimapur","dindigul","dindori","diu","doda","dohad","dumka","dungarpur","durg","east","east garo hills","east godavari","east jaintia hills","east kameng","east khasi hills","east nimar","east siang","ernakulam","erode","etah","etawah","faizabad","faridabad","faridkot","farrukhabad","fatehabad","fatehgarh","fatehpur","fazilka","firozabad","firozpur","gadag","gadchiroli","gajapati","ganderbal","gandhinagar","ganganagar","ganjam","garhwa","garhwal","gariyaband","gautam buddha nagar","gaya","ghaziabad","ghazipur","gir somnath","giridih","goalpara","godda","golaghat","gomati","gonda","gondiya","gopalganj","gorakhpur","gulbarga","gumla","guna","guntur","gurdaspur","gurgaon","gwalior","hailakandi","hamirpur","hanumangarh","haora","hapur","harda","hardoi","hardwar","hassan","hathras","haveri","hazaribagh","hingoli","hisar","hoshangabad","hoshiarpur","hugli","hyderabad","idukki","imphal east","imphal west","indore","jabalpur","jagatsinghapur","jaintia hills","jaipur","jaisalmer","jajapur","jalandhar","jalaun","jalgaon","jalna","jalor","jalpaiguri","jammu","jamnagar","jamtara","jamui","janjgir - champa","jashpur","jaunpur","jehanabad","jhabua","jhajjar","jhalawar","jhansi","jharsuguda","jhunjhunun","jind","jodhpur","jorhat","junagadh","jyotiba phule nagar","kabeerdham","kachchh","kadapa","kaimur","kaithal","kalahandi","kamrup","kamrup metropolitan","kancheepuram","kandhamal","kangra","kannauj","kanniyakumari","kannur","kanpur dehat","kanpur nagar","kanshiram","kapurthala","karaikal","karauli","karbi anglong","kargil","karimganj","karimnagar","karnal","karur","kasaragod","kathua","katihar","katni","kaushambi","kendrapara","kendujhar","khagaria","khammam","kheda","kheri","khordha","khowai","khunti","kinnaur","kiphire","kishanganj","kishtwar","koch bihar","kodagu","koderma","kohima","kokrajhar","kolar","kolasib","kolhapur","kolkata","kollam","kondagaon","koppal","koraput","korba","koriya","kota","kottayam","kozhikode","krishna","krishnagiri","kulgam","kullu","kupwara","kurnool","kurukshetra","kurung kumey","kushinagar","lahul & spiti","lakhimpur","lakhisarai","lakshadweep","lalitpur","latehar","latur","lawngtlai","leh","lohardaga","lohit","longding","longleng","lower dibang valley","lower subansiri","lucknow","ludhiana","lunglei","madhepura","madhubani","madurai","mahasamund","mahbubnagar","mahe","mahendragarh","mahesana","mahisagar","mahoba","mahrajganj","mainpuri","malappuram","maldah","malkangiri","mamit","mandi","mandla","mandsaur","mandya","mansa","marigaon","mathura","mau","mayurbhanj","medak","meerut","mewat","mirzapur","moga","mokokchung","mon","moradabad","morbi","morena","muktsar","mumbai","mungeli","munger","murshidabad","muzaffarnagar","muzaffarpur","mysore","nabarangapur","nadia","nagaon","nagapattinam","nagaur","nagpur","nainital","nalanda","nalbari","nalgonda","namakkal","nanded","nandurbar","narayanpur","narmada","narsimhapur","nashik","navsari","nawada","nayagarh","neemuch","new delhi","nicobars","nizamabad","north","north & middle andaman","north garo hills","north goa","north tripura","north twenty four parganas","north west","north-east","nuapada","osmanabad","pakaur","palakkad","palamu","pali","palwal","panch mahals","panchkula","panipat","panna","papum pare","parbhani","paschim medinipur","pashchim champaran","pashchimi singhbhum","patan","pathanamthitta","pathankot","patiala","patna","perambalur","peren","phek","pilibhit","pithoragarh","porbandar","prakasam","pratapgarh","puducherry","pudukkottai","pulwama","punch","pune","purba champaran","purba medinipur","purbi singhbhum","puri","purnia","puruliya","rae bareli","raichur","raigarh","raipur","raisen","rajauri","rajgarh","rajkot","rajnandgaon","rajsamand","ramanagara","ramanathapuram","ramban","ramgarh","rampur","ranchi","rangareddy","ratlam","ratnagiri","rayagada","reasi","rewa","rewari","ri bhoi","rohtak","rohtas","rudraprayag","rupnagar","sabar kantha","sagar","saharanpur","saharsa","sahibganj","sahibzada ajit singh nagar","saiha","salem","samastipur","samba","sambalpur","sambhal","sangli","sangrur","sant kabir nagar","sant ravidas nagar bhadohi","saran","sarikela-kharswana","satara","satna","sawai madhopur","sehore","senapati","seoni","sepahijala","serchhip","shahdara","shahdol","shaheed bhagat singh nagar","shahjahanpur","shajapur","shamali","sheikhpura","sheohar","sheopur","shimla","shimoga","shivpuri","shrawasti","shupiyan","sibsagar","siddharthnagar","sidhi","sikar","simdega","sindhudurg","singrauli","sirmaur","sirohi","sirsa","sitamarhi","sitapur","sivaganga","siwan","solan","solapur","sonapur","sonbhadra","sonipat","sonitpur","south","south andaman","south east delhi","south garo hills","south goa","south tripura","south twenty four parganas","south west delhi","south west garo hills","south west khasi hills","sri potti sriramulu nellore","srikakulam","srinagar","sukma","sultanpur","sundargarh","supaul","surajpur","surat","surendranagar","surguja","tamenglong","tapi","tarn taran","tawang","tehri garhwal","thane","thanjavur","the dangs","the nilgiris","theni","thiruvallur","thiruvananthapuram","thiruvarur","thoothukkudi","thoubal","thrissur","tikamgarh","tinsukia","tirap","tiruchirappalli","tirunelveli","tiruppur","tiruvannamalai","tonk","tuensang","tumkur","udaipur","udalguri","udham singh nagar","udhampur","udupi","ujjain","ukhrul","umaria","una","unakoti","unnao","upper siang","upper subansiri","uttar dinajpur","uttara kannada","uttarkashi","vadodara","vaishali","valsad","varanasi","vellore","vidisha","viluppuram","virudhunagar","visakhapatnam","vizianagaram","warangal","wardha","washim","wayanad","west","west garo hills","west godavari","west kameng","west khasi hills","west nimar","west siang","west tripura","wokha","yadgir","yamunanagar","yanam","yavatmal","zunheboto"]
	#"num","state","district","tier",
	columns = ["sex ratio","total births to women 15 to 19","mean births to women 40 to 49","family planning methods used","modern familt planning methods used","unmet need family planning","institutional deliveries","home delivery skilled","full vaccinated children","prevalence acute illness","Prevalence Chronic illness","prevalence anaemia 6 to 59 months","prevalence severe anaemia 6 to 59 months","prevalence anaemia pregnant women aged 15 to 49 years","prevalence severe anaemia pregnant women aged 15 to 49 years","prevalence anaemia women aged 15 to 49 years","prevalence severe anaemia women aged 15 to 49 years","mean age marriage girls","mean age marriage boys","women married less than 18","men married less than 18","villages sub health centres less than 3 km","villages sub health centres less than 10 km","24 7 phc","district hospitals","primary gross enrolment ratio","primary net enrolment ratio","primary drop out rate","primary pupil teacher ratio","primary student classroom ratio","primary girl enrolment","primary female teachers","primary new government schools since 2003","primary schools with girls toilet","primary schools with boys toilet","primary schools with drinking water facility","primary schools with electricity","upper primary gross enrolment ratio","upper primary net enrolment ratio","upper primary drop out rate","upper primary pupil teacher ratio","upper primary student classroom ratio","upper primary girls enrolment","upper primary female teachers","upper primary new government schools since 2003","upper primary schools with girls toilet","upper primary schools with boys toilet","upper primary schools with drinking water facility","upper primary schools with electricity","population total","population male","population female","percentage houses with electricity","number total houses in district","percentage houses with improved source of drinking water","percentage total houses in district","percentage houses with electricity as main source","percentage houses with solar energy as main source","percentage houses with no lighting","number houses with electricity as main source","number houses with solar energy as main source","number houses with no lighting","percentage houses main source of drinking water within premises","percentage houses receiving treated tap water within premises","percentage houses receiving untreated tap water within premises","number houses main source of drinking water within premises","number houses receiving treated tap water within premises","number houses receiving untreated tap water within premises","pecentage houses with landline phone","pecentage houses with mobile phone","pecentage houses with computer/laptop with internet connection","number of houses","total population","total male population","total female population","0 to 6 age group persons","0 to 6 age group males","0 to 6 age group females","scheduled caste persons","scheduled caste males","scheduled caste females","scheduled tribe persons","scheduled tribe males","scheduled tribe females","person literates","male literates","female literates","person illiterates","male illiterates","female illiterates","total workers","total workers male","total workers female","main workers persons","main workers male","main workers female","main workers cultivators persons","main workers cultivators male","main workers cultivators female","main workers agricultural labourer persons","main workers agricultural labourer male","main workers agricultural labourer female","main workers household industry persons","main workers household industry male","main workers household industry female","main workers other persons","main workers other male","main workers other female","MW persons","MW male","MW female","MW cultivators persons","MW cultivators male","MW cultivators female","MW agricultural labourer persons","MW agricultural labourer male","MW agricultural labourer female","MW household industry persons","MW household industry male","MW household industry female","MW other persons","MW other male","MW other female","MW worked 3 to 6 months last year persons","MW worked 3 to 6 months last year male","MW worked 3 to 6 months last year female","MW cultivators worked 3 to 6 months last year persons","MW cultivators worked 3 to 6 months last year male","MW cultivators worked 3 to 6 months last year female","MW agricultural labourer worked 3 to 6 months last year persons","MW agricultural labourer worked 3 to 6 months last year male","MW agricultural labourer worked 3 to 6 months last year female","MW household industry worked 3 to 6 months last year persons","MW household industry worked 3 to 6 months last year male","MW household industry worked 3 to 6 months last year female","MW other worked 3 to 6 months last year persons","MW other worked 3 to 6 months last year male","MW other worked 3 to 6 months last year female","MW worked 0 to 3 months last year persons","MW worked 0 to 3 months last year male","MW worked 0 to 3 months last year female","MW cultivators worked 0 to 3 months last year persons","MW cultivators worked 0 to 3 months last year male","MW cultivators worked 0 to 3 months last year female","MW agricultural labourer worked 0 to 3 months last year persons","MW agricultural labourer worked 0 to 3 months last year male","MW agricultural labourer worked 0 to 3 months last year female","MW household industry worked 0 to 3 months last year persons","MW household industry worked 0 to 3 months last year male","MW household industry worked 0 to 3 months last year female","MW other worked 0 to 3 months last year persons","MW other worked 0 to 3 months last year male","MW other worked 0 to 3 months last year female","non workers persons","non workers male","non workers female"]
	operations = ["greater than", "more than", "above", "less than", "below"]
	tiers = [" rural ", " urban "]

	state_arr = []
	district_arr =[]
	tier_arr = []
	sex_arr = []
	num_arr = []
	_column_arr = []
	column_arr = []
	key_column_arr = []
	column_guess =  ""
	operation_arr = []
	

	#get state
	for state in states:
		if state.lower() in text:
			state_arr.append("'"+state+"'")
			
	#get district		
	for district in districts:
		if district.lower() in text:
			district_arr.append("'"+district+"'")

	#get tier
	for tier in tiers:
		if tier.lower() in text:
			tier_arr.append("'"+tier.strip()+"'")

	#get columns
	for column in columns:
		if column in text:
			_column_arr.append(["\""+column+"\"",text.find(column)])
	if _column_arr:
		#sort by second list
		_column_arr.sort(key = lambda x : x [1])
		#get just columns
		column_arr, _ = zip(*_column_arr)


	#estimate if direct not found
	#not gonna do estimates for all because you never know what it might spew up, or where to stop
	#maybe look into minimum scores? 
	prev_score = 0
	if not column_arr:
		for column in columns:
			score = similar(text, column)
			if score > prev_score:
				#prev_score2, column_guess2 = prev_score, column_guess
				prev_score, column_guess = score, column		
			#elif score > prev_score2:
				#prev_score2, column_guess2 = score, column
			same_words = set.intersection(set(column_guess.split(" ")), set(text.split(" ")))
		if same_words:
			column_arr.append("\""+column_guess+"\"")		
			#column_arr.append("\""+column_guess2+"\"")

	#get operations
	for operation in operations:
		if operation in text:
			operation_arr.append(operation)

	#find numbers
	num_arr = re.findall('\d+',text)

	# if state_arr:
		# print("State", sorted(state_arr, key=len))
	# if district_arr:
		# print("District", sorted(district_arr, key=len))
	# print("Tier", tier_arr)
	# print("operation", operation_arr)
	# print("columns", column_arr)
	# print("Key columns", key_column_arr)

	if not column_arr:
		#print("no columns?")
		return("no_columns")
	else:
		#conn_string = "host='10.87.169.18' dbname='janoindia' user='postgres' password='password'"
		conn_string = "host='10.11.241.37' port='57870' dbname='A9BVSbLmy3FIe5GL' user='fQ5XZQOqQUVdiHBP' password='mLqMm6GFb8EYFt51'"
		# print the connection string we will use to connect
		#print("Connecting to database\n" + conn_string)
	 
		# get a connection, if a connect cannot be made an exception will be raised here
		conn = psycopg2.connect(conn_string)
	 
		# conn.cursor will return a cursor object, you can use this cursor to perform queries
		cursor = conn.cursor()
		
		col,qry = gen_query(state_arr,district_arr,tier_arr,column_arr,operation_arr,num_arr)
		# execute our Query
		cursor.execute("SELECT * FROM("+qry+") a") 
		#cursor.execute("SELECT 'Hello World'") 
		#a limit 10")
		
		# retrieve the records from the database
		records = cursor.fetchall()
		results = str(records)
		results = re.sub("Decimal\('(\d+|\d+\.\d+)'\)","\\1",results).replace("[",",")
		# print out the records using pretty print
		# note that the NAMES of the columns are not shown, instead just indexes.
		# for most people this isn't very useful so we'll show you how to return
		# columns as a dictionary (hash) in the next example.
		#pprint.pprint(records)
		return("["+col+results).replace("(","[").replace(")","]").replace("'",'"').replace("None",'""')
 
if __name__ == "__main__":
	#text = "women married before age 18 in anantapur andhra pradesh"
	#text = "houses in rural areas with mobile phones"
	#text = "Districts where female literates are more than male literates"
	#text = "Relationship between percentage of girls enrolling in school and the percentage of female teachers"
	#text = "Net enrolment rate of education" 
	#text = "percentage houses in rural areas of Anantapur with mobile phones"
	#text = "total working population in Anantpur"
	#text = "Districts where female literates are more than male literates"
	#text = "Districts where sex rato more than 200"
	text = input("Enter your query: ")
	print(query(text))