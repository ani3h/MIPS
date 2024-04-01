#include <stdio.h>

int main()
{
    int n1 = 0, n2 = 1;
    int n3;
    int number = 5; 
   
    for(int i = 2; i < number; ++i)  
    {    
        n3 = n1 + n2;     
        n1 = n2;    
        n2 = n3;    
    }  

    printf("%d", n3);

    return 0;
}
