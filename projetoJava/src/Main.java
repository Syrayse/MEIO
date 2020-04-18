public class Main {
    public static int min(int a,int b)
    {
        if (a>b) return b;
        else return a;
    }
    public static void main(String[] args) {
        double [] pedidos1 =  {0.0356,0.0904,0.1380,0.1400,0.1224,0.1292,0.0952,0.0820,0.0560,0.0496,0.0324,0.0216, 0.0076};
        double [] encomendas1 = {0.0448,0.1632,0.2220,0.2092,0.1620,0.1056,0.0556,0.0236,0.0100,0.0036,0.0000,0.0000,0.0004};
        double [] pedidos2  = {0.0612,0.1204,0.1476,0.1228,0.1080,0.1100,0.0788,0.0776,0.0576,0.0516,0.0328,0.0236,0.0080};
        double [] encomendas2 = {0.0192,0.0848,0.1540,0.1956,0.2040,0.1528,0.0884,0.0556,0.0284,0.0100,0.0040,0.0024,0.0008};
        double [][][][] transicao = new double[13][13][13][13];
        int numCarrosI1,numCarrosF1,numCarrosI2,numCarrosF2;
        double p1=0.d,p2=0.d,total=0.d;
        System.out.println(p1 +" "+ p2);
        for (numCarrosI2=0;numCarrosI2<=12;numCarrosI2++) {
            for (numCarrosF2 = 0; numCarrosF2 <= 12; numCarrosF2++) {
                p2 = getP(pedidos2, encomendas2, numCarrosI2, numCarrosF2, p2);
                for (numCarrosI1 = 0; numCarrosI1 <= 12; numCarrosI1++) {
                    for (numCarrosF1 = 0; numCarrosF1 <= 12; numCarrosF1++) {
                        p1 = getP(pedidos1, encomendas1, numCarrosI1, numCarrosF1, p1);
                        transicao[numCarrosI1][numCarrosI2][numCarrosF1][numCarrosF2]=p1*p2;
                        p1 = 0.d;
                    }
                }
                p2=0.d;
            }
        }
        // Ajustar probabilidades
        for (int k=0;k<13;k++)
        {
            for(int m=0;m<13;m++)
            {
                for (int i = 0; i < 13; i++)
                {
                    for (int j = 0; j < 13; j++)
                    {
                        total += transicao[k][m][i][j];
                    }
                }
                transicao[k][m][12][12]+=1-total;
                total=0.d;
            }
        }
        //Verificar soma das linhas
        /*for (int i = 0; i < 13; i++)
        {
            for (int j = 0; j < 13; j++)
            {
                System.out.println(transicao[7][7][i][j]);
                total += transicao[12][12][i][j];
            }
        }
        System.out.println(total);*/
        //System.out.println(transicao[8][4][12][12]);


    }

    private static double getP(double[] pedidos1, double[] encomendas1, int numCarrosI1, int numCarrosF1, double p1) {
        int numPedidos1;
        int numEncomendas1;
        if (numCarrosI1 == numCarrosF1) {
            for (numPedidos1 = 0; numPedidos1 <= 12; numPedidos1++) {
                numEncomendas1 = min(numCarrosI1, numPedidos1);
                p1 += pedidos1[numPedidos1] * encomendas1[numEncomendas1];
            }
        } else if (numCarrosI1 > numCarrosF1) {
            for (numPedidos1 = numCarrosI1 - numCarrosF1; numPedidos1 <= 12; numPedidos1++) {
                numEncomendas1 = min(numPedidos1 - (numCarrosI1 - numCarrosF1), numCarrosF1);
                p1 += pedidos1[numPedidos1] * encomendas1[numEncomendas1];
            }
        } else {
            for (numPedidos1 = 0; numPedidos1 <= 12; numPedidos1++) {
                numEncomendas1 = min(numCarrosF1, numCarrosF1 - (numCarrosI1 - numPedidos1));
                p1 += pedidos1[numPedidos1] * encomendas1[numEncomendas1];
            }
        }
        return p1;
    }
}
