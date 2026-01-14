FROM goropikari/dmoj-judger

# ユーザを root に変更
USER root

# TeCSimulatorForTCL を取得
RUN cd /root && \
    git clone https://github.com/i21yamazaki/TeCSimulatorForTCL tec

# fmt を取得
RUN cd /root/tec && \
    git clone https://github.com/fmtlib/fmt

# std format の代わりに fmt::formatを参照するように変更
RUN cd /root/tec/src && \
    echo "#define FMT_HEADER_ONLY\n#include \"../fmt/include/fmt/format.h\"\nnamespace std {using fmt::format;}" > format.hpp && \
    sed -i 's/#include <format>/#include "format.hpp"/g' tasm.cpp && \
    sed -i 's/#include <format>/#include "format.hpp"/g' tec.cpp

# TeCSimulatorForTCL をビルド & インストール
RUN cd /root/tec && \
    make all && \
    make install

# TEC.py（Executor）をコピー
COPY TEC.py /root/judge-server/dmoj/executors/

# judge-server をビルド
RUN cd ~/judge-server && \ 
    python3 -m pip install -r requirements.txt && \
    python3 setup.py install

# ユーザを judge に戻す
USER judge

# wait until site server is active.
ENTRYPOINT sleep 20 && dmoj -c ~/problems/judge.yml ${SITE_HOST}
