FROM goropikari/dmoj-site

# TeCが含まれた言語リストをコピー
COPY language_ex.json /home/ubuntu/site/judge/fixtures/

# TeC用サンプル問題が含まれた初期データをコピー
COPY demo_ex.json /home/ubuntu/site/judge/fixtures/

# entrypoint.shを変更
COPY entrypoint.sh ./

CMD bash entrypoint.sh
