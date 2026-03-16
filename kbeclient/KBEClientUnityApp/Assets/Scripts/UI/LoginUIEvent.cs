using System;
using System.Collections;
using System.Collections.Generic;
using KBEngine;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class LoginUIEvent : MonoBehaviour
{
    public static LoginUIEvent Instance;
    public GameObject loginPanel;
    public GameObject selectAvatarPanel;
    public GameObject createAvatarPanel;


    public GameObject avatarList;


    public TMP_InputField username;
    public TMP_InputField password;
    public TMP_InputField avatarName;


    public GameObject avatarItemPrefab;



    private Int64 selectedAvatarDBID = 0;


    private void Awake()
    {
        loginPanel.SetActive(true);
        selectAvatarPanel.SetActive(false);
        createAvatarPanel.SetActive(false);


        // KBEngine.Event.registerOut(KBECustomEventTypes.onLoginSuccessfully, this, "OnLoginSuccessfully");
        Instance = this;
    }

    private void OnDestroy()
    {
        KBEngine.Event.deregisterOut(this);
    }


    public void UpdateAvatarList(List<AVATAR_INFO> avatarInfos)
    {
        // 1. 清空旧列表
        for (int i = avatarList.transform.childCount - 1; i >= 0; i--)
        {
            Destroy(avatarList.transform.GetChild(i).gameObject);
        }

        // 2. 遍历 avatarInfos
        foreach (var info in avatarInfos)
        {
            // 3. 创建 Button
            GameObject obj = Instantiate(avatarItemPrefab, avatarList.transform);
            Button btn = obj.GetComponent<Button>();

            // 设置文字
            TMP_Text txt = obj.GetComponentInChildren<TMP_Text>();
            if (txt)
            {
                txt.text = info.name;
            }

            // 4. 添加点击事件
            string name = info.name; // 防止闭包问题
            Int64 dbid = info.dbid; // 防止闭包问题
            btn.onClick.AddListener(() =>
            {
                Debug.Log("Click Avatar: " + name + "dbid:" + dbid);
                selectedAvatarDBID = dbid;
            });

        }
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


        Account.instance.baseEntityCall.reqAvatarList();
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
        if (selectedAvatarDBID == 0) return;

        Account.instance.baseEntityCall.reqRemoveAvatar(selectedAvatarDBID);
    }


    /// <summary>
    /// 选择角色页面进入游戏按钮点击
    /// </summary>
    public void OnSelectAvatarPanelEnterGameBtnClick()
    {
        if (selectedAvatarDBID == 0) return;

        Account.instance.baseEntityCall.reqAvatarEnterGame(selectedAvatarDBID);
    }


    /// <summary>
    /// 创建角色页面创建按钮点击
    /// </summary>
    public void OnCreateAvatarPanelCreateBtnClick()
    {
        if (avatarName.text.Length < 1)
        {
            LogMgr.Instance.AddLog("Avatar name must be at least 2 characters.");
            return;
        }


        Account.instance.baseEntityCall.reqCreateAvatar(avatarName.text);
        avatarName.text = "";
        createAvatarPanel.SetActive(false);

    }

    /// <summary>
    /// 创建角色页面返回按钮点击
    /// </summary>
    public void OnCreateAvatarPanelReturnBtnClick()
    {
        createAvatarPanel.SetActive(false);
    }


}
