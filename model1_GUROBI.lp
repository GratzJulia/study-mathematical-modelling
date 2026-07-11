\ Model ex1-TransporteDeProdutos
\ LP format - for model browsing. Use MPS format to capture full model detail.
\ Signature: 0x294c6cf66b050404
Minimize
  110 qtd_viagens_com[A] + 75 qtd_viagens_com[B]
Subject To
 capacidade[0]: 20 qtd_viagens_com[A] + 20 qtd_viagens_com[B] >= 160
 capacidade[1]: 30 qtd_viagens_com[A] + 10 qtd_viagens_com[B] >= 120
 regra_B: qtd_viagens_com[B] >= 4
Bounds
Generals
 qtd_viagens_com[A] qtd_viagens_com[B]
End
