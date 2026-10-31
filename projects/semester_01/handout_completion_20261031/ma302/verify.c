#include <stdio.h>
#include <math.h>
#include <stdlib.h>
typedef void (*rhs)(double,const double*,double*);
static void decay(double t,const double*y,double*f){(void)t;f[0]=-y[0];}
static void lorenz(double t,const double*y,double*f){(void)t;f[0]=10*(y[1]-y[0]);f[1]=28*y[0]-y[1]-y[0]*y[2];f[2]=y[0]*y[1]-(8.0/3)*y[2];}
static void hh_demo(double t,const double*y,double*f){(void)t;double V=y[0],m=y[1],h=y[2],n=y[3];f[0]=-m*m*m*h*(V-1)-n*n*n*n*(V+1)-V;for(int i=1;i<4;i++)f[i]=1-2*y[i];}
static void rk4(rhs f,int n,double t,double h,double*y){double a[4],b[4],c[4],d[4],z[4];f(t,y,a);for(int i=0;i<n;i++)z[i]=y[i]+h*a[i]/2;f(t+h/2,z,b);for(int i=0;i<n;i++)z[i]=y[i]+h*b[i]/2;f(t+h/2,z,c);for(int i=0;i<n;i++)z[i]=y[i]+h*c[i];f(t+h,z,d);for(int i=0;i<n;i++)y[i]+=h*(a[i]+2*b[i]+2*c[i]+d[i])/6;}
static double integrate(rhs f,int n,int steps,double T,double*y){double h=T/steps;for(int k=0;k<steps;k++){rk4(f,n,k*h,h,y);for(int j=0;j<n;j++)if(!isfinite(y[j])){fprintf(stderr,"nonfinite\n");exit(2);}}return h;}
int main(void){int fail=0;double prevE=0,prevR=0;printf("steps,euler_error,rk4_error,euler_ratio,rk4_ratio\n");for(int n=10;n<=80;n*=2){double eu=1,y[4]={1,0,0,0},h=1.0/n;for(int k=0;k<n;k++)eu*=1-h;integrate(decay,1,n,1,y);double E=fabs(eu-exp(-1)),R=fabs(y[0]-exp(-1));printf("%d,%.12g,%.12g,%.7g,%.7g\n",n,E,R,prevE?prevE/E:0,prevR?prevR/R:0);if(prevR && !(prevR/R>14 && prevR/R<18))fail++;prevE=E;prevR=R;}
 double y[4]={0.2,0.5,0.5,0.5};integrate(hh_demo,4,1000,5,y);double he=fabs(y[0]-0.2*exp(-1.125*5));printf("hh_teaching_case_exact_error,%.12g\n",he);if(he>1e-10)fail++;
 double a[4]={1,1,1,0},b[4]={1,1,1,0};integrate(lorenz,3,1000,1,a);integrate(lorenz,3,2000,1,b);printf("lorenz_T1_step_halving_distance,%.12g\n",sqrt(pow(a[0]-b[0],2)+pow(a[1]-b[1],2)+pow(a[2]-b[2],2)));
 FILE*out=fopen("logistic_bifurcation.csv","w");if(!out)return 3;fprintf(out,"r,x\n");for(int j=0;j<=200;j++){double r=2.8+1.2*j/200.0,x=0.271828;for(int k=0;k<2000;k++)x=r*x*(1-x);for(int k=0;k<128;k++){x=r*x*(1-x);if(x<0||x>1||!isfinite(x))fail++;fprintf(out,"%.9g,%.17g\n",r,x);}}fclose(out);
 printf("failures,%d\n",fail);return fail?1:0;}
