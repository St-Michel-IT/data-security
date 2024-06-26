#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int check_authentication(char *password) {
    int buffer_size = 16;
    char password_buffer[buffer_size];
    int auth_flag = 0;
    strncpy(password_buffer, password, buffer_size); // Not so safe but better
    if (strcmp(password_buffer, "brillig") == 0)
        auth_flag = 1;
    if (strcmp(password_buffer, "outgrabe") == 0)
        auth_flag = 1;
    return auth_flag;
}
int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <password>\n", argv[0]);
        exit(0);
    }
    if (check_authentication(argv[1])) {
        printf("Access Granted.\n");
    } else {
        printf("Access Denied.\n");
    }
}