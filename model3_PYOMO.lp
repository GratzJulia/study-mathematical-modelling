\* Source Pyomo model name=ex3-CorteDeChapasMetalicas *\

min 
obj:
+1 matriz(1)
+2 matriz(2)
+3 matriz(3)
+2 matriz(4)

s.t.

c_l_corte(medio)_:
+8 matriz(1)
+4 matriz(2)
+2 matriz(3)
>= 500

c_l_corte(grande)_:
+1 matriz(2)
+2 matriz(3)
+3 matriz(4)
>= 350

bounds
   0 <= matriz(1) <= +inf
   0 <= matriz(2) <= +inf
   0 <= matriz(3) <= +inf
   0 <= matriz(4) <= +inf
general
  matriz(1)
  matriz(2)
  matriz(3)
  matriz(4)
end
