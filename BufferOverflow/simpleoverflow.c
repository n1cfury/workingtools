//Straight Outta Hacking:  The Art of Exploitation

#include <stdio.h>
#include <string.h>

int main(void)
{
		char first[5]="Hello";
		char second[5]="world";
		printf("%s -%s\n", first, second);
		strcopy(second, "ABCDEFGHIJLKMNOPQRSTUVWXYZ"); 	//Vulnerable Line
		printf("%s -%s\n", first, second);
		return 0;
}