\ Model PLFC2N
\ LP format - for model browsing. Use MPS format to capture full model detail.
\ Signature: 0xff1abbe13233ac67
Minimize
  43 transp_fabrica_deposito[0,0] + 42 transp_fabrica_deposito[0,1]
   + 41 transp_fabrica_deposito[1,0] + 35 transp_fabrica_deposito[1,1]
   + 60 transp_deposito_cliente[0,0] + 64 transp_deposito_cliente[0,1]
   + 63 transp_deposito_cliente[0,2] + 62 transp_deposito_cliente[0,3]
   + 61 transp_deposito_cliente[0,4] + 57 transp_deposito_cliente[1,0]
   + 58 transp_deposito_cliente[1,1] + 59 transp_deposito_cliente[1,2]
   + 57 transp_deposito_cliente[1,3] + 62 transp_deposito_cliente[1,4]
   + 27022 abertura_fabrica[0] + 29545 abertura_fabrica[1]
   + 15000 abertura_deposito[0] + 12000 abertura_deposito[1]
Subject To
 demanda_cliente_0: transp_deposito_cliente[0,0]
   + transp_deposito_cliente[1,0] = 11
 demanda_cliente_1: transp_deposito_cliente[0,1]
   + transp_deposito_cliente[1,1] = 18
 demanda_cliente_2: transp_deposito_cliente[0,2]
   + transp_deposito_cliente[1,2] = 15
 demanda_cliente_3: transp_deposito_cliente[0,3]
   + transp_deposito_cliente[1,3] = 15
 demanda_cliente_4: transp_deposito_cliente[0,4]
   + transp_deposito_cliente[1,4] = 12
 fluxo_deposito_0: transp_fabrica_deposito[0,0]
   + transp_fabrica_deposito[1,0] - transp_deposito_cliente[0,0]
   - transp_deposito_cliente[0,1] - transp_deposito_cliente[0,2]
   - transp_deposito_cliente[0,3] - transp_deposito_cliente[0,4] >= 0
 fluxo_deposito_1: transp_fabrica_deposito[0,1]
   + transp_fabrica_deposito[1,1] - transp_deposito_cliente[1,0]
   - transp_deposito_cliente[1,1] - transp_deposito_cliente[1,2]
   - transp_deposito_cliente[1,3] - transp_deposito_cliente[1,4] >= 0
 capacidade_fabrica_0: transp_fabrica_deposito[0,0]
   + transp_fabrica_deposito[0,1] - 298 abertura_fabrica[0] <= 0
 capacidade_fabrica_1: transp_fabrica_deposito[1,0]
   + transp_fabrica_deposito[1,1] - 274 abertura_fabrica[1] <= 0
 capacidade_deposito_0: transp_deposito_cliente[0,0]
   + transp_deposito_cliente[0,1] + transp_deposito_cliente[0,2]
   + transp_deposito_cliente[0,3] + transp_deposito_cliente[0,4]
   - 500 abertura_deposito[0] <= 0
 capacidade_deposito_1: transp_deposito_cliente[1,0]
   + transp_deposito_cliente[1,1] + transp_deposito_cliente[1,2]
   + transp_deposito_cliente[1,3] + transp_deposito_cliente[1,4]
   - 450 abertura_deposito[1] <= 0
Bounds
Binaries
 abertura_fabrica[0] abertura_fabrica[1] abertura_deposito[0]
 abertura_deposito[1]
End
