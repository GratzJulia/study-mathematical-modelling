\ Model Carregamento_Navio
\ LP format - for model browsing. Use MPS format to capture full model detail.
\ Signature: 0x32575c036827d836
Maximize
  1e+07 x[Ouro,1-Proa] + 1e+07 x[Ouro,2-Centro] + 1e+07 x[Ouro,3-Popa]
   + 5e+06 x[Pedras_Preciosas,1-Proa] + 5e+06 x[Pedras_Preciosas,2-Centro]
   + 5e+06 x[Pedras_Preciosas,3-Popa]
Subject To
 disponibilidade_Ouro: x[Ouro,1-Proa] + x[Ouro,2-Centro] + x[Ouro,3-Popa]
   <= 5000
 disponibilidade_Pedras_Preciosas: x[Pedras_Preciosas,1-Proa]
   + x[Pedras_Preciosas,2-Centro] + x[Pedras_Preciosas,3-Popa] <= 2000
 limite_peso_1-Proa: x[Ouro,1-Proa] + x[Pedras_Preciosas,1-Proa] <= 2000
 limite_peso_2-Centro: x[Ouro,2-Centro] + x[Pedras_Preciosas,2-Centro]
   <= 3100
 limite_peso_3-Popa: x[Ouro,3-Popa] + x[Pedras_Preciosas,3-Popa] <= 1500
 limite_volume_1-Proa: 0.3571428571428572 x[Ouro,1-Proa]
   + 0.5555555555555556 x[Pedras_Preciosas,1-Proa] <= 1100
 limite_volume_2-Centro: 0.3571428571428572 x[Ouro,2-Centro]
   + 0.5555555555555556 x[Pedras_Preciosas,2-Centro] <= 1400
 limite_volume_3-Popa: 0.3571428571428572 x[Ouro,3-Popa]
   + 0.5555555555555556 x[Pedras_Preciosas,3-Popa] <= 600
 equilibrio_proa_centro: 3100 x[Ouro,1-Proa] - 2000 x[Ouro,2-Centro]
   + 3100 x[Pedras_Preciosas,1-Proa] - 2000 x[Pedras_Preciosas,2-Centro]
   = 0
 equilibrio_centro_popa: 1500 x[Ouro,2-Centro] - 3100 x[Ouro,3-Popa]
   + 1500 x[Pedras_Preciosas,2-Centro] - 3100 x[Pedras_Preciosas,3-Popa]
   = 0
Bounds
End
