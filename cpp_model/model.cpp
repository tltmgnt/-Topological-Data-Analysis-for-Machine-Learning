// Vietoris-Rips H0 connected components
// Repository: https://github.com/tltmgnt/-Topological-Data-Analysis-for-Machine-Learning
// Standalone C++17, offline, synthetic reference model.
// Build: c++ -std=c++17 -O2 -Wall -Wextra -pedantic cpp_model/model.cpp -o model
// Run: ./model    (runs built-in assertions and prints a bounded demo result)
// Research-only: no trained AI, independent validation, external actions or approval.
#include <algorithm>
#include <cmath>
#include <functional>
#include <iostream>
#include <limits>
#include <numeric>
#include <queue>
#include <set>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

void require(bool ok,const char* msg){if(!ok)throw std::runtime_error(msg);}
namespace model {
int components_at_threshold(std::vector<double> points,double eps){if(eps<0||!std::isfinite(eps))throw std::invalid_argument("epsilon");int n=(int)points.size();std::vector<int> p(n);std::iota(p.begin(),p.end(),0);
 std::function<int(int)> root=[&](int x){return p[x]==x?x:p[x]=root(p[x]);};int c=n;for(int i=0;i<n;++i)for(int j=i+1;j<n;++j)if(std::abs(points[i]-points[j])<=eps){int a=root(i),b=root(j);if(a!=b){p[a]=b;--c;}}return c;}
void demo(){require(components_at_threshold({0,.4,3},.5)==2,"H0 components");std::cout<<"H0_components_epsilon_0_5="<<components_at_threshold({0,.4,3},.5)<<" higher_homology_not_computed=1";}
} // namespace model
int main(){try{std::cout<<std::boolalpha;model::demo();std::cout<<'\n';return 0;}catch(const std::exception&e){std::cerr<<"model test failed: "<<e.what()<<'\n';return 1;}}
