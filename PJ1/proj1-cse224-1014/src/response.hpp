#ifndef RESPONSE_H_
#define RESPONSE_H_

#include <arpa/inet.h>  /* for sockaddr_in and inet_ntoa() */
#include <iostream>			// input output
#include <fstream>
#include <string>			// for bzero
#include <sys/socket.h> 	// creating socket
#include <netinet/in.h>		// for sockaddr_in
#include <unistd.h>			// for close
#include <sys/stat.h>
#include <fcntl.h>
#include <assert.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/uio.h>
#include <thread>
#include <mutex>
#include <vector>
#include <deque>
#include <map>

using namespace std;

map<string, string> mime_dic;

void make_mime_dictionary(void) {
    ifstream file("mime.types");
    string temp_str;
    while (!file.eof())
    {
        std::getline(file, temp_str);
		int pos = temp_str.find(" ");
		string str_after_the_first_space = temp_str.substr(pos+1);
		int pos2 = str_after_the_first_space.find(" ");
		string key = temp_str.substr(0,pos);
		string value = str_after_the_first_space.substr(0, pos2);
		
        mime_dic.insert(make_pair(key, value));
    }
	file.close();
	mime_dic.erase("");
	mime_dic.erase(" ");
}

string get_file_mmtime(const char* filepath){
	struct stat finfo;

    if (stat(filepath, &finfo) != 0) {
        return "-1";
        //die_system("stat() failed");
    }

	time_t mod_time = finfo.st_mtime;
	struct tm * timeinfo;
    char buffer [80];

    time(&mod_time);
    timeinfo = localtime(&mod_time);

    strftime(buffer,80,"%a, %d %b %y %T %z",timeinfo);
	string times(buffer);
    return times;
}

int get_file_size2(const char* filepath)
{
    struct stat finfo;

    if (stat(filepath, &finfo) != 0) {
        return -1;
        //die_system("stat() failed");
    }

    return (int) finfo.st_size;
}

string readfile(string full_path){
	FILE *f = fopen(full_path.c_str(), "rb");
    fseek(f, 0, SEEK_END);
    unsigned long filesize = ftell(f);
    char *buffer = (char*)malloc(sizeof(char)*filesize);
    rewind(f);
    // store read data into buffer
    fread(buffer, sizeof(char), filesize, f);
	string html(buffer);

	return html;
}


string build_200_ok_headers(string filepath, string myserver){
	// find mime extension
	if(mime_dic.size() == 0) make_mime_dictionary();
    size_t pos = filepath.find_last_of("/");
	string filename = filepath.substr(pos+1);

    string mime_type = "application/octet-stream"; // default
	size_t dot_pos;
	string extention;
    // if there is an extention
	if(filename.find(".") != std::string::npos) {
		dot_pos = filename.find(".");
		extention = filename.substr(dot_pos);
		if(mime_dic.find(extention) != mime_dic.end()) {
			mime_type = mime_dic[extention];
		}
	}
	
	string response;
	response += "HTTP/1.1 200 OK\r\n";
	response += "Server: " + myserver + "\r\n";
	response += "Last-Modified: " + get_file_mmtime(filepath.c_str()) + "\r\n";
	response += "Content-Length: "+ to_string(get_file_size2(filepath.c_str())) +"\r\n";
	//determine mime type 

	response += "Content-Type: " + mime_type +"\r\n";
	response += "\r\n";
   
   // add last modified
	return response;

}

string build_404_notfound_headers(string myserver){
	string response;
	string filepath = "errorPage.html";
	response += "HTTP/1.1 404 NOT FOUND\r\n";
	response += "Server: " + myserver + "\r\n";
	response += "Content-Length: "+ to_string(get_file_size2(filepath.c_str())) +"\r\n";
	response += "Content-Type: text/html\r\n";
	response += "\r\n";
	string html = readfile(filepath);
	response += html;

	return response;
}

string build_400_badrequest_headers(string myserver){
	string response;
	string filepath = "errorPage.html";
	response += "HTTP/1.1 400 CLIENT ERROR\r\n";
	response += "Server: " + myserver + "\r\n";
	response += "Content-Length: "+ to_string(get_file_size2(filepath.c_str())) +"\r\n";
	response += "Content-Type: text/html\r\n";
	response += "Connection: close\r\n";
	response += "\r\n";
	string html = readfile(filepath);
	response += html;

	return response;
}

// if return -1, stop any later request, close socket
void send_response(int is_valid, int is_valid_header, string full_path, int client_sock, string myserver) {
	string headers;
    if(is_valid_header == -1) {
		headers = build_400_badrequest_headers(myserver);
		send(client_sock, (void*) headers.c_str(), (ssize_t) headers.size(), 0);
		close(client_sock);
	} else if(is_valid == -1) {
		headers = build_404_notfound_headers(myserver);
		send(client_sock, (void*) headers.c_str(), (ssize_t) headers.size(), 0);
	} else {
		// connection close
		headers = build_200_ok_headers(full_path, myserver);
		send(client_sock, (void*) headers.c_str(), (ssize_t) headers.size(), 0);

		FILE *f = fopen(full_path.c_str(), "rb");
		fseek(f, 0, SEEK_END);
		unsigned long filesize = ftell(f);
		char *buffer = (char*)malloc(sizeof(char)*filesize);
		// char buffer[256];
		rewind(f);
		fread(buffer, sizeof(char), filesize, f);
		send(client_sock, buffer, filesize, 0);
		// store read data into buffer
		// char buffer[256];  // array of bytes, not pointers-to-bytes
		// bzero(buffer, 256);
		// int bytesRead = 0; 

		// if (f != NULL)    
		// {
		// 	// read up to sizeof(buffer) bytes
		// 	while ((bytesRead = fread(buffer, sizeof(char), sizeof(buffer), f)) > 0)
		// 	{
		// 		// process bytesRead worth of data in buffer
		// 		send(client_sock, buffer, sizeof(buffer), 0);
		// 		bzero(buffer, 256);
		// 	}
		// }
		// send buffer to client
		 // error checking is done in actual code and it sends perfectly
	}
}

#endif // RERSPONSE_H_