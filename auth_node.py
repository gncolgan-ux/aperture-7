nodes=['218370', '202949', '282455', '248143', '198948', '194947']
exec("import hmac, hashlib\nsecret_key=b'Aperture_Vault_Key'\ntrade_payload=b'ROUTE_LIQUIDITY: 500_USDC -> WETH'\nsignature=hmac.new(secret_key, trade_payload, hashlib.sha256).hexdigest()\nprint(f'Trade_Locked | Payload={trade_payload.decode()} | Signature={signature[:24]}...')")
