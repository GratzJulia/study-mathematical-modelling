\ Model ex4-FabricaAutomovel
\ LP format - for model browsing. Use MPS format to capture full model detail.
\ Signature: 0x757733db4eaacb04
Minimize
  3 qtd_carros_enviados[1,3] + 4 qtd_carros_enviados[1,4]
   + 0 qtd_carros_enviados[1,5] + 0 qtd_carros_enviados[1,6]
   + 0 qtd_carros_enviados[1,7] + 2 qtd_carros_enviados[2,3]
   + 5 qtd_carros_enviados[2,4] + 0 qtd_carros_enviados[2,5]
   + 0 qtd_carros_enviados[2,6] + 0 qtd_carros_enviados[2,7]
   + 0 qtd_carros_enviados[3,3] + 7 qtd_carros_enviados[3,4]
   + 8 qtd_carros_enviados[3,5] + 6 qtd_carros_enviados[3,6]
   + 0 qtd_carros_enviados[3,7] + 0 qtd_carros_enviados[4,3]
   + 0 qtd_carros_enviados[4,4] + 0 qtd_carros_enviados[4,5]
   + 4 qtd_carros_enviados[4,6] + 9 qtd_carros_enviados[4,7]
   + 0 qtd_carros_enviados[5,3] + 0 qtd_carros_enviados[5,4]
   + 0 qtd_carros_enviados[5,5] + 5 qtd_carros_enviados[5,6]
   + 0 qtd_carros_enviados[5,7] + 0 qtd_carros_enviados[6,3]
   + 0 qtd_carros_enviados[6,4] + 0 qtd_carros_enviados[6,5]
   + 0 qtd_carros_enviados[6,6] + 3 qtd_carros_enviados[6,7]
Subject To
 rest_no1: qtd_carros_enviados[1,3] + qtd_carros_enviados[1,4] = 1000
 rest_no2: qtd_carros_enviados[2,3] + qtd_carros_enviados[2,4] = 1200
 rest_no3: - qtd_carros_enviados[1,3] - qtd_carros_enviados[2,3]
   + qtd_carros_enviados[3,4] + qtd_carros_enviados[3,5]
   + qtd_carros_enviados[3,6] = 0
 rest_no4: - qtd_carros_enviados[1,4] - qtd_carros_enviados[2,4]
   - qtd_carros_enviados[3,4] + qtd_carros_enviados[4,6]
   + qtd_carros_enviados[4,7] = 0
 rest_no5: - qtd_carros_enviados[3,5] + qtd_carros_enviados[5,6] = -800
 rest_no6: - qtd_carros_enviados[3,6] - qtd_carros_enviados[4,6]
   - qtd_carros_enviados[5,6] + qtd_carros_enviados[6,7] = -900
 rest_no7: qtd_carros_enviados[4,7] + qtd_carros_enviados[6,7] = 500
Bounds
Generals
 qtd_carros_enviados[1,3] qtd_carros_enviados[1,4] qtd_carros_enviados[1,5]
 qtd_carros_enviados[1,6] qtd_carros_enviados[1,7] qtd_carros_enviados[2,3]
 qtd_carros_enviados[2,4] qtd_carros_enviados[2,5] qtd_carros_enviados[2,6]
 qtd_carros_enviados[2,7] qtd_carros_enviados[3,3] qtd_carros_enviados[3,4]
 qtd_carros_enviados[3,5] qtd_carros_enviados[3,6] qtd_carros_enviados[3,7]
 qtd_carros_enviados[4,3] qtd_carros_enviados[4,4] qtd_carros_enviados[4,5]
 qtd_carros_enviados[4,6] qtd_carros_enviados[4,7] qtd_carros_enviados[5,3]
 qtd_carros_enviados[5,4] qtd_carros_enviados[5,5] qtd_carros_enviados[5,6]
 qtd_carros_enviados[5,7] qtd_carros_enviados[6,3] qtd_carros_enviados[6,4]
 qtd_carros_enviados[6,5] qtd_carros_enviados[6,6] qtd_carros_enviados[6,7]
End
