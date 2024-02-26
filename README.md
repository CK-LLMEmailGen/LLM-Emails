# LLM-Emails

# Deliverables by the end of March.

- Requirements & Process Flow:
	- Application Interface: An interface by which the customer can interact with.
	- Crunchbase: getting the companies data into the interface by filtering:
		- Getting JSON from Crunchbase based on customer-preferences such as:
			- Company size
			- Domain(s) of operation.
			- Personal details of C-level execs (CTO, CMO, etc..)
			- Based out of (location).
			- Series of funding (if it's a startup), etc...
		- Details of the social media profiles (main focus on LinkedIN) of the execs is taken.
	- LinkedIN: Using the linkedin profile urls of the execs, the following should be extracted:
		- Name.
		- Current position.
		- Location
		- Previous Experience.
		- Education, etc...
	- Knowledge Graph and database:
		- Using all of the data collected above, a knowledge graph should be shown in the Application.
   		- The details should be stored in neo4j AuraDB.
	- Zoho CRM:
		- Using the personal details of the execs, leads should be created.
		- The mail context from LLM is used to send an email to the lead.
		- Based on the reply, the conversation is taken forward.
		- Workflow is automated to continue the conversation (with required permissions from employees, and monitoring).
		- If lead is interested, then move onto negotiations for:
			- Product requirements.
			- Pricing
			- Support, etc..
	- LLM, embeddings and vector storage:
		- The context extracted above should be stored in a database and then embeddings created.
		- The model embeddings are also to be taken.
		- A framework (like langchain) is to be used to build this RAG application and knowledge graph.
		- The LLM uses this context and then creates a hyper-personalized mail context.

<br></br>
<br></br>

- Products required (all are paid):
	- [Crunchbase](https://www.crunchbase.com/): for getting company and execs' personal data.
	- [Zoho CRM](https://www.zoho.com/en-in/crm/): A CRM to manage marketing, sales and mail conversation with the leads.
	- [LinkedPro](https://marketplace.zoho.com/app/crm/linked-pro-for-zoho-crm): An extension to scrape, extract and obtain LinkedIN profile data of the execs and populate as leads in ZOHO.
	- [OpenAI](https://openai.com/product) / [Gemini](https://makersuite.google.com/app/prompts/new_freeform) (for LLM).
	- Costs for the products (with upfront investment). Link [Pricing details of various Softwares](https://docs.google.com/spreadsheets/d/1saKLeNFeRGcq6NwnVS3dCYguLO_rVlZJBBhoL9QKHDk/edit#gid=0).
- Product that isn't paid:
	- [AuraDB](https://neo4j.com/pricing/): for storing and managing neo4j graph database in the cloud.
- Products that are optional to be used:
	- Crunchbase Databoost and apptopia (even more company data) [link](https://about.crunchbase.com/data-boost/).

<br></br>
<br></br>

- Further questions:
	- Should LLM-generated emails be extended for logistics, inventory and financials?
	- Should the mails be monitored with the use of a email-marketing, analytics tool such as Mailchimp?

