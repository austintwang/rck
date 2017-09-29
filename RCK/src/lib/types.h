class motif
{
 public:
  
  list<pair<int, double> > occurList;
  double pBoundVal;
  double totalPosSum;
  double totalAllSum;
  double storeAvg;
/*
  motif()
  {
  	
  }
*/
  void PushFront(int seqID, double annotProb)
  {
      occurList.push_front(pair<int, double>(seqID, annotProb));
  }



  friend ostream& operator << (ostream& out, motif &t)
    {
      //out<<t.matrixScore[0]<<" "<<t.matrixScore[1];
      for (list<pair<int, double> >::iterator ite=t.occurList.begin(); ite!=t.occurList.end(); ite++)
	{
	  out<<" <"<<ite->first<<","<<ite->second<<">";
	}
      return out;
    }
};


struct eqstr {

  bool operator()(const string s1, const string s2) const{
    return strcmp(s1.c_str(),s2.c_str())==0;
  }
};


namespace __gnu_cxx {
  
  template<> struct hash<const string>  {
    size_t operator() (const string & key) const {
      return hash<const char*>()(key.c_str());
    }
  };
}


typedef hash_map<const string, motif, hash<const string>, eqstr>  hash_map_string;

class value_order {
 public:
  double value;
  int order;
};


struct lessValueOrder {
  bool operator()(const value_order v1, const value_order v2) const {
    return v1.value < v2.value;
  }
};


