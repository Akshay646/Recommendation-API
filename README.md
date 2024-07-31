# Recommendation-API
This API is built using Flask (Python) and provides news recommendations by searching into the News API. It leverages TF-IDF and cosine similarity algorithms to recommend articles based on provided keywords or sentences.

# **Recommendation API

#**IMPORTANT!!!!**
The functionalities of this API are demonstrated using a news database, with queries and requests tailored to this dataset. You can modify the endpoints and use cases to fit your specific requirements, while the core recommendation logic remains unchanged

#  **Overview**
This API is built using Flask (Python) and provides news recommendations by searching into the News API. It leverages TF-IDF and cosine similarity algorithms to recommend articles based on provided keywords or sentences.

# **Features**
Search news articles using keywords or sentences
Generate recommendations based on search results

# **Clone the repository:**
git clone https://github.com/yourusername/Recommendation-API.git

# **Install dependencies**: 
pip install -r requirements.txt

# **Run the server:** 
flask run

# **Endpoints**
**1. /api/news/search?q=<Insert-Your-Search-Query-Here>**
**2. /api/news/recommendations?q=<Insert-Your-Query-Here>**

# **Usage**
Access the API at http://localhost:5000
Use endpoints for searching and getting recommendations based on provided keywords or sentences.

# **Contributing**
Contributions are welcome! Please submit a pull request or open an issue for suggestions or improvements.
