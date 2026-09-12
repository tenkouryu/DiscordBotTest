import base64
import hashlib
import hmac
import json
import os


"""
    標準ライブラリのみで動作する暗号化・復号化サービス。

    暗号化結果:
        Base64( nonce + ciphertext + tag )

    nonce:
        暗号化ごとに生成する32バイトの乱数

    ciphertext:
        HMAC-SHA256から生成したキーストリームとのXOR結果

    tag:
        HMAC-SHA256による改ざん検知用タグ
    
    author:Mikado Ohkouchi
"""
class crypto_service:
    NONCE_SIZE = 32
    KEY_SIZE = 32
    TAG_SIZE = 32

    def __init__(self, key_path: str):
        self.key = self._load_key(key_path)

    def _load_key(self, key_path: str) -> bytes:
        """JSONファイルから暗号化キーを読み込む。"""

        with open(key_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        key_string = config.get("encryption_key")

        if not key_string:
            raise ValueError("encryption_key が設定されていません。")

        try:
            key = base64.b64decode(key_string, validate=True)
        except Exception as e:
            raise ValueError("encryption_key はBase64形式で設定してください。") from e

        if len(key) != self.KEY_SIZE:
            raise ValueError("暗号化キーは32バイトである必要があります。")

        return key

    def _generate_keystream(self, nonce: bytes, length: int) -> bytes:
        """
        HMAC-SHA256を利用してキーストリームを生成する。
        """

        stream = bytearray()
        counter = 0

        while len(stream) < length:
            counter_bytes = counter.to_bytes(8, "big")

            block = hmac.new(
                self.key,
                nonce + counter_bytes,
                hashlib.sha256
            ).digest()

            stream.extend(block)
            counter += 1

        return bytes(stream[:length])

    def _xor_bytes(self, data: bytes, key_stream: bytes) -> bytes:
        """データとキーストリームをXORする。"""

        return bytes(
            a ^ b
            for a, b in zip(data, key_stream)
        )

    def encrypt(self, plaintext: str) -> str:
        """
        文字列を暗号化してBase64文字列を返す。
        """

        if not isinstance(plaintext, str):
            raise TypeError("plaintext は文字列で指定してください。")

        # UTF-8に変換
        plaintext_bytes = plaintext.encode("utf-8")

        # 暗号化ごとに異なるnonceを生成
        nonce = os.urandom(self.NONCE_SIZE)

        # キーストリームを生成
        keystream = self._generate_keystream(
            nonce,
            len(plaintext_bytes)
        )

        # XORで暗号化
        ciphertext = self._xor_bytes(
            plaintext_bytes,
            keystream
        )

        # 改ざん検知用タグを生成
        tag = hmac.new(
            self.key,
            nonce + ciphertext,
            hashlib.sha256
        ).digest()

        # nonce + ciphertext + tag を結合
        encrypted_data = nonce + ciphertext + tag

        # Base64で文字列化
        return base64.b64encode(encrypted_data).decode("ascii")

    def decrypt(self, encrypted_text: str) -> str:
        """
        Base64文字列を復号化して元の文字列を返す。
        """

        if not isinstance(encrypted_text, str):
            raise TypeError("encrypted_text は文字列で指定してください。")

        try:
            encrypted_data = base64.b64decode(
                encrypted_text,
                validate=True
            )
        except Exception as e:
            raise ValueError("暗号化文字列が不正です。") from e

        # 最低でも nonce + tag が必要
        if len(encrypted_data) < self.NONCE_SIZE + self.TAG_SIZE:
            raise ValueError("暗号化文字列が短すぎます。")

        # データを分割
        nonce = encrypted_data[:self.NONCE_SIZE]

        ciphertext = encrypted_data[
            self.NONCE_SIZE:-self.TAG_SIZE
        ]

        tag = encrypted_data[-self.TAG_SIZE:]

        # 改ざん検知
        expected_tag = hmac.new(
            self.key,
            nonce + ciphertext,
            hashlib.sha256
        ).digest()

        if not hmac.compare_digest(tag, expected_tag):
            raise ValueError(
                "暗号化文字列が改ざんされているか、"
                "暗号化キーが間違っています。"
            )

        # キーストリームを生成
        keystream = self._generate_keystream(
            nonce,
            len(ciphertext)
        )

        # XORで復号化
        plaintext_bytes = self._xor_bytes(
            ciphertext,
            keystream
        )

        # UTF-8に戻す
        try:
            return plaintext_bytes.decode("utf-8")
        except UnicodeDecodeError as e:
            raise ValueError("復号化されたデータが不正です。") from e