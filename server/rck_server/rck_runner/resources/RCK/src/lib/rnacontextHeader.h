/*
 *  leastHeader.h
 *  least
 *
 *  Created by Hilal Kosucu on 16/01/09.
 *  Copyright 2009 __MyCompanyName__. All rights reserved.
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <float.h>
#include <algorithm>
#include <list>
#include <ext/hash_map>

using namespace std;
using namespace __gnu_cxx;

#include "types.h" //must stay here

// Macros
#define SMALL1 (0.1  / 1000)     // strength of regularization on w
#define SMALL2 (1.0 / 1000)    /*(10.0 / validPairNum)*/    // strength of regularization on theta
#define MAX(x,y) ((x) > (y) ? (x) : (y))
#define MAX_ERROR 1000000000
#define RANDOM_PARAM_ENTRY ((RAND_0_1-0.5)*0.1) //smaller initial values

// Default values
#define MIN_INITIAL_PROB 0.01

/* Represents NaN */

/* set DEBUG to 1 to print out debug info */
#define DEBUG 1

/* Macros for measuring time */
#include <time.h>
clock_t cputime_global = 0;
clock_t last_time;
double spot1, spot2, spot3, spot4;
#define INIT_TIME (last_time = clock());
#define DIFF_TIME(s) s += difftime(clock(), last_time); last_time = clock();
#define TIC cputime_global = clock();
#define TOC logprintf("Elapsed time: %.4g seconds\n", ((double)(clock()-cputime_global)) / CLOCKS_PER_SEC);

#define HERE fprintf(stderr, "File %s, Line number %d\n", __FILE__, __LINE__);
//#define HERE ;

#define BASE 1
#define ANNOT 2
#define BIASS 3
#define BIASA 4
#define A 5
#define B 6


// type definitions
typedef vector<vector<vector<double > > > Annots;  
hash_map_string hash_kMers;



struct kmerScores
{
	int seqID;
	int kmerNum;
	double affinity;
	double seqAffinity;
	double annotAffinity;
};

struct sort_by_one
{
	bool operator () (const kmerScores& lhs , const kmerScores& rhs)
	{
     	return lhs.affinity > rhs.affinity;
	}
};


int AlphabetSize;
int AnnotAlphabetSize;
int numBaseParams;
int numAnnotParams;
int motifWidth;
int trainSeqNum; // number of sequences used (pos+neg) smaller than origSeqNum
int testSeqNum;


Annots inputAnnotsTrain;
Annots inputAnnotsTest; // annotations (structures)
int *kmerNumsTrain;
int *kmerNumsTest;


int trainPosSeqNum;
int testPosSeqNum;


vector<string> seqsTrain;  // sequences
vector<string> seqsTest;
char *annotAlphabet; // alphabet of the annotation
char *baseAlphabet;

// parameters
double *baseParams; //for each position (motif length), for each {A,G,C,T}, for each {P,H,O,E} //change
double **annotParams;
double biasS; //change
double biasA;
double parA;
double parB;

double **baseParamsPWM; //for each position (motif length), for each {A,G,C,T}, for each {P,H,O,E} //change
double *annotParamsPWM;
double *gradBaseParams;
double *gradAnnotParams;
double gradBiasS;
double gradBiasA;


int ***baseDeltaValsTrain; // for each sequence and then for each kmer and then for each param
int ***baseDeltaValsTest; // for each sequence and then for each kmer and then for each param
double **affinityValsTrain; //for each sequence and then for each kmer change (N())
double **AffinitySeqVals; // for each sequence and then for each kmer
double **AffinityAnnotVals; // for each sequence and then for each kmer
double **sumBaseParamsTrain; // for each sequence and then for each kmer
double ***sumAnnotParamsTrain; // for each sequence and then for each  letter and then for each kmer


double *means;
double *variances;

vector<double> ratiosTrain;
vector<double> ratiosTest;

vector<double> scoresTrain;
vector<double> scoresTest;




