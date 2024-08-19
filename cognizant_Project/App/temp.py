import pandas as pd
def read_files():
    customers = pd.read_csv("/Users/ashwiniyadav/Downloads/cust_segmented_p2(pp).csv")
    customers = customers[["CustomerID","Age_og","Income_og","Cibil_Score_og","RFM_Score_og","Prev_Product_og","Cluster_ID"]]
    products = pd.read_csv("/Users/ashwiniyadav/Downloads/Products.csv")
    print(customers.columns)
    return customers,products

def get_customers(product_name,customers,product_data):
  # Find the clusters that have this curr_product
  clusters = customers[customers.Prev_Product_og == product_name].Cluster_ID.unique()
  prod_index = customers[customers.Prev_Product_og == product_name].index

  # Find how many times the curr_product has appeared in those clusters
  cluster_curr_product = customers.loc[:,["Cluster_ID","Prev_Product_og"]]
  eligibles = []
  mapping = {cluster:0 for cluster in clusters} #cluster: count of curr_product_name that has this cluster
  for index in prod_index:
    cluster_no = cluster_curr_product.iloc[index]["Cluster_ID"]
    mapping[cluster_no] += 1
    eligibles.append(index)
  print(mapping)

  # find the cluster that has this curr_product max number of times
  best_cluster = sorted(mapping.items(),key=lambda pair:pair[1],reverse=True)[0][0]

  # Find the customers that belong to this cluster and aren't using this curr_product
  target_inds = customers[((customers.Cluster_ID == best_cluster) & (customers.Prev_Product_og!=product_name))].index
  return customers.iloc[list(filter(lambda index: is_eligible(index,product_name,product_data),target_inds))]

# Filter Recommendations based on eligibility criteria in products table
def is_eligible(index,product,customers):
  min_age, max_age, income,cibil = product[product.Product_Type==product][["Min Age","Max Age","Income","Cibil_Score"]].iloc[0]
  cust_age,cust_inc,cust_cibil = customers.iloc[index][["Age_og","Income_og","Cibil_Score_og"]]

  if cust_age >= min_age and cust_age <= max_age and cust_inc >= income and cust_cibil >= cibil:
    return True
  else:
    return False

def recommend(product_name,customers,products_data):
    targets = get_customers(product_name,customers,products_data)
    targets.iloc[:,:].rename(columns={"Age_og":"Age","Income_og":"Income","Cibil_Score_og":"Cibil_Score","RFM_Score_og":"RFM_Score","Prev_Product_og":"Prev_Product"},inplace=True)
    return targets

import google.generativeai as genai
#he ekdach run karaycha ahe
def setup_genai():
    api = "AIzaSyAISyCQdC9CQlA910QA_3JLhONfqv90O18"

    genai.configure(api_key = api)
    model = genai.GenerativeModel('gemini-1.5-flash',system_instruction="You are sales team lead in bank")
    return model

def generate(product_name,cust_data,target_list,model_gemini,customers):
    hot_lead_id = targets.CustomerID.iloc[0]
    print(hot_lead_id)

    customer = customers[customers.CustomerID == hot_lead_id]
    recommendation = product_name
    prompt = f"""
            Given this customer profile (Age: {customer.Age_og.iloc[0]} yrs, Cibil Score: {customer.Cibil_Score_og.iloc[0]},
            RFM Score: {customer.RFM_Score_og.iloc[0]}, Previous Product: {customer.Prev_Product_og.iloc[0]})
            State why {recommendation} would be good recommendation for this customer.
            Answer in tabular format with following columns:
            'Parameter' - (Strength Features's Value),'Strengths' - (Why would customer be good fit for the product),
            'Benefit of {recommendation}', 'Recommendations', and 'Important Considerations'
            Just include bullet points with only limited keywords; no explanations.
          """

    response = model.generate_content(prompt)

    # display(Markdown((response.text)))
    return response

if __name__ == "__main__":
    customer_data,product_data = read_files()
    model = setup_genai()
    product = "Saving Account"
    targets = recommend(product,customer_data,product_data)
    result = generate(product,customer_data,targets,model)
