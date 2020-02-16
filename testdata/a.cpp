#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <ctime>
#include <map>
#include <vector>
using namespace std;
int n,m,c,a[12],sum,cnt;
int label[1000];
int e[1000000][2];
map<pair<int,int>, bool>M;
vector<int>community[12];
int main()
{
    freopen("test2.txt","w",stdout);
    srand(unsigned(time(0)));
    n = rand()%100+50;
    c = rand()%10+2;
    int N = n-c, n1;
    int dd = N/c;
    for(int i=1;i<=c;i++)
    {
        if(N!=0) n1 = rand()%dd+1;
        else n1 = 0;
        if(i==c) n1=N;
        N-=n1;
        a[i]=n1+1;
        M.clear();
        int K=rand()%min(a[i],10);
        for(int j=1;j<=(a[i] * K)/2 ;j++)
        {
            int x = rand()%a[i] + 1, y = rand()%a[i] + 1;
            if(x != y)
            {
                if(M[make_pair(x,y)]!=true && M[make_pair(y,x)]!=true)
                {
                    M[make_pair(x,y)]=true;
                    ++cnt;
                    e[cnt][0] = sum+x;
                    e[cnt][1] = sum+y;
                }
            } 
        }
        for(int j=sum;j<=sum+a[i];j++) label[j]=i;
        for(int j=sum;j<=sum+a[i];j++) community[i].push_back(j);
        sum+=a[i];
    }
    printf("n m c:\n");
    cout<<n<<" "<<cnt<<" "<<c<<endl;
    printf("[");
    for(int i=1;i<=n;i++) printf("[%d], ",label[i]);
    printf("]\n");

    printf("[");
    for(int i=1;i<=c;i++)
    {
        printf("[");
        for(int j=0;j<community[i].size();j++) printf("%d, ",community[i][j]);
        printf("],");
    }
    printf("]\n");

    printf("[\n");
    for(int i=1;i<=cnt;i++)
    {
        printf("(%d, %d),",e[i][0],e[i][1]);
    }
    printf("]\n");
    return 0;
}