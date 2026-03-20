using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Event = KBEngine.Event;

public class WorldScene : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        LogMgr.Instance.AddLog("Event resume");
        // 场景切换后恢复事件
        Event.resume();
    }

}
