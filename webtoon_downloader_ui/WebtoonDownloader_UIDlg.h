
// WebtoonDownloader_UIDlg.h : 헤더 파일
//

#pragma once
#include "afxwin.h"


// CWebtoonDownloader_UIDlg 대화 상자
class CWebtoonDownloader_UIDlg : public CDialog
{
// 생성입니다.
public:
	CWebtoonDownloader_UIDlg(CWnd* pParent = NULL);	// 표준 생성자입니다.

// 대화 상자 데이터입니다.
	enum { IDD = IDD_WEBTOONDOWNLOADER_UI_DIALOG };

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV 지원입니다.


// 구현입니다.
private:
	CComboBox m_cbType;
	CEdit m_edEpisode1;
	CEdit m_edEpisode2;
	CEdit m_edTitle;
	CEdit m_edTitleID;
	CEdit m_edRssUrl;
	int m_currentType;

	void ExecuteDownload(CString cmd, CString param);

protected:
	HICON m_hIcon;

	// 생성된 메시지 맵 함수
	virtual BOOL OnInitDialog();
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	DECLARE_MESSAGE_MAP()

public:
	afx_msg void OnBnClickedBtStart();
	afx_msg void OnCbnSelchangeCbType();
	afx_msg void OnBnClickedBtUsage();
	virtual BOOL PreTranslateMessage(MSG* pMsg);
};
