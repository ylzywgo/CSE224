#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>
#include <arpa/inet.h>


int main(){
    // int sockfd
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);

    struct sockaddr_in sa = {};
    sa.sin_family = AF_INET;
    sa.sin_port = htons(5555);
    sa.sin_addr.s_addr = inet_addr("cse224.sysnet.ucsd.edu");

    connect(sockfd, (struct sockaddr*) &sa, sizeof(sa));
    socklen_t client_len = sizeof(sa);

    // char *msg = "A53280596\r\n";
    int buff = sendto(sockfd, "A53280596\r\n", 11, 0, (struct sockaddr*) &sa, client_len);

    char buf[1024];
    int n = recvfrom(sockfd, buf, sizeof(buf)-1, 0, (struct sockaddr*) &sa, &client_len);

    printf("client received %s\n", buf);
    return 0;
}