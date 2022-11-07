import streamlit as st
import pandas as pd
import numpy as np
import re
import time
import fuzzyset
import wikipedia
import gc
import itertools
from io import BytesIO

#Initialization of storage
if 'Status' not in st.session_state:
    st.session_state['Status'] = 'Input'

if 'Dataset' not in st.session_state:
    st.session_state['Dataset'] = None

if 'Output' not in st.session_state:
    st.session_state['Output'] = None

df=st.session_state['Dataset'] 
engine=pd.read_csv("GADMsmall.csv",encoding="utf-8-sig")


def CheckEnglish(s): #Checks whether string is strictly English, if not, search with wiki API
    isEnglish=True
    isEnglish=bool(re.match("^[a-zA-Z\s\.,-/&'\"()]+$",s))
    return isEnglish

def LayerQuery(num):
    layer=-1 
    if num <=2:
        layer=1
    elif num<=5:
        layer=2
    elif num<=8:
        layer=3
    elif num<=10:
        layer=4
    else:
        layer=5
    return layer

def FindAll(search_list, search_item):
    indices = []
    for (index, item) in enumerate(search_list):
        if item == search_item:
            indices.append(index)
    return indices

def MinSearch(ls):
    lf=[]
    indices=[]    
    minimum=min(itertools.chain.from_iterable(ls))
    for i in range(len(ls)):
        try:
            j=FindAll(ls[i],minimum)
            indices=indices+[j]
            lf=lf+[i]
        except:
            pass
    indices=np.array(indices)
    
    if indices.any():
        indices = np.hstack(indices)
    else:
        indices = indices.flatten()
    indices=sorted(list(indices.flatten()))
    return minimum,lf,indices



@st.cache
def convert_csv(df):
    return df.to_csv(index=False).encode('utf-8-sig')

