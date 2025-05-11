# 純網站版

## 環境安裝

* python

## 套件安裝

```sh
pip install -r ./requirements.txt
```

## API key 設定

在根目錄創一個檔案叫 `.env`

```env
GOOGLE_API_KEY="YOUR_API_KEY"
```

把它換成你的 API key

目錄結構應該會長這樣

```text
MyGo_Flipper/
├── .env
├── .gitignore
├── README.md
├── app.py
├── esp32_control.py
├── picsort.py
├── requirements.txt
├── words.json
├── static/
│   └── pics/
└── templates/
```


## 執行

```sh
python app.py
```
