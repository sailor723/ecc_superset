import pandas as pd
from sqlalchemy import create_engine

# Sample data for edges (relationships)
relationships_data = {
    "source": [
        # Agriculture & Food Production
        "Agricultural Energy Use",
        "Agriculture",
        "Agriculture",
        "Agriculture",
        "Agriculture",
        "Agriculture Soils",
        "Rice Cultivation",
        "Food Processing",
        "Food Processing",
        "Food Storage",
        "Food Transportation",
        "Fertilizer Production",
        "Fertilizer Production",
        "Irrigation Systems",
        # Industrial processes
        "Air",
        "Aluminium Non-Ferrous Metals",
        "Aluminium Non-Ferrous Metals",
        "Iron and Steel",
        "Iron and Steel",
        "Cement",
        "Cement",
        "Glass Production",
        "Paper Production",
        "Paper Production",
        "Textile Manufacturing",
        "Electronics Manufacturing",
        "Electronics Manufacturing",
        "Plastic Production",
        "Plastic Production",
        # Energy sector
        "Coal Mining",
        "Coal Mining",
        "Oil and Gas Processing",
        "Oil and Gas Processing",
        "Natural Gas Leakage",
        "Power Plants",
        "Power Plants",
        "Nuclear Power",
        "Solar Power",
        "Wind Power",
        "Hydroelectric Power",
        "Geothermal Energy",
        "Biomass Burning",
        "Biomass Burning",
        # Land use & Forestry
        "Deforestation",
        "Forest Management",
        "Wetlands",
        "Wetlands",
        "Peatlands",
        "Urban Development",
        "Land Clearing",
        "Soil Erosion",
        # Waste Management
        "Landfills",
        "Landfills",
        "Wastewater Treatment",
        "Wastewater Treatment",
        "Waste Incineration",
        "Waste Incineration",
        "Composting",
        "Recycling Process",
        # Transport
        "Road Transport",
        "Rail Transport",
        "Marine Transport",
        "Air Transport",
        "Public Transportation",
        "Electric Vehicles",
        "Freight Transport",
        "Port Operations",
        # Buildings & Construction
        "Residential Buildings",
        "Commercial Buildings",
        "Industrial Buildings",
        "Construction Process",
        "Building Heating",
        "Building Cooling",
        "Building Lighting",
        "Building Demolition",
        # Chemical Industry
        "Chemical Processing",
        "Chemical Processing",
        "Pharmaceutical Production",
        "Petrochemical Industry",
        "Petrochemical Industry",
        "Solvent Use",
        "Paint Production",
        "Cleaning Products",
    ],
    "target": [
        # Agriculture connections
        "Carbon Dioxide",
        "Agriculture Soils",
        "Livestock and Manure",
        "Other Agriculture",
        "Rice Cultivation",
        "Nitrous Oxide",
        "Methane",
        "Carbon Dioxide",
        "Energy Consumption",
        "HFCs - PFCs",
        "Carbon Dioxide",
        "Nitrous Oxide",
        "Carbon Dioxide",
        "Energy Consumption",
        # Industrial connections
        "Carbon Dioxide",
        "Carbon Dioxide",
        "HFCs - PFCs",
        "Carbon Dioxide",
        "Methane",
        "Carbon Dioxide",
        "Particulate Matter",
        "Carbon Dioxide",
        "Carbon Dioxide",
        "Water Pollution",
        "Chemical Waste",
        "HFCs - PFCs",
        "Energy Consumption",
        "Chemical Waste",
        "Carbon Dioxide",
        # Energy connections
        "Methane",
        "Carbon Dioxide",
        "Carbon Dioxide",
        "Methane",
        "Methane",
        "Carbon Dioxide",
        "Sulfur Dioxide",
        "Nuclear Waste",
        "Energy Production",
        "Energy Production",
        "Energy Production",
        "Energy Production",
        "Carbon Dioxide",
        "Particulate Matter",
        # Land use connections
        "Carbon Dioxide",
        "Carbon Storage",
        "Methane",
        "Carbon Storage",
        "Carbon Dioxide",
        "Heat Island Effect",
        "Soil Degradation",
        "Carbon Release",
        # Waste connections
        "Methane",
        "Groundwater Pollution",
        "Methane",
        "Nitrous Oxide",
        "Carbon Dioxide",
        "Toxic Emissions",
        "Methane",
        "Energy Savings",
        # Transport connections
        "Carbon Dioxide",
        "Carbon Dioxide",
        "Carbon Dioxide",
        "Carbon Dioxide",
        "Emissions Reduction",
        "Clean Energy Usage",
        "Carbon Dioxide",
        "Air Pollution",
        # Building connections
        "Carbon Dioxide",
        "Carbon Dioxide",
        "Carbon Dioxide",
        "Particulate Matter",
        "Energy Consumption",
        "HFCs - PFCs",
        "Energy Consumption",
        "Waste Generation",
        # Chemical connections
        "Nitrous Oxide",
        "HFCs - PFCs",
        "Chemical Waste",
        "Carbon Dioxide",
        "Water Pollution",
        "VOC Emissions",
        "VOC Emissions",
        "Chemical Waste",
    ],
    "value": [
        # Agriculture values
        1.4,
        5.2,
        5.4,
        1.7,
        1.5,
        5.2,
        2.8,
        1.9,
        2.3,
        0.8,
        1.2,
        3.1,
        2.4,
        1.6,
        # Industrial values
        1.7,
        1.0,
        0.2,
        3.8,
        0.6,
        4.2,
        0.8,
        2.1,
        1.9,
        0.7,
        1.2,
        0.5,
        2.8,
        1.1,
        1.4,
        # Energy values
        2.8,
        1.9,
        3.5,
        1.2,
        2.4,
        6.7,
        1.8,
        0.0,
        0.0,
        0.0,
        0.1,
        0.2,
        2.9,
        0.8,
        # Land use values
        4.1,
        1.8,
        2.2,
        1.5,
        3.2,
        1.7,
        2.1,
        1.9,
        # Waste values
        3.4,
        0.9,
        2.1,
        1.2,
        1.8,
        0.7,
        0.4,
        0.3,
        # Transport values
        5.6,
        1.8,
        2.4,
        4.2,
        0.8,
        0.2,
        3.1,
        1.2,
        # Building values
        3.2,
        2.8,
        2.5,
        1.4,
        2.9,
        1.6,
        2.2,
        0.9,
        # Chemical values
        1.6,
        0.9,
        0.7,
        2.8,
        1.5,
        1.1,
        0.8,
        0.6,
    ],
}

