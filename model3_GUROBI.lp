\ Model ex3-CorteDeChapasMetalicas
\ LP format - for model browsing. Use MPS format to capture full model detail.
\ Signature: 0xcb900c8fe5e6309f
Minimize
  matriz[1] + 2 matriz[2] + 3 matriz[3] + 2 matriz[4]
Subject To
 corte_medio: 8 matriz[1] + 4 matriz[2] + 2 matriz[3] >= 500
 corte_grande: matriz[2] + 2 matriz[3] + 3 matriz[4] >= 350
Bounds
Generals
 matriz[1] matriz[2] matriz[3] matriz[4]
End
