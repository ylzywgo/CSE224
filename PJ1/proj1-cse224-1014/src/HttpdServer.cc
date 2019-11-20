#include <sysexits.h>

#include <arpa/inet.h>  /* for sockaddr_in and inet_ntoa() */
#include <iostream>			// input output
#include <sstream>
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
#include <regex>

#include "logger.hpp"
#include "HttpdServer.hpp"
#include "response.hpp"

#include <vector>
#include <deque>

const string CRLF = "\r\n";
const string CRLF_CRLF = CRLF + CRLF;

void die_with_error(const char *err_message) {
    perror(err_message);
    exit(1);
}

int is_valid_path(string s){
    if (s.at(0) != '/') return -1;
    for (auto c : s){
        if (!isalpha(c) && !isdigit(c) && c != '/' && c != '.') {
			return -1;
		}
    }
    return 0;
}

int is_valid_kv(string s){
	for (auto c : s){
        if (!isalpha(c) && !isdigit(c)) return -1;
    }
    return 0;
}

int is_valid_firstline(string fln){
	auto log = logger();
    istringstream iss(fln);
	log->info("firstline is {}", fln);
    string s;
    int space = 0;
    while (getline( iss, s, ' ' )){
		log->info("cur item is {}", s);
        if (s.compare("") == 0){
			log->info("too much space");
			return -1;
		} 						
        switch (space) 
        { 
            case 0:{
                if (s.compare("GET") != 0){
					log->info("get error");
					return -1;
				}
                break;
            } 
            case 1:{
                if (is_valid_path(s) != 0){
					log->info("path error");
					return -1;
				}
                break;
            }
            case 2:{
                if (s.compare("HTTP/1.1") != 0){
					log->info("http error");
					return -1;
				}
                break;
            }
            default:{ 
				log->info("too much space at the end"); 
                return -1;
			}   
        }
        space++;
    }
	log->info("end firstline");
    return 0;
}

vector<string> split (const string &s, char delim) {
    vector<string> result;
    stringstream ss (s);
    string item;

    while (getline (ss, item, delim)) {
        result.push_back (item);
    }

    return result;
}

int validate_file(string &url, string doc_root){
	if (url.compare("/") == 0){
		url = doc_root + "/index.html";
		return 1;
	}
	url = doc_root + url;

	if (access(url.c_str(), F_OK) == -1){
		return -1;
	}else{
		// Check if the file path doesn't escape the document root.
		// Check if the file has right permissions 
        vector<string> paths = split (url, '/');
        deque<string> p_deque;
        for (auto path : paths){
            if (path.compare(".") == 0){
                continue;
            }
            else if (path.compare("..") == 0){
                if (p_deque.empty()){
                    return -1;
                }
                else{
                    p_deque.pop_back();
                }
            }
            else{
                if (path.compare("") != 0){
                    p_deque.push_back(path);
                }            
            }
        }
        url = "";
        for (auto s : p_deque){
            url += "/";
            url += s;
        }

		int pos = url.find(doc_root);

		return pos == 0 ? 1 : -1; 
	}
}

void split(const string &s, const string &delim, vector<string> &tokens) {
    std::regex regex(delim);
    std::copy(std::sregex_token_iterator(s.begin(), s.end(), regex, -1),
              std::sregex_token_iterator(),
              std::back_insert_iterator<vector<string>>(tokens));
}


int judge_malformed(string &ss, string &myserver){
	auto log = logger();
	string host = "host";

    bool host_exist = false;
	
	vector<string> lines;
	split(ss, CRLF, lines);
	int i = 0;

    for (auto cur : lines){
		log->info("cur line {} is {}", i, cur);
		if (i == 0) {
			i = 1;
			continue;
		}
		transform(cur.begin(), cur.end(), cur.begin(),[](unsigned char c){ return std::tolower(c); });
        int colon = cur.find(": ");
        if (colon == -1){
			cout << "colon error!" << endl;
			return -1;
		}

        string key = cur.substr(0, colon);
		log->info("cur value is {}", key);
		cout << key << endl;
		if (key.compare(host) == 0){
            host_exist = true;
			myserver = cur.substr(colon + 2);
        }
		if (key.compare("connection") == 0){
			string value = cur.substr(colon+1);
			value.erase(remove_if(value.begin(), value.end(), ::isspace), value.end());
			if(value == "close") {
				cout<<"we can now close socket";
				return 1;
			}
		}
    }

    if (!host_exist) {
		cout << "host not exist" << endl;
		return -1;
	}

    return 0;
}