stopwords=['sub-prefecture',
 'city council',
 'emirate',
 'local municipality',
 'ward',
 'distrito',
 'neighborhood',
 'circuit',
 'corregimiento departamental',
 'clan',
 'autonomous district',
 'water body',
 'region',
 'aboriginal council',
 'metropolitan municipality',
 "'autonomous region'",
 'water body',
 'unitary district',
 'captial city district',
 'upazilla',
 'village block',
 'administrative district',
 'districts',
 'metropolitan borough (city)',
 'colline',
 'borough district',
 'canton municipality',
 'ressort',
 'banner',
 'capital region',
 'conservancy',
 'new district',
 'london borough (city)',
 'decentralized administration',
 'directly governed city',
 'settlement',
 'districts|municipals',
 'sovereign territory',
 'atoll',
 'united counties',
 'chartered community',
 'london borough',
 'administrative zone',
 'unitary authority (wales)',
 'subregion',
 'free state',
 'autonomous sector',
 'commune-cotiere',
 'island',
 'village',
 'kingdom',
 'autonomous county',
 'metropolitan borough',
 'sub district',
 'metropolitan borough',
 'area',
 'rural commune',
 'islands',
 'not classified',
 'city with powiat rights',
 'republic',
 'prefecture city',
 'small town',
 'island group',
 'statistical region',
 'autonomous okurg',
 'unitary authority (city)',
 'subdivision of unorganized',
 'union',
 'other',
 'town council',
 'municipality|prefecture',
 'village nordique',
 'independent town',
 'county',
 'governorate',
 '?',
 'regional district',
 'island municipality',
 'rural community',
 'island council',
 'special woreda',
 'regional district electoral area',
 'province',
 'capital metropolitan city',
 'regional county municipality',
 'rural municipality',
 "nisga'a village",
 'commune',
 'part',
 'london borough (royal)',
 'autonomous community',
 'independent city',
 'resort village',
 'subprefecture',
 'special area',
 'metropolitan city',
 'special administrative region',
 'rural city',
 'city council',
 'village cri',
 'municpality|city council',
 'special city',
 'administrative subdivisions',
 'union territory',
 'state reserve',
 'locality',
 'mukim',
 'regional municipality',
 'urban district',
 'county municipality',
 'capital district',
 'headquarter',
 'hamlet',
 'sector',
 'island area',
 'unincorporated area',
 'borough',
 'chef-lieu-wilaya',
 'metropolis',
 'census division',
 'district municipality',
 'local authority',
 'statutory city',
 'special municipality',
 'canton',
 'city municipality',
 'voivodeship',
 'indian settlement',
 'subdivision',
 'raion',
 'united cantons municipality',
 'reef',
 'northern village',
 'sovereign base area',
 'quarter',
 'cantonal head',
 'ceremonial county',
 'municipal region',
 'delegation',
 'zone',
 'capital territory',
 'metropolitan autonomous city',
 'unknown',
 'metropolian region',
 'autonomous prefecture',
 'outer islands',
 'entity',
 'census area',
 'specialized municipality',
 'lake',
 'development region',
 'constituency',
 'village naskapi',
 'federal territory',
 'autonomous city',
 'autonomous republic',
 'commissiary',
 'parish district',
 'parish municipality',
 'unitary authority',
 'sub-province',
 'unitary authority (county)',
 'indian government district',
 'constituent country',
 'indian reserve',
 'sub-commune',
 'cell',
 'special region|zone',
 'metropolitan borough (city)',
 'territory',
 'circle',
 'city and borough',
 'sub-district',
 'autonomous banner',
 'capital',
 'inuite land',
 'unitary authority (county)',
 'national district',
 'districts of republican subordin',
 'unitary district (city)',
 'town',
 'league',
 'area council',
 'division',
 'autonomous province',
 'city county',
 'prefecture',
 'autonomous island',
 'shire',
 'sub-county',
 'local council',
 'economic prefecture',
 'waterbody',
 'district council',
 'municipality (urban-rural)',
 'village development committee',
 'sub-region',
 'dependency',
 'group of islands',
 'improvement district',
 'ville',
 'state',
 'northern hamlet',
 'special ward',
 'reserve',
 'rural parish',
 'urban commune',
 'united county',
 'community',
 'subdistrict',
 'subdivision of county municipali',
 'autonomous region',
 'unitary authority (city)',
 'teslin land',
 'territorial unit',
 'traditional authority',
 'area outside territorial authori',
 'statutory city',
 'autonomous territory',
 'sub-prefecture',
 'metropolitan district',
 'intendancy',
 'village district',
 'indigenous territory',
 'autonomous island',
 'regency',
 'administrative county',
 'administrative county district',
 'federal district',
 'centrally administered area',
 'city',
 'town district',
 'municipiality',
 'city and county',
 'unorganized',
 'turkey',
 "nisga'a land",
 'townlet',
 'training center',
 'town|municipal',
 'atol',
 'sous colline',
 'asia',
 'chiefdom',
 'local government district',
 'sum',
 'township',
 'commune (same as level 3)',
 'commune|municipality',
 'urban',
 'county city',
 'autononous region',
 'department',
 'unitary authority',
 'provincie',
 'national park',
 'assembly',
 'administrative committee',
 'municipality',
 'comarca',
 'union territory',
 'municipality (rural)',
 'township and royalty',
 'sub-chief',
 'summer village',
 'unitary district',
 'capital city',
 'municipal district',
 'taluk',
 'municipal district',
 'administrative area',
 'regional council',
 'distict',
 'distrito metropolitano',
 'land reserved',
 'special district',
 'village|township',
 'urban community',
 'urban prefecture',
 'parish',
 'arrondissement',
 'sovereign territories',
 'neighbourhood democratic',
 'minor district',
 'district',
 'municipality (urban)',
 'autonomous commune',
 'provincial city',
 'unitary district (city)',
 'city of regional significance',
 'cadastral community']


#Program starts here-------------------------------------------------------------------------

#Header
st.title("Automation of Geographical Matching at all levels")
st.write("This web app takes a dataset with a column of place names, even with spelling mistakes or in a different language, and return its match from the GADM database")