# Create nodes data with more detailed categories
nodes = set(relationships_data["source"]).union(set(relationships_data["target"]))
nodes_data = {
    "id": list(nodes),
    "name": list(nodes),
    "category": [
        "Energy"
        if any(
            x in node
            for x in [
                "Energy",
                "Power",
                "Coal",
                "Oil",
                "Gas",
                "Nuclear",
                "Solar",
                "Wind",
                "Hydro",
                "Geothermal",
            ]
        )
        else "Agriculture"
        if any(
            x in node
            for x in [
                "Agriculture",
                "Rice",
                "Livestock",
                "Manure",
                "Food",
                "Fertilizer",
                "Irrigation",
            ]
        )
        else "Industry"
        if any(
            x in node
            for x in [
                "Industrial",
                "Steel",
                "Metals",
                "Cement",
                "Glass",
                "Paper",
                "Textile",
                "Electronics",
                "Plastic",
            ]
        )
        else "Transport"
        if any(
            x in node
            for x in ["Transport", "Vehicle", "Road", "Rail", "Marine", "Air", "Port"]
        )
        else "Buildings"
        if any(
            x in node
            for x in ["Building", "Construction", "Heating", "Cooling", "Lighting"]
        )
        else "Waste"
        if any(x in node for x in ["Waste", "Landfill", "Recycling", "Composting"])
        else "Chemical"
        if any(
            x in node
            for x in ["Chemical", "Pharmaceutical", "Petrochemical", "Solvent", "Paint"]
        )
        else "Land Use"
        if any(
            x in node
            for x in ["Forest", "Wetland", "Peatland", "Urban", "Soil", "Land"]
        )
        else "Emissions"
        if any(
            x in node
            for x in [
                "Carbon",
                "Methane",
                "Oxide",
                "HFCs",
                "PFCs",
                "Sulfur",
                "VOC",
                "Pollution",
                "Toxic",
                "Waste",
            ]
        )
        else "Other"
        for node in nodes
    ],
}

# Create DataFrames
nodes_df = pd.DataFrame(nodes_data)
relationships_df = pd.DataFrame(relationships_data)

# MySQL connection settings
mysql_settings = {
    "host": "172.17.0.2",
    "user": "root",
    "password": "root",
    "database": "superset",
}

# Create MySQL connection
engine = create_engine(
    f"mysql+mysqlconnector://{mysql_settings['user']}:{mysql_settings['password']}@{mysql_settings['host']}/{mysql_settings['database']}"
)

# Save to MySQL
nodes_df.to_sql("emissions_network_nodes", engine, if_exists="replace", index=False)
relationships_df.to_sql(
    "emissions_network_edges", engine, if_exists="replace", index=False
)

print("Data successfully loaded into MySQL!")
print(f"Created {len(nodes_df)} nodes and {len(relationships_df)} relationships")
print("\nCategories distribution:")
print(nodes_df["category"].value_counts())
