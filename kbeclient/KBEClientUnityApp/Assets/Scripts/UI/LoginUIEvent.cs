using System;
using System.Collections;
using System.Collections.Generic;
using KBEngine;
using TMPro;
using UnityEngine;

public class LoginUIEvent : MonoBehaviour
{
    public static LoginUIEvent instance;
    public GameObject loginPanel;
    public GameObject selectAvatarPanel;
    public GameObject createAvatarPanel;


    public GameObject avatarList;


    public TMP_InputField username;
    public TMP_InputField password;
    public TMP_InputField avatarName;


    private void Awake()
    {
        loginPanel.SetActive(true);
        selectAvatarPanel.SetActive(false);
        createAvatarPanel.SetActive(false);


        // KBEngine.Event.registerOut(KBECustomEventTypes.onLoginSuccessfully, this, "OnLoginSuccessfully");
        instance = this;
    }

    private void OnDestroy()
    {
        KBEngine.Event.deregisterOut(this);
    }

    /// <summary>
    /// 登录成功
    /// </summary>
    /// <param name="entityId">entityId</param>
    public void OnLoginSuccessfully(int entityId)
    {
        LogMgr.Instance.AddLog($"OnLoginSuccessfully:: login success, entityId:{entityId}");

        loginPanel.SetActive(false);
        selectAvatarPanel.SetActive(true);
    }

    /// <summary>
    /// 登录按钮点击
    /// </summary>
    public void OnLoginPanelLoginBtnClick()
    {

        if (username.text.Length < 5)
        {
            LogMgr.Instance.AddLog("Username length must be at least 5 characters.");
            return;
        }

        if (password.text.Length < 5)
        {
            LogMgr.Instance.AddLog("Password length must be at least 5 characters.");
        }


        // 调用KBE底层的login方法
        KBEngineApp.app.login(username.text, password.text,Array.Empty<byte>());
    }

    /// <summary>
    /// 注册按钮点击
    /// </summary>
    public void OnLoginPanelRegisterBtnClick()
    {
        if (username.text.Length < 5)
        {
            LogMgr.Instance.AddLog("Username length must be at least 5 characters.");
            return;
        }

        if (password.text.Length < 5)
        {
            LogMgr.Instance.AddLog("Password length must be at least 5 characters.");
        }

        KBEngineApp.app.createAccount(username.text, password.text,Array.Empty<byte>());
    }

    /// <summary>
    /// 选择角色页面创建按钮点击
    /// </summary>
    public void OnSelectAvatarPanelCreateAvatarBtnClick()
    {

        createAvatarPanel.SetActive(true);
    }

    /// <summary>
    /// 选择角色页面删除按钮点击
    /// </summary>
    public void OnSelectAvatarPanelRemoveAvatarBtnClick()
    {

    }


    /// <summary>
    /// 选择角色页面进入游戏按钮点击
    /// </summary>
    public void OnSelectAvatarPanelEnterGameBtnClick()
    {

    }


    /// <summary>
    /// 创建角色页面创建按钮点击
    /// </summary>
    public void OnCreateAvatarPanelCreateBtnClick()
    {

    }

    /// <summary>
    /// 创建角色页面返回按钮点击
    /// </summary>
    public void OnCreateAvatarPanelReturnBtnClick()
    {
        createAvatarPanel.SetActive(false);
    }


}
