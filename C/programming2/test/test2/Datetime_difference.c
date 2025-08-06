#include <stdio.h>
#include <stdbool.h>

typedef struct _Datetime{
	int year, month, day;
	int hour, minute, second;
}Datetime;

bool isVaildDatetime(Datetime a){
	bool vaild = (a.year>0)&&(a.month>0&&a.month<13)&&(a.day>0&&a.day<32);
	vaild&=(a.hour>-1&&a.hour<24)&&(a.minute>-1&&a.minute<60)&&(a.second>-1&&a.second<60);
	if(a.month==2||a.month==4||a.month==6||a.month==9||a.month==11){
		vaild&=(a.day<31);
		if(a.month==2)
			if((a.year%400!=0 && a.year%100==0) || a.year%4!=0)vaild&=(a.day<29);
			else vaild&=(a.day<30);
	}
	return vaild;
}



void swapIfneeded(Datetime *a, Datetime *b){
	// maintain the datetime a is earlier than datetime b.
	bool swap = false;

	if(a->year > b->year) swap=true;
	else if(a->year == b->year){
		if(a->month > b->month)swap=true;
		else if(a->month == b->month){
			if(a->day > b->day) swap=true;
			else if(a->day == b->day){
				if(a->hour > b->hour) swap=true;
				else if(a->hour == b->hour){
					if(a->minute > b->minute) swap=true;
					else if(a->minute == b->minute)
					if(a->second > b->second) swap=true;
				}
			}
		}
	}

	int t;
	if(swap){
		t = a->year, a->year=b->year, b->year=t;
		t = a->month, a->month=b->month, b->month=t;
		t = a->day, a->day=b->day, b->day=t;
		t = a->hour, a->hour=b->hour, b->hour=t;
		t = a->minute, a->minute=b->minute, b->minute=t;
		t = a->second, a->second=b->second, b->second=t;
	}

}

int toDay(Datetime a){
	//這個function内有些判斷閏年的條件和題目所給的程式碼不同，原因是忘記更新到題目的程式碼，非常抱歉，
	//但由於這題是計算datetime差異，我們這邊也測試過兩個版本的function，都是可以通過測試資料的，所以這並不影響同學的作答。

	int days = a.day, M[12]={31,28,31,30,31,30,31,31,30,31,30,31};

	for(int i=1; i<a.year; i++){
		if((i%100==0 && i%400!=0) || i%4!=0)days+=365;
		else days+=366;
	}

	if(a.year%4==0 && (a.year%100!=0 || a.year%400==0))M[1]=29;
	for(int i=0; i<a.month; i++)days+=M[i];

	return days;
}

int toSecond(Datetime a){
	int sec=a.second;
	sec+=a.hour*3600;
	sec+=a.minute*60;
	return sec;
}

Datetime datetimeDiff(Datetime a, Datetime b){
	Datetime diff;

	//to make sure the datetime A is earlier than datetime B
	swapIfneeded(&a, &b);

	int days_a = toDay(a), sec_a = toSecond(a);
	int days_b = toDay(b), sec_b = toSecond(b);

	diff.day = days_b-days_a;
	if(sec_b<sec_a){
		diff.day--;
		diff.second = sec_b + (24*60*60 - sec_a);
	}
	else diff.second = sec_b - sec_a;

	diff.minute = diff.second/60, diff.second%=60;
	diff.hour = diff.minute/60, diff.minute%=60;

	return diff;
}

void printDatetime(Datetime a){
	printf("%d %02d:%02d:%02d", a.day, a.hour, a.minute, a.second);
}


int main()
{
	Datetime A, B;

	scanf("%d %*c %d %*c %d %d %*c %d %*c %d", &A.year, &A.month, &A.day, &A.hour, &A.minute, &A.second);
	scanf("%d %*c %d %*c %d %d %*c %d %*c %d", &B.year, &B.month, &B.day, &B.hour, &B.minute, &B.second);

	bool isVaild=true;

	if(!isVaildDatetime(A)){
		printf("The first datetime is invalid.\n");
		isVaild=false;
	}
	if(!isVaildDatetime(B)){
		printf("The second datetime is invalid.\n");
		isVaild=false;
	}
	if(!isVaild)return 0;

	Datetime Diff = datetimeDiff(A, B);
	printDatetime(Diff);

	return 0;
}
