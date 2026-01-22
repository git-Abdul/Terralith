from google import genai
from main import API_KEY

client = genai.Client(api_key=API_KEY)

uinput = input("Enter string: ")
response = client.models.generate_content(
    model="gemma-3-4b-it",
    contents=f'DO NOT USE BOLD TEXT ANYWHERE IN THE INPUT DO NOT USE ASTERIX TO DENOTE ANYTHING. You are an expert in biomes and sustainable architecture/renewable energy. USER INPUT IS: {uinput}, respond in the following structured format with clear section labels and bullet points. First, output ONLY the single closest matching biome name from this exact list ["brine","canyon","coastal_desert","desert","inland_coastal","marsh","mediterranean","montane_plateau","mountainous_alpine","plains","polar","rainforest","riverine","savannah","steppe","temperate_forest","temperate_oceanic","tundra","volcanic","windy_coastal"]. Then include these sections in order: Biome Characteristics (4–6 concise bullet points covering climate, terrain, vegetation, geology, and visual appearance), Sustainable Energy Resources (bullet points listing viable renewables such as solar, wind, hydro, geothermal, biomass with brief reasons tied to local geography and climate), Commercial & Residential Opportunities (bullet points describing realistic developments like eco-tourism, energy farms, off-grid housing, eco-villages aligned with renewables), and Cautions (bullet points highlighting key environmental, ecological, cultural, and practical constraints such as habitat protection, water scarcity, erosion, flooding risks, protected areas, or indigenous heritage). Do not add extra commentary outside these sections.',
)

print(response.text.partition("Cautions")[2])
