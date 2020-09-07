# t3_segmentation

pip install virtualenv
virtualenv venvt

source venv/Scripts/activate
pip install -r requirements.txt
pip install ipykernel
python -m ipykernel install --user --name=venvt
jupyter notebook
