FROM goropikari/dmoj-site

# TeCが含まれた言語リストをコピー
COPY language_ex.json /home/ubuntu/site/judge/fixtures/

# TeC用サンプル問題が含まれた初期データをコピー
COPY demo_ex.json /home/ubuntu/site/judge/fixtures/

# TeCが含まれた言語リストを参照するように変更
RUN sed -i 's/language_all/language_ex/g' entrypoint.sh

# TeC用サンプル問題が含まれた初期データを参照するように変更
RUN sed -i 's/demo/demo_ex/g' entrypoint.sh

CMD bash entrypoint.sh
