# Dados Relativos a filial 1.
pedidos1 =  [0.0356,0.0904,0.1380,0.1400,0.1224,0.1292,0.0952,0.0820,0.0560,0.0496,0.0324,0.0216, 0.0076];
encomendas1 = [0.0448,0.1632,0.2220,0.2092,0.1620,0.1056,0.0556,0.0236,0.0100,0.0036,0.0000,0.0000,0.0004];

# Dados Relativos a filial 2.
pedidos2  = [0.0612,0.1204,0.1476,0.1228,0.1080,0.1100,0.0788,0.0776,0.0576,0.0516,0.0328,0.0236,0.0080];
encomendas2 = [0.0192,0.0848,0.1540,0.1956,0.2040,0.1528,0.0884,0.0556,0.0284,0.0100,0.0040,0.0024,0.0008];

# Calcula probabilidade associada a passar do estado i para j, sem transbordo.
function val = p(i,j,C,pedidos,encomendas)
  val = 0;
  
  for ex = max(0,j-i):(j-1)
    val += pedidos(ex + (i - j) + 1) * encomendas(ex + 1);
  endfor
  
  for p = i:C
    val += pedidos(p + 1)*encomendas(j + 1);
  endfor
endfunction

# Calcula probabilidade de acontecer transbordo partindo de i.
function val = phi(i,C,pedidos,encomendas)
  val = 0;

  for k = 0:(i - 1)
    for w = 1:(i - k)
      val += pedidos(k + 1) * encomendas(C-i+w+k+1);
    endfor
  endfor
endfunction

function val = buildTransitionMatrix(C,pedidos,encomendas)
  val = zeros(C,C);
  
  for i = 0:C
    for j = 0:C
      val(i + 1,j + 1) = p(i,j,C,pedidos,encomendas);
    endfor
    
    val(i + 1,C + 1) += phi(i,C,pedidos,encomendas);
    
  endfor
endfunction


function val = total(i,C,pedidos, encomendas)
  val = phi(i,C,pedidos,encomendas);
  
  printf("phi is %f\n", val);
  
  for j = 0:C
    x = p(i,j,C,pedidos,encomendas);
    
    printf("j = %d, x = %f\n", j, x);
    
    val += x;
    
  endfor
endfunction