#Accept file as input
st.header("Input")
file=st.file_uploader('Upload your dataset',type=["csv","xls","xlsx"]) 
submit=st.button("Submit")
if submit==True:
    try:
        if file!=None:
            if file.name.find(".csv")!=-1: #Found .csv extension in file name
                df=pd.read_csv(file)
                st.session_state['Dataset'] = df
                st.session_state['Status'] = 'Settings'
            else: #Other extensions
                df=pd.read_excel(file)
                st.session_state['Dataset'] = df
                st.session_state['Status'] = 'Settings'
    except NameError:
        st.subheader("File not found. Please upload your file above.")
    except ValueError:
        st.subheader("File not found. Please upload your file above.")

#Shows dataset uploaded
if st.session_state['Status'] == 'Settings':
    st.subheader("Your dataset:")
    displaydf=df.astype("str")
    try:
        st._legacy_dataframe(displaydf)
    except:
        st.dataframe(displaydf)


#Custom settings for the user
st.header("Settings")
if st.session_state['Status'] == 'Settings':
    options=list(df.columns)
    st.subheader("Column of place names")
    choice=st.selectbox("Select the column of place names in your dataset",options)
   
    
    start=st.button("Match")
    message=st.empty()
    progresslabel=st.empty()
    progressbar=st.empty()
    successful=st.empty()
    outputlabel=st.empty()
    outputdf=st.empty()

    if start:
        #ADD CORE HERE
        hierarchy=['NAME_1', 'VARNAME_1', 'NL_NAME_1', 'NAME_2', 'VARNAME_2', 'NL_NAME_2', 'NAME_3', 'VARNAME_3', 'NL_NAME_3', 'NAME_4', 'VARNAME_4', 'NAME_5']
        namecols=['NAME_0', 'NAME_1', 'NAME_2', 'NAME_3', 'NAME_4', 'NAME_5']
        names=list(df[choice])
        results=[]
        results_layerfound=[]
                

        #attempt direct match
        for i in range(len(names)): #one name at a time
            target=names[i].lower()
            matched=False
            repeated=False
            found=[]
            layerfound=[]
            
            if target in names[:i]:
                repeated=True
                found=results[names[:i].index(target)]
                layerfound=results_layerfound[names[:i].index(target)]
                

            if not repeated:
                for j in range(len(hierarchy)): #for the one name, start cycling through each layer
                    pool=engine[hierarchy[j]].str.lower().values 
                    
                    for k in range(len(pool)): #match with each item in the pool layer of database
                        element=pool[k]
                        if target==element:
                            if k in found:
                                layerfound.pop(found.index(k))
                                found.remove(k)
                            matched=True
                            found=found+[k]
                            layerfound=layerfound+[j]

                        if "|" in str(element):
                            alternatives=element.split("|")
                            for m in range(len(alternatives)):
                                if target==alternatives[m]:
                                    if k in found:
                                        layerfound.pop(found.index(k))
                                        found.remove(k)
                                    matched=True
                                    found=found+[k]
                                    layerfound=layerfound+[j]
                    
                if not matched: #all layers cycled but zero direct match
                    if CheckEnglish(target)==False: #if not English word, wiki query to English and perform direct search
                        try:
                            wikimatch=wikipedia.search(target)[0]
                            wikimatchsplit=wikimatch.split()
                            if len(wikimatchsplit)>=1: #Remove parenthesis and stopwords from the actual place name
                                resultwords  = [word for word in wikimatchsplit if word.lower() not in stopwords]
                                wikimatch = ' '.join(resultwords).strip().replace('(','').replace(')','').replace(',','')
                            target=wikimatch.lower()
                            
                            for j in range(len(hierarchy)): #for the one name, start cycling through each layer
                                pool=engine[hierarchy[j]].str.lower().values 
                                for k in range(len(pool)): #match with every name in pool layer
                                    element=pool[k]
                                    if target==element:
                                        if k in found:
                                            layerfound.pop(found.index(k))
                                            found.remove(k)
                                        matched=True
                                        found=found+[k]
                                        layerfound=layerfound+[j]
                                    if "|" in str(element):
                                        alternatives=element.split("|")
                                        for m in range(len(alternatives)):
                                            if target==alternatives[m]:
                                                if k in found:
                                                    layerfound.pop(found.index(k))
                                                    found.remove(k)
                                                matched=True
                                                found=found+[k]
                                                layerfound=layerfound+[j]
                        except:
                            pass
                    

                    if not matched: #if still zero direct match (either English word zero direct match, or translated to English zero direct match)
                    
                        
                        matrix = fuzzyset.FuzzySet()
                        

                        for j in range(len(hierarchy)): #add each word from each layer to the fuzzy set algo
                            pool=engine[hierarchy[j]].str.lower().values 
                            for k in range(len(pool)):
                                element=pool[k]
                                if type(element)==str:
                                    if "|" in str(element):
                                        temp=[]
                                        alternatives=element.split("|")
                                        for m in range(len(alternatives)):
                                            matrix.add(alternatives[m])    
                                    else:
                                        matrix.add(element)
                        
                        closest=matrix.get(target)[0][1] #return closest match
                        fitness=matrix.get(target)[0][0] #return cosine similarity
                        threshold=0.7 #set threshold
                        
                        
                        if fitness>=threshold: #only attempt closest match if similarity is over a certain threshold
                            for j in range(len(hierarchy)): #for the one name, start cycling through each layer
                                pool=engine[hierarchy[j]].str.lower().values 
                                for k in range(len(pool)): #match with each item in the pool layer of database
                                    element=pool[k]
                                    if closest==element:
                                        if k in found:
                                            layerfound.pop(found.index(k))
                                            found.remove(k)
                                        matched=True
                                        found=found+[k]
                                        layerfound=layerfound+[j]
                                    if "|" in str(element):
                                        alternatives=element.split("|")
                                        for m in range(len(alternatives)):
                                            if closest==alternatives[m]:
                                                if k in found:
                                                    layerfound.pop(found.index(k))
                                                    found.remove(k)
                                                matched=True
                                                found=found+[k]
                                                layerfound=layerfound+[j]
                    


            
            results=results+[found] #add all matches back to the output list
            results_layerfound=results_layerfound+[layerfound]
            progresslabel.write(f"Matching item {i+1} out of {len(names)}...")
            progressbar.progress(int((i+1)/len(names)*90))

        #handling results-------------------------------------------
        final=[]
        output=[]
        layernames=[]
        concataddress=[]
        layernumbers=[]
        queryvars=[]
        lastgid=[]

        #extract all record matched into a list of dataframes
        progresslabel.write("Formatting output...")
        for i in range(len(results)):
            matches=results[i]
            if len(matches)!=0:
                matchdf=engine.loc[matches]
            else:
                matchdf=pd.DataFrame()
            final=final+[matchdf]

        #number of matches for each word
        matchnum=[len(x) for x in final]

        #return layer number
        for i in range(len(results_layerfound)):
            layers=results_layerfound[i]
            tempnumbers=[]
            for j in range(len(layers)):
                tempnumbers=tempnumbers+[LayerQuery(layers[j])]
            layernumbers=layernumbers+[tempnumbers]


        #return layer name so that you know what is the scale of the match
        for i in range(len(layernumbers)):
            tempvars=[]
            tempnames=[]
            for j in range(len(layernumbers[i])):
                tempvars=tempvars+["ENGTYPE_"+str(layernumbers[i][j])]
                tempnames=tempnames+[final[i].loc[results[i][j]]["ENGTYPE_"+str(layernumbers[i][j])]]
            queryvars=queryvars+[tempvars]
            layernames=layernames+[tempnames]

        #return last gid of the match
        for i in range(len(layernumbers)):
            tempvars=[]
            tempgid=[]
            for j in range(len(layernumbers[i])):
                tempvars=tempvars+["GID_"+str(layernumbers[i][j])]
                tempgid=tempgid+[final[i].loc[results[i][j]]["GID_"+str(layernumbers[i][j])]]
            queryvars=queryvars+[tempvars]
            lastgid=lastgid+[tempgid]

        #stick it back to the dataframes
        for i in range(len(layernumbers)):
            final[i]["LayerNumberFound"]=layernumbers[i]
            final[i]["LayerNumberFound"]=final[i]["LayerNumberFound"].astype(int)

        for i in range(len(lastgid)):
            final[i]["LastLayerGID"]=lastgid[i]

        for i in range(len(layernames)):
            final[i]["LayerNameFound"]=layernames[i]

        for i in range(len(final)):
            if all(item in list(final[i].columns) for item in namecols):
                final[i]['Address'] = final[i][namecols].apply(lambda row: '/'.join(row.values.astype(str)), axis=1)
                final[i]['Address'] = final[i]['Address'].str.replace("/nan","")

        #rearrange the order of columns
        for i in range(len(final)):
            if all(item in list(final[i].columns) for item in ["LayerNumberFound","LayerNameFound","Address","LastLayerGID"]):
                neworder=final[i].columns.tolist()
                neworder.remove("LastLayerGID")
                neworder.remove("LayerNumberFound")
                neworder.remove("LayerNameFound")
                neworder.remove("Address")
                neworder=["Address","LayerNameFound","LayerNumberFound","LastLayerGID"]+neworder
                final[i]=final[i][neworder]
                #-----!!!
                final[i]=final[i][["Address","LayerNameFound","LayerNumberFound","LastLayerGID"]]

        #combining all rows to one row
        rows=[]
        columns=[]
        for i in range(len(final)):
            temprows=[]    
            tempcolumns=[]
            for j in range(len(final[i])):
                tempdf=final[i].loc[[results[i][j]]].reset_index(drop=True)
                tempdf.columns=["MATCH"+str(j+1)+"_"+str(x) for x in final[i].loc[[results[i][j]]].columns.tolist()]
                temprows=temprows+[tempdf]
            rows=rows+[temprows]


        for i in range(len(rows)):
            if len(rows[i])>=2:
                output=output+[pd.concat(rows[i],axis=1)]
            elif len(rows[i])==1:
                output=output+[rows[i][0]]
            else:
                output=output+[pd.DataFrame()]

        for i in range(len(output)):
            output[i]["NUM_MATCHES"]=[matchnum[i]]

        #rearrange the order of columns
        for i in range(len(output)):
            neworder=output[i].columns.tolist()
            neworder.remove("NUM_MATCHES")
            neworder=["NUM_MATCHES"]+neworder
            output[i]=output[i][neworder]

        outputdf=pd.concat(output)
        outputdf["QUERY"]=names

        #rearrange the order of columns
        neworder=outputdf.columns.tolist()
        neworder.remove("QUERY")
        neworder=["QUERY"]+neworder
        outputdf=outputdf[neworder]

        outputdf = outputdf.convert_dtypes()




        progressbar.progress(100)
        totalmatches=0
        for i in matchnum:
            if i >0:
                totalmatches+=1
        successful.success(f"Matching complete! At least one match returned for {totalmatches} out of {len(names)} items. {len(names)-totalmatches} out of {len(names)} items returned no match.")
        st.session_state['Output']=outputdf
        displayoutput=st.session_state['Output'].astype("str")
        outputlabel.subheader("Output:")

        #Export buttons
    if st.session_state['Output'] is not None:
        displayoutput=st.session_state['Output'].astype("str")
        outputlabel.subheader("Output:")
        try:
            st._legacy_dataframe(displayoutput)
        except:
            st.dataframe(displayoutput)
        col1, col2 = st.columns(2)
        csv=convert_csv(st.session_state['Output'])
        st.download_button(
        label="Download as CSV",
        data=csv,
        mime='text/csv',)

        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            st.session_state['Output'].to_excel(writer,index=False, sheet_name='Sheet1')
            writer.save()
        
        st.download_button(label="Download as Excel",file_name="output.xlsx",data=buffer,)

        
        

    
        






