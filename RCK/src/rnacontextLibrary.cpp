#include "lib/rnacontextHeader.h"
#include <stdarg.h>

#define MAX_FNAME_LENGTH 10000L
#define MAX_ALPHABET_LENGTH 256L
#define MAX_OPTION_LENGTH 256L
#define MAX_LINE_LENGTH 10000L
#define MAX_LOGENTRIES 100000000L
#define MAX_MOTIFWIDTH 256L
#define NUMBER_SIGN '#'
#define NANVAL (-1*DBL_MAX)

// Minimum standard random number generator
// Park and Miller, ``Random Number Generators: Good Ones are Hard to Find''
#define RAND_0_1 PMrand()
#define AAA 48271
#define MMM 2147483647
#define QQQ (MMM / AAA)
#define RRR (MMM % AAA)

static long int seed = 1;//time(NULL); //1;

using namespace std;
double PMrand()
{
	long int hi = seed / QQQ;
	long int lo = seed % QQQ;
	long int test = AAA * lo - RRR * hi;
	if(test > 0)
		seed = test;
	else	seed = test + MMM;
	return (double) seed / MMM;
}


typedef struct alphabet_struct {
	char alphabet[MAX_ALPHABET_LENGTH];
	char dontCareCharacters[MAX_ALPHABET_LENGTH];
	char rcLookup[MAX_ALPHABET_LENGTH];
	char validChars[MAX_ALPHABET_LENGTH];
	char lookup[MAX_ALPHABET_LENGTH];
	char translation[MAX_ALPHABET_LENGTH];
	int doReverseComplementFlag;
} AlphabetStruct;

typedef struct param_struct {
	char trainDataFileName[MAX_FNAME_LENGTH];
	char testDataFileName[MAX_FNAME_LENGTH];
	char annotFileNameTrain[MAX_FNAME_LENGTH];
	char annotFileNameTest[MAX_FNAME_LENGTH];
	char outFileName[MAX_FNAME_LENGTH];
	char outDir[MAX_FNAME_LENGTH];
	char logFileName[MAX_FNAME_LENGTH];
	char pwmFileName[MAX_FNAME_LENGTH];
	char respFileName[MAX_FNAME_LENGTH];
	char dontCareCharacters[MAX_ALPHABET_LENGTH];
	char paramsFileNameInput[MAX_FNAME_LENGTH];
	char alphabet[MAX_ALPHABET_LENGTH];
	char annotation[MAX_ALPHABET_LENGTH];
	char rcAlphabet[MAX_ALPHABET_LENGTH];
	char motifFileName[MAX_FNAME_LENGTH];
	int minWidth;
	int maxWidth;
	int maxIter;
	int seedNum;
	int seedWidth;
	int negSeqNum;
	int utr;
	int outFileNameDefinedFlag;
	int inputModelFlag;
	int motifFileNameDefinedFlag;
	int hasAnnotParamsFlag;
	int ignoreAnnotFlag;
	int doLogTransformFlag;
	int doReverseComplementFlag;
	int optimizewFlag;
} InputParams;


InputParams defaultParameters() {
	InputParams p;
	strcpy(p.motifFileName, "");
	strcpy(p.outFileName, "output.txt");
	strcpy(p.logFileName, "logfile.txt");
	strcpy(p.outDir, "./outputs/");
	
	strcpy(p.respFileName, "");
	strcpy(p.dontCareCharacters, "");
	strcpy(baseAlphabet, "ACGU");
	strcpy(annotAlphabet, "PHOE");
	strcpy(p.rcAlphabet, "");
	p.minWidth = 7;
	p.maxWidth = 7;
	p.maxIter = 200;
	p.seedNum = 5;
	p.seedWidth = -1;
	p.outFileNameDefinedFlag = 0;
	p.inputModelFlag = 0;
	p.hasAnnotParamsFlag = 0;
	p.ignoreAnnotFlag=0;
	p.motifFileNameDefinedFlag = 0;
	p.doLogTransformFlag = 0;
	p.doReverseComplementFlag = 0;
	p.optimizewFlag=0;
	return p;
}

