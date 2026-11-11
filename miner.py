nodes=['202949', '282455', '248143', '198948', '194947', '218370']
exec("import hashlib\ntarget='00000'\nbase='Aperture_Genesis_Block_'\nnonce=0\nwhile True:\n h=hashlib.sha256((base+str(nonce)).encode()).hexdigest()\n if h.startswith(target): break\n nonce+=1\nprint(f'Collision_Found: Nonce={nonce} | Hash={h}')")
