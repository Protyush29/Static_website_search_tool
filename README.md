# Static_website_search_tool
Search tool for a website , given a json details regarding every page. Elasticsearch used for implementation as a dependency. Hence it will be necessary to install it additionally. The steps below provides the complete process. For more info refer to https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-elasticsearch-on-ubuntu-20-04 .

#Installation\
Create a new conda environment and launch the app by following steps below:\

conda create -n new_env python=3\
conda activate new_env\

curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -\
echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list\
sudo apt update\
sudo apt install elasticsearch\

pip install -r requirements.txt\

sudo systemctl start elasticsearch\
flask --app app run


The server will be launched on http://127.0.0.1:5000  , open a browser to this address.