// check if the header is validate, 
//-1-> not validate; 0 -> validate; 1-> validate and has connection: close
int validate_header(char* buf) {
	char* buf_copy = (char*)malloc(strlen(buf) + 1); 
	strcpy(buf_copy, buf);

    cout<<buf_copy<<endl;
	char* one_line = strsep(&buf_copy, "\r\n"); // slicing
	cout<<one_line<<endl;
	while((one_line = strsep(&buf_copy, "\r\n")) != nullptr) {
		string one_ln(one_line);

		//about find(): The function returns the index of the first occurrence of sub-string, 
		//if the sub-string is not found it returns string::npos
		size_t pos_of_colon = one_ln.find(":");
		// TODO: now I only care about format like [key: value] 
		if(one_ln.find(":") == string::npos || one_ln.at(pos_of_colon+1) != ' ') {
			return -1;
		}
		//QQQ???? do we need to consider if case-sensitive???
		if(one_ln.substr(0, pos_of_colon) == "Connection") {
			string value = one_ln.substr(pos_of_colon+1);
			value.erase(remove_if(value.begin(), value.end(), ::isspace), value.end());
			if(value == "close") {
				cout<<"we can now close socket";
				return 1;
			}
		}

	}
	return 0;
}

void HttpdServer::handle_request(int &client_sock){
	// while(1){
	auto log = logger();
	char buf[256];
	bzero(buf, 256);
	ssize_t numOfBytes;
	char *allBytes = new char[256];
	size_t sizeOfAllBytesArray = 256;
	size_t tmpNum = 0;
	// read all data from dat file 
		
	while((numOfBytes = recv(client_sock, buf, 256, 0)) > 0) {
		std::cout<<"number bytes: "<<numOfBytes<<endl;
		if(tmpNum + numOfBytes >= sizeOfAllBytesArray) {
			sizeOfAllBytesArray += 256;
			char *tmp = new char[sizeOfAllBytesArray];
			for(size_t i = 0;i < sizeOfAllBytesArray; i++){
				tmp[i] = allBytes[i];
			}
			allBytes = tmp;
		} else{
			for(int i = 0; i < numOfBytes; i++) {
				allBytes[i+tmpNum] = buf[i];
			}
		}
			tmpNum += numOfBytes;
	}

	if (numOfBytes > 0){
		cout << "Message received: " << endl << allBytes << endl;
		cout << "Message length: " << numOfBytes << endl;
	}
	string ss(allBytes);
	std::vector<string> requests;
    // split(ss, CRLF_CRLF, requests);
	int index = 0;
	log->info("cur info is {}", ss);
	index = ss.find("\r\n\r\n");
	while ((index = ss.find("\r\n\r\n")) != -1){
		string cur = ss.substr(0, index);
		log->info("cur item is {}", cur);
		ss = ss.substr(index + 4);
		requests.push_back(cur);
	}
	for (auto request : requests){
		log->info("request is {}",request);
	}
	for (auto request : requests){
		// if (request.compare(CRLF_CRLF) == 0 || request.size() == 0) continue;
		char* buf = (char*)malloc(request.size() + 1);;
		strcpy(buf, request.c_str());
		log->info("cur item is {}", buf);
		log->info("handle request");
		//Copy the buffer to parse
		char* buf_copy = (char*)malloc(strlen(buf) + 1); 
		strcpy(buf_copy, buf);

		// Get the filename
		char* first_line = strsep(&buf_copy, "\r\n");
		string fln(first_line);
		int valid_firstline = is_valid_firstline(fln);
		log->info("valid_path: {} is {}", first_line, valid_firstline);

		strsep(&first_line," ");
		char* url = strsep(&first_line," ");
		log->info("url is:{}", url);
		log->info("handling end");

		// Prepend document root to get the absolute path
		// Prepend document root to get the absolute path
		char real_path[PATH_MAX];
		const char* doc_root_char = doc_root.c_str();
		realpath(doc_root_char, real_path);

		string surl(url);
		string full_path = real_path + surl;
		log->info("full path is: {}", full_path);


		// Validate the file path requested.
		int is_valid = -1;
		if (valid_firstline != -1){
			is_valid = validate_file(surl, real_path);
			log->info("valid_path: {} is {}", surl, is_valid);
		}

		string str_copy(buf);
		string myserver = "";
		int is_valid_header = judge_malformed(str_copy, myserver);

		// int is_valid_header = validate_header(buf);
		log->info("valid_header: {}", is_valid_header);

		int is_valid_head = 1;

		if (is_valid_header == -1 || valid_firstline == -1){
			is_valid_head = -1;
		}

		// connnection close
		send_response(is_valid, is_valid_head, surl, client_sock, myserver);
		log->info("valid_header: {}", is_valid_header);

		if(is_valid_header == 1) {
			log->info("close connection");
			close(client_sock);
			return;
		} 
	}

	if(numOfBytes  < 0) {
		if (errno == EWOULDBLOCK){
			log->info("timeout");
  		}
		else{
			log->info("ERROR WHILE GETTING MESSAGE");
		}
	}
	close(client_sock);
}



