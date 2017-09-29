#include <iostream>
#include <string>
#include <fstream>
#include <sstream>


using namespace std;

/*
	parses SFOLD output files and prints annotation profile that consists of Paired, Loop, Misc. (Bulge | Internal | Multiloop), 
	and Unstructured (External Region) probabilities for each position.  

    If you want to use another alphabet than the described above (P, L, U, M) you can change the part of code that prints the 
	profiles. Probabilities for each structural context (e.g. paired, unpaired, in hairpin loop, in bulge) are stored in probX 
	arrays. 

*/
int main(int argc, char* argv[])
{   
   ifstream inputSS; // sstrand.out 
   inputSS.open(argv[1]);
   if(inputSS.fail())
     cout<<"couldnt open input file "<<argv[1]<<endl;

   ifstream inputLoop; // loopr.out
   inputLoop.open(argv[2]);
   if(inputLoop.fail())
     cout<<"couldnt open input file "<<argv[2]<<endl;
   
   string outFilename = argv[3]; //profile output file 

   string sequence = argv[4]; 
   int seqLength = sequence.length();
   
   double probP[seqLength] , probU[seqLength], probH[seqLength], probB[seqLength],probT[seqLength], probM[seqLength], probE[seqLength];
   string lineSS, lineLoop;

   string foo;
   int count = 0;
   
   
   // Parsing SFOLD ouput
   while(getline(inputSS, lineSS) && getline(inputLoop, lineLoop))
   {        
      istringstream insSS;
      insSS.str(lineSS);
      insSS>>foo>>foo>>foo>>probU[count]>>foo>>foo; // read the probability of being unpaired value
      probP[count] = 1- probU[count];
      
      istringstream insLoop;
      insLoop.str(lineLoop);
	  
	  //read the prob of being in H, B, T, M and E context. H : hairpin, B: bulge, T: internal loop, M: multiloop, E: external loop
      insLoop>>foo>>foo>>probH[count]>>probB[count]>>probT[count]>>probM[count]>>probE[count]>>foo;
      count++;
   }
   

   // printing profiles in the following order: P, L, M, U 
   ofstream out;
   out.open(outFilename.c_str(), ios::app);
   out<<">"<<sequence<<endl;

   for(int i =0 ; i < seqLength ; i++)
   {
		out<<"\t"<< probP[i];  // P
   }
   out<<endl;
   for(int i =0 ; i < seqLength ; i++)
   {
   		out<<"\t"<<probH[i]; // L
   }
   out<<endl;

   for(int i =0 ; i < seqLength ; i++)
   {
		out<<"\t"<<probB[i] + probT[i]+ probM[i]; // M stands for miscellaneous = B (bulge) + T (internal) + M (multiloop)
   }
   out<<endl;
   for(int i =0 ; i < seqLength ; i++)
   {
		out<<"\t"<<probE[i]; // U
   }

   out<<endl;
   out.close();

   return 0;
}

