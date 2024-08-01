from collections.abc import ValuesView
import streamlit as st
import requests
import csv

with open("Pokedex.txt", "r") as f:
    read=f.read()
    options=read.split("\n")
    f.close()
with open("Type_Data.csv", encoding="utf8") as f:
    cr=csv.reader(f)
    next(f)
    Type_Data={}
    for row in cr:
        d={}
        headers=["","Coverages","Color","Resistance","Weakness","Immunity"]
        for value in range(len(row)):
            if value==0:
                continue
            if value ==2:
                d[headers[value]]=row[value]
            else:
                d[headers[value]]=eval(row[value])
        Type_Data[row[0]]=d

try:
    pokemon=st.selectbox("Pokemon Name", placeholder="Select a Pokemon", options=options)
    url = "https://pokeapi.co/api/v2/pokemon/" + pokemon.lower().rstrip().lstrip()
    data = requests.get(url).json()
    name = data['name'].title()
    image_url = data['sprites']['front_default']
    types_string=":gray[Types:] "
    coverages = []
    coverage_string=":gray[Coverage Options:] "
    types=[]
    for type_data in data["types"]:
        type = type_data["type"]["name"].capitalize()
        types.append(type)
        types_string+=f'<span style="color:{Type_Data[type]["Color"]}">{type}</span>'+', '
        for coverage in Type_Data[type]["Coverages"]:
            if coverage not in coverages:
                coverages.append(coverage)
                coverage_string+=f'<span style="color:{Type_Data[coverage]["Color"]}">{coverage}</span>'+', '
    imm,res,weak=[],[],[]
    immstring,resstring,weakstring=f":gray[Immunities:] ",f":gray[Resistances:] ",f":gray[Weaknesses:] " 
    for i in types:
        im=(Type_Data[i]["Immunity"])
        for j in im:
            imm.append(j)
            immstring+=f'<span style="color:{Type_Data[j]["Color"]}">{j}</span>'+', '
    for i in types:
        res=(Type_Data[i]["Resistance"])
        for j in res:
            if j not in imm:
                res.append(j)
                resstring+=f'<span style="color:{Type_Data[j]["Color"]}">{j}</span>'+', '
    for i in types:
        weak=(Type_Data[i]["Weakness"])
        for j in weak:
            if j not in imm and j not in res:
                weak.append(j)
                weakstring+=f'<span style="color:{Type_Data[j]["Color"]}">{j}</span>'+', '
    base_stats = {}
    for stat in data["stats"]:
        base_stats[stat["stat"]["name"]] = stat["base_stat"]
    col1, col2 = st.columns(2)
    with col1:
        st.write(f':gray[{name} Info]')
        st.markdown(types_string[0:-2:], unsafe_allow_html=True)
        for stat in ["hp","attack","defense","special-attack","special-defense","speed"]:
            stat_value=base_stats[stat]
            if stat_value>0 and stat_value<80:
                stat_int=f'<span style="color:red">{stat_value}</span>'
            elif stat_value>=80 and stat_value<100:
                stat_int=f'<span style="color:orange">{stat_value}</span>'
            elif stat_value>=100 and stat_value<120:
                stat_int=f'<span style="color:gold">{stat_value}</span>'
            elif stat_value>=120 and stat_value<140:
                stat_int=f'<span style="color:limegreen">{stat_value}</span>'
            elif stat_value>=140 and stat_value<160:                
                stat_int=f'<span style="color:green">{stat_value}</span>'
            else:                
                stat_int=f'<span style="color:DarkTurquoise">{stat_value}</span>'
            st.write(f":gray[{stat.title()}:] "+stat_int, unsafe_allow_html=True)
        st.write(coverage_string[0:-2:], unsafe_allow_html=True)
        
    with col2:
        st.image(image_url, width=100) 
    st.write("BOOYEA")
    st.write(weakstring[0:-2:], unsafe_allow_html=True)
    st.write(resstring[0:-2:], unsafe_allow_html=True)
    st.write(immstring[0:-2:], unsafe_allow_html=True)
except Exception as e:
    st.write(e)
