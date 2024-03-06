# Kth-Group4-DM2586
![Result_step2](https://github.com/rickystanley76/Kth-Group4-DM2586/assets/1774630/0c0bb35b-8e1c-4583-a7ce-812105ee6432)
As a part of a course in Generative AI and Media and interactive design in KTH, we have developed this Multimodal RAG applicaation.
## The total architecture of the Application
![MM-RAG Arch](https://github.com/rickystanley76/Kth-Group4-DM2586/assets/1774630/aeaa0072-ce18-4e1b-a3c9-4efc08274476)
## Data
Some of the sample data are there in data/images folder, you can use your own data for this application.
## Weaviate database
you need to install weaviate database in your local machine using docker and the docker-compose.yml file.
for more info: https://weaviate.io/developers/weaviate/installation/docker-compose 
## Adding Data in the database
Make a env in your python, install the requirements.txt, run >python add_data_in_batch.py .
As you may have many images, so in the code we are inserting the 200 images at a time and embedd those. It may take time depending on the numbers of images.
## Running the application MM-RAG
in the env, run streamlit run app_with_vision_description.py .
To generate the description, you need to have Open AI API key.
You can have that from: https://platform.openai.com/ 

Without the Open AI API key the application will work but user can't get the generated description from the vision model. The text and image semantic search will work perfectly.


