```
git clone https://github.com/maximedrn/opensea-automatic-bulk-upload-and-sale.git
virtualenv -p python3 venv
. venv/bin/activate
pip install -r opensea-automatic-bulk-upload-and-sale/requirements.txt

mkdir assets data
```

Put files into images dir, with jpg extension

```
python generate_upload_list.py --output data/test.json --source-dir images/
python opensea-automatic-bulk-upload-and-sale/main.py
```
