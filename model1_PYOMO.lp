\* Source Pyomo model name=ex1-TransporteDeProdutos *\

min 
obj:
+110 qtd_viagens_com(A)
+75 qtd_viagens_com(B)

s.t.

c_l_capacidade(Refrigerado)_:
+20 qtd_viagens_com(A)
+20 qtd_viagens_com(B)
>= 160

c_l_capacidade(N_o_Refrigerado)_:
+30 qtd_viagens_com(A)
+10 qtd_viagens_com(B)
>= 120

c_l_regra_B_:
+1 qtd_viagens_com(B)
>= 4

bounds
   0 <= qtd_viagens_com(A) <= +inf
   0 <= qtd_viagens_com(B) <= +inf
general
  qtd_viagens_com(A)
  qtd_viagens_com(B)
end
