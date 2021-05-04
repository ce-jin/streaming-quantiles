#include<bits/stdc++.h>
using namespace std;

const int N = 1e6;
int n,k;

struct box {
	int h,g;
} boxes[N], newboxes[N]; // boxes[1..k]

void sqweeze() {
	int min_i, minh = 1e9;
	for (int i=2;i<=k+1;i++) {
		int h = newboxes[i].h + newboxes[i].g;
		if(h<minh) {
			minh=h;
			min_i=i;
		}
	}
	// merge i-1, i
	
	for (int j=1;j<min_i-1;j++) boxes[j] = newboxes[j];
	boxes[min_i-1] = (box) {newboxes[min_i].h+newboxes[min_i].g, newboxes[min_i-1].g};
	if (min_i<=k) {
		boxes[min_i] = (box) {newboxes[min_i+1].h, newboxes[min_i+1].g+newboxes[min_i].g};
	}
	for (int j=min_i+2;j<=k+1;j++) boxes[j-1] = newboxes[j];
}
void update(int i) { // 1<=i<=k
	for (int j=1;j<=i;j++) newboxes[j]=boxes[j];
	newboxes[i+1] = (box) {boxes[i].h, 1};
	for (int j = i+1;j<=k;j++) newboxes[j+1]=boxes[j];
	sqweeze();
}

void init() {
	for (int i = 1; i <= k; i++) {
		boxes[i].h=0;
		if (i == 1) {
			boxes[i].g=0;
		} else boxes[i].g=1;
	}
}
int maxh() {
	int max_h=0;
	for (int i=1;i<=k;i++) max_h = max(max_h, boxes[i].h);
	return max_h;
}
void printall() {
	for (int i=1;i<=k;i++) {
		printf("(h=%d g=%d) ", boxes[i].h, boxes[i].g);
	}
	printf("\n");
}
int main() {
	scanf("%d%d",&n,&k);
	init();
	//printall();
	for (int i=k+1;i<=n;i++) {
		update(1);
		//printall();
		if ((i&-i)==i) {
			double edo = 1.4 * i * log(0.019 * i) / k;
			int mh = maxh();
			printf("n=%d: maxhight=%d edo = %.1lf err = %.3lf kewen = %.3lf\n",i, mh, edo, (edo-mh)/mh , 1.0*i/(k*mh));
		}
	}
	//printf("%d\n", maxh());
	return 0;
}