HttpdServer::HttpdServer(INIReader& t_config)
	: config(t_config)
{
	auto log = logger();

	string pstr = config.Get("httpd", "port", "");
	if (pstr == "") {
		log->error("port was not in the config file");
		exit(EX_CONFIG);
	}
	port = pstr;

	string dr = config.Get("httpd", "doc_root", "");
	if (dr == "") {
		log->error("doc_root was not in the config file");
		exit(EX_CONFIG);
	}
	doc_root = dr;
}

void HttpdServer::launch()
{
	auto log = logger();

	log->info("Launching web server");
	log->info("Port: {}", port);
	log->info("doc_root: {}", doc_root);
    
	// 1. socket()
	int sock = socket(AF_INET, SOCK_STREAM, 0);

	// if socket was created successfully, 
	// socket() returns a non-negative number
	if(sock < 0) {
		cout << "ERROR WHILE CREATING SOCKET" << endl;
		return;
	}   

	// create a sockaddr_in struct
	struct sockaddr_in server_address;
	memset(&server_address, 0, sizeof(server_address));
	server_address.sin_family = AF_INET;
	server_address.sin_port = htons(stoul(port));
	server_address.sin_addr.s_addr = htonl(INADDR_ANY);

	// 2. bind()
	int b = ::bind(sock, (struct sockaddr*) &server_address,
				 sizeof(server_address));

	// if bind is successful it returns a 0, else 1
	if(b < 0) {
		cout << "ERROR WHILE BINDING SOCKET" << endl;
		close(sock);
		return;
	}

	cout << "SERVER IS RUNNING" << endl;

	// 3. listen
	listen(sock, 10);

	struct sockaddr_in client_address;
	socklen_t client_length = sizeof(client_address);

	// 4. accept and receive
	while(1){
		int new_sock = accept(sock, (struct sockaddr*)&client_address,
						  &client_length);


	// if connection was created successfully, 
	// accept() returns a non-negative number
		if(new_sock < 0) {
			cout << "ERROR WHILE ACCEPTING CONNECTION" << endl;
			close(sock);
			continue;
		}
		struct timeval tv;
		tv.tv_sec = 5;
		tv.tv_usec = 0;

		if(setsockopt(new_sock, SOL_SOCKET, SO_RCVTIMEO,(char *) &tv, sizeof(tv))<0) {
			die_with_error("error when setting socket opt");
		} 
		if(setsockopt(new_sock, SOL_SOCKET, SO_SNDTIMEO, (char *)&tv, sizeof(tv))<0) {
			die_with_error("error when setting socket opt");
		} 
		int MAX_BL = 1;
        if(setsockopt(sock, SOL_SOCKET, SO_REUSEADDR, &MAX_BL, sizeof(MAX_BL))<0) {
            die_with_error("cannot set backlog");
		} 
	
		thread(bind(&HttpdServer::handle_request, this, new_sock)).detach();

    }
	close(sock);
}