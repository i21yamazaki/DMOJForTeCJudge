from dmoj.executors.compiled_executor import CompiledExecutor

from dmoj.util.ansi import print_ansi
from dmoj.utils.error import print_protection_fault
from dmoj.utils.unicode import utf8bytes

import os
import subprocess
import sys
import traceback

from typing import List, Optional


# CompiledExecutorをベースとする（アセンブルのため）
class Executor(CompiledExecutor):
    # ファイルの拡張子
    ext: str = "t7"
    # アセンブラ
    assembler: str = "tasm"
    # シミュレータ
    simulator: str = "tec"
    # テストプログラムの名前
    test_name: str = "test"
    # テストプログラム
    test_program: str = """
SIOD    EQU     02H     ; シリアルIOデータのIOアドレス
SIOS    EQU     03H     ; シリアルIO状態のIOアドレス
READ    EQU     0F6H    ; G0に1バイト入力（IPL内）

START
        LD      SP, #0DCH   ; スタックポインタ設定
LOOP
        CALL    READ        ; G0に1バイト入力
        CMP     G0, #0      ; G0が0なら
        JZ      END         ; ENDへ
        CALL    WRITE       ; 1バイト出力
        JMP     LOOP        ; LOOPへ
END
        HALT                ; 終了

WRITE
        IN      G1, SIOS    ; 状態を読んでG1に入れる
        AND     G1, #80H    ; MSBが0なら
        JZ      WRITE       ; ループで待機
        OUT     G0, SIOD    ; G0のデータを書き込み
        RET                 ; 戻る
"""

    def __init__(self, problem_id, source_code, dest_dir=None, hints=None, unbuffered=False, **kwargs):
        super().__init__(problem_id, source_code, dest_dir, hints, unbuffered, **kwargs)

    # 実行可能ファイルを取得する。
    def get_executable(self) -> str:
        simulator = self.get_simulator()
        assert simulator is not None
        return simulator

    # 初期化（起動時のテスト実行）を行う。
    @classmethod
    def initialize(cls) -> bool:
        assembler = cls.get_assembler()
        simulator = cls.get_simulator()
        if assembler is None:
            print(f"assembler was not found.")
            return False
        if simulator is None:
            print(f"simulator was not found.")
            return False
        if not os.path.isfile(assembler):
            print(f"assembler: {assembler} is not a file.")
            return False
        if not os.path.isfile(simulator):
            print(f"simulator: {simulator} is not a file.")
            return False
        if cls.test_program is None:
            return True
        try:
            executor = cls(cls.test_name, utf8bytes(cls.test_program))
            proc = executor.launch(
                time=cls.test_time, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            input_message = b"$RUN\n$SERIAL \"Hello, World.\", 0\n"
            output_message = b"Hello, World."
            stdout, stderr = proc.communicate(input_message)
            if proc.is_tle:
                print_ansi("#ansi[Time Limit Exceeded](red|bold)")
                return False
            if proc.is_mle:
                print_ansi("#ansi[Memory Limit Exceeded](red|bold)")
                return False
            res = stdout.strip() == output_message and not stderr
            usage = f"[{proc.execution_time:.3f}s, {proc.max_memory} KB]"
            print_ansi(
                f"{['#ansi[Failed](red|bold)', '#ansi[Success](green|bold)'][res]} {usage:<19}", end=" ")
            print_ansi(", ".join(
                [f"#ansi[{runtime}](cyan|bold) {'.'.join(map(str, version))}" for runtime, version in cls.get_runtime_versions()]))
            if stderr:
                print(stderr, file=sys.stderr)
            if proc.protection_fault:
                print_protection_fault(proc.protection_fault)
            return res
        except Exception:
            print_ansi("#ansi[Failed](red|bold)")
            traceback.print_exc()
            return False

    # アセンブラのパスを取得する。
    @classmethod
    def get_assembler(cls) -> Optional[str]:
        return cls.runtime_dict.get(cls.assembler)

    # シミュレータのパスを取得する。
    @classmethod
    def get_simulator(cls) -> Optional[str]:
        return cls.runtime_dict.get(cls.simulator)

    # コンパイラ（アセンブラ）引数を取得する。
    def get_compile_args(self) -> List[str]:
        assembler = self.get_assembler()
        assert assembler is not None
        assert self._code is not None
        return [assembler, self._code]

    # シミュレーション実行用のコマンドライン文字列を取得する。
    def get_cmdline(self, **kwargs) -> List[str]:
        simulator = self.get_simulator()
        assert simulator is not None
        return [simulator, f"{self.get_compiled_file()}.bin", f"{self.get_compiled_file()}.nt"]

    # ランタイムバージョンを取得する。
    @classmethod
    def get_runtime_versions(cls):
        return [("TeC", (1, 0, 0))]
