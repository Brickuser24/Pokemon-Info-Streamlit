import streamlit as st
import requests
import csv

with open("Pokedex.txt", "r") as f:
    read=f.read()
    options=read.split("\n")
    f.close()

with open("Type_Data.csv", encoding="utf8") as f:
    cr = csv.reader(f)
    next(cr)
    Type_Data = {}
    headers = ["", "Coverages", "Color", "Resistance", "Weakness", "Immunity"]
    for row in cr:
        d = {}
        for value in range(len(row)):
            if value == 0:
                continue
            if value == 2:
                d[headers[value]] = row[value]
            else:
                d[headers[value]] = eval(row[value])
        Type_Data[row[0]] = d
    f.close()

coverage_options = {
    "Normal": (["Fighting", "Psychic", "Dark"],"WhiteSmoke"),
    "Water": (["Ice", "Steel", "Psychic"],"DodgerBlue"),
    "Poison": (["Bug", "Grass", "Electric"],"MediumOrchid"),
    "Psychic": (["Fairy", "Ghost", "Water"],"HotPink"),
    "Fighting": (["Electric", "Ice", "Fire"],"Brown"),
    "Flying": (["Steel", "Dragon", "Fighting"],"LightSkyBlue"),
    "Grass": (["Ground", "Poison", "Rock"],"ForestGreen"),
    "Ground": (["Rock", "Grass", "Dark"],"Sienna"),
    "Bug": (["Dark", "Poison", "Ground"],"YellowGreen"),
    "Rock": (["Ground", "Fire", "Electric"],"DarkKhaki"),
    "Dark": (["Rock", "Electric", "Poison"],"DimGray"),
    "Fairy": (["Psychic", "Water", "Grass"],"Magenta"),
    "Steel": (["Ice", "Ground", "Ghost"],"DarkGray"),
    "Ghost": (["Poison", "Flying", "Bug"],"RebeccaPurple"),
    "Ice": (["Water", "Fairy", "Steel"],"DeepSkyBlue"),
    "Dragon": (["Fire", "Grass", "Psychic"],"MediumBlue"),
    "Electric": (["Fairy", "Grass", "Dragon"],"Gold"),
    "Fire": (["Dragon", "Electric", "Fighting"],"OrangeRed")
}

try:
    pokemon=st.selectbox("Pokemon Name", placeholder="Select a Pokemon", options=options)
    url = "https://pokeapi.co/api/v2/pokemon/" + pokemon.lower().rstrip().lstrip()
    data = requests.get(url).json()
    name = data['name'].title()
    image_url = data['sprites']['front_default']
    types_string=":gray[Types:] "
    coverages = []
    coverage_string=":gray[Coverage Options:] "
    imm,res,weak = [],[],[]
    for type_data in data["types"]:
        type = type_data["type"]["name"].capitalize()
        imm.extend(Type_Data[type]["Immunity"])
        res.extend(Type_Data[type]["Resistance"])
        weak.extend(Type_Data[type]["Weakness"])
        types_string+=f'<span style="color:{coverage_options[type][1]}">{type}</span>'+', '
        for coverage in coverage_options[type][0]:
            if coverage not in coverages:
                coverages.append(coverage)
                coverage_string+=f'<span style="color:{coverage_options[coverage][1]}">{coverage}</span>'+', '
    base_stats = {}
    for stat in data["stats"]:
        base_stats[stat["stat"]["name"]] = stat["base_stat"]
    res_=[]
    for r in res:
        if r not in res_ and r not in weak and r not in imm:
            res_.append(r)
    weak_=[]
    for w in weak:
      if w not in res and w not in weak_ and w not in imm:
          weak_.append(w)
    imm_string=":gray[Immunities:] "
    res_string=":gray[Resistances:] "
    weak_string=":gray[Weaknesses:] "
    for i in imm:
        imm_string+=f'<span style="color:{coverage_options[i][1]}">{i}</span>'+', '
    if len(imm)==0:
        imm_string+=":gray[None]  "
    for r in res_:
        res_string+=f'<span style="color:{coverage_options[r][1]}">{r}</span>'+', '
    if len(res_)==0:
        res_string+=":gray[None]  "
    for w in weak_:
        weak_string+=f'<span style="color:{coverage_options[w][1]}">{w}</span>'+', '
    if len(weak_)==0:
        weak_string+=":gray[None]  "
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
        st.markdown(weak_string[0:-2:], unsafe_allow_html=True)
        st.markdown(imm_string[0:-2:], unsafe_allow_html=True)
        st.markdown(res_string[0:-2:], unsafe_allow_html=True)
    with col2:
        st.image(image_url, width=100)  
except Exception as e:
    st.write(e)
