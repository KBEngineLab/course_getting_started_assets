using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class LoginUIEvent : MonoBehaviour
{
    public GameObject loginPanel;
    public GameObject selectAvatarPanel;
    public GameObject createAvatarPanel;


    public GameObject avatarList;


    public InputField username;
    public InputField password;
    public InputField avatarName;


    private void Awake()
    {
        loginPanel.SetActive(true);
        selectAvatarPanel.SetActive(false);
        createAvatarPanel.SetActive(false);
    }

    /// <summary>
    /// 登录按钮点击
    /// </summary>
    public void OnLoginPanelLoginBtnClick()
    {
        loginPanel.SetActive(false);
        selectAvatarPanel.SetActive(true);
    }

    /// <summary>
    /// 注册按钮点击
    /// </summary>
    public void OnLoginPanelRegisterBtnClick()
    {

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
