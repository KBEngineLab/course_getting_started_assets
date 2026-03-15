
using System;
using KBEngine;
using UnityEngine.SceneManagement;

public class KBEApp : UnityKBEMain
{
    public KBEApp()
    {
        KBELog.Init(new UnityLogProvider());

        InstallEvents();
    }

    protected override void OnDestroy()
    {
        base.OnDestroy();
        KBEngine.Event.deregisterOut(this);
    }


    void InstallEvents()
    {
        // 连接相关事件
        Event.registerOut(EventOutTypes.onKicked, this, "OnKicked");
        Event.registerOut(EventOutTypes.onDisconnected, this, "OnDisconnected");
        Event.registerOut(EventOutTypes.onConnectionState, this, "OnConnectionState");


        // 资源校验
        Event.registerOut(EventOutTypes.onVersionNotMatch, this, "OnVersionNotMatch");
        Event.registerOut(EventOutTypes.onScriptVersionNotMatch, this, "OnScriptVersionNotMatch");

        // 登录相关事件
        Event.registerOut(EventOutTypes.onLoginFailed, this, "OnLoginFailed");
        Event.registerOut(EventOutTypes.onLoginBaseappFailed, this, "OnLoginBaseappFailed");
        Event.registerOut(EventOutTypes.onLoginBaseapp, this, "OnLoginBaseapp");
        Event.registerOut(EventOutTypes.onCreateAccountResult, this, "OnCreateAccountResult");
    }

    public void OnKicked(UInt16 failedcode)
    {
        LogMgr.Instance.AddLog($"KBEApp::OnKicked:{KBEngineApp.app.serverErr(failedcode)}");
        SceneManager.LoadScene("Scenes/Login");
    }

    public void OnDisconnected()
    {
        LogMgr.Instance.AddLog("KBEApp::OnDisconnected");
        SceneManager.LoadScene("Scenes/Login");
    }

    public void OnConnectionState(bool isconnected)
    {
        LogMgr.Instance.AddLog($"KBEApp::OnConnectionState: isconnected:{isconnected}");
    }

    public void OnVersionNotMatch(string verInfo, string serVerInfo)
    {
        LogMgr.Instance.AddLog($"KBEApp::OnVersionNotMatch: verInfo:{verInfo}，serVerInfo:{serVerInfo}");
    }

    public void OnScriptVersionNotMatch(string verInfo, string serVerInfo)
    {
        LogMgr.Instance.AddLog($"KBEApp::OnScriptVersionNotMatch: verInfo:{verInfo}，serVerInfo:{serVerInfo}");
    }

    public void OnLoginFailed(UInt16 failedcode)
    {
        LogMgr.Instance.AddLog($"KBEApp::OnLoginFailed:{KBEngineApp.app.serverErr(failedcode)}");
    }

    public void OnLoginBaseappFailed(UInt16 failedcode)
    {
        LogMgr.Instance.AddLog($"KBEApp::OnLoginBaseappFailed:{KBEngineApp.app.serverErr(failedcode)}");
    }

    public void OnLoginBaseapp()
    {
        LogMgr.Instance.AddLog("KBEApp::OnLoginBaseapp success");
    }

    public void OnCreateAccountResult(UInt16 retcode)
    {
        if (retcode != 0)
        {
            LogMgr.Instance.AddLog($"KBEApp::OnCreateAccountResult: {KBEngineApp.app.serverErr(retcode)}");
            return;
        }

        LogMgr.Instance.AddLog("KBEApp::OnCreateAccountResult: Create account success");
    }
}
