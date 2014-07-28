
// WebtoonDownloader_UIDlg.cpp : 구현 파일
//

#include "stdafx.h"
#include "WebtoonDownloader_UI.h"
#include "WebtoonDownloader_UIDlg.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif


// CWebtoonDownloader_UIDlg 대화 상자


CWebtoonDownloader_UIDlg::CWebtoonDownloader_UIDlg(CWnd* pParent /*=NULL*/)
	: CDialog(CWebtoonDownloader_UIDlg::IDD, pParent)
{
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
	m_currentType = 0;
}

void CWebtoonDownloader_UIDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	DDX_Control(pDX, IDC_CB_TYPE, m_cbType);
	DDX_Control(pDX, IDC_ED_EP1, m_edEpisode1);
	DDX_Control(pDX, IDC_ED_EP2, m_edEpisode2);
	DDX_Control(pDX, IDC_ED_TITLEID, m_edTitleID);
	DDX_Control(pDX, IDC_ED_RSSURL, m_edRssUrl);
	DDX_Control(pDX, IDC_ED_TITLE, m_edTitle);
}

BEGIN_MESSAGE_MAP(CWebtoonDownloader_UIDlg, CDialog)
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	//}}AFX_MSG_MAP
	ON_BN_CLICKED(IDC_BT_START, &CWebtoonDownloader_UIDlg::OnBnClickedBtStart)
	ON_CBN_SELCHANGE(IDC_CB_TYPE, &CWebtoonDownloader_UIDlg::OnCbnSelchangeCbType)
	ON_BN_CLICKED(IDC_BT_USAGE, &CWebtoonDownloader_UIDlg::OnBnClickedBtUsage)
END_MESSAGE_MAP()


// CWebtoonDownloader_UIDlg 메시지 처리기

BOOL CWebtoonDownloader_UIDlg::OnInitDialog()
{
	CDialog::OnInitDialog();

	// 이 대화 상자의 아이콘을 설정합니다. 응용 프로그램의 주 창이 대화 상자가 아닐 경우에는
	//  프레임워크가 이 작업을 자동으로 수행합니다.
	SetIcon(m_hIcon, TRUE);			// 큰 아이콘을 설정합니다.
	SetIcon(m_hIcon, FALSE);		// 작은 아이콘을 설정합니다.

	m_cbType.InsertString(0, _T("Naver Webtoon"));
	m_cbType.InsertString(1, _T("Naver Best Challenge - BETA"));
	m_cbType.InsertString(2, _T("Daum Webtoon"));	
	m_cbType.SetCurSel(0);

	m_edEpisode1.SetWindowTextW(_T("1"));
	m_edEpisode2.SetWindowTextW(_T("3"));

	CheckDlgButton(IDC_CK_MERGE, TRUE);
	CheckDlgButton(IDC_CK_PNG, FALSE);

	m_edRssUrl.EnableWindow(FALSE);

	return TRUE;  // 포커스를 컨트롤에 설정하지 않으면 TRUE를 반환합니다.
}

// 대화 상자에 최소화 단추를 추가할 경우 아이콘을 그리려면
//  아래 코드가 필요합니다. 문서/뷰 모델을 사용하는 MFC 응용 프로그램의 경우에는
//  프레임워크에서 이 작업을 자동으로 수행합니다.

void CWebtoonDownloader_UIDlg::OnPaint()
{
	if (IsIconic())
	{
		CPaintDC dc(this); // 그리기를 위한 디바이스 컨텍스트

		SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);

		// 클라이언트 사각형에서 아이콘을 가운데에 맞춥니다.
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		// 아이콘을 그립니다.
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialog::OnPaint();
	}
}

// 사용자가 최소화된 창을 끄는 동안에 커서가 표시되도록 시스템에서
//  이 함수를 호출합니다.
HCURSOR CWebtoonDownloader_UIDlg::OnQueryDragIcon()
{
	return static_cast<HCURSOR>(m_hIcon);
}


void CWebtoonDownloader_UIDlg::OnBnClickedBtStart()
{
	CString ep1, ep2, title, titleid, rssurl, param;

	m_edEpisode1.GetWindowText(ep1);
	m_edEpisode2.GetWindowText(ep2);

	ep1 = ep1.Trim();
	ep2 = ep2.Trim();

	if (ep1.GetLength() == 0 || ep2.GetLength() == 0) {
		MessageBox(_T("Input episode range"), _T("Warning"), MB_OK | MB_ICONWARNING);
		return;
	}

	BOOL isMerge = IsDlgButtonChecked(IDC_CK_MERGE);
	BOOL isPng = IsDlgButtonChecked(IDC_CK_PNG);
	switch (m_currentType) {
		case 0: // naver
		case 1:
			m_edTitle.GetWindowText(title);
			m_edTitleID.GetWindowText(titleid);
			title = title.Trim();
			titleid = titleid.Trim();
			if (title.GetLength() == 0 || titleid.GetLength() == 0) {
				MessageBox(_T("Input Title or TitleID"), _T("Warning"), MB_OK | MB_ICONWARNING);
				return;
			}
			param.Format(_T("-e %s-%s -t %s -n %s -w naver"), ep1, ep2, titleid, title);
			if (m_currentType == 1)
				param += " -b";
			break;
		case 2: // daum
			m_edRssUrl.GetWindowText(rssurl);
			rssurl = rssurl.Trim();
			if (rssurl.GetLength() == 0) {
				MessageBox(_T("Input Rss Url"), _T("Warning"), MB_OK | MB_ICONWARNING);
				return;
			}
			param.Format(_T("-e %s-%s -r %s -w daum"), ep1, ep2, rssurl);
			break;
	}

	if (isMerge)
		param += " -m";
	if (isPng)
		param += " -p";

	ExecuteDownload(_T(".\\downloader.exe"), param);
}

void CWebtoonDownloader_UIDlg::OnCbnSelchangeCbType()
{
	m_currentType = m_cbType.GetCurSel();

	switch (m_currentType) {
		case 0: // naver
		case 1: // naver best challenge
			m_edTitle.EnableWindow(TRUE);
			m_edTitleID.EnableWindow(TRUE);
			m_edRssUrl.EnableWindow(FALSE);
			break;
		case 2: // daum
			m_edTitle.EnableWindow(FALSE);
			m_edTitleID.EnableWindow(FALSE);
			m_edRssUrl.EnableWindow(TRUE);
			break;
	}
}

void CWebtoonDownloader_UIDlg::OnBnClickedBtUsage()
{
	ShellExecute(NULL, _T("open"), _T("http://blog.naver.com/liush79/60191630812"), _T(""), _T(""), SW_SHOW);	
}

void CWebtoonDownloader_UIDlg::ExecuteDownload(CString cmd, CString param)
{
	SHELLEXECUTEINFO si = {0,};

	si.cbSize = sizeof(SHELLEXECUTEINFO);
	si.hwnd = NULL;
	si.fMask = SEE_MASK_FLAG_DDEWAIT;
	si.lpVerb = _T("runas");
	si.lpFile = cmd;
	si.lpParameters = param;
	si.nShow = SW_SHOWNORMAL;
	si.lpDirectory = 0;

	ShellExecuteEx(&si);
}
BOOL CWebtoonDownloader_UIDlg::PreTranslateMessage(MSG* pMsg)
{
	switch (pMsg->message)
	{
	case WM_KEYDOWN:
		if (pMsg->wParam == VK_ESCAPE || pMsg->wParam == VK_RETURN)
			return FALSE;
		break;
	default:
		break;
	}

	return CDialog::PreTranslateMessage(pMsg);
}
