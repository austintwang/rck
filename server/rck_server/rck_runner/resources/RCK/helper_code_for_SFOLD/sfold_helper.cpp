#include <cstdlib>
#include <iostream>
#include <string>
#include <fstream>
#include <sstream>


using namespace std;
/* 
  runs SFOLD for each sequence in the input FASTA file and parses the output files to generate the annotation profile.

  Note : If you want to use another alphabet than P, L, U, M you can change the sprofile.cpp code accordingly. 

*/
int main(int argc, char* argv[])
{

   ifstream input;
   input.open(argv[1]); // input file name that contains a set of sequences in fasta format
   
   if(input.fail())
     cout<<"couldnt open input file "<<argv[1]<<endl;

   string outFilename = argv[2]; //output file name
   
   
   
   ofstream out;
   
   string leftrightComm;
   string line, foo, sequence, seqline;
   double prob;

   string profileComm = "./sprofile ./out/sstrand.out ./out/loopr.out   ./"  + outFilename;
   cout << profileComm<<endl;
   
   int seqLength;
   string sfoldComm = "";
   int seqCount = 0;
   string profileCommLast;
   while( getline(input,line)) //fasta header
   {
   	  out.open("./data/seqinput.txt"); 
      getline(input,seqline);
	  istringstream ins;
	  ins.str(seqline);
	  ins>>sequence;
      out<<line<<endl<<sequence<<endl; // sequence
      seqLength = sequence.length();
      out.close();
      //run sfold
	  sfoldComm = "./bin/sfold -a 0 -o ./out ./data/seqinput.txt";
      system(sfoldComm.c_str());
      //run helper program to parse the sfold output
      profileCommLast = profileComm + " " + sequence;
      system(profileCommLast.c_str());

      seqCount++;
   }
   
   return 0;
}

