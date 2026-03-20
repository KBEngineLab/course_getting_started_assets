using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class WorldUIEvent : MonoBehaviour
{
    public static WorldUIEvent Instance;

    public Button buttonRevive;
    void Awake()
    {
        Instance = this;
    }

    /// <summary>
    /// 复活按钮点击
    /// </summary>
    public void OnButtonReviveClick()
    {
        KBEngine.Avatar.Instance.cellEntityCall.relive();
    }

    public void UpdateReviveBtnState(int  state)
    {
        buttonRevive.gameObject.SetActive(state != 0);
    }


}