void setParameters(int argc, char **argv, InputParams *params) {
	// Set up user-defined parameters 
	char tmpOptions[MAX_OPTION_LENGTH], tmpChar, *tmpP;
	int checkWidthFlag = 0;
	for (int i=1; i<argc; i+=2) {
		strcpy(tmpOptions, argv[i]);
		if (tmpOptions[0] != '-') {
			printf("here\n");
			printf("Invalid options: %s\n", tmpOptions[0]);
			exit(1);
		}
		else {
			tmpChar = tmpOptions[1];
			switch (tmpChar) {
				cout<<tmpChar<<endl;	
				case 'a':  // a : alphabet (default "ACGT")
					if (strlen(argv[i+1]) > MAX_ALPHABET_LENGTH-1) {
						fprintf(stderr,"%s exceeds maximum alphabet length of %d\n", 
								MAX_ALPHABET_LENGTH-1);
					}
					strcpy(params->alphabet, argv[i+1]);
					baseAlphabet = argv[i+1];
					AlphabetSize = strlen(argv[i+1]);
					break;

				case 'b': // b: maxIter
                                        strcpy(tmpOptions, argv[i+1]);
					params->maxIter = atoi(tmpOptions);
					break;
					
				case 'c':  // c : data file name (no default)
					printf("data file name range\n");
					if (strlen(argv[i+1]) > MAX_FNAME_LENGTH-1) {
						fprintf(stderr,"%s exceeds maximum alphabet length of %d\n", MAX_FNAME_LENGTH-1);
					}
					strcpy(params->trainDataFileName, argv[i+1]);
					printf("Data file name range after\n");
					break;	
					
				case 'd':  // d : data file name (no default)
					if (strlen(argv[i+1]) > MAX_FNAME_LENGTH-1) {
						fprintf(stderr,"%s exceeds maximum alphabet length of %d\n", MAX_FNAME_LENGTH-1);
					}
					strcpy(params->testDataFileName, argv[i+1]);
					break;
					
				case 'e': // e: annotation level alphabet i.e. L, R, U, C 
					if (strlen(argv[i+1]) > MAX_FNAME_LENGTH-1) {
						fprintf(stderr,"%s exceeds maximum alphabet length of %d\n", 
								MAX_FNAME_LENGTH-1);
					}
					strcpy(params->annotation, argv[i+1]);
					annotAlphabet = argv[i+1];
					AnnotAlphabetSize = strlen( argv[i+1]);
					break;
					
				case 'f':  // f : PWM file name, default "", i.e. generate one
					if (strlen(argv[i+1]) > MAX_FNAME_LENGTH-1) {
						fprintf(stderr,"%s exceeds maximum alphabet length of %d\n", 
								MAX_FNAME_LENGTH-1);
					}
					strcpy(params->pwmFileName, argv[i+1]);
					break;
					
				case 'g': // g : Logfile name
					if (strlen(argv[i+1]) > MAX_FNAME_LENGTH-1) {
						fprintf(stderr,"%s exceeds maximum alphabet length of %d\n", 
								MAX_FNAME_LENGTH-1);
					}
					strcpy(params->logFileName, argv[i+1]);
					break;
					
				case 'h': // annotation input filename
					if (strlen(argv[i+1]) > MAX_FNAME_LENGTH-1) {
						fprintf(stderr,"%s exceeds maximum filename length of %d\n", 
								MAX_FNAME_LENGTH-1);
					}
					strcpy (params->annotFileNameTrain, argv[i+1]);
					break;
					
				case 'l': //
					if (strlen(argv[i+1]) > MAX_FNAME_LENGTH-1) {
						fprintf(stderr,"%s exceeds maximum filename length of %d\n", 
								MAX_FNAME_LENGTH-1);
					}
					strcpy (params->motifFileName, argv[i+1]);
					params->motifFileNameDefinedFlag = 1;
					break;
					
				case 'n': // annotation input filename2
					if (strlen(argv[i+1]) > MAX_FNAME_LENGTH-1) {
						fprintf(stderr,"%s exceeds maximum filename length of %d\n", 
								MAX_FNAME_LENGTH-1);
					}
					strcpy (params->annotFileNameTest, argv[i+1]);
					break;
					
				case 'i':  // i : don't care characters, (default "")
					if (strlen(argv[i+1]) > MAX_ALPHABET_LENGTH-1) {
						fprintf(stderr,"%s exceeds maximum alphabet length of %d\n", 
								MAX_ALPHABET_LENGTH-1);
					}
					strcpy(params->dontCareCharacters, argv[i+1]);
					break;
				case 'p':  // 
					if (strlen(argv[i+1]) > MAX_FNAME_LENGTH-1) {
						fprintf(stderr,"%s exceeds maximum filename length of %d\n", 
								MAX_FNAME_LENGTH-1);
					}
					strcpy (params->paramsFileNameInput, argv[i+1]);
					params->inputModelFlag = 1;
					break;
					
				case 'j':  // i : don't care characters, (default "")
					params->hasAnnotParamsFlag = atoi(argv[i+1]);
					break;					
				case 'q':  // q: ignore annotations
					params->ignoreAnnotFlag=1;
					break;
				case 'o':  // o : output file name (default ???)
					if (strlen(argv[i+1]) > MAX_FNAME_LENGTH-1) {
						fprintf(stderr,"%s exceeds maximum alphabet length of %d\n", 
								MAX_FNAME_LENGTH-1);
					}
					strcpy(params->outFileName, argv[i+1]);
					params->outFileNameDefinedFlag = 1;
					break;
					
				case 'm': // m: output dir
					if (strlen(argv[i+1]) > MAX_FNAME_LENGTH-1)
                                                fprintf(stderr,"%s exceeds maximum alphabet length of %d\n", 
                                                        MAX_FNAME_LENGTH-1);
					strcpy(params->outDir, argv[i+1]);
					
				case 'r':  // r : reverse complement alphabet (no default)
					if (strlen(argv[i+1]) > MAX_ALPHABET_LENGTH-1) {
						fprintf(stderr,"%s exceeds maximum alphabet length of %d\n", 
								MAX_ALPHABET_LENGTH-1);
					}
					params->doReverseComplementFlag = 1;
					strcpy(params->rcAlphabet, argv[i+1]);
					break;
					
				case 's':  // s : # of seeds. (default ???)
					params->seedNum = atoi(argv[i+1]);
					break;
					
				case 'u':  // u : log transform data
					params->doLogTransformFlag = atoi(argv[i+1]);
					break;
					
				case 'v':  // v : seed width (default ???)
					params->seedWidth = atoi(argv[i+1]);
					printf(" seed width %d\n", params->seedWidth);
					break;
					
				case 'y': // utr or not 
					params->utr = atoi(argv[i+1]);
					break;
					
				case 'w':  // w : width range (default ???)
					printf("width range\n");
					strcpy(tmpOptions, argv[i+1]);
					tmpP = strchr(tmpOptions, '-');
					if (tmpP == NULL) {
						params->minWidth = atoi(tmpOptions);
						params->maxWidth = params->minWidth;
					}	  
					else {
						*tmpP = '\0';
						params->minWidth = atoi(tmpOptions);
						params->maxWidth = atoi(tmpP+1);
						printf("min width %d\n", params->minWidth);
						printf("max width %d\n", params->maxWidth);
						if (params->minWidth > params->maxWidth) {
							fprintf(stderr, "Min width %d is greater than max width %d\n",
									params->minWidth,
									params->maxWidth);
						}
					}
					//checkWidthFlag = 1;  //should not be 1
					checkWidthFlag = 0;
					break;
				
				case  'z': //set 1 if you want to optimize w 	
					params->optimizewFlag=atoi(argv[i+1]);
					break; 	
				
				default:
					printf("default\n");
					printf("Invalid options!\n");
					exit(1);
			}
		}
	}
	
	printf("Read file\n");
	// check options
	if (checkWidthFlag) {
		if (params->seedWidth < 0) {
			params->seedWidth = params->minWidth;
		}
		if (params->seedWidth > params->minWidth) {
			fprintf(stderr,
					"Seed width %d is not larger than motif minimum width %d\n",
					params->seedWidth,
					params->minWidth);
			exit(-1);
		}
	} 
}
// ----------------------------------------------------- 
// --------------  FUNCTIONS FOR LOGGING ---------------
// ----------------------------------------------------- 

