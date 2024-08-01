import streamlit as st
import requests

with open("Pokedex.txt", "r") as f:
    read=f.read()
    options=read.split("\n")
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
    for type_data in data["types"]:
        type = type_data["type"]["name"].capitalize()
        types_string+=f'<span style="color:{coverage_options[type][1]}">{type}</span>'+', '
        for coverage in coverage_options[type][0]:
            if coverage not in coverages:
                coverages.append(coverage)
                coverage_string+=f'<span style="color:{coverage_options[coverage][1]}">{coverage}</span>'+', '
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
except:
    st.write("An error occured")
