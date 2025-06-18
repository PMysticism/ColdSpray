import streamlit as st
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph
import pandas as pd
import os

current_dir = os.path.dirname(__file__)
image_path = os.path.join(current_dir, "logo.jpg")


prologue_text = "SELECT DISTINCT ?title "
coldspray_text =""
custom_results = ""


@st.cache_resource
def load_graph(ttl_path):
    g = Graph()
    g.parse(ttl_path, format="ttl")
    return g

def run_query(g, query):
    results = g.query(query)
    rows = []
    for row in results:
        rows.append([str(cell) for cell in row])
    cols = results.vars
    return pd.DataFrame(rows, columns=[str(c) for c in cols])

st.title("Cold Spray Database")
st.image(image_path, width=200)

ttl_file = st.file_uploader("Upload RDF file", type=["ttl"])

if ttl_file is not None:
    g = load_graph(ttl_file)

    query_materials = {
        "any":"""""",
        "Aluminum and Aluminum Alloys":"""
        
            ?paper a cs:ColdSprayPaper ;
         cs:hasMetadata ?metadata ;
         cs:hasMaterial ?material .
  ?material cs:hasComposition ?composition .
  ?metadata cs:hasTitle ?title .
  FILTER (regex(?composition, "Al|Aluminum|aluminum"))
        """,
        "Copper and Copper Alloys":"""
        
            ?paper a cs:ColdSprayPaper ;
         cs:hasMetadata ?metadata ;
         cs:hasMaterial ?material .
  ?material cs:hasComposition ?composition .
  ?metadata cs:hasTitle ?title .
  FILTER (regex(?composition, "Cu|Copper|copper"))
        """,
        "Nickel and Nickel Alloys":"""
        
            ?paper a cs:ColdSprayPaper ;
         cs:hasMetadata ?metadata ;
         cs:hasMaterial ?material .
  ?material cs:hasComposition ?composition .
  ?metadata cs:hasTitle ?title .
  FILTER (regex(?composition, "Ni|Nickel|nickel"))
        """,
        "Titanium and Titanium Alloys":"""
        
            ?paper a cs:ColdSprayPaper ;
         cs:hasMetadata ?metadata ;
         cs:hasMaterial ?material .
  ?material cs:hasComposition ?composition .
  ?metadata cs:hasTitle ?title .
  FILTER (regex(?composition, "Ti|Titanium|titanium"))
        """,
        "Iron and Steel Alloys":"""
        
            ?paper a cs:ColdSprayPaper ;
         cs:hasMetadata ?metadata ;
         cs:hasMaterial ?material .
  ?material cs:hasComposition ?composition .
  ?metadata cs:hasTitle ?title .
  FILTER (regex(?composition, "Fe|Iron|Steel|iron|steel"))
        """,
        "Magnesium and Magnesium Alloys":"""
        
            ?paper a cs:ColdSprayPaper ;
         cs:hasMetadata ?metadata ;
         cs:hasMaterial ?material .
  ?material cs:hasComposition ?composition .
  ?metadata cs:hasTitle ?title .
  FILTER (regex(?composition, "Mg|Magnesium|magnesium"))
        """,
        "Carbides":"""
        
            ?paper a cs:ColdSprayPaper ;
         cs:hasMetadata ?metadata ;
         cs:hasMaterial ?material .
  ?material cs:hasComposition ?composition .
  ?metadata cs:hasTitle ?title .
  FILTER (regex(?composition, "SiC|WC|CBN|Carbide|carbide"))
        """,
        "Keyword Search":"""

    ?paper a cs:ColdSprayPaper ;
            cs:hasMetadata ?metadata ;
            cs:hasMaterial ?material .
    ?material cs:hasComposition ?composition .
    ?metadata cs:hasTitle ?title .
    FILTER (regex(?composition, "keyword"))

""",
    }

    query_preprocessing = {
        "any":"""""",
        "Heat Treatment":"""
        
            ?paper cs:hasPreprocessing ?preprocessing .
  ?preprocessing cs:hasHeatTreatment ?heatTreatment .
  ?heatTreatment cs:annealingTemperature ?annealingTemperature .
  ?heatTreatment cs:annealingTime ?annealingTime .
  BIND(CONCAT(STR(?annealingTemperature), ", ", STR(?annealingTime)) AS ?preprocessingMethod)
        """,

        "Powder Production":"""
        
            ?paper cs:hasPreprocessing ?preprocessing .
  ?preprocessing cs:hasPowderProduction ?preprocessingMethod .
  
        """,

        "Substrate Preparation":"""
        
            ?paper cs:hasPreprocessing ?preprocessing .
  ?preprocessing cs:hasSubstratePreparation ?preprocessingMethod .

        """,
        
    }

    query_characterization = {
        "any":"""""",
        "Scanning Electron Microscopy":"""
        
            ?paper cs:hasCharacterization ?characterization .
  ?characterization cs:techniqueName ?techniqueName .
  FILTER (regex(?techniqueName, "SEM|Scanning Electron Microscopy|scanning electron microscopy|sem"))
  ?characterization cs:parameter ?parameter .
  BIND(CONCAT("SEM"," ", STR(?parameter)) AS ?characterizationMethod)
  
        """,
        "Transmission Electron Microscopy":"""
        
            ?paper cs:hasCharacterization ?characterization .
  ?characterization cs:techniqueName ?techniqueName .
  FILTER (regex(?techniqueName, "TEM|Transmission Electron Microscopy|transmission electron microscopy|tem"))
  ?characterization cs:parameter ?parameter .
  BIND(CONCAT("TEM"," ", STR(?parameter)) AS ?characterizationMethod)
  
        """,
        "Light Optical Microscopy":"""
        
            ?paper cs:hasCharacterization ?characterization .
  ?characterization cs:techniqueName ?techniqueName .
  FILTER (regex(?techniqueName, "LOM|Light Optical Microscopy|light optical microscopy|Optical Microscopy|optical microscopy"))
  ?characterization cs:parameter ?parameter .
  BIND(CONCAT("LOM"," ", STR(?parameter)) AS ?characterizationMethod)
  
        """,
        "Electron Backscatter Diffraction":"""
        
            ?paper cs:hasCharacterization ?characterization .
  ?characterization cs:techniqueName ?techniqueName .
  FILTER (regex(?techniqueName, "EBSD|Electron Backscatter Diffraction|ebsd|electron backscatter diffraction"))
  ?characterization cs:parameter ?parameter .
  BIND(CONCAT("EBSD"," ", STR(?parameter)) AS ?characterizationMethod)
  
        """,
        "Energy-dispersive X-ray":"""
        
            ?paper cs:hasCharacterization ?characterization .
  ?characterization cs:techniqueName ?techniqueName .
  FILTER (regex(?techniqueName, "Energy-dispersive X-ray|EDS|EDX|EDAX"))
  ?characterization cs:parameter ?parameter .
  BIND(CONCAT("EDS/EDAX"," ", STR(?parameter)) AS ?characterizationMethod)
  
        """,
        "X-ray Diffraction":"""
        
            ?paper cs:hasCharacterization ?characterization .
  ?characterization cs:techniqueName ?techniqueName .
  FILTER (regex(?techniqueName, "X-ray Diffraction|XRD|X-ray diffraction|xrd"))
  ?characterization cs:parameter ?parameter .
  BIND(CONCAT("XRD"," ", STR(?parameter)) AS ?characterizationMethod)
  
        """,
        "X-ray Photoelectron Spectroscopy":"""
        
            ?paper cs:hasCharacterization ?characterization .
  ?characterization cs:techniqueName ?techniqueName .
  FILTER (regex(?techniqueName, "X-ray Photoelectron Spectroscopy|XPS|X-ray photoelectron spectroscopy|xps"))
  ?characterization cs:parameter ?parameter .
  BIND(CONCAT("XPS"," ", STR(?parameter)) AS ?characterizationMethod)
  
        """,

        
    }

    query_results = {"None":"""""",
        "Microstructure":"""
        
            ?paper cs:hasMicrostructureResult ?featureDes .
  ?featureDes cs:featureDescription ?Microstructure .
  FILTER (regex(?Microstructure, "microstructure"))
  ?featureDes cs:featureValue ?featureval .
  BIND(CONCAT("Microstructure"," ", STR(?featureval)) AS ?resultsMethod)
        """,

        "Mechanical Properties":"""
        
            ?paper a cs:ColdSprayPaper ;
                cs:hasResult ?result.
            ?result cs:hasMechanicalProperty ?mechanicalProperty .
            ?mechanicalProperty cs:propertyName ?propertyName .
            ?mechanicalProperty cs:propertyValue ?propertyValue.
            ?mechanicalProperty cs:propertyUnit ?propertyUnit.
  
            FILTER(
            (REGEX(?propertyName = "tensile", "i"))

            )

                    """,



    }


    selected_materials_query = st.selectbox("Primary Material", ["any", "Aluminum and Aluminum Alloys", "Copper and Copper Alloys", "Nickel and Nickel Alloys", "Titanium and Titanium Alloys", "Iron and Steel Alloys", "Magnesium and Magnesium Alloys", "Carbides", "Keyword Search"])
    if query_materials[selected_materials_query] != "":
        prologue_text = prologue_text + "?composition " 

    if selected_materials_query == "Keyword Search":
        custom_material = st.text_input("Enter material keyword:")
        query_materials = {
        "any":"""""",
        "Aluminum and Aluminum Alloys":"""
        
            ?paper a cs:ColdSprayPaper ;
         cs:hasMetadata ?metadata ;
         cs:hasMaterial ?material .
        ?material cs:hasComposition ?composition .
        ?metadata cs:hasTitle ?title .
        FILTER (regex(?composition, "Al|Aluminum|aluminum"))
                """,
                "Copper and Copper Alloys":"""
                
                    ?paper a cs:ColdSprayPaper ;
                cs:hasMetadata ?metadata ;
                cs:hasMaterial ?material .
        ?material cs:hasComposition ?composition .
        ?metadata cs:hasTitle ?title .
        FILTER (regex(?composition, "Cu|Copper|copper"))
                """,
                "Nickel and Nickel Alloys":"""
                
                    ?paper a cs:ColdSprayPaper ;
                cs:hasMetadata ?metadata ;
                cs:hasMaterial ?material .
        ?material cs:hasComposition ?composition .
        ?metadata cs:hasTitle ?title .
        FILTER (regex(?composition, "Ni|Nickel|nickel"))
                """,
                "Titanium and Titanium Alloys":"""
                
                    ?paper a cs:ColdSprayPaper ;
                cs:hasMetadata ?metadata ;
                cs:hasMaterial ?material .
        ?material cs:hasComposition ?composition .
        ?metadata cs:hasTitle ?title .
        FILTER (regex(?composition, "Ti|Titanium|titanium"))
                """,
                "Iron and Steel Alloys":"""
                
                    ?paper a cs:ColdSprayPaper ;
                cs:hasMetadata ?metadata ;
                cs:hasMaterial ?material .
        ?material cs:hasComposition ?composition .
        ?metadata cs:hasTitle ?title .
        FILTER (regex(?composition, "Fe|Iron|Steel|iron|steel"))
                """,
                "Magnesium and Magnesium Alloys":"""
                
                    ?paper a cs:ColdSprayPaper ;
                cs:hasMetadata ?metadata ;
                cs:hasMaterial ?material .
        ?material cs:hasComposition ?composition .
        ?metadata cs:hasTitle ?title .
        FILTER (regex(?composition, "Mg|Magnesium|magnesium"))
                """,
                "Carbides":"""
                
                    ?paper a cs:ColdSprayPaper ;
                cs:hasMetadata ?metadata ;
                cs:hasMaterial ?material .
        ?material cs:hasComposition ?composition .
        ?metadata cs:hasTitle ?title .
        FILTER (regex(?composition, "SiC|WC|CBN|Carbide|carbide"))
                """,
                "Keyword Search":f"""

            ?paper a cs:ColdSprayPaper ;
                    cs:hasMetadata ?metadata ;
                    cs:hasMaterial ?material .
            ?material cs:hasComposition ?composition .
            ?metadata cs:hasTitle ?title .
            FILTER (regex(?composition, "{custom_material}"))

            """,
                }
        
        

    selected_preprocessing_query = st.selectbox("Preprocessing", list(query_preprocessing.keys()))
    coldspray_checkbox = st.checkbox("Cold Spray Details", value=False)
    selected_characterization_query = st.selectbox("Characterization", list(query_characterization.keys()))
    selected_result_query = st.selectbox("Results", ["None", "Microstructure", "Mechanical Properties"])
    if selected_result_query != "None":
        if selected_result_query == "Microstructure" or "Mechanical Properties":
            custom_results = st.text_input("Enter Result keyword:")
            query_results = {"None":"""""",
            "Microstructure":f"""
            
                ?paper a cs:ColdSprayPaper ;
                    cs:hasResult ?result.
                ?result cs:hasMicrostructureResult ?microstructure .
                ?microstructure cs:featureDescription ?featureDescription .
                ?mechanicalProperty cs:featureValue ?featureValue.
                ?mechanicalProperty cs:featureUnit ?featureUnit.
      
                FILTER (REGEX(STR(?featureDescription), "{custom_results}", "i"))
    
                        """,
    
                    "Mechanical Properties":f"""
            
                ?paper a cs:ColdSprayPaper ;
                    cs:hasResult ?result.
                ?result cs:hasMechanicalProperty ?mechanicalProperty .
                ?mechanicalProperty cs:propertyName ?propertyName .
                ?mechanicalProperty cs:propertyValue ?propertyValue.
                ?mechanicalProperty cs:propertyUnit ?propertyUnit.
      
                FILTER (REGEX(STR(?propertyName), "{custom_results}", "i"))
    
                        """,
    
    
    
                }

            
        #st.write(query_results[selected_result_query])
        

    

    if query_preprocessing[selected_preprocessing_query] != """""":
        prologue_text = prologue_text + "?preprocessingMethod " 

    if coldspray_checkbox:
        prologue_text = prologue_text + "?carrierGas " + "?gasPressure " + "?nozzleTemperature " + "?standOffDistance "
        coldspray_text = """?paper cs:hasColdSprayProcess ?process . 
  ?process cs:carrierGas ?carrierGas .
  ?process cs:gasPressure ?gasPressure .
  ?process cs:nozzleTemperature ?nozzleTemperature .
  ?process cs:standOffDistance ?standOffDistance ."""
        
    if query_characterization[selected_characterization_query] != """""":
        prologue_text = prologue_text + "?characterizationMethod " 

    #if query_results[selected_result_query] != """""":
    #    prologue_text = prologue_text + "?propertyName " + "?propertyValue " + "?propertyUnit" 

    if selected_result_query != "None":
        if selected_result_query == "Mechanical Properties":
            prologue_text = prologue_text + "?propertyName " + "?propertyValue " + "?propertyUnit"

        if selected_result_query == "Microstructure":
            prologue_text = prologue_text + "?featureDescription " + "?featureValue " + "?featureUnit"


    title_text = """?paper a cs:ColdSprayPaper ;
         cs:hasMetadata ?metadata.
  ?metadata cs:hasTitle ?title ."""
    query_text = prologue_text + "\n WHERE {" + title_text + query_materials[selected_materials_query] + query_preprocessing[selected_preprocessing_query] + coldspray_text + query_characterization[selected_characterization_query] + query_results[selected_result_query] +  "}"

    with st.expander("SPARQL Query"):
        st.code(query_text, language="sparql")

    if st.button("Run Query"):
        df = run_query(g, query_text)
        st.dataframe(df)

    st.subheader("Query")
    custom_query = st.text_area("Enter your SPARQL Query here", height=200)
    if st.button("Run Custom Query"):
        try:
            df = run_query(g, custom_query)
            st.dataframe(df)
        except Exception as e:
            st.error(f"Query failed: {e}")