FILE *global_logfp;           // LOGFILE POINTER
int global_logfile_length;    // LOGFILE LENGTH
int global_maxlogfile_length; // MAXIMUM LOGFILE LENGTH, INFINITE IF NEGATIVE

void initLogFile(FILE *fp, int max_length) {
  global_logfp = fp;
  global_maxlogfile_length = max_length;
  global_logfile_length = 0;
}

// OPENLOGFILE - opens log file for update
void openlogfile(char *logfile, int max_length) {
  FILE *fp;
  if (logfile == NULL || strlen(logfile) == 0) {
    fp == stdout;
  }
  else {
    fp = fopen(logfile, "a");
    if (fp == NULL) {
      perror("RankMotif logfile");
      exit(-1);
    }
  }
  initLogFile(fp, max_length);
}

// CLOSELOGFILE - closed the log file
void closelogfile()
{
  if (global_logfp != stdout) {
    int iserror;
    iserror = fclose(global_logfp);
    if (iserror == EOF) {
      perror("RankMotif logfile");
      exit(-1);
    }
  }
}

FILE *logfilePointer() {
  return global_logfp;
}

// LOGPRINTF - adds an entry to the log file
void logprintf(char *fmt, ...)
{
  va_list args;

  if (global_maxlogfile_length > 0 && 
      global_logfile_length <= global_maxlogfile_length) {
    va_start(args, fmt);
    vfprintf(global_logfp, fmt, args);
    fflush(global_logfp);
    va_end(args);
    global_logfile_length++;
  }
}


/* ReadPWM -- READS A PWM FROM A FILE POINTER
   Reads a PWM from a Tab-delimited text file. Each line is one row of the
   PWM.

    PWMFileName:  string that contains the PWM filename
     motifWidth:  length of motif, i.e. # of entries in each row
   alphabetSize:  number of rows in the motif
            pwm:  the input pwm will be read into this preallocated pointer
                  array
*/
void ReadPWM(FILE *fp,
	     int motifWidth,
	     int AlphabetSize,
	     double **pwm) {

  for(int i=0; i<AlphabetSize; i++) {
    for (int j=0; j<motifWidth; j++) {
      fscanf(fp, "%lf", &pwm[i][j]);
      pwm[i][j] = log(pwm[i][j]+DBL_MIN);
    }
  }
}


/*
  Convert all nucleotides in the seqs to upper case.
*/
void Upper(char *s) {
  int length = strlen(s);
  for (int i=0; i<length; i++) {
    char temp = *(s+i);
    if (temp>='a' && temp<='z')  
      *(s+i) = temp-'a'+'A';
  }
}

double square(double x)
{
	return x * x;
}
