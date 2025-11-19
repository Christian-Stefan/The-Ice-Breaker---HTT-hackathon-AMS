# Github Workflow

To keep work streamlined, accessible and to reduce risk of data loss, follow these recommendations before any action:

1. Short commentary format for updates/features/bug fixes
   - Use this required short-comment template for commits, PR descriptions and issue summaries:
     [Type] (Location): Short description. [Status]
     - Type: Fix | Feat | Docs | Refactor | Chore | Test
     - Location: folder, file path or branch (e.g. backend/api, ui/login, branch:feature/x)
     - Status: WIP | tested | not tested | reviewed
   - Examples:
     - Fix (backend/api): handle null user in login endpoint. [tested]
     - Feat (ui/login): add remember-me checkbox. [WIP]
     - Docs (README): clarify workflow examples. [not tested]

2. Local clones & backups
   - Keep a current local clone and push changes frequently.
   - Do not rely solely on GitHub as a single backup — keep local and (if needed) external backups.
  
# Prompt Engineering
Outline of expectations for input and output in each use case. 

## Sustainability Check from Clothing Label
**Expected input:**
- Image with clothing label reasonably visible; inform user if image cannot be used?

**Expected output:** 
- Evaluation of item on certain metrics
- Potential key metrics to check:
    - Carbon footprint 
    - Material composition
        - Consequences of materials
    - Country of origin
    - Durability (average)
- Final decision/advice 
- Give short suggestion for how to make best use of the clothes (3 bullet points)
- Advice is negative $\Rightarrow$ ask to provide alternatives; this leads into next use case
- No hallucination, if information is not available then simply say so
- Provide list of sources used 

### Prompt Building
- System: "You are a helpful expert in sustainable fashion practices. You have profound knowledge of the fast fashion industry. You will be providing advise to consumers on their clothing purchases."
- Content: "Consider the label in the image provided. It belongs to a " + clothing_item + ". From all available information determine the following metrics for the item of clothing to which this label belongs: carbon footprint (in CO2 equivalents), material composition, country of origin, durability. Make sure to format the output as a JSON as follows in the example below:

{
    "carbon_footprint" : "10 CO2e",
    "material_composition" : [{"material_name" : "acryllic", "environmental_consequence" : "Microplastic Pollution: Like other synthetic fabrics, acrylic releases microplastic fibers every time the garment is washed, contributing significantly to water pollution and environmental harm."}, {"material_name" : "polyester", "environmental_consequence" : "Non-Biodegradable and Petrochemical Base: Polyester is made from petroleum (a fossil fuel), meaning its production is highly energy-intensive and contributes to greenhouse gas emissions. As a plastic, it is not biodegradable and will persist in landfills for hundreds of years."}],
    "country_origin" : "China",
    "expected_durability" : "5 years",
    "final_decision" : false
}

 For each harmful material explain the environmental consequences in at most 50 words. Based on your analysis of the previous metrics give a final yes or no decision on whether the clothing is environmentally sustainable. Finally, in three bullet points suggest how the user can make more sustainable decisions for their existing item of clothing." 
