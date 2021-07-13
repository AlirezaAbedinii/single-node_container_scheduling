#include<iostream>

using namespace std;

int main(int argc, char** argv)

{
        cout<<"There is "<<argc<<" arguments"<<endl;
        cout<<"\nHello World,\nWelcome to my first C ++ program on Ubuntu Linux\n\n"<<endl;
        cout<<"your input was";
        for(int i=0;i<argc;i++){
                cout<<"argument number "<<i<<": "<<argv[i]<<endl;
        }
        return 0;
}