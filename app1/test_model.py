# test_model.py

import spacy

def test_model(model_path, test_text):
    # Load the trained model
    nlp = spacy.load(model_path)
    # Process the test text
    doc = nlp(test_text)
    # Print the entities recognized by the model
    for ent in doc.ents:
        # if ent.label_ in ("ORG", "PERSON"):
            print(f"{ent.text} ({ent.label_})")

if __name__ == "__main__":
    # Test the trained model
    
    test_text = """

     
    
# """

def fun():  
  a = []
  b = test_model("data_model", test_text)
  a.append(b)
  
  return a

fun()

# ------------------------------------------------------------------------------------------------------

# import spacy

# def test_model(model_path, test_text):
#     # Load the trained model
#     nlp = spacy.load(model_path)
#     # Process the test text
#     doc = nlp(test_text)

#     # Initialize variables to hold information for grouping
#     company_info = []
#     processed_companies = set()  # Track processed companies for uniqueness
#     other_entities = []

#     current_company = {
#         "Company": None,
#         "Designation": None,
#         "Start Date": None,
#         "End Date": None
#     }

#     # Iterate over recognized entities
#     for ent in doc.ents:
#         if ent.label_ == "ORG":
#             # Add the previous company if it hasn't been processed yet
#             if current_company["Company"] and current_company["Company"] not in processed_companies:
#                 company_info.append(current_company.copy())
#                 processed_companies.add(current_company["Company"])

#             # Start a new company entry
#             current_company = {
#                 "Company": ent.text,
#                 "Designation": None,
#                 "Start Date": None,
#                 "End Date": None
#             }
        
#         elif ent.label_ == "DESIGNATION":
#             current_company["Designation"] = ent.text

#         elif ent.label_ == "DATE":
#             if not current_company["Start Date"]:
#                 current_company["Start Date"] = ent.text
#             else:
#                 current_company["End Date"] = ent.text

#         else:
#             # Store other entities like PERSON, SKILL, etc.
#             other_entities.append({
#                 "Entity": ent.text,
#                 "Label": ent.label_
#             })

#     # Add the final company entry if it hasn't been processed
#     if current_company["Company"] and current_company["Company"] not in processed_companies:
#         company_info.append(current_company)
    
#     return company_info, other_entities

# def fun():
#     # Sample test text
#     test_text = """

#     """

#     # Get the results from the model
#     company_info, other_entities = test_model("team_model", test_text)
    
#     # Format company data for unique, structured output
#     unique_company_info = {frozenset(company.items()) for company in company_info}
#     # Convert back to a list of dictionaries for readability
#     unique_company_info = [dict(company) for company in unique_company_info]

#     # Output results
#     print("Job History:")
#     for company in unique_company_info:
#         print(f"Company: {company['Company']}")
#         print(f"Designation: {company.get('Designation', 'None')}")
#         print(f"Start Date: {company.get('Start Date', 'None')}")
#         print(f"End Date: {company.get('End Date', 'None')}\n")

#     print("Other Entities:")
#     for entity in other_entities:
#         print(f"{entity['Entity']} ({entity['Label']})")

#     return unique_company_info, other_entities

# # Run the integration function
# fun()

# ------------------------------------------------------------------------------------------------------